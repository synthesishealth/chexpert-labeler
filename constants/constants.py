from pathlib import Path

# Paths
HOME_DIR = Path.home()
PARSING_MODEL_DIR = HOME_DIR / ".local/share/bllipparser/GENIA+PubMed"

# Observation constants
CARDIOMEGALY = "Cardiomegaly"
ENLARGED_CARDIOMEDIASTINUM = "Enlarged Cardiomediastinum"
SUPPORT_DEVICES = "Support Devices"
NO_FINDING = "No Finding"
OBSERVATION = "observation"
CATEGORIES = ["No_finding",
              "Atelectasis",
              "Consolidation",
              "Emphysema",
              "Linear Scar or Fibrotatic Bands",
              "Lung Cavity",
              "Lung Cyst",
              "Nodule Mass",
              "Pleural Effusion",
              "Pleural Thickening",
              "Pulmonary Edema",
              "Undifferentiated Lung Opacity"]

# Numeric constants
POSITIVE = 1
NEGATIVE = 0
UNCERTAIN = -1

# Misc. constants
UNCERTAINTY = "uncertainty"
NEGATION = "negation"
REPORTS = "Reports"
