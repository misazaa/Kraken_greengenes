These files can be used to obtain the Greengenes database for Kraken without running the scripts:

- gg_13_5_kraken_headers.txt.tar.gz
  - archive with a .txt file with the headers to switch for in the original fasta file (after removing duplicated sequences).
  - headers result of the concatenation: '>' + 'Greengenes identifier' + '|kraken:taxid|' + 'taxonomic id determined'
  
- names.dmp:
  - file that has the same format as the NCBI names.dmp file.
  - 1st field: the taxonomic id of the node, IDs are sequential (from 1 to 3094).
  - 2nd field: name designation of the node associated with the identifier.
  - 3rd field: unique variant of this name if name not unique (empty).
  - 4th field: type of name (all 'scientific name' since that's the only type of name provided and needed)
  
- nodes.dmp
  - file that has the same format as the NCBI nodes.dmp file.
  - 1st field: node id in the names.dmp file.
  - 2nd field: parent node id.
  - 3rd field: rank designation ('no rank' for 'root', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', species')
  - the last 3 fields are the only necessary and used by Kraken.
  
Instructions:

- Download Greengenes 13_5 fasta file from: ftp://greengenes.microbio.me/greengenes_release/current/gg_13_5_with_header.fasta.gz

- Remove duplicated sequences with the help of seqkit (https://github.com/shenwei356/seqkit)
 - Example command: seqkit rmdup -s gg_13_5_with_header.fasta > gg_13_5_with_header_noDUPS.fasta

- Switch headers from fasta file without duplicated sequences with the headers present in the gg_13_5_kraken_headers.txt file
  - Example command: awk '/^>/{getline < "gg_13_5_kraken_headers.txt"}1' gg_13_5_with_header_noDUPS.fasta > gg_13_5_kraken_ready.fasta

In order to construct the custom Greengenes database for Kraken:

- Create 'taxonomy' folder inside db directory and move Greengenes names.dmp and nodes.dmp to that folder.
- Add Greengenes fasta file without duplicates and with headers specific for Kraken to the db library.
  - Example command: kraken-build --add-to-library gg_13_5_kraken_ready.fasta --db <db_name>
- Build custom Greengenes database.
  - Example command: kraken-build --build --threads 4 --db <db_name>
  
After following these steps, the database should be ready to be used by Kraken to classify 16S sequences.
