import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, DC, DCTERMS, XSD
import pandas as pd

#Namespaces
CDWA = Namespace("https://www.getty.edu/research/publications/electronic_publications/cdwa/")
SCHEMA = Namespace("https://schema.org/")
CIDOC_CRM = Namespace("https://www.cidoc-crm.org/")
DBPEDIA_OWL = Namespace("https://dbpedia.org/ontology/")
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
g.namespace_manager.bind('rdf', rdflib.namespace.RDF)
g.namespace_manager.bind('dcterms', rdflib.namespace.DCTERMS)
g.namespace_manager.bind('dc', rdflib.namespace.DC)
g.namespace_manager.bind('owl', rdflib.namespace.OWL)
g.bind("dbpedia-owl", DBPEDIA_OWL)
g.bind("cdwa", CDWA)
g.bind("schema", SCHEMA)
g.bind("cido-crm", CIDOC_CRM)

# Create predicate URIRefs
rdf_type = URIRef(RDF['type'])
owl_sameAs = URIRef(OWL['sameAs'])
dc_title = URIRef(DC['title'])
dc_subject = URIRef(DC['subject'])
cdwa_DimensionDescription = URIRef(CDWA['DimensionDescription'])
cdwa_MaterialTechniqueDescription = URIRef(CDWA['MaterialTechniqueDescription'])
schema_name = URIRef(SCHEMA['name'])
schema_material = URIRef(SCHEMA['material'])
dc_creator = URIRef(DC['creator'])
dcterms_spatial = URIRef(DCTERMS['spatial'])
dcterms_isPartOf = URIRef(DCTERMS['isPartOf'])
cidoc_crm_P21HadGeneralPurpose = URIRef(CIDOC_CRM['P21HadGeneralPurpose'])
dcterms_created = URIRef(DCTERMS['created'])
schema_startDate = URIRef(SCHEMA['startDate'])
schema_endDate = URIRef(SCHEMA['endDate'])

df_monument = pd.read_csv("csv files/lighthouse_of_alexandria.csv")

for _, row in df_monument.iterrows():

    subject_uri = URIRef(item + row["Subject"])
    predicate = row["Predicate"]
    obj = row["Object"]

    if predicate is rdf_type or predicate is owl_sameAs:
        obj = URIRef(obj)
    elif predicate is dc_title or predicate is schema_name or predicate is dc_subject or predicate is cdwa_DimensionDescription or predicate is cdwa_MaterialTechniqueDescription or predicate is schema_material:
       obj = Literal((obj), datatype=XSD.string)
    elif predicate is dc_creator or predicate is CDWA.Commissioner or predicate is SCHEMA.agent:
        obj = URIRef(person + obj).replace(" ", "_")
    elif predicate is dcterms_spatial or predicate is CDWA.CurrentLocation:    
        obj = URIRef(place + obj).replace(" ", "_")
    elif predicate is dcterms_isPartOf:
        obj = URIRef(group + obj).replace(" ", "_")

    g.add((subject_uri, predicate, obj))    

g.serialize("output3.ttl", format="turtle", encoding="utf8")    