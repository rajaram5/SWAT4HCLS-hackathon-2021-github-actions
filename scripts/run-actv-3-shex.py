import re
import glob
import logging
import sys

# set log level
logging.basicConfig(level=logging.INFO)

root_path = "../"

for filename in glob.iglob(root_path+ '**/*.rdf', recursive=True):
        logging.info("Validating rdf file " + filename)
        try:
            #Open file and reads it
            with open(filename) as f:
                content = f.read()

            #Get all prefixes
            prefixes = re.findall(r'PREFIX(.*?)<', content)
            prefixes = [x.strip().split(":")[0] for x in prefixes]

            #Remove prefixes from content
            content = re.sub(r'PREFIX(.*?)\n', '', content)

            #Get all expressions and check if prefix occurs
            error = False
            unused = ''
            for p in prefixes:
                rgx = p + ':'
                rgx = re.compile(rgx)
                if rgx.search(content) == None:
                    error = True
                    unused = unused + p + '\n'
            
            #If at least one of them have not been used, raise exception
            if error:
                raise Exception("Unused prefix: {}".format(unused))
        except Exception as e:
                logging.error(e)
                logging.error("Syntaxic error reading turtle file [" +filename+"]")
                sys.exit(1)

print("RDF files syntaxic validation is successful")