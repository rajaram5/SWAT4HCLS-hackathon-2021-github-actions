import re
import glob
import logging
import sys

# set log level
logging.basicConfig(level=logging.INFO)

root_path = "../"

for filename in glob.iglob(root_path+ '**/*.ttl', recursive=True):
		logging.info("Validating rdf file " + filename)
		try:
			#Open file and reads it
			filename = "test-ttl.ttl"
			with open(filename) as f:
				content = f.read()

			#Get all prefixes
			declared_prefixes = re.findall(r'@prefix(.*?)<', content)
			declared_prefixes = [x.strip().split(":")[0] for x in declared_prefixes]

			#Remove prefixes from content
			content = re.sub(r'@prefix(.*?)\n', '', content)

			#Get used prefixes
			used_prefixes = re.findall(r'.*?\:.*? ', content)
			used_prefixes = [x.split(":")[0].split(" ")[-1] for x in used_prefixes]

			#Fix literals
			used_prefixes = [x.split("^^")[-1].split(":")[0] for x in used_prefixes]

			#Remove duplicates
			used_prefixes = list(dict.fromkeys(used_prefixes))

			#Remove used prefixes from the declared prefixes list
			unused_prefixes = [x for x in declared_prefixes if x not in used_prefixes]

			if len(unused_prefixes) > 0:
				msg = ''
				for u in unused_prefixes:
					msg = msg + u + '\n'
				raise Exception("Unused prefix: {}".format(msg))

		except Exception as e:
			print(e)
			logging.error(e)
			logging.error("Syntaxic error reading turtle file [" +filename+"]")
			sys.exit(1)

print("RDF files syntaxic validation is successful")