# Triplet Extraction webapp 
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

The following is the code base for the web application - DBpedia Extract. The application extracts triples from text and displays the rdf generated from the triples extracted. The following is a project done under DBpedia during the summer of 2019 under the Google Summer of Code Program

The application can be found - `http://text2rdf.linkeddata.es` [link](http://text2rdf.linkeddata.es)

The manual for the following application can be found at the following [link](https://docs.google.com/document/d/1wjDltKVBqwjA3020mLj9TlBXviKq_f_n_Ga82tJJN6g/edit?usp=sharing)

Experiments, Results and other source code developed for the purpose of the application can be found [here](https://github.com/sahitpj/GSoC-codebase)

![image](main.png)

The application runs on `Flask`, uses `stanford coreNLP`, Google's `SyntaxNet` and `Spacy` for parsers and dependency parsers. RDF generated from the application is in the `turtle` format.
