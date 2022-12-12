import argparse
import re
parser = argparse.ArgumentParser()
parser.add_argument('--gene_file', type=str, required=True)
parser.add_argument('--proteome_fa', type=str, required=True)
args = parser.parse_args()

motif = r""
with open(args.gene_file, 'r') as blastgene:
    for prot in blastgene:
        motif = motif + re.escape(prot.strip()) + "|"
    motif = motif[:-1]

blast_gene = re.compile(motif)
proteome_header = re.compile(r">")

unmatched = 0
with open(args.proteome_fa, 'r') as protmatch:
    while True:
        if not unmatched:
            ln = protmatch.readline().strip()
        unmatched = 0
        if blast_gene.search(ln):
            head_split = ln.split() #splits between the gap
            gene_id = head_split[0] #keep the formated header
            print(gene_id) #print in file
            ln = protmatch.readline().strip()
            while not proteome_header.search(ln):
                print(ln) #print the seq
                ln = protmatch.readline().strip()
                unmatched = 1
        if not ln:
            break
