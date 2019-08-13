from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF

def createRDF(annotated_triples, triples):
    """
    returns string with the triples in the rdf 'turtle' format. This can be written to file
    """
    rdfGraph = Graph()
    for i in range(len(triples)):
        subject = None
        predicate = None
        obj = None
        """
        subject checking 
        """
        if annotated_triples[i][0]:
            subject = URIRef(annotated_triples[i][0][0])
        else:
            subject_obj = BNode()
            rdfGraph.add( (subject, FOAF.name, Literal(triples[i][0])) )
        """
        predicate checking 
        """
        if annotated_triples[i][1]:
            predicate = URIRef(annotated_triples[i][1])
        else:
            predicate = BNode()
            rdfGraph.add( (predicate, FOAF.name, Literal(triples[i][1])) )
            # rdfGraph.add( (predicate, RDF.type, RDF.Property) )
        """
        object checking 
        """
        if annotated_triples[i][2]:
            obj = URIRef(annotated_triples[i][2][0])
        else:
            obj = BNode()
            rdfGraph.add( (obj, FOAF.name, Literal(triples[i][2])) )

        rdfGraph.add( (subject, predicate, obj) ) 
    return rdfGraph.serialize(format='turtle')

def writeRDFtoFile(annotated_triples, triples, destination):
    """
    returns string with the triples in the rdf 'turtle' format. This can be written to file
    """
    rdfGraph = Graph()
    for i in range(len(triples)):
        subject = None
        predicate = None
        obj = None
        """
        subject checking 
        """
        if annotated_triples[i][0]:
            subject = URIRef(annotated_triples[i][0][0])
            rdfGraph.add( (subject, RDF.type, FOAF.Document) )
        else:
            subject = BNode()
            rdfGraph.add( (subject, RDF.type, FOAF.Document) )
            rdfGraph.add( (subject, FOAF.name, Literal(triples[i][0])) )
        """
        predicate checking 
        """
        if annotated_triples[i][1]:
            predicate = URIRef(annotated_triples[i][1])
            rdfGraph.add( (predicate, RDF.type, FOAF.Property) )
        else:
            if triples[i][1] == "hypernym (low confidence)":
                triples[i][1] = "hypernym_low_confidence"
            predicate = URIRef("http://predicateProperty.org/{}".format(triples[i][1]))
            rdfGraph.add( (predicate, FOAF.name, Literal(triples[i][1])) )
            rdfGraph.add( (predicate, RDF.type, RDF.Property) )
        """
        object checking 
        """
        if annotated_triples[i][2]:
            obj = URIRef(annotated_triples[i][2][0])
            rdfGraph.add( (obj, RDF.type, FOAF.Document) )
        else:
            obj = BNode()
            rdfGraph.add( (obj, RDF.type, FOAF.Document) )
            rdfGraph.add( (obj, FOAF.name, Literal(triples[i][2])) )

        rdfGraph.add( (subject, predicate, obj) ) 
    rdfGraph.serialize(format='turtle', destination=destination)