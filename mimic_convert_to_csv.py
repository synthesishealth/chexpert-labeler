import re
import pandas as pd
from tqdm import tqdm

nlp_csv_file = "./MIMIC-CXR-reports-w-ML-predictions.csv"
output_file = "./MIMIC-CXR-reports.csv"

def clean_mimic(report):
    finding_match = re.search("FINDINGS:", report)
    if finding_match is not None:
        report = report[finding_match.span()[0]:]
    else:
        comparison_match = re.search(r"COMPARISON:(.|\n)+?(?=\n \n)", report)
        rfe_match = re.search(r"REASON FOR EXAM:|EXAMINATION:(.|\n)+?(?=\n \n)", report)
        history_match = re.search(r"HISTORY:(.|\n)+?(?=\n \n)", report)
        examination_match = re.search(r"EXAMINATION:(.|\n)+?(?=\n \n)", report)

        if comparison_match is not None:
            report = report[comparison_match.span()[1]:]
        elif rfe_match is not None:
            report = report[rfe_match.span()[1]:]
        elif history_match is not None:
            report = report[history_match.span()[1]:]
        elif examination_match is not None:
            report = report[examination_match.span()[1]:]

    report = re.sub(r"\s{2,}", " ", report)
    report = re.sub("$\n", "", report)
    return report


NLP_csv = pd.read_csv(nlp_csv_file, usecols=['path', 'report', 'ml_predictions'])
NLP_csv = NLP_csv.rename(columns={"report": "org_report"})

NLP_csv["report"] = NLP_csv.apply(lambda row: clean_mimic(row["org_report"]), axis=1)

NLP_csv = NLP_csv[['path', 'org_report', 'report', 'ml_predictions']]

print(f"Save output file to {output_file}")
NLP_csv.to_csv(output_file, index=False)
