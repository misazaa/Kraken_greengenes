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
    root_name = root_rank + "\t" + "|" + "\t" + "root" + "\t" + "|" + "\t" + "\t" + "|" + "\t" + "scientific name" + "\t" + "|"
    names_list.append(root_name)
    
    # Create nodes list to append nodes
    nodes_list = []
    # Add root rank to nodes_list
    root_node = root_rank + "\t" + "|" + "\t" + root_rank + "\t" + "|" + "\t" + "no rank" + "\t" + "|"
    nodes_list.append(root_node)
    
    # Define 7 main ranks
    rank_names = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
    # Create dict to keep track of variables
    rank_dict = collections.OrderedDict()
    # Add root to dict
    rank_dict['root'] = root_rank
    
    for rank in range(0, len(rank_names)):
        
        # identify unique name values
        names = list(set(taxid_df[rank_names[rank]]))
        # remove possible nan value
        names = [n for n in names if str(n) != 'nan']
        # create dict to store rank info
        rank_dict[rank_names[rank]] = collections.OrderedDict()
        
        for n in names:
            # increment id by 1
            i += 1
            # determine parent node name
            parent_name = taxid_df.loc[taxid_df[rank_names[rank]] == str(n), rank_names[rank-1]].iloc[0]
            # Create name string and append to names_list
            if rank_names[rank] == "Species":
                # if rank is 'Species', genus name is concatenated with species name
                name = str(i) + "\t" + "|" + "\t" + (str(parent_name) + ' ' + str(n)) + "\t" + "|" + "\t" + "\t" + "|" + "\t" + "scientific name" + "\t" + "|"
                names_list.append(name)
                
            else:
                name = str(i) + "\t" + "|" + "\t" + str(n) + "\t" + "|" + "\t" + "\t" + "|" + "\t" + "scientific name" + "\t" + "|"
                names_list.append(name)
            # Add rank name with id to dict
            (rank_dict[rank_names[rank]])[str(n)] = i
            # Create node string to append to nodes_list
            if rank_names[rank] == "Kingdom":
                # if rank is 'Kingdom', parent node is 'root'
                node = str((rank_dict[rank_names[rank]])[str(n)]) + "\t" + "|" + "\t" + rank_dict['root'] + "\t" + "|" + "\t" + rank_names[rank].lower() + "\t" + "|"
                nodes_list.append(node)
                
            else:
                node = str((rank_dict[rank_names[rank]])[str(n)]) + "\t" + "|" + "\t" + str((rank_dict[rank_names[rank-1]])[parent_name]) + "\t" + "|" + "\t" + rank_names[rank] + "\t" + "|"
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
    
    # read tsv file with headers from deduplicated fasta file
    gg_noDUPS = pd.read_csv(noDups_tsv, sep = '\t')

    # Create transpose of dataframe to facilitate retrieval of last non-nan elements
    transpose_df = gg_noDUPS.transpose()
    
    num_columns = transpose_df.shape[1]
    # create dict to store info for headers construction
    headers_dict = collections.OrderedDict()
    for col in range(0, num_columns):
        # greengenes id
        gg_id = transpose_df[col][0]
        # determine last valid rank (last non-nan rank)
        last_valid_rank = transpose_df[col].last_valid_index()
        # name of the last valid rank
        rank_name = transpose_df[col][str(last_valid_rank)]
        # add greengenes id and rank_name to dict
        headers_dict[gg_id] = rank_name
        
        # determine rank name id and substitute in headers dict
        if str(last_valid_rank) == "Kingdom":
            headers_dict[gg_id] = rank_dict["Kingdom"][headers_dict[gg_id]]
            
        if str(last_valid_rank) == "Phylum":
            headers_dict[gg_id] = rank_dict["Phylum"][headers_dict[gg_id]]
            
        if str(last_valid_rank) == "Class":
            headers_dict[gg_id] = rank_dict["Class"][headers_dict[gg_id]]
            
        if str(last_valid_rank) == "Order":
            headers_dict[gg_id] = rank_dict["Order"][headers_dict[gg_id]]
            
        if str(last_valid_rank) == "Family":
            headers_dict[gg_id] = rank_dict["Family"][headers_dict[gg_id]]
            
        if str(last_valid_rank) == "Genus":
            headers_dict[gg_id] = rank_dict["Genus"][headers_dict[gg_id]]
            
        if str(last_valid_rank) == "Species":
            headers_dict[gg_id] = rank_dict["Species"][headers_dict[gg_id]]
    
    # create list with headers    
    kraken_headers_list = []
    for ele in headers_dict:
        header = ">" + str(ele) + "|" + "kraken:taxid" + "|" + str(headers_dict[ele])
        kraken_headers_list.append(header)
        
    # save headers in file
    kraken_headers = open('gg_13_5_headers_kraken_noDUPS.txt', 'w')
    
    for header in kraken_headers_list:
        kraken_headers.write("%s\n" % header)
    
    kraken_headers.close()
    
    
# Execute function to generate names, nodes files and kraken headers
gg_to_kraken(sys.argv[1], sys.argv[2])
    
