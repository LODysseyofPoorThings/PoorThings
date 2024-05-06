import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, DC, DCTERMS, XSD
import pandas as pd

#Namespaces
CDWA = Namespace("https://www.getty.edu/research/publications/electronic_publications/cdwa/")
SCHEMA = Namespace("https://schema.org/")
CIDOC_CRM = Namespace("https://www.cidoc-crm.org/")
pt = Namespace("https://w3id.org/PoorThings.org/")

#creating uris
item = URIRef(pt + "item/")
person = URIRef(pt + "person/")
place = URIRef(pt + "place/")
time = URIRef(pt + "time/")
group = URIRef(pt + "group/")
concept = URIRef(pt + "concept/")

#creating a rdf graph
g = rdflib.Graph()

#bind namespaces to graph
g.bind("rdf", RDF)
g.bind("dcterms", DCTERMS)
g.bind("dc", DC)
g.bind("owl", OWL)
g.bind("cdwa", CDWA)
g.bind("schema", SCHEMA)
g.bind("cidoc-crm", CIDOC_CRM)

df_monument = pd.read_csv("csv files/lighthouse_of_alexandria.csv")

for _, row in df_monument.iterrows():

    subject_uri = URIRef(item + row["Subject"])
    predicate = row["Predicate"]
    obj = row["Object"]

    if "rdf" in predicate:
        ps = predicate.split(":")
        predicate_uri = RDF + ps[1]
        obj = URIRef(obj)
    
    g.add((subject_uri, predicate_uri, obj))  

g.serialize("output3.ttl", format="turtle", encoding="utf8")

'''
obj = row["Object"]
        
if predicate in [RDF.type, OWL.sameAs]:
    obj = URIRef(obj)
elif predicate in [DC.creator, CDWA.Commissioner, SCHEMA.agent]:
    obj = URIRef(person + obj).replace(" ", "_")
elif predicate in [DCTERMS.spatial, CDWA.CurrentLocation]:    
    obj = URIRef(place + obj).replace(" ", "_")
elif predicate is DCTERMS.isPartOf:
    obj = URIRef(group + obj).replace(" ", "_")
else:
    obj = Literal((obj), datatype=XSD.string)    

g.add((subject_uri, predicate, obj))    

g.serialize("output3.ttl", format="turtle", encoding="utf8")
'''