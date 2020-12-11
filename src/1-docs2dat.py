# coding=utf-8
"""
Old script for extracting text from Doc and Docx

This is large obsolete now; most functionality can be
replace by one-liners using the ```docx``` library.
"""

import os, re
import docx2txt, textract
import pandas as pd

def list_files(dirpath):
    """
    Walk all files in directory 'dir' and subdirectories
    """
    r = []
    for root, dirs, files in os.walk(dirpath):
        for name in files:
            r.append(os.path.join(root, name))
    return r

if __name__ == "__main__":
    # denoise fnames
    pattern = re.compile("~")

    # Data not included in repo - privacy and security reasons
    path = os.path.join("data" ,"PRÆDIKENER_RENSET")

    # Cleaning up filenames, etc
    fnames = sorted(list_files(path))
    errors = []
    clean_fnames = []
    for i, fname in enumerate(fnames):
        tmp = fname.split("/")[-1]
        if pattern.match(tmp):
            errors.append(i)
        else:
            clean_fnames.append(fname)

    # classify file type and remove metadata
    clean_fnames.pop(0)
    clean_fnames.pop(0)
    data = []
    pat1 = re.compile(r"% \S+")
    pat2 = re.compile(r"\n+")
    i = 0

    # For each sermon
    for fname in clean_fnames:
        print("file {}".format(i))
        i += 1
        filetype = fname.split(".")[-1]
        # Select correct filetype
        if filetype == "doc":
            text = textract.process(fname).decode('utf-8')
        elif filetype == "docx":
            text = docx2txt.process(fname)
        else:
            print(fname)# TODO read odt
        # remove metadata
        text = pat1.sub("", text)
        text = pat2.sub("\n", text)
        #append to dataframe
        data.append([fname.split("/")[-1].split(".")[0], text])

    # save df, keeping only sermon_ID and text content
    df = pd.DataFrame(data)
    df.columns = ["id", "content"]
    outpath =  os.path.join("data", "content.dat")
    df.to_csv(outpath, encoding='utf-8')
