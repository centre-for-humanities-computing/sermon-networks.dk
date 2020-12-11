"""
Creating edgelist from characters in sermons
"""
import os
import pandas as pd
import itertools
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict

def create_pairs(df):
    """
    df: Pandas dataframe
    
    Find all pairs of entities in any list of entities

    Returns list of paired tuples of the for [(A,B), (B,C)]
    """
    # Join as lists
    l = [''.join(row) for row in df["ID"]]
    # Tokenize strings
    w = [[x.strip() for x in my_string.split(',')] for my_string in l]
    # Create pairs
    pairs = [list(itertools.combinations(set(sermon), 2)) for sermon in w]
    # Create edgelist
    pairlist = [item for sublist in pairs for item in sublist]
    
    return pairlist

def create_edgelist_from(pairs):
    """
    pairs: A list of paired tuples, of the form [(A,B), (B,C)]
    
    Function to create edgelists

    Returns results in a way that will be useful in Gephi
    """
    # Create edgelist using defaultDict
    edges = defaultdict(int)
    for people in pairs:
        for personA in people:
            for personB in people:
                if personA < personB:
                    edges[personA + ",undirected," + personB] += 1

    # Create a dataframe from the defaultDict
    df = pd.DataFrame.from_dict(edges, orient='index')
    df.reset_index(level=0, inplace=True)
    # Split cell on comma into muliple columns
    split = (df['index'].str\
                        .split(',', expand=True)\
                        .rename(columns=lambda x: f"col{x+1}"))
    # Merge these split columns with the 'weights' from the first df
    merged = split.join(df[0])
    # Rename columns for use in Gephi
    merged.columns = ["Source", "Type", "Target", "Weight"]

    return merged

# Read data
maps = pd.read_csv(os.path.join("meta", "map.csv"))
data = pd.read_csv(os.path.join("data","all_entities.csv", sep="\t"))
merged = pd.merge(maps, data, 
                    left_on="Entity", 
                    right_on="Entity", 
                    how="outer")
merged["ID"].fillna(merged["Entity"], inplace=True)
#merged.to_csv(os.path.join("data", "cleaned_entities.csv"))

# Group by sermon
grouped = pd.DataFrame(merged\
                            .groupby('fname')['ID']\
                            .apply(lambda x: x.str.cat(sep=',')))

# Create edgelist
final_edges = create_edgelist_from(create_pairs(grouped))

# Save
final_edges.to_csv(os.path.join("output", "all_edges.csv", 
                                sep=",", 
                                index=False, 
                                header=True)
