# Triplet Extraction webapp 
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

The following is the code base for the web application - DBpedia Extract. The application extracts triples from text and displays the rdf generated from the triples extracted. 

The application can be found - `http://text2rdf.linkeddata.es` [link](http://text2rdf.linkeddata.es)

![image](main.png)

The application runs on `Flask`, uses `stanford coreNLP`, Google's `SyntaxNet` and `Spacy` for parsers and dependency parsers. RDF generated from the application is in the `turtle` format.