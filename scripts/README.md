These scripts can be used to create all necessary files for the construction of a Greengenes 13_5 Kraken database.

- GG_to_kraken.sh
  - Bash script with commands to download the Greengenes 13_5 fasta file, obtain sequences headers, remove duplicated sequences. Also calls the python script and switches original headers with headers for Kraken db building.

- GG_to_kraken.py
  - Python script that creates names.dmp, nodes.dmp and the sequence headers specific for Kraken.

Instructions:

- Dependencies:
  - python 3 (script written in Python 3.6.3).
  - pandas (install before running scripts, will output error if not installed).
  - seqkit (shouldn't be necessary to install, bash script automatically checks and installs if not available).
  - 'sys' and 'collections' modules, that should be available in default python.
  
 After checking dependencies, just run the 'GG_to_kraken.sh' script:
  - with root privileges:
    - Example command: ./GG_to_kraken.sh
  - without root provoleges:
    - Example command: sudo ./GG_to_kraken.sh

The process takes a while, but there are outputs indicating the step at which it is (around 9 minutes with i5-6200U and 8Gb ram laptop).
After running, the output files of interest are:
  - gg_13_5_kraken_ready.fasta (fasta file with the sequences ready to be added to custom database of Kraken).
  - names.dmp and nodes.dmp (files to be moved/copied to the 'taxonomy' folder of the Kraken custom database).
  
The scripts should run well but there might be issues due to some configurations that are not script dependent (the python script is called like './GG_to_kraken.py file1 file2' and has the shebang '#!/usr/bin/python3' expression to assure that your default python3 is used. Not having pandas installed in the called python3 or having pandas only on a different python installation than the one called will lead to import error. Using a different version of Greengenes might not work, just use 13_5 that's the one the script downloads).
  
Instructions for building the Kraken Greengenes DB after generating the files:

- Create 'taxonomy' folder inside db directory and move Greengenes names.dmp and nodes.dmp to that folder.
- Add Greengenes fasta file without duplicates and with headers specific for Kraken to the db library.
  - Example command: kraken-build --add-to-library gg_13_5_kraken_ready.fasta --db <db_name>
- Build custom Greengenes database.
  - Example command: kraken-build --build --threads 4 --db <db_name>
  
After following these steps, the database should be ready to be used by Kraken to classify 16S sequences.
