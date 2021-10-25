"""Entry-point script to label radiology reports."""
import concurrent.futures
import multiprocessing
import os
from itertools import repeat

import numpy as np
import pandas as pd
from tqdm import tqdm

from args import ArgParser
from constants import *
from loader import Loader
from stages import Extractor, Classifier, Aggregator


def write(reports, path, ml_predictions, org_report,  labels, output_path, verbose=False):
    """Write labeled reports to specified path."""
    labeled_reports = pd.DataFrame({"path": path, "org_report": org_report, REPORTS: reports,
                                    "ml_predictions": ml_predictions})
    for index, category in enumerate(CATEGORIES):
        labeled_reports[category] = labels[:, index]
    if verbose:
        print(f"Writing reports and labels to {output_path}.")
    labeled_reports.to_csv(output_path, index=False)


def label(args, df, index):
    """Label the provided report(s)."""
    loader = Loader(args.reports_path, df, args.extract_impression)

    extractor = Extractor(args.mention_phrases_dir,
                          args.unmention_phrases_dir,
                          verbose=args.verbose)

    classifier = Classifier(args.pre_negation_uncertainty_path,
                            args.negation_path,
                            args.post_negation_uncertainty_path,
                            verbose=args.verbose)
    aggregator = Aggregator(CATEGORIES,
                            verbose=args.verbose)

    # Load reports in place.
    loader.load()

    # Extract observation mentions in place.
    extractor.extract(loader.collection)

    # Classify mentions in place.
    classifier.classify(loader.collection)

    # Aggregate mentions to obtain one set of labels for each report.
    labels = aggregator.aggregate(loader.collection)
    path = str(args.output_path).replace(".csv", "_"+str(index)+".csv")
    write(loader.reports, loader.path, loader.ml_predictions, loader.org_report, labels, path, args.verbose)


output_file = "./labeled_reports.csv"

if __name__ == "__main__":
    parser = ArgParser()

    """Load and clean the reports."""
    df = pd.read_csv(parser.parse_args().reports_path)
    max_workers = multiprocessing.cpu_count()
    print(f"Generate labels using {max_workers} CPUs")
    df_split = np.array_split(df, max_workers)

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        list(tqdm(executor.map(label, repeat(parser.parse_args()), [df_split[i] for i in range(max_workers)],
                               [i for i in range(max_workers)]), total= max_workers))

    merged_df = pd.concat([pd.read_csv(f"./labeled_reports_{str(index)}.csv") for index in range(max_workers)],
                          ignore_index=True)
    for index in range(max_workers):
        os.remove(f"./labeled_reports_{str(index)}.csv")

    merged_df.reset_index(drop=True, inplace=True)
    merged_df.to_csv(output_file, index=False)
