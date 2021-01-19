# Checks if all declared prefixes are used in the RDF File

import glob
import logging
import sys
import rdflib
from rdflib import Graph, RDF, URIRef
from rdflib.namespace import NamespaceManager

# set log level
logging.basicConfig(level=logging.INFO)

root_path = "../"

rdf_file_extension = {".ttl": "turtle", ".nt": "nt", ".rdf": "application/rdf+xml"}

for extension in rdf_file_extension.keys():
    files_to_check = "**/*" + extension

    for filename in glob.iglob(root_path + files_to_check, recursive=True):
        logging.info("Validating file " + filename)
        try:
            g = Graph()
            g = g.parse(filename, format=rdf_file_extension[extension])

            # Get declared prefixes
            declared_prefixes = [n for n in g.namespace_manager.namespaces()]

            # Get prefixes used through the file
            used_prefixes_p = [e.n3(g.namespace_manager).split(":")[0] for e in g.predicates(None, None)]
            used_prefixes_o = [e.n3(g.namespace_manager).split(":")[0] for e in g.objects(None, None)]
            used_prefixes = used_prefixes_p + used_prefixes_o

            # Remove duplicates
            used_prefixes = list(dict.fromkeys(used_prefixes))

            # Remove used prefixes from declared prefixes list
            unused_prefixes = [x for x in declared_prefixes if x[0] not in used_prefixes]

            # Remove xml and xds
            unused_prefixes = [x for x in unused_prefixes if all([x[0] != 'xml', x[0] != 'xsd', x[0] != 'rdfs'])]

            if len(unused_prefixes) > 0:
                msg = ''
                for u in unused_prefixes:
                    msg = msg + u[0] + '\n'
                raise Exception("Unused prefix: {}".format(msg))

        except Exception as e:
            logging.error(e)
            logging.error("Syntaxic error reading turtle file [" + filename + "]")
            sys.exit(1)

    print("Files prefixs validation is successful")