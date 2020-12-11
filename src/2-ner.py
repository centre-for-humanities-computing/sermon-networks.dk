"""
NER for sermons in content.dat
"""
import os
import pandas as pd
import numpy as np
from polyglot.text import Text
import nltk.data
from nltk.stem.snowball import DanishStemmer
stemmer = DanishStemmer()

if __name__ == "__main__":
    """
    First processing to create NER outputs
    """
    df = pd.read_csv(os.path.join("data", "content", "content.dat", 
                        encoding='utf-8', 
                        header = 0, 
                        index_col = None))

    content = df["content"].tolist()
    fnames = df["id"].tolist()
    tokenizer = nltk.data.load(os.path.join("tokenizers", "punkt", "norwegian.pickle"))

    entity_list = []
    i = 0
    for i, text in enumerate(content):
    #for i, text in enumerate(content[:4]):
        print(f"file {i}")
        # sentence disambiguation
        sents = tokenizer.tokenize(text)
        # NER1
        text_entities = []
        for blob in sents:
            textblob = Text(blob, hint_language_code='da')
            text_entities.append(textblob.entities)
            #if textblob.entities:
            #    text_entities.append(textblob.entities)
        entity_list.append([fnames[i],text_entities])
        
    df_ner = pd.DataFrame(entity_list)
    df_ner.columns = ["id", "NE"]
    df_ner.to_csv(os.path.join("data", "content_entities.dat", index = False))


    """
    Extract all occurrences of I-PER at sentence level for each document.
    """
    entity_class = "I-PER"
    entities = df_ner["NE"].tolist()
    fname = df_ner["id"]

    out = []
    for i, doc in enumerate(entities):
        for ii, sent in enumerate(doc):
            if sent:
                for entity in sent:
                    if entity.tag == entity_class:
                        out.append([fname[i], ii, (", ".join(entity))])
    people = pd.DataFrame(out)
    people.columns = ["fname","sentence", entity_class]

    # Clean up any punctuation, whitespace, etc
    people["I-PER"] = people['I-PER'].str.replace('[^\w\s]','')
    # To lower
    people["I-PER"] = people["I-PER"].str.lower()
    # Replace any empty cells with Nan; remove NaN
    people["I-PER"].replace('', np.nan, inplace=True)
    people = people.dropna()

    # Stem remaining names with Snowball
    # This is far from perfect but it gets rid of things like possessives
    people["I-PER"] = people["I-PER"].apply(lambda x: stemmer.stem(x))
    people.to_csv(os.path.join("data",f"content_{entity_class}.dat", index = False))

    """
    Join with metadata
    """
    meta = pd.read_excel(os.path.join("data", "meta", "Joined_Meta.xlsx"))
    ner_people_with_meta = people.merge(meta, 
                                        left_on='fname', 
                                        right_on='ID-dok', 
                                        how='left')
    ner_people_with_meta.to_csv(os.path.join("data", "ner_people_with_meta.dat", 
                                        encoding='utf8')

