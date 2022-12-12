echo '-- Example: bash ergasia_script.sh claudin human 5 --'
echo '-- Best works when using the Protein Name [DE] (ex. claudin) and Taxonomy ID [OC] (ex. 9606). The third variable is the annotation score (1-5) with 5 beeing the best. --'
echo '-- Organism ID can be found in the .tsv file --'
#Make variables
ref_prot=$1
ref_org=$2
ref_score=$3


python3 ergasia_get_ref_protein.py --family $ref_prot --organism $ref_org --score $ref_score

#Fix Headers of Reference Protein
sed 's/\ OS.*//g' pre_${1}_${2}.fa | sed 's/ /_/g' > ${1}_${2}.fa


#Python script to get the proteomes of interest
echo "-- If you are having trouble, make an org_proteome.txt with the organism's Proteome ID (e.x UP000002277) in each line --"
echo 'Downloading Proteomes'
for org in $( cat org_proteome.txt ); do
    echo "Downloading_Organism ${org}"
    python3 ergasia_get_proteome.py --organism $org 
done

#Fix Headers of Proteomes
echo 'Processing Proteomes'
for prtms in $( ls *_proteome.fa ); do
    mv ${prtms} ${prtms}.1
    sed 's/ /_/g' ${prtms}.1 | sed 's/_OS/ OS/g' > ${prtms}
    rm ${prtms}.1
done

    

#Blast pipe via diamond
#Insert name via the column of the organism_id

echo 'Starting Blast'
for j in $( ls *_proteome.fa ); do
    query=${1}_${2}.fa
    echo $query
    organism=$( echo $j | sed 's/_proteome.fa//' )
    echo 'Blast for: ${organism}'
    diamond makedb --in ${j} --db ${organism}
    diamond blastp --query $query --db ${organism}.dmnd --outfmt 6 --out ${1}\:${2}_VS_${organism}.blast --ultra-sensitive --threads 6
    cut -f2 ${1}\:${2}_VS_${organism}.blast | sort -u > ${organism}.genes
    python3 ergasia_seq.py --gene_file ${organism}.genes --proteome_fa ${j} > ${1}_${organism}.fa
done

#Make a joint file
cat ${1}_*.fa > combined_${1}.fa

echo "Preparing alignment file with mafft"

mafft combined_${1}.fa > ${1}.aln

echo '-- Alignment done. A cool way to check mafft results is: seaview file.aln (installation needed) --'

#Alternative way to run Phylogenetic tree with raxml-ng
#echo 'Starting Phylogenetic Tree via raxml-ng. This may take a while. Maybe it is time for some fresh air and water.'
#raxml-ng --all --msa ${1}.aln --model LG+G8+F --tree pars{10} --bs-trees 200

echo 'Starting Phylogenetic Tree via IQ tree. This may take a while. Maybe it is time for some fresh air and water.'

#With IQ tree
#iqtree -s ${1}.aln -m LG+G8+F

echo '- If protein_organism.fa has an ID name, then the reference organism name is found in the file Reference_Organism.name -'
echo '-- If proteome.fa has an ID name, then the proteome organism names are found in the file Proteome_Organism.names --'
echo '--- View Maximum Likelihood tree in NEWICK format from .treefile file. Example: figtree  example.treefile ---'
echo '-_-_-_- You are all done! Full result of the run (report file) is found as example.iqtree -_-_-_-'
