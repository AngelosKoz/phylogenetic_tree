# %3A = ":" // %28 = "(" // %29 = ")"


#example: python3 protein_family.py --organism human --family aquaporine

import argparse
import requests
import csv
parser = argparse.ArgumentParser(description='Add Command Line Inputs')
parser.add_argument('--family', type=str, required=True)
parser.add_argument('--organism', type=str, required=True)
parser.add_argument('--score', type=str, required=True)
args = parser.parse_args()

protein = args.family
ref_organism = args.organism
score = args.score
ref_organism_id = args.organism


if ref_organism == "human":
    ref_organism_id = str(9606)
    
if ref_organism == "chimp" or ref_organism == "chimpanzee":
    ref_organism_id = str(9598)
    
elif ref_organism == "mouse" or ref_organism == "mus":
    ref_organism_id = str(10090)

elif ref_organism == "drosophila" or ref_organism == "melanogaster":
    ref_organism_id = str(7227)
else:
    with open('uniprot_organism_id.tsv', newline = '') as g:
        uniprot_file = csv.reader(g, delimiter = '\t')
        for orgid in uniprot_file:
            if str(ref_organism_id) == str(orgid[2]):
                temp_file = open("Reference_Organism.name", "a")
                n = temp_file.write(orgid[1])
                n = temp_file.write("\n")
                temp_file.close()
                break


output_file = 'pre_'+protein+'_'+ref_organism+'.fa'

url='https://rest.uniprot.org/uniprotkb/stream?format=fasta&query=%28%28protein_name%3A'+protein+'%29%20AND%20%28organism_id%3A'+ref_organism_id+'%29%29%20AND%20%28annotation_score%3A'+score+'%29'

with requests.get(url, stream=True) as request:
    request.raise_for_status()
    with open(output_file, 'wb') as f:
        for chunk in request.iter_content(chunk_size=2**20):
            f.write(chunk)
