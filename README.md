# Studying sermons in the Danish national church

This repository contains code and repo in relation the following publication:

Agersnap, A, Kristensen-McLachlan, R.D., and Johansen, K.H. (TBC). 'Unveiling the character gallery - A social network analysis of 11,955 Danish sermons', TBC.

In this article, we present the results of a network analysis performed on named entities extracted from a corpus of 11,995 Danish sermons.

## Content

All code used in the article can be found in the folder ```src```. All code is written in Python and is modular. Scripts are numbered sequentially, in the order that they should be executed, with each creating transformed data for the next script to use.

The is presented for evaluative purposes only. These scripts would require substantial refactoring in order to be considered production-ready!

The results of the final script in ```src``` is a weighted edgelist, which is to then be read into the network visualisation software (Gephi)[https://gephi.org/].

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
