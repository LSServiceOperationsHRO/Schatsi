import os
import io
import csv
import boto3
import pdftotext
import pandas as pd
from datetime import datetime
import SCHATSI003  # import string_preparation, count_words, references, reference_data_cutting
import SCHATSI004  # import terms, bigrams, trigrams, term_filtering,....

"""
Start of the program:
1. First timestamp for the calculation of the runtime
2. One run of the whole programm, incl. SCHATSI002, SCHATSI003, SCHATSI004....
3. Second timestamp for the calculation of the runtime
4. Calculate the duration -> write the timestamps and the duration into the file "SCHATSI_runtime
"""


def main():
    # This sets the AWS profile to use; uncomment if running locally
    # os.environ['AWS_PROFILE'] = "default"
    # os.environ['AWS_DEFAULT_REGION'] = "eu-central-1"

    # Runtime
    # open file for runtime

    # LOCAL PATH FOR TESTING:
    # runtime = open("SCHATSI_runtime.csv", 'w', newline='')
    # PATH FOR DOCKER:
    runtime = open("../data/output/SCHATSI_runtime.csv", 'w', newline='')
    runtime_file = csv.writer(runtime, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    # writing a headline into the file
    kopfzeile_runtime = ["start processing", "end processing", "duration (minutes)"]
    runtime_file.writerow(kopfzeile_runtime)

    # timestamp at the begin of the program and the normalized version which is written into "SCHATSI_runtime"
    start = datetime.now()
    print("Execution started at", start.isoformat())

    output_included = []
    output_data_cleansing = []
    output_references = []
    output_terms = []

    run_id = os.environ.get("RUN_ID", "default")
    bucket_params = "schatsi-nlp-params"
    bucket_io = "schatsi-nlp-io"

    print("Fetching parameters...", end="", flush=True)

    """
    Preparation of the Stopwords for use in SCHATSI004 functions - import from file "SCHATSI_stopwords.csv
    """
    s3_client = boto3.client('s3')
    stopwords_obj = s3_client.get_object(
        Bucket=bucket_params,
        Key="stopwords.csv"
    )
    stopwords = pd.read_csv(stopwords_obj['Body'])

    print("done")
    print("Processing files for run", run_id, ":")

    input_prefix = "{}/input/".format(run_id)
    result = s3_client.list_objects(Bucket=bucket_io, Prefix=input_prefix)
    for o in result.get('Contents'):
        key = o.get('Key')
        if key == input_prefix:
            continue
        filename = key.split('/')[-1]
        print(filename)
        data = s3_client.get_object(Bucket=bucket_io, Key=key)
        contents = data['Body'].read()
        try:
            pdf = pdftotext.PDF(io.BytesIO(contents))
            text = "\n\n".join(pdf)
        except:
            if filename.endswith(".pdf") or filename.endswith(".PDF"):
                datatype = "pdf"
            elif filename.endswith(".txt") or filename.endswith(".TXT"):
                datatype = "txt"
            elif filename.endswith(".csv") or filename.endswith(".CSV"):
                datatype = "csv"
            elif filename.endswith(".docx") or filename.endswith(".DOCX"):
                datatype = "docx"
            elif filename.endswith(".odt") or filename.endswith(".ODT"):
                datatype = "odt"
            else:
                datatype = "unknown datatype"
            zeile = [filename, datatype, "__", "X"]

        else:
            if filename.endswith(".pdf") or filename.endswith(".PDF"):
                datatype = "pdf"
                # All files that are successfully read in where the type is 'pdf' will be used in the next steps
                text_only, references = SCHATSI003.string_preparation(text)
                total_num_words = SCHATSI003.count_words(text_only)
                zeile_data_cleansing = [filename, datatype, total_num_words]
                output_data_cleansing.append(zeile_data_cleansing)

                reference_list = SCHATSI003.references(references)
                for element in reference_list:
                    author, year, title = SCHATSI003.reference_data_cutting(element)
                    output_references.append([filename, author, year, title])

                # Aufruf SCHATSI004: Filtering the expressions from the text and rank the Papers at the Base of the
                # functional terms given by the User
                monogram = SCHATSI004.terms(text_only)
                bigram = SCHATSI004.bigrams(monogram)
                trigram = SCHATSI004.trigrams(monogram)
                mono_filtered, mono_number = SCHATSI004.term_filtering(monogram, stopwords)
                bigram_filtered, bigram_number = SCHATSI004.bigram_filtering(bigram, stopwords)
                trigram_filtered, trigram_number = SCHATSI004.trigram_filtering(trigram, stopwords)
                # Result: 2 lists each: one with the filtered terms, the other with the counts of the terms
                # Writing in "SCHATSI_terms.csv"
                i, j, k = 0, 0, 0
                for i in range(0, len(mono_filtered)):
                    output_terms.append([filename, mono_filtered[i], mono_number[i]])
                for j in range(0, len(bigram_filtered)):
                    bi = bigram_filtered[j][0] + " " + bigram_filtered[j][1]
                    output_terms.append([filename, bi, bigram_number[j]])
                for k in range(0, len(trigram_filtered)):
                    tri = trigram_filtered[k][0] + " " + trigram_filtered[k][1] + " " + trigram_filtered[k][2]
                    output_terms.append([filename, tri, trigram_number[k]])

            elif filename.endswith(".txt") or filename.endswith(".TXT"):
                datatype = "txt"
            elif filename.endswith(".csv") or filename.endswith(".CSV"):
                datatype = "csv"
            elif filename.endswith(".docx") or filename.endswith(".DOCX"):
                datatype = "docx"
            elif filename.endswith(".odt") or filename.endswith(".ODT"):
                datatype = "odt"
            else:
                datatype = "unknown datatype"

            output_included.append([filename, datatype, "X", "__"])

            # the outputfile will get a layout like this
            """
            filename | type | included | excluded
            --------------------------------------
            abc.pdf  | pdf  |     X    |    __        <-- The text of this document could be extracted without any problems
            err.pdf  | pdf  |    __    |     X        <-- There was a problem and the document text could not be extracted,
            ...                                           the files wont be included in the next steps 
            ...
            """

    print("Saving output files...", end="", flush=True)

    outputs = [
        ['schatsi_included.csv', pd.DataFrame(output_included, columns=["filename", "type", "included", "excluded"])],
        ['schatsi_data_cleansing.csv',
         pd.DataFrame(output_data_cleansing, columns=["filename", "type", "Total Count"])],
        ['schatsi_references.csv', pd.DataFrame(output_references,
                                                columns=["filename", "reference_author", "reference_year",
                                                         "reference_title"])],
        ['schatsi_terms.csv', pd.DataFrame(output_terms, columns=["filename", "term", "term count"])]
    ]

    for output in outputs:
        csv_buffer = io.BytesIO()
        output[1].to_csv(csv_buffer, mode="wb", encoding="utf-8", index=False)
        csv_buffer.seek(0)
        s3_client.put_object(
            Body=csv_buffer,
            Bucket=bucket_io,
            Key="{}/output/{}".format(run_id, output[0])
        )

    print("done")

    # Calculate the runtime -> last step of the programm

    # second timestamp
    finish = datetime.now()
    print("Execution finished at", finish.isoformat())
    # calculation of the duration
    duration_program = (finish - start).seconds / 60

    # write start_normalized, finish_normalized and duration into "SCHATSI_runtime.csv"
    datetime_format = "%m/%d/%Y %H:%M:%S"
    zeile_runtime = [start.strftime(datetime_format), finish.strftime(datetime_format), duration_program]
    runtime_file.writerow(zeile_runtime)


if __name__ == "__main__":
    main()
