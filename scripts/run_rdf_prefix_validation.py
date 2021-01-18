#Checks if all declared prefixes are used in the RDF File

import glob
import logging
import sys
import rdflib
from rdflib import Graph, RDF, URIRef
from rdflib.namespace import NamespaceManager

# set log level
logging.basicConfig(level=logging.INFO)

root_path = "../"

for filename in glob.iglob(root_path+ '**/*.rdf', recursive=True):
        logging.info("Validating rdf file " + filename)
        try:
            g = Graph()
            g = g.parse(filename)

            #Get declared prefixes
            declared_prefixes = [n for n in g.namespace_manager.namespaces()]

            #Get prefixes used through the file
            used_prefixes = [e.n3(g.namespace_manager).split(":")[0] for e in g.predicates(None, None)]
            #Remove duplicates
            used_prefixes = list(dict.fromkeys(used_prefixes))

            #Remove used prefixes from declared prefixes list
            unused_prefixes = [x for x in declared_prefixes if x[0] not in used_prefixes]

            #Remove xml and xds
            unused_prefixes = [x for x in unused_prefixes if all([x[0] != 'xml', x[0] != 'xsd'])]

            if len(unused_prefixes) > 0:
                msg = ''
                for u in unused_prefixes:
                    msg = msg + u[0] + '\n'
                raise Exception("Unused prefix: {}".format(msg))

        except Exception as e:
                logging.error(e)
                logging.error("Syntaxic error reading turtle file [" +filename+"]")
                sys.exit(1)

print("RDF files syntaxic validation is successful")
