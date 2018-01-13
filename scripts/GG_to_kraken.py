#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import collections
import pandas as pd

def gg_to_kraken(headers_tsv, noDups_tsv):
    
    # separated by tabs due to commas in fields
    taxid_df = pd.read_csv(headers_tsv, sep = '\t')
    
    i = 1
    
    root_rank = str(i)

    # Create names list to append names
    names_list = []
    # Add root rank to names_list
    root_name = root_rank + "\t|\troot\t|\t\t|\tscientific name\t|"
    names_list.append(root_name)
    
    # Create nodes list to append nodes
    nodes_list = []
    # Add root rank to nodes_list
    root_node = root_rank + "\t|\t" + root_rank + "\t|\tno rank\t|"
    nodes_list.append(root_node)
    
    # Define 7 main ranks
    rank_names = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
    # Create dict to keep track of variables
    rank_dict = collections.OrderedDict()
    # Add root to dict
    rank_dict['root'] = root_rank
    
    for rank in range(0, len(rank_names)):
        # Determine name of the rank and name of the parent rank
        rank_name = rank_names[rank]
        parent_rank = rank_names[rank-1]
        # Create dict to assign rank names and taxIDs
        rank_dict[rank_name] = collections.OrderedDict()
        
        # identify unique name values
        names = list(set(taxid_df[rank_name] + '|' + taxid_df[parent_rank]))
        # remove missing values
        names = [n for n in names if str(n) != 'nan']
        # create dict to assign names
        names_dict = collections.OrderedDict()
        
        # Create child|parent dict
        for name in names:
            n = name.split('|')
            names_dict[n[0]] = n[1]
        
        for n in names_dict:
            # increment id by 1
            i += 1
            # determine parent node name
            parent_name = names_dict[n]
            # Create name string and append to names_list
            if rank_name == "Species":
                species_name = parent_name + ' ' + n
                # if rank is 'Species', genus name is concatenated with species name
                name = "%s\t|\t%s\t|\t\t|\tscientific name\t|" % (str(i), species_name)
                names_list.append(name)
                
            else:
                name = "%s\t|\t%s\t|\t\t|\tscientific name\t|" % (str(i), n)
                names_list.append(name)
            # Add rank name with id to dict
            rank_dict[rank_name][n] = i
            node_id = rank_dict[rank_name][n]
            # Create node string to append to nodes_list
            if rank_name == "Kingdom":
                # if rank is 'Kingdom', parent node is 'root'
                node = "%s\t|\t%s\t|\t%s\t|" % (node_id, rank_dict['root'], "kingdom")
                nodes_list.append(node)
                
            else:
                parent_id = rank_dict[parent_rank][parent_name]
                node = "%s\t|\t%s\t|\t%s\t|" % (node_id, parent_id, rank_name)
                nodes_list.append(node)
            
    # Create and fill names and nodes files
    names_dmp = open('names.dmp', 'w')
    nodes_dmp = open('nodes.dmp', 'w')

    for name in names_list:
        names_dmp.write("%s\n" % name)

    for node in nodes_list:
        nodes_dmp.write("%s\n" % node)

    names_dmp.close()
    nodes_dmp.close()
    
    # Call function that will create kraken headers
    kraken_headers(noDups_tsv, rank_dict)


def kraken_headers(noDups_tsv, rank_dict):
    
    rank_names = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
    # read tsv file with headers from deduplicated fasta file
    gg_noDUPS = pd.read_csv(noDups_tsv, sep = '\t')
    
    num_lines = gg_noDUPS.shape[0]
    # create dict to store info for headers construction
    headers_dict = collections.OrderedDict()
    
    tax_lol = list(gg_noDUPS.values.tolist())
    
    for e in range(0, num_lines):
        tax_lol[e] = [n for n in tax_lol[e] if str(n) != 'nan']
    
    for l in range(0, num_lines):
        
        # greengenes id
        gg_id = tax_lol[l][0]
       
        rank_name = tax_lol[l][-1]
        rank_lol = rank_names[len(tax_lol[l])-5]
        # determine rank name id and substitute in headers dict
        headers_dict[gg_id] = rank_dict[rank_lol][rank_name]
        
    # create list with headers    
    kraken_headers_list = []
    for ele in headers_dict:
        header = ">" + str(ele) + "|kraken:taxid|" + str(headers_dict[ele])
        kraken_headers_list.append(header)
        
    # save headers in file
    kraken_headers = open('gg_13_5_headers_kraken_noDUPS.txt', 'w')
    
    for header in kraken_headers_list:
        kraken_headers.write("%s\n" % header)
    
    kraken_headers.close()
    
    
# Execute function to generate names, nodes files and kraken headers
gg_to_kraken(sys.argv[1], sys.argv[2])
    
