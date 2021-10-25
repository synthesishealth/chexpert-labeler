# chexpert-labeler - MIMIC dataset

- You should read and implement all steps in original readme file first.
- Run mimic_convert_to_csv.py to generate CSV file for MIMIC with case report.
- Run the following commends to generate the M2IMIC label using chexpert-labeler
  - `export PYTHONPATH=~/models/NegBio/`
  - `python label.py --reports_path ./MIMIC-CXR-reports.csv`
