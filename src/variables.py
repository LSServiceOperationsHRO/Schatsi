import os

run_id = os.getenv('RUN_ID', default='')
path_prefix = os.path.join("/data", run_id)


SCHATSI_RUNTIME = f"{path_prefix}/output/schatsi_runtime.csv"
SCHATSI_STOPWORDS = f"{path_prefix}/params/stopwords.csv"
SCHATSI_INPUT_FOLDER = f"{path_prefix}/input"