import xml.etree.ElementTree as ET
import rdflib
from rdflib import Namespace, URIRef, Literal
from rdflib.namespace import RDF, FOAF, RDFS, DC, DCTERMS

#namespaces definition
TEI = Namespace("http://www.tei-c.org/ns/1.0")
DBO = Namespace("https://dbpedia.org/ontology/")
SCHEMA = Namespace("https://schema.org/")

#parsing the xml document
tree = ET.parse('tei.xml')

#creating a graph
g = rdflib.Graph()

#define namespace for tei
ns = {"tei": TEI}

#base_uri
pt = URIRef("https://w3id.org/PoorThings.org/")

#bind namespaces to graph
g.bind("dbo", DBO)
g.bind("schema", SCHEMA)

#extraction of metadata
title = tree.find(".//tei:titleStmt/tei:title", ns).text
author = tree.find(".//tei:titleStmt/tei:author", ns).text
format = tree.find(".//tei:editionStmt/tei:edition", ns).text
extent = tree.find(".//tei:extent", ns).text
publisher = tree.find(".//tei:publicationStmt/tei:publisher/tei:orgName", ns).text
address = tree.find(".//tei:publicationStmt/tei:address/tei:addrLine", ns).text
id = tree.find(".//tei:publicationStmt/tei:idno", ns).text
copyright = tree.find(".//tei:publicationStmt/tei:availability/tei:p", ns).text
date = tree.find(".//tei:publicationStmt/tei:date", ns).text

#metadata uris
title_uri = URIRef(pt + title.replace(" ", "_"))
author_uri = URIRef(pt + author.replace(" ", "_"))
publisher_uri = URIRef(pt + publisher.replace(" ", "_"))

#adding metadata triples to the graph
g.add((title_uri, RDF.type, DCTERMS.BibliographicResource))
g.add((title_uri, DC.creator, author_uri))
g.add((title_uri, DCTERMS.issued, Literal(date)))
g.add((title_uri, DC.format, Literal(format)))
g.add((title_uri, DCTERMS.extent, Literal(extent)))
g.add((title_uri, DCTERMS.publisher, publisher_uri))
g.add((title_uri, DC.identifier, Literal(id)))
g.add((title_uri, DC.rights, Literal(copyright)))
g.add((author_uri, RDF.type, FOAF.Person))
g.add((title_uri, RDFS.label, Literal(title)))
g.add((publisher_uri, RDF.type, DBO.publisher))
g.add((publisher_uri, SCHEMA.address, Literal(address)))

#characters extraction
for character in tree.findall(".//tei:profileDesc/tei:particDesc/tei:listPerson/tei:person", ns):
    name = character.find("tei:persName", ns).text.rstrip()
    id = character.get("{http://www.w3.org/XML/1998/namespace}id")
    character_uri = URIRef(pt + "character/" + name.replace(" ", "_"))
    g.add((character_uri, RDF.type, FOAF.Person))
    g.add((character_uri, RDFS.label, Literal(name)))

    if character.find("tei:occupation", ns) is not None:
        occupation = character.find("tei:occupation", ns).text
        g.add((character_uri, SCHEMA.hasOccupation, Literal(occupation)))

    for line in tree.findall(".//tei:text/tei:body/tei:div/tei:l", ns):
        text = ''.join(line.itertext())
        mention = line.find("tei:name[@type='person']", ns)
        if mention is not None:
            ref = mention.get("ref").strip('#')
            if ref == id:
                g.add((character_uri, DCTERMS.isReferencedBy, Literal(text)))
        
#places extraction       
for line in tree.findall(".//tei:text/tei:body/tei:div/tei:l", ns):
    text = ''.join(line.itertext())
    place = line.find("tei:name[@type='place']", ns)
    if place is not None:
        place_uri = URIRef(pt + "place/" + place.text.replace(" ", "_"))
        g.add((place_uri, RDF.type, SCHEMA.place))
        g.add((place_uri, RDFS.label, Literal(place.text)))
        g.add((place_uri, DCTERMS.isReferencedBy, Literal(text)))

                
#serialize the graph to Turtle format
g.serialize("output_xml_rdf.ttl", format="turtle", encoding="utf-8")
