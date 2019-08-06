from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF

def createRDF(annotated_triples, triples):
    """
    returns string with the triples in the rdf 'turtle' format. This can be written to file
    """
    rdfGraph = Graph()
    for i in range(len(triples)):
        subject = URIRef(annotated_triples[i][0])
        predicate = None
        if annotated_triples[i][1]:
            predicate = URIRef(annotated_triples[i][1])
        else:
            predicate_obj = BNode()
            rdfGraph.add( (predicate_obj, FOAF.name, Literal(triples[i][1])) )
            rdfGraph.add( (predicate_obj, RDF.type, RDF.Property) )
        predicate = URIRef(triple[1])
        obj = URIRef(triple[2])

        rdfGraph.add( (subject, predicate, obj) ) 
    return rdfGraph.serialize(format='turtle')

def writeRDFtoFile(annotated_triples, triples, destination):
    rdfGraph = Graph()
    for i in range(len(triples)):
        subject = URIRef(annotated_triples[i][0])
        predicate = None
        if annotated_triples[i][1]:
            predicate = URIRef(annotated_triples[i][1])
        else:
            predicate_obj = BNode()
            rdfGraph.add( (predicate_obj, FOAF.name, Literal(triples[i][1])) )
            rdfGraph.add( (predicate_obj, RDF.type, RDF.Property) )
        predicate = URIRef(triple[1])
        obj = URIRef(triple[2])

        rdfGraph.add( (subject, predicate, obj) ) 
    rdfGraph.serialize(format='turtle', destination=destination)