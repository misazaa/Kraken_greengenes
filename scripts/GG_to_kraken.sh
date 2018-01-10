#!/bin/bash

echo "Downloading GreenGenes fasta.gz file with headers..."
wget ftp://greengenes.microbio.me/greengenes_release/current/gg_13_5_with_header.fasta.gz
echo "Extracting fasta.gz archive..."
gunzip gg_13_5_with_header.fasta.gz
echo "Extracted!"

echo "Creating tsv file with sequences headers from full fasta file..."
headers=$(mktemp)
grep '>.*' gg_13_5_with_header.fasta >> headers
gg_IDs=$(mktemp)
cut -d'	' -f1 headers | cut -d'>' -f2 >> gg_IDs
acc_num=$(mktemp)
cut -d'	' -f2 headers | cut -d'.' -f1 >> acc_num
acc_ver=$(mktemp)
cut -d'	' -f2 headers >> acc_ver
names=$(mktemp)
cut -d'	' -f3 headers >> names
taxonomy=$(mktemp)
cut -d'	' -f4 headers >> taxonomy
kingdom=$(mktemp)
cut -d';' -f1 taxonomy | awk -F 'k__' '{print $2}' >> kingdom
phylum=$(mktemp)
cut -d';' -f2 taxonomy | awk -F 'p__' '{print $2}' >> phylum
class=$(mktemp)
cut -d';' -f3 taxonomy | awk -F 'c__' '{print $2}' >> class
order=$(mktemp)
cut -d';' -f4 taxonomy | awk -F 'o__' '{print $2}' >> order
family=$(mktemp)
cut -d';' -f5 taxonomy | awk -F 'f__' '{print $2}' >> family
genus=$(mktemp)
cut -d';' -f6 taxonomy | awk -F 'g__' '{print $2}' >> genus
species=$(mktemp)
cut -d';' -f7 taxonomy | awk -F 's__' '{print $2}' >> species

# Separated by tabs due to commas inside fields
echo "gg_ID	Accession	Version	Sci_Name	Kingdom	Phylum	Class	Order	Family	Genus	Species" > gg_13_5_header.tsv
paste -d'	' gg_IDs acc_num acc_ver names kingdom phylum class order family genus species >> gg_13_5_header.tsv

rm headers gg_IDs acc_num acc_ver names taxonomy kingdom phylum class order family genus species

echo "Created!"

echo "Removing duplicates from original fasta file..."

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' seqkit | grep "install ok installed")
echo Checking for seqkit: $PKG_OK
if [ "" == "$PKG_OK" ]; then
	echo "No seqkit. Setting up seqkit."
	wget -q "https://github.com/shenwei356/seqkit/releases/download/v0.7.2/seqkit_linux_amd64.tar.gz"
	tar -zxvf *.tar.gz
	rm seqkit_linux_amd64.tar.gz
	cp seqkit /usr/local/bin/
	rm seqkit
fi

seqkit rmdup -s gg_13_5_with_header.fasta > gg_13_5_with_header_noDUPS.fasta

echo "Removed duplicated sequences!"

echo "Creating tsv file with sequences headers from non-dups fasta file..."
headers=$(mktemp)
grep '>.*' gg_13_5_with_header_noDUPS.fasta >> headers
gg_IDs=$(mktemp)
cut -d'	' -f1 headers | cut -d'>' -f2 >> gg_IDs
acc_num=$(mktemp)
cut -d'	' -f2 headers | cut -d'.' -f1 >> acc_num
acc_ver=$(mktemp)
cut -d'	' -f2 headers >> acc_ver
names=$(mktemp)
cut -d'	' -f3 headers >> names
taxonomy=$(mktemp)
cut -d'	' -f4 headers >> taxonomy
kingdom=$(mktemp)
cut -d';' -f1 taxonomy | awk -F 'k__' '{print $2}' >> kingdom
phylum=$(mktemp)
cut -d';' -f2 taxonomy | awk -F 'p__' '{print $2}' >> phylum
class=$(mktemp)
cut -d';' -f3 taxonomy | awk -F 'c__' '{print $2}' >> class
order=$(mktemp)
cut -d';' -f4 taxonomy | awk -F 'o__' '{print $2}' >> order
family=$(mktemp)
cut -d';' -f5 taxonomy | awk -F 'f__' '{print $2}' >> family
genus=$(mktemp)
cut -d';' -f6 taxonomy | awk -F 'g__' '{print $2}' >> genus
species=$(mktemp)
cut -d';' -f7 taxonomy | awk -F 's__' '{print $2}' >> species

# Separated by tabs due to commas inside fields
echo "gg_ID	Accession	Version	Sci_Name	Kingdom	Phylum	Class	Order	Family	Genus	Species" > gg_13_5_header_noDups.tsv
paste -d'	' gg_IDs acc_num acc_ver names kingdom phylum class order family genus species >> gg_13_5_header_noDups.tsv

rm headers gg_IDs acc_num acc_ver names taxonomy kingdom phylum class order family genus species

echo "Creating names.dmp, nodes.dmp and fasta file with headers specific for Kraken..."

python GG_to_kraken.py gg_13_5_header.tsv gg_13_5_header_noDups.tsv

awk '/^>/{getline < "gg_13_5_headers_kraken_noDUPS.txt"}1' gg_13_5_with_header_noDUPS.fasta > gg_13_5_kraken_ready.fasta

rm gg_13_5_header.tsv gg_13_5_with_header_noDUPS.fasta gg_13_5_header_noDups.tsv

echo "Created!"
echo "Done!"

