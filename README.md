# Kraken Greengenes
Conversion of Greengenes database taxonomy and fasta file into formats adequate for building a Kraken (DerrickWood, https://github.com/DerrickWood/kraken) custom Greengenes DB. The correspondence between Greengenes and NCBI identifiers and accession numbers is unsuitable since most of the sequences in NCBI aren't well annotated in terms of taxonomy. The process available in this repository manages to build a Greengenes custom DB for Kraken with the Greengenes sequences and taxonomy.

- Folder 'files' has files and a README with instructions to simply and quickly get the needed files to build the Greengenes Kraken DB.

- Folder 'scripts' has 2 scripts (one bash, one python) and a README that can be used to carry out the whole process from scratch and in a fully automated way with only one initial command.
