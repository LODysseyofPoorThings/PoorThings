import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, DC, DCTERMS, XSD, FOAF
import pandas as pd

#Namespaces
CDWA = Namespace("https://www.getty.edu/research/publications/electronic_publications/cdwa/")
SCHEMA = Namespace("https://schema.org/")
CRM = Namespace("https://www.cidoc-crm.org/")
MO = Namespace("http://musicontology.com/")
DBO = Namespace("https://dbpedia.org/ontology/")

#creating a rdf graph
g = rdflib.Graph()

#base_uri
pt = URIRef("https://w3id.org/PoorThings.org/") 

#creating uris
item = URIRef(pt + "item/")
person = URIRef(pt + "person/")
place = URIRef(pt + "place/")
time = URIRef(pt + "time/")
group = URIRef(pt + "group/")
concept = URIRef(pt + "concept/")

#bind namespaces to graph
g.bind("cdwa", CDWA)
g.bind("schema", SCHEMA)
g.bind("crm", CRM)
g.bind("mo", MO)
g.bind("dbo", DBO)

#list of csv files
files_csv = ["csv files/monument.csv",  "csv files/poor_things_movie.csv", "csv files/portrait.csv", "csv files/activity.csv", "csv files/book.csv", "csv files/article.csv", "csv files/movie.csv", "csv files/painting.csv", "csv files/bio_ent_char.csv", "csv files/bio_ent_pers.csv", "csv files/soundtrack.csv"]

#for loop that iterates all the csv files and add data to the same graph
for file in files_csv:

    #create a pandas dataframe to read csv 
    df = pd.read_csv(file)
    
    #dict to store uris
    uris_dict = dict()
 
    #iterate through the dataframe:
    for _, row in df.iterrows():
        
        #get row's subject, predicate and object
        subject = row["Subject"]
        predicate = row["Predicate"]
        object = row["Object"] 
        
        #create subject uri
        if subject not in uris_dict:
            subject_uri = URIRef((item + subject).replace(" ", "_"))
            uris_dict[subject] = subject_uri
        else:
            subject_uri = uris_dict[subject]
                                                                   
        #specify predicates
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

        elif predicate == "crm:P21_had_general_purpose":
            predicate_uri = CRM.P21_had_general_purpose

        elif predicate == "crm:P82a_begin_of_the_begin":
            predicate_uri = CRM.P82a_begin_of_the_begin 

        elif predicate == "crm:P82b_end_of_the_end":
            predicate_uri = CRM.P82b_end_of_the_end        

        #specify if objects are uris or litterals and add uris to uris_dict
        if predicate_uri == RDF.type or predicate_uri == OWL.sameAs:
            obj = URIRef(object)

        elif predicate_uri == DC.creator or predicate_uri == CDWA.Commissioner or predicate_uri == SCHEMA.agent:
            obj = URIRef(person + object.replace(" ", "_"))
            uris_dict[object] = obj

        elif predicate_uri == DCTERMS.spatial or predicate_uri == CDWA.CurrentLocation:    
            obj = URIRef(place + object.replace(" ", "_"))
            uris_dict[object] = obj

        elif predicate_uri == DCTERMS.isPartOf:
            obj = URIRef(group + object.replace(" ", "_"))
            uris_dict[object] = obj 

        elif predicate_uri == CRM.P21_had_general_purpose:
            obj = URIRef(concept + object.replace(" ", "_"))
            uris_dict[object] = obj

        elif predicate_uri == DCTERMS.created:
            if "-" in object:    
               obj = URIRef(time + object.replace(" ", "_"))
               uris_dict[object] = obj
            else:
                obj = Literal(object, datatype=XSD.gYear)   

        elif predicate_uri == SCHEMA.startDate or predicate_uri == SCHEMA.endDate or predicate_uri == CRM.P82a_begin_of_the_begin or predicate_uri == CRM.P82b_end_of_the_end:
            obj = Literal(object, datatype=XSD.gYear)

        else:
            obj = Literal(object, datatype=XSD.string)    

        #add triple to graph
        g.add((subject_uri, predicate_uri, obj))

# Serialize the graph to Turtle format
turtle_str = g.serialize(format="turtle", base=pt, encoding="utf-8")

# Write the Turtle string to a file
with open("output.ttl", "wb") as f:
    f.write(turtle_str)