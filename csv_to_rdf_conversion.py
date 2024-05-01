import csv
from csv import DictReader
import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, DC, DCTERMS, XSD, FOAF, RDFS
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
group = URIRef(pt + "group/")
concept = URIRef(pt + "concept/")

#creating a rdf graph
g = rdflib.Graph()

#bind namespaces to graph
g.bind("cdwa", CDWA)
g.bind("schema", SCHEMA)
g.bind("cido-crm", CIDOC_CRM)

df_monument = pd.read_csv("csv files/lighthouse_of_alexandria.csv")

monument_uri = URIRef(item + df_monument.loc[0]["Subject"])
g.add((monument_uri, RDF.type, URIRef(df_monument.loc[0]["Object"])))
g.add((monument_uri, OWL.sameAs, URIRef(df_monument.loc[1]["Object"])))
g.add((monument_uri, DC.title, Literal(df_monument.loc[2]["Object"], datatype=XSD.string)))
g.add((monument_uri, DCTERMS.created, Literal(df_monument.loc[3]["Object"], datatype=XSD.gYear)))
g.add((monument_uri, CDWA.Commissioner, URIRef(person + df_monument.loc[4]["Object"].replace(" ", "_"))))
g.add((monument_uri, DCTERMS.spatial, URIRef(place + df_monument.loc[5]["Object"].replace(" ", "_"))))
g.add((monument_uri, SCHEMA.material, Literal(df_monument.loc[6]["Object"], datatype=XSD.string)))
g.add((monument_uri, CDWA.DimensionDescription, Literal(df_monument.loc[7]["Object"], datatype=XSD.string)))
g.add((monument_uri, SCHEMA.endDate, Literal(df_monument.loc[8]["Object"], datatype=XSD.gYear)))
g.add((monument_uri, DCTERMS.isPartOf, URIRef(group + df_monument.loc[8]["Object"].replace(" ", "_"))))

df_portrait = pd.read_csv("csv files/portrait.csv")

portrait_uri = URIRef(item + df_portrait.loc[0]["Subject"])
g.add((portrait_uri, RDF.type, URIRef(df_portrait.loc[0]["Object"])))
g.add((portrait_uri, OWL.sameAs, URIRef(df_portrait.loc[1]["Object"])))
g.add((portrait_uri, DC.title, Literal(df_portrait.loc[2]["Object"], datatype=XSD.string)))
g.add((portrait_uri, DCTERMS.created, Literal(df_portrait.loc[3]["Object"], datatype=XSD.gYear)))
g.add((portrait_uri, DC.creator, URIRef(person + df_portrait.loc[4]["Object"].replace(" ", "_"))))
g.add((portrait_uri, CDWA.CurrentLocation, URIRef(place + df_portrait.loc[5]["Object"].replace(" ", "_"))))
g.add((portrait_uri, CDWA.MaterialTechniqueDescription, Literal(df_portrait.loc[6]["Object"], datatype=XSD.string)))
g.add((portrait_uri, CDWA.DimensionDescription, Literal(df_portrait.loc[7]["Object"], datatype=XSD.string)))
g.add((portrait_uri, DC.subject, Literal(df_portrait.loc[8]["Object"], datatype=XSD.string)))

df_activity = pd.read_csv("csv files/grand_tour.csv")

activity_uri = URIRef(item + df_activity.loc[0]["Subject"])
g.add((activity_uri, RDF.type, URIRef(df_activity.loc[0]["Object"])))
g.add((activity_uri, OWL.sameAs, URIRef(df_activity.loc[1]["Object"])))
g.add((activity_uri, SCHEMA.name, Literal(df_activity.loc[2]["Object"], datatype=XSD.string)))
g.add((activity_uri, SCHEMA.agent, URIRef(person + df_activity.loc[3]["Object"].replace(" ", "_"))))
g.add((activity_uri, DCTERMS.spatial, URIRef(place + df_activity.loc[4]["Object"].replace(" ", "_"))))
g.add((activity_uri, SCHEMA.startDate, Literal(df_activity.loc[5]["Object"], datatype=XSD.string)))
g.add((activity_uri, SCHEMA.endDate, Literal(df_activity.loc[6]["Object"], datatype=XSD.string)))
g.add((activity_uri, CIDOC_CRM.P21HadGeneralPurpose, URIRef(concept + df_activity.loc[7]["Object"])))

g.serialize("output.ttl", format="turtle", encoding="utf8")