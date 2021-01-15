import glob
import logging
from rdflib import Graph
import sys

# set log level
logging.basicConfig(level=logging.INFO)

root_path = "../"

for filename in glob.iglob(root_path+ '**/*.ttl', recursive=True):
     logging.info("Validating turtle file " + filename)
     try:
         g = Graph()
         g.parse(filename, format="ttl")
     except Exception as e:
         logging.error(e)
         logging.error("Syntaxic error reading turtle file [" +filename+"]")
         sys.exit(1)

print("RDF files syntaxic validation is successful")