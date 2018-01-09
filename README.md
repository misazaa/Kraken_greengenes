# Kraken Greengenes
Conversion of Greengenes database taxonomy into names and nodes files with same format as NCBI taxdump names.dmp and nodes.dmp files. 

The conversion of the Greengenes taxonomy to this format might be useful when seeking to use the Greengenes database with software/programs that use NCBI names.dmp and nodes.dmp. Switching the .dmp NCBI files by the .dmp Greengenes files can facilitate usage of the Greengenes taxonomy (Ex: Kraken taxonomic sequence classification system, by DerrickWood, https://github.com/DerrickWood/kraken).

For now, only the names.dmp and nodes.dmp files are available.

- The taxids identifiers for 'root' and 'cellular organisms' of NCBI are present.
- The rest of the identifiers are sequential from 2 to n.

- The names file has 4 fields: node identifier, name, synonym that is name repetition (will probably be switched by empty field) and type designation.
- The names are the ones present in the Greengenes taxonomy and all the entries are of the type 'scientific name' (adding other information probably isn't that important and might be quite challenging).

- The nodes file has 3 fields: node identifier, parent node indentifier and rank designation (kingdom-->phylum-->class-->order-->family-->genus-->species).
- The nodes.dmp file has all the relations between children and parent nodes and only the necessary 3 fields to present those relations.

Conversion scripts will be added later! Open to and welcome suggestions to improve or correct issues!
