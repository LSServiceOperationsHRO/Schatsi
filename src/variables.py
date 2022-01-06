import os

run_id = os.getenv('RUN_ID', default='')


SCHATSI_RUNTIME = f"{run_id}/data/output/schatsi_runtime.csv"
SCHATSI_STOPWORDS = f"{run_id}/data/params/SCHATSI_stopwords.csv"
SCHATSI_INPUT_FOLDER = "/data/input"