import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, DC, DCTERMS, XSD, FOAF, SKOS
import pandas as pd

#Namespaces
CDWA = Namespace("https://www.getty.edu/research/publications/electronic_publications/cdwa/")
SCHEMA = Namespace("https://schema.org/")
CRM = Namespace("https://www.cidoc-crm.org/")
MO = Namespace("http://musicontology.com/")
DBO = Namespace("https://dbpedia.org/ontology/")
DBP = Namespace("https://dbpedia.org/page/DBP/")
FABIO = Namespace("https://sparontologies.github.io/fabio/current/fabio.html")

#creating a rdf graph
g = rdflib.Graph()

#base_uri
pt = URIRef("https://w3id.org/PoorThings.org/") 

#creating uris
item = URIRef(pt + "item/")
person = URIRef(pt + "person/")
organization = URIRef(pt + "organization/")
place = URIRef(pt + "place/")
time = URIRef(pt + "time/")
group_of_objects = URIRef(pt + "group_of_objects/")
group_of_people = URIRef(pt + "group_of_people/")
concept = URIRef(pt + "concept/")
conceptual_object = URIRef(pt + "conceptual_object/")
song = URIRef(pt + "song/")
phisical_thing = URIRef(pt + "phisical_thing/")

#bind namespaces to graph
g.bind("cdwa", CDWA)
g.bind("schema", SCHEMA)
g.bind("crm", CRM)
g.bind("mo", MO)
g.bind("dbo", DBO)
g.bind("dbp", DBP)
g.bind("fabio", FABIO)

#list of csv files
files_csv = ["csv files/poor_things_movie.csv", "csv files/activity.csv", "csv files/article.csv", "csv files/bio_ent_char.csv", "csv files/bio_ent_person.csv", "csv files/movie.csv", "csv files/monument.csv", "csv files/book.csv", "csv files/painting.csv", "csv files/portrait.csv", "csv files/soundtrack.csv"]

