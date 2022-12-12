
import argparse, requests, csv, os

parser = argparse.ArgumentParser(description='Add Command Line Inputs Prot')
parser.add_argument('--organism', type=str, required=True)
args = parser.parse_args()

proteome_organism_id = args.organism
output_file_prot= proteome_organism_id+'_proteome.fa'

if args.organism == "chimp" or args.organism == "chimpanzee":
    proteome_organism_id = "UP000002277"
elif args.organism == "mouse" or args.organism == "mus":
    proteome_organism_id = "UP000000589"
elif args.organism == "drosophila" or args.organism == "melanogaster":
    proteome_organism_id = "UP000000803"
else:
    with open('uniprot_organism_id.tsv', newline = '') as g:
        uniprot_file = csv.reader(g, delimiter = '\t')
        for protid in uniprot_file:
            if str(proteome_organism_id) == str(protid[0]):
                temp_file = open("Proteome_Organism.names", "a")
                n = temp_file.write(protid[1])
                n = temp_file.write("\n")
                temp_file.close()
                break

url_prot = 'https://rest.uniprot.org/uniprotkb/stream?format=fasta&query=%28proteome%3A'+proteome_organism_id+'%29'


with requests.get(url_prot, stream=True) as request: #pipeline etoimo. Xwrizei se mikra kommatia
    request.raise_for_status()
    with open(output_file_prot, 'wb') as f:
        for chunk in request.iter_content(chunk_size=2**20):
            f.write(chunk)
