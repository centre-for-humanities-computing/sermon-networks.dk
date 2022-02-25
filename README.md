# Studying sermons in the Danish national church

This repository contains code and data in relation the following publication:

Agersnap, A, Kristensen-McLachlan, R.D., & Johansen, K.H. (2022). "*Unveiling the character gallery - A social network analysis of 11,955 Danish sermons*", Tenemos, [Edition TBC].

In this article, we present the results of a network analysis performed on named entities extracted from a corpus of 11,995 Danish sermons.

## Content

All code used in the article can be found in the folder ```src```. All code is written in Python and is modular. Scripts are numbered sequentially, in the order that they should be executed, with each creating transformed data for the next script to use.

The is presented for evaluative purposes only. These scripts would require substantial refactoring in order to be considered production-ready!

The results of the final script in ```src``` is a weighted edgelist, which is to then be read into the network analysis software [Gephi](https://gephi.org/).

## Methodology

The 'raw data' of the sermons is in the form of Word documents (both .docx and .doc format). These formats are not generally amenable to being used by computational tools. To begin, then, the first step of our method is to 'extract' the text from the Word files and to save these separately. This is performed by the script in ```src/1-doc2text.py```, which extracts the text of the sermon and the sermon ID.

Having extracted this data, is is now saved in a tabular format with one sermon per row. The next step is then to find all of the 'named entities' that appear in each of the sermons. To do this, we used a *named entity recognition* script, found in ```src/2-ner.py```. This script goes through the text extracted at the previous step, finds text which seems to refer to individual people, and then saves only these named entities. The output of this step is therefore another tabular structure with one sermon per row, with named entities linked to the sermon in which they appear. At the time of conducting this research, the most effective NER library for Danish langage text was the Python library called ```Polyglot```, which is what we used here. Recently, new Python packages like ```stanza``` or ```spaCy``` which rely entirly on *neural architectures* have been created and might perform slightly better, if this experiment were to be repeated.

The output from the initial NER are somewhat 'noisy' and require additional cleaning. Moreover, in some case multiple names might refer to the same person, such as *Jesus* and *Kristus*. To fix this, a list was created manually to map the noisy data onto a cleaner, more compact set of names. This list can be found in ```meta/map.csv```.

The extracted entities are used to create an *edgelist* which is used for network analysis. For our purposes, an *edge* is created between characters if they appear together in a sermon. For example, if a sermon mentions both Mary and Joseph, this creates the edge (Mary, Joseph). Our edgelist is *weighted*, meaning that we count the number of times a particular pairing occurs in the corpus. So if Mary in Joseph appear in 10 sermons together, we'd have (Mary, Joseph, 10). 

It is important to note that these edges are *undirected*, insofar as there is no directed interaction between these characters. This is unlike a situation where two characters interat in a *directed* manner, such as Mary speaking *to* Joseph. Directed and undirected networks have different underlying properties from a mathematical perspective, so it is necessary to specify that our network is undirected. So, to indicate this in our example, our complete edge would then be (Mary, undirected, Joseph, 10). The script ```src/3-edges.py``` automatically extracts this undirected, weighted edgelist for all of our data and saves it in ```output/all_edges.csv```. 

Finally, this edgelist was read into the network analysis software [Gephi](https://gephi.org/) for further analysis. Using Gephi, we calculated a number of different metrics which might be used to study the network, which can be found in ```output/network_node_metrics.csv```. While we primarily focus on *modularity* in the article, each of the metrics in this table are potentially of interest from a network analysis perspective. The file ```ouput/dk_sermons.gephi``` is a *graph file* exported from Gephi, and which can be read into the programme again for closer inspection of the structure of the network.

## Output

There are a number of relevant and interrelated outputs in the ```output``` folder. These are:

| File | Description|
|--------|:-----------|
| all_edges.csv | A weighted edgelist of named entities, to be read into Gephi |
| dk_sermons.gephi | A graph file created by Gephi from the file above |
| network_node_metrics.csv | A table of node metrics for every character in the character gallery |

## Data Access
Unfortunately, for reasons of data protective and privacy, we are unable to share either the sermons or the metadata in relation to this corpus.

However, if you are interested in working with the data for a specific research project, you can contact either of the first two listed authors.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
