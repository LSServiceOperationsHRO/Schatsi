import os
import csv
import pdftotext
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
    # Runtime
    # open file for runtime

    # LOCAL PATH FOR TESTING:
    # runtime = open("SCHATSI_runtime.csv", 'w', newline='')
    # PATH FOR DOCKER:
    runtime = open("data/output/SCHATSI_runtime.csv", 'w', newline='')
    runtime_file = csv.writer(runtime, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    # writing a headline into the file
    kopfzeile_runtime = ["start processing", "end processing", "duration (minutes)"]
    runtime_file.writerow(kopfzeile_runtime)

    # timestamp at the begin of the program and the normalized version which is written into "SCHATSI_runtime"
    start = datetime.now()
    print ("Execution started at", start.isoformat())
    print ("Preparing parameter and output files...", end="", flush=True)

    # At first: open the Output-File --> "SCHATSI_included.csv"
    # LOCAL PATH FOR TESTING:
    # output = open("SCHATSI_included.csv", 'w', newline='')
    # PATH FOR DOCKER:
    output = open("data/output/SCHATSI_included.csv", 'w', newline='')
    # create a writer object, which is used to write the lines into the csv
    file = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    # onetime writing of a headline into the csv
    kopfzeile = ["filename", "type", "included", "excluded"]
    file.writerow(kopfzeile)

    """
    preparation of data_cleansing.csv 
    """
    # LOCAL PATH FOR TESTING:
    # data_cleansing = open("SCHATSI_data_cleansing.csv", 'w', newline='')
    # PATH FOR DOCKER:
    data_cleansing = open("data/output/SCHATSI_data_cleansing.csv", 'w', newline='')
    data_cleansing_file = csv.writer(data_cleansing, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    kopfzeile_data_cleansing = ["filename", "type", "Total Count"]
    data_cleansing_file.writerow(kopfzeile_data_cleansing)


    """
    preparation of schatsi_references.csv
    """
    # LOCAL PATH FOR TESTING:
    # refs = open("SCHATSI_references.csv", 'w', newline='')
    # PATH FOR DOCKER:
    refs = open("data/output/SCHATSI_references.csv", 'w', newline='')
    refs_file = csv.writer(refs, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    kopfzeile_refs = ["filename", "reference_author", "reference_year", "reference_title"]
    refs_file.writerow(kopfzeile_refs)

    """
    preparation of schatsi_terms.csv
    """
    # LOCAL PATH FOR TESTING:
    # terms = open("SCHATSI_terms.csv", 'w', newline='')
    # PATH FOR DOCKER:
    terms = open("data/output/SCHATSI_terms.csv", 'w', newline='')
    terms_file = csv.writer(terms, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    kopfzeile_terms = ["filename", "term", "term count"]
    terms_file.writerow(kopfzeile_terms)

    """
    Preparation of the Stopwords for use in SCHATSI004 functions - import from file "SCHATSI_stopwords.csv
    """
    stopwords_list = []
    # LOCAL FOR TESTING:
    # with open('SCHATSI_stopwords.csv') as stop:
    # PATH FOR DOCKER:
    with open('data/params/SCHATSI_stopwords.csv') as stop:
        csv_reader_object = csv.reader(stop)
        for row in csv_reader_object:
            stopwords_list.append(row[0])
    stopwords = set(stopwords_list)

    print("done")

    input_dir = 'data/input'
    print ("Processing files in ", input_dir, "...")

    # For all paths, subdirectories and files in the input-folder do:
    # LOCAL PATH FOR TESTING: "r'/home/h/Github/Testpdfs'"
    # for path, subdirs, files in os.walk(r'/home/h/Downloads/Testpdfs'):
    # PATH FOR DOCKER:
    for path, subdirs, files in os.walk(input_dir):
        for filename in files:
            print (filename)

            # with data path
            g = os.path.join(path, filename)

            # Filename in 'Schatsi_included.txt' schreiben, ohne den Dateipfad/ in csv-Datei
            f = os.path.join(filename)

            # try to read in a pdf and extract text from it
            try:
                with open(g, "rb") as pdffile:
                    # create an object which is filled with a raw byte stream, which contains the text from the pdf
                    pdf = pdftotext.PDF(pdffile)
                    # force python to turn the byte stream into a string
                    text = "\n\n".join(pdf)
            # if there is an exception or an error, they will be catched and the file wont be included in the next steps
            except:
                if f.endswith(".pdf") or f.endswith(".PDF"):
                    datatype = "pdf"
                elif f.endswith(".txt") or f.endswith(".TXT"):
                    datatype = "txt"
                elif f.endswith(".csv") or f.endswith(".CSV"):
                    datatype = "csv"
                elif f.endswith(".docx") or f.endswith(".DOCX"):
                    datatype = "docx"
                elif f.endswith(".odt") or f.endswith(".ODT"):
                    datatype = "odt"
                else:
                    datatype = "unknown datatype"
                zeile = [f, datatype, "__", "X"]
            # if it succeeds do:
            else:
                if f.endswith(".pdf") or f.endswith(".PDF"):
                    datatype = "pdf"
                    # All files that are successfully read in where the type is 'pdf' will be used in the next steps
                    text_only, references = SCHATSI003.string_preparation(text)
                    total_num_words = SCHATSI003.count_words(text_only)
                    zeile_data_cleansing = [filename, datatype, total_num_words]
                    data_cleansing_file.writerow(zeile_data_cleansing)

                    reference_list = SCHATSI003.references(references)
                    for element in reference_list:
                        author, year, title = SCHATSI003.reference_data_cutting(element)
                        refs_zeile = [filename, author, year, title]
                        refs_file.writerow(refs_zeile)

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
                        zeile_terms = [filename, mono_filtered[i], mono_number[i]]
                        terms_file.writerow(zeile_terms)
                    for j in range(0, len(bigram_filtered)):
                        bi = bigram_filtered[j][0] + " " + bigram_filtered[j][1]
                        zeile_terms = [filename, bi, bigram_number[j]]
                        terms_file.writerow(zeile_terms)
                    for k in range(0, len(trigram_filtered)):
                        tri = trigram_filtered[k][0] + " " + trigram_filtered[k][1] + " " + trigram_filtered[k][2]
                        zeile_terms = [filename, tri, trigram_number[k]]
                        terms_file.writerow(zeile_terms)

                elif f.endswith(".txt") or f.endswith(".TXT"):
                    datatype = "txt"
                elif f.endswith(".csv") or f.endswith(".CSV"):
                    datatype = "csv"
                elif f.endswith(".docx") or f.endswith(".DOCX"):
                    datatype = "docx"
                elif f.endswith(".odt") or f.endswith(".ODT"):
                    datatype = "odt"
                else:
                    datatype = "unknown datatype"

                zeile = [f, datatype, "X", "__"]

            file.writerow(zeile)

            # the outputfile will get a layout like this
            """
            filename | type | included | excluded
            --------------------------------------
            abc.pdf  | pdf  |     X    |    __        <-- The text of this document could be extracted without any problems
            err.pdf  | pdf  |    __    |     X        <-- There was a problem and the document text could not be extracted,
            ...                                           the files wont be included in the next steps 
            ...
            """


    # Calculate the runtime -> last step of the programm

    # second timestamp
    finish = datetime.now()
    print ("Execution finished at", finish.isoformat())
    # calculation of the duration
    duration_program = (finish - start).seconds / 60

    # write start_normalized, finish_normalized and duration into "SCHATSI_runtime.csv"
    datetime_format = "%m/%d/%Y %H:%M:%S"
    zeile_runtime = [start.strftime(datetime_format), finish.strftime(datetime_format), duration_program]
    runtime_file.writerow(zeile_runtime)

if __name__ == "__main__":
    main()