#for loop that iterates all the csv files and add data to the same graph
for file in files_csv:

    #create a pandas dataframe to read csv 
    df = pd.read_csv(file)   
    
    #dict to store uris
    uris_dict = dict()

    items_list = ["Activity", "Article", "Biographic entity character", "Biographic entity person", "Book", "Monument", "Movie", "Painting", "Portrait", "Soundtrack", "Poor Things Movie"]
 
    #iterate through the dataframe:
    for _, row in df.iterrows():
        
        #get row's subject, predicate and object
        subject = row["Subject"]
        predicate = row["Predicate"]
        object = row["Object"]
        
        #create subject uri
        if subject not in uris_dict:
            subject_uri = URIRef(item + subject.replace(" ", "_"))
            uris_dict[subject] = subject_uri   
        else:
            subject_uri = uris_dict[subject]
                                                                   
        #specify predicates
        if predicate == "rdf:type":
            predicate_uri = RDF.type

        elif predicate== "owl:sameAs":
            predicate_uri = OWL.sameAs 
        
        elif predicate == "dc:publisher":
            predicate_uri = DC.publisher
 
        elif predicate == "dc:subject":
            predicate_uri = DC.subject

        elif predicate == "dcterms:creator":
            predicate_uri = DCTERMS.creator        

        elif predicate == "dcterms:created":
            predicate_uri = DCTERMS.created

        elif predicate == "dcterms:temporal":
            predicate_uri = DCTERMS.temporal    

        elif predicate == "dcterms:issued":
            predicate_uri = DCTERMS.issued    

        elif predicate == "dcterms:spatial":
            predicate_uri = DCTERMS.spatial 

        elif predicate == "dcterms:hasPart":
            predicate_uri = DCTERMS.hasPart

        elif predicate == "dcterms:isPartOf":
            predicate_uri = DCTERMS.isPartOf

        elif predicate == "dcterms:references":
            predicate_uri = DCTERMS.references

        elif predicate == "dcterms:isReferencedBy":
            predicate_uri = DCTERMS.isReferencedBy

        elif predicate == "dcterms:extent":
            predicate_uri = DCTERMS.extent                

        elif predicate == "foaf:member":
            predicate_uri = FOAF.member

        elif predicate == "foaf:name":
            predicate_uri = FOAF.name            

        elif predicate == "cdwa:Commissioner":
            predicate_uri = CDWA.Commissioner

        elif predicate == "cdwa:DimensionDescription":
            predicate_uri = CDWA.DimensionDescription       

        elif predicate == "cdwa:MaterialTechniqueDescription":
            predicate_uri = CDWA.MaterialTechniqueDescription

        elif predicate == "cdwa:Style":
            predicate_uri = CDWA.Style    

        elif predicate == "schema:gender":
            predicate_uri = SCHEMA.gender

        elif predicate == "schema:genre":
            predicate_uri = SCHEMA.genre    

        elif predicate == "schema:hasOccupation":
            predicate_uri = SCHEMA.hasOccupation    

        elif predicate == "schema:birthPlace":
            predicate_uri = SCHEMA.birthPlace

        elif predicate == "schema:birthDate":
            predicate_uri = SCHEMA.birthDate        

        elif predicate == "schema:parent":
            predicate_uri = SCHEMA.parent

        elif predicate == "schema:character":
            predicate_uri = SCHEMA.character    

        elif predicate == "schema:award":
            predicate_uri = SCHEMA.award               

        elif predicate == "schema:containedInPlace":
            predicate_uri = SCHEMA.containedInPlace

        elif predicate == "schema:containsPlace":
            predicate_uri = SCHEMA.containsPlace    

        elif predicate == "schema:startDate":
            predicate_uri = SCHEMA.startDate

        elif predicate == "schema:endDate":
            predicate_uri = SCHEMA.endDate

        elif predicate == "schema:agent":
            predicate_uri = SCHEMA.agent

        elif predicate == "schema:isBasedOn":
            predicate_uri = SCHEMA.isBasedOn   

        elif predicate == "schema:inLanguage":
            predicate_uri = SCHEMA.inLanguage

        elif predicate == "schema:copyrightHolder":
            predicate_uri = SCHEMA.copyrightHolder      

        elif predicate == "crm:P102_has_title":
            predicate_uri = CRM.P102_has_title

        elif predicate == "crm:P2_has_type":
            predicate_uri = CRM.P2_has_type   

        elif predicate == "crm:P14_carried_out_by":
            predicate_uri = CRM.P14_carried_out_by    

        elif predicate == "crm:P55_has_current_location":
            predicate_uri = CRM.P55_has_current_location    

        elif predicate == "crm:P129_is_about":
            predicate_uri = CRM.P129_is_about       

        elif predicate == "crm:P21_had_general_purpose":
            predicate_uri = CRM.P21_had_general_purpose

        elif predicate == "crm:P82a_begin_of_the_begin":
            predicate_uri = CRM.P82a_begin_of_the_begin 

        elif predicate == "crm:P82b_end_of_the_end":
            predicate_uri = CRM.P82b_end_of_the_end

        elif predicate == "dbp:yeardeactivated":
            predicate_uri = DBP.yeardeactivated

        elif predicate == "mo:published_as":
            predicate_uri = MO.published_as                

        #specify if objects are uris or litterals and add uris to uris_dict
        if predicate_uri == RDF.type:
            if object == "crm:E7_Activity":
                obj = CRM.E7_Activity
            elif object == "crm:E21_Person":
                obj = CRM.E21_Person  
            elif object == "crm:E53_Place":
                obj = CRM.E53_Place
            elif object == "crm:E4_Period":
                obj = CRM.E4_Period
            elif object == "crm:E52_Time-Span":
                obj = CRM.E52_Time_Span
            elif object == "crm:E74_Group":
                obj = CRM.E74_Group  
            elif object == "crm:E28_Conceptual_Object":
                obj = CRM.E28_Conceptual_Object
            elif object == "crm:E79_Curated_Holding":
                obj = CRM.E79_Curated_Holding   
            elif object == "schema:Movie":
                obj = SCHEMA.Movie
            elif object == "schema:Organization":
                obj = SCHEMA.Organization        
            elif object == "foaf:Group":
                obj = FOAF.Group
            elif object == "skos:Concept":
                obj = SKOS.Concept
            elif object == "mo:soundtrack":
                obj = MO.soundtrack
            elif object == "mo:track":
                obj = MO.track
            elif object == "fabio:journalarticle":
                obj = FABIO.journalarticle
            elif object == "dbo:Artwork":
                obj = DBO.Artwork    
            elif object == "dbo:Monument":
                obj = DBO.Monument 
            elif object == "dcterms:BibliographicResource":
                obj = DCTERMS.BibliographicResource 

        elif predicate_uri == OWL.sameAs:
            obj = URIRef(object)
        
        elif predicate_uri == DCTERMS.references or predicate_uri == DCTERMS.isReferencedBy or predicate_uri == SCHEMA.character or predicate_uri == SCHEMA.isBasedOn or predicate_uri == DCTERMS.hasPart:
            if object not in uris_dict:  
                obj = URIRef(item + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]     

        elif predicate_uri == CRM.P129_is_about:
            if object not in uris_dict:
                if object in items_list:
                    obj = URIRef(item + object.replace(" ", "_"))
                    uris_dict[object] = obj
                elif object == "Feminism":
                    obj = URIRef(concept + object.replace(" ", "_"))
                    uris_dict[object] = obj
                else:
                    obj = URIRef(phisical_thing + object.replace(" ", "_"))
                    uris_dict[object] = obj
            else:
                obj = uris_dict[object]

        elif predicate_uri == DCTERMS.creator:
            if object not in uris_dict:
                if object in items_list:
                    obj = URIRef(item + object.replace(" ", "_"))
                    uris_dict[object] = obj
                else:    
                    obj = URIRef(person + object.replace(" ", "_"))
                    uris_dict[object] = obj
            else:
                obj = uris_dict[object]           
        
        elif predicate_uri == CDWA.Commissioner or predicate_uri == CRM.P14_carried_out_by:
            if object not in uris_dict:
                obj = URIRef(person + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]    

        elif predicate_uri == FOAF.member:
            if object not in uris_dict:
                groups_list = ["Greek Weird Wave", "Ptolemaic dinasty", "Young upper-class men"]
                if object in groups_list:
                    obj = URIRef(group_of_people + object.replace(" ", "_"))
                    uris_dict[object] = obj
                else:
                    obj = URIRef(person + object.replace(" ", "_"))
                    uris_dict[object] = obj    
            else:
                obj = uris_dict[object] 
         
        elif predicate_uri == SCHEMA.agent:
            if object not in uris_dict:
                if object in items_list:
                    obj = URIRef(item + object.replace(" ", "_"))
                    uris_dict[object] = obj
                else:
                    obj = URIRef(group_of_people + object.replace(" ", "_"))
                    uris_dict[object] = obj
            else:
                obj = uris_dict[object]                    

        elif predicate_uri == DC.publisher or predicate_uri == SCHEMA.copyrightHolder:
            if object not in uris_dict:
                obj = URIRef(organization + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]      

        elif predicate_uri == DCTERMS.spatial or predicate_uri == CRM.P55_has_current_location or predicate_uri == SCHEMA.containedInPlace or predicate_uri == SCHEMA.containsPlace or predicate_uri == SCHEMA.birthPlace:    
            if object not in uris_dict:
                obj = URIRef(place + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]    

        elif predicate_uri == DCTERMS.isPartOf:
            if object not in uris_dict:
                obj = URIRef(group_of_objects + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]          

        elif predicate_uri == CRM.P21_had_general_purpose:
            if object not in uris_dict:
                obj = URIRef(concept + object.replace(" ", "_"))
                uris_dict[object] = obj
            else:
                obj = uris_dict[object]    

        elif predicate_uri == MO.published_as:
            if object not in uris_dict:
                obj = URIRef(song + object.replace(" ", "_"))
                uris_dict[object] = obj   
            else:
                obj = uris_dict[object]

        elif predicate_uri == SCHEMA.parent:
            if object not in uris_dict:
                obj = URIRef(conceptual_object + object.replace(" ", "_"))
                uris_dict[object] = obj  
            else:
                obj = uris_dict[object]        

        elif predicate_uri == DCTERMS.created:
            if object not in uris_dict:
                if "-" in object:    
                    obj = URIRef(time + object.replace(" ", "_"))
                    uris_dict[object] = obj  
                else:
                    obj = Literal(object, datatype=XSD.gYear)
            else:
                obj = uris_dict[object]    
        
        elif predicate_uri == DCTERMS.issued:
            if object not in uris_dict:
                if "-" in object:
                    obj = Literal(object, datatype=XSD.date)   
                else:
                    obj = Literal(object, datatype=XSD.gYear)   
            else:
                obj = uris_dict[object]               

        elif predicate_uri == DCTERMS.temporal:
            if object not in uris_dict:
                obj = URIRef(time + object.replace(" ", "_"))
                uris_dict[object] = obj       
            else:
                obj = uris_dict[object]

        elif predicate_uri == SCHEMA.startDate or predicate_uri == SCHEMA.endDate or predicate_uri == CRM.P82a_begin_of_the_begin or predicate_uri == CRM.P82b_end_of_the_end or predicate_uri == SCHEMA.birthDate or predicate_uri == DBP.yeardeactivated:
            obj = Literal(object, datatype=XSD.gYear)

        elif predicate_uri == DCTERMS.extent:
             obj = Literal(object, datatype=XSD.dayTimeDuration)    

        elif predicate_uri == SCHEMA.inLanguage:
            obj = Literal(object, datatype=XSD.language)    

        else:
            obj = Literal(object, datatype=XSD.string)      

        #add triple to graph
        g.add((subject_uri, predicate_uri, obj))

#serialize the graph to Turtle format
turtle_str = g.serialize(format="turtle", base=pt, encoding="utf-8")

#write the Turtle string to a file
with open("output_rdf_visualization.ttl", "wb") as f:
    f.write(turtle_str)
  