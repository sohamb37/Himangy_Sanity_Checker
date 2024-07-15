import pandas as pd
import numpy as np
import re
import sys
import argparse
# from langdetect import detect
from fastlangid.langid import LID

def main():
    ## Setting up the argument parser
    parser = argparse.ArgumentParser(description="The command is python sanity.py <filename> <source_lang_code> <target_lang_code>. Note: Language detection method is unavailable for Dogri (doi) and Kashmiri (ks).")
    parser.add_argument('filename', type=str, help='The name of the file to process')
    parser.add_argument('src_lang', type=str, help='The source language code')
    parser.add_argument('tgt_lang', type=str, help='The target language code')
    
    ## Parse arguments
    args = parser.parse_args()
    
    filename = args.filename
    src_lang = args.src_lang
    tgt_lang = args.tgt_lang

    ## Reading the file
    with open(filename, "r", encoding="utf-8") as f:
        f = f.readlines()

    data = pd.DataFrame(columns=["src", "tgt"])
    itr = 0
    for itr, line in enumerate(f):
        if line.count('\t') == 0:
            print("No tab in line number:", itr+1,"This is either an empty line or a line with only source text.")
            data.loc[itr, 'src'] = line
        elif line.count('\t') > 1:
            print("Multiple tabs exist in line number:", itr+1, "The entire line is considered as source text.")
            data.loc[itr, "src"] = line
        else:
            data.loc[itr, 'src'] = line.split('\t')[0]
            data.loc[itr, 'tgt'] = line.split('\t')[1]        

    # Language Pairs:
    # Dogri - doi*
    # Gujrati - gu
    # Hindi - hi
    # Kannada - kn
    # Kashmiri - ks*
    # Odiya - or*
    # Punjabi - pa
    # Sindhi - sd*
    # Telegu - te
    # Urdu - ur
    # Wrong alignment and  detection of different sentences in the '*' marked languages are not feasible

    # Checking if the input language pairs belong to the list of languages or not
    lang_list = ["doi", "gu", "hi", "kn", "ks", "or", "pa", "sd", "te", "ur"]
    if src_lang not in lang_list or tgt_lang not in lang_list:
        print("This language pair is not supported")
        sys.exit()
    # Checking if the source and target language codes are the same or not
    elif src_lang == tgt_lang:
        print("Source and target language code is the same")
        sys.exit()
    # Checking if the input file is empty or not
    elif len(data) == 0:
        print("The input file is empty")
        sys.exit()
    else:
        # The file is otherwise loaded
        print("The input file is loaded successfully")

    # Checking if an abnormal new line is inserted in the text and corrected
    def detect_inserted_line(text):
        for char in text:
            if char == '\n':
                return True
            else:
                return False

    # Checking if the text is empty or not
    def detect_empty_line(text):
        return text == ""

    # Checking if the input text has only url
    def detect_only_url(text):
        url_pattern = re.compile(r'(https?://(?:www\.)?|www\.)[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+(/[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=%]*)?')
        final_text = url_pattern.sub('', text)
        if final_text.strip() == "":
            return True
        else:
            return False

    # Checking if the text has only symbols and special characters and no words
    def detect_no_words(text):
        special_c = re.compile(r'[^\w\s]')
        final_text = special_c.sub('', text)
        if final_text.strip() == "":
            return True
        else:
            return False

    # Checking for untranslated data
    def detect_untranslated_data(source, target):
        if source.lower() == target.lower():
            return True
        else:
            return False

    # Checking if the text language is different from expected language.
    # This is not applicable for these language codes = ["ks", "doi", "sn", "or"]   
    def detect_different_sentence(code, text):
        if code in ["ks", "doi"]:
            return False
        else:
            try:
                langid = LID()
                detected_lang = langid.predict(text)
                if code != detected_lang:
                    return True
                else:
                    return False
            except Exception as e:
                return True

    # Checking if wrong alignment is existent. 
    # This is not applicable for these language codes = ["ks", "doi", "sn", "or"]
    def detect_reverse_alignment(source, target, src_code, tgt_code):
        if src_lang in ["ks", "doi"] or tgt_lang in ["ks", "doi"]:
            return False
        else:
            try:
                langid = LID()
                source_lang = langid.predict(source)
                target_lang = langid.predict(target)
                if source_lang == tgt_code and target_lang == src_code:
                    return True
                else:
                    return False
            except Exception as e:
                return True

    # An error list is created for a specific line
    # All the errors in the line are combined to give an error_string
    # This error_string is then appended to errors_list
    # Lastly this errors list is added as a column to a new tsv file with the data
    no_of_unique_lines_with_error = 0
    errors_list = []
    for i in range(len(data)):
        src_line = str(data.iloc[i]['src']).strip()
        tgt_line = str(data.iloc[i]['tgt']).strip()
        error = []
        src_empty = False
        tgt_empty = False
        if detect_inserted_line(src_line):
            error.append("Newline detected in source!")
        if detect_inserted_line(tgt_line):
            error.append("Newline detected in target!")
        if detect_only_url(src_line):
            error.append("Only URL detected in source!")
        if detect_only_url(tgt_line):
            error.append("Only URL detected in target!")        
        if detect_empty_line(src_line):
            error.append("Empty line detected in source!")
            src_empty = True
        if detect_empty_line(tgt_line):
            error.append("Empty line detected in target!")
            tgt_empty = True
        if detect_no_words(src_line) and not src_empty:
            error.append("No word detected in source!")
        if detect_no_words(tgt_line) and not tgt_empty:
            error.append("No word detected in target!")
        if detect_untranslated_data(src_line, tgt_line) and (not src_empty) and (not tgt_empty):
            error.append("Untranslated data!")
        if detect_different_sentence(src_lang, src_line) and not src_empty:
            error.append("Warning! Different language may be present in source text!")
        if detect_different_sentence(tgt_lang, tgt_line) and not tgt_empty:
            error.append("Warning! Different language may be present in target text!")
        if detect_reverse_alignment(src_line, tgt_line, src_lang, tgt_lang):
            error.append("Warning! Probable Wrong Alignment!")

        if len(error) > 0:
            no_of_unique_lines_with_error += 1        
            error_string = " ".join(error)
            errors_list.append(error_string)
            print("Error at line no. ", i+1,error_string)
        else:
            errors_list.append("OK")

    print("\n Total number of errors in the file: ", no_of_unique_lines_with_error)
    data['errors'] = errors_list
    data.to_csv(filename + ".errors.tsv", sep="\t", index = 'False')

if __name__ == "__main__":
    main()
