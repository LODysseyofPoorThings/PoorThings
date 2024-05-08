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
g.bind("cdwa", CDWA)
g.bind("schema", SCHEMA)
g.bind("cidoc-crm", CIDOC_CRM)

files_csv = ["csv files/lighthouse_of_alexandria.csv", "csv files/portrait.csv", "csv files/grand_tour.csv"]

for file in files_csv:

    df = pd.read_csv(file)

    for _, row in df.iterrows():

        subject_uri = URIRef(item + row["Subject"].replace(" ", "_"))
        predicate = row["Predicate"]
        obj = row["Object"]

        if predicate == "rdf:type":
            predicate_uri = RDF.type

        elif predicate== "owl:sameAs":
            predicate_uri = OWL.sameAs

        elif predicate == "dc:title":
            predicate_uri = DC.title 

        elif predicate == "dc:creator":
            predicate_uri = DC.creator    

        elif predicate == "dc:subject":
            predicate_uri = DC.subject    

        elif predicate == "dcterms:created":
            predicate_uri = DCTERMS.created

        elif predicate == "dcterms:spatial":
            predicate_uri = DCTERMS.spatial 

        elif predicate == "dcterms:isPartOf":
            predicate_uri = DCTERMS.isPartOf    

        elif predicate == "cdwa:Commissioner":
            predicate_uri = CDWA.Commissioner

        elif predicate == "cdwa:DimensionDescription":
            predicate_uri = CDWA.DimensionDescription  

        elif predicate == "cdwa:CurrentLocation":
            predicate_uri = CDWA.CurrentLocation      

        elif predicate == "cdwa:MaterialTechniqueDescription":
            predicate_uri = CDWA.MaterialTechniqueDescription

        elif predicate == "schema:material":
            predicate_uri = SCHEMA.material    

        elif predicate == "schema:startDate":
            predicate_uri = SCHEMA.startDate

        elif predicate == "schema:endDate":
            predicate_uri = SCHEMA.endDate

        elif predicate == "schema:name":
            predicate_uri = SCHEMA.name

        elif predicate == "schema:agent":
            predicate_uri = SCHEMA.agent

        elif predicate == "cidoc-crm:P21 had general purpose":
            predicate_uri = CIDOC_CRM.P21hadGeneralPurpose


        if predicate_uri == RDF.type or predicate_uri == OWL.sameAs:
            obj = URIRef(obj)

        elif predicate_uri == DC.creator or predicate_uri == CDWA.Commissioner or predicate_uri == SCHEMA.agent:
            obj = URIRef(person + obj.replace(" ", "_"))

        elif predicate_uri == DCTERMS.spatial or predicate_uri == CDWA.CurrentLocation:    
            obj = URIRef(place + obj.replace(" ", "_"))

        elif predicate_uri == DCTERMS.isPartOf:
            obj = URIRef(group + obj.replace(" ", "_"))

        elif predicate_uri == DCTERMS.created or predicate_uri == SCHEMA.startDate or predicate_uri == SCHEMA.endDate:    
            obj = URIRef(time + obj.replace(" ", "_")) 

        elif predicate_uri == CIDOC_CRM.P21hadGeneralPurpose:
            obj = URIRef(concept + obj.replace(" ", "_"))   

        else:
            obj = Literal(obj, datatype=XSD.string)    


        g.add((subject_uri, predicate_uri, obj))    

g.serialize("outputprova3.ttl", format="turtle", encoding="utf8")                                 
                          