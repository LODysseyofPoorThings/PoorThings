from lxml import etree
import os

# Define the absolute paths for the XML and XSLT files
base_path = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(base_path, "tei.xml")
xslt_path = os.path.join(base_path, "html.xslt")

# Load XML input and XSLT stylesheet
xml_doc = etree.parse(xml_path)
xslt_doc = etree.parse(xslt_path)

# Create an XSLT transformer
transform = etree.XSLT(xslt_doc)

# Apply the transformation
result_tree = transform(xml_doc)

# Output the transformed HTML to a new file
with open(os.path.join(base_path, "result_conversion.html"), "wb") as f:
    f.write(etree.tostring(result_tree, pretty_print=True))