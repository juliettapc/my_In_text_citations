import sys
import glob   
import pickle
import gzip
import os,glob
import numpy as np
import pandas as pd
import operator
import random
from  scipy import stats
#sys.path

from datetime import datetime
import math
import itertools



def main():









    ###### dict_plos_UT_list_references_used_prior*

    path = '../data/dict_plos_UT_list_references_used_prior*'   

    
    
    
    
    lista_files=sorted(glob.glob(path))

    dict_plos_UT_list_references_used_prior  = {}
    

    for filename in lista_files:
        now = datetime.now()
        print(f"{now}:     loading    {filename}")  
        with open(filename, 'rb') as f:
            aux_dict_plos_UT_list_references_used_prior = pickle.load(f)

      
        now = datetime.now()
        dict_len = len(aux_dict_plos_UT_list_references_used_prior)
        print(f"  {now}: done loading, len: {dict_len}")
       

        dict_plos_UT_list_references_used_prior.update(aux_dict_plos_UT_list_references_used_prior)
        del(aux_dict_plos_UT_list_references_used_prior)
        now = datetime.now()
        dict_len = len(dict_plos_UT_list_references_used_prior)
        print (f"  {now}: master dict updated, len: {dict_len}")

        
        
        
  #  with open('../data/master_dict_plos_UT_list_references_used_prior_ALL.pkl', 'wb') as handle:
   #              pickle.dump(dict_plos_UT_list_references_used_prior, handle, protocol = 2)
#    print ("written:",'../data/master_dict_plos_UT_list_references_used_prior_ALL.pkl',len(master_dict))   
    print ("loaded master dictionary from partial dicts (not dumped though!)",len(dict_plos_UT_list_references_used_prior))   


    lista_all_authored_UTs = list(dict_plos_UT_list_references_used_prior.keys())
    print ("len lista_all_authored_UTs:", len(lista_all_authored_UTs))













    try:

        list_paper_UT = pickle.load(open('../data/list_paper_UT.pkl', 'rb'))   
        print ("done loading  ../data/list_paper_UT.pkl") 
    except:        
        print ("MISSING FILE!  ../data/list_paper_UT.pkl           FORCED EXIT.")
      #  exit()






    try:

        plos_df_simple = pickle.load(open('../data/plos_df.pkl', 'rb'))   
        print ("done loading  ../data/plos_df.pkl") 
    except:        
        print ("MISSING FILE!  ../data/plos_df.pkl           FORCED EXIT.")
       # exit()








    try:

        filename = '../data/master_dict_plos_UT_list_papers_authored_by_team_until_then.pkl'
        dict_plos_UT_list_papers_authored_by_team = pickle.load(open(filename, 'rb'))   
        print ("done loading ", filename, len(dict_plos_UT_list_papers_authored_by_team)) 

    except:        
        print ("MISSING FILE!  ", filename, "        FORCED EXIT.")
        #exit()











    df_merged = pickle.load(open('../data/df_reference_cite_plos_merged_simplified_added_more_columns_no_self-cit_one_ref_per_sect_ONLY_ARTICLES.pkl', 'rb'))
    print ("done loading df_merged", df_merged.shape)













    print ("\n adding team_expertise to pandas df  ..................")
    list_expertise_papers= []
    for paper_UT in list_paper_UT:
        list_expertise_papers.append(len(dict_plos_UT_list_papers_authored_by_team[paper_UT]))

    del (dict_plos_UT_list_papers_authored_by_team)   # i delete the dict to free memory

    ### add column
    plos_df_simple['team_expertise'] = list_expertise_papers



    ###### i merge dataframes
    df_merged = pd.merge(df_merged,  plos_df_simple, on='paper_UT', how='left')






    path = '../data/df_reference_cite_plos_merged_with_team_expertise.pkl'
    df_merged.to_pickle(path, compression='infer', protocol=2)
    print ("written df_reference_cite_plos_merged_with_team_expertise.pkl", df_merged.shape)








    ############ i add the recycled_ref label to the plos_ref database:
    print ("\n adding recycled_ref label to pandas df  ..................")
    df_merged['recycled_ref'] = df_merged.apply (lambda row: get_reclycle_ref_yes_no(row, dict_plos_UT_list_references_used_prior),axis=1)


    del (dict_plos_UT_list_references_used_prior)   # i delete the dict to free space






    path = '../data/df_reference_cite_plos_merged_with_team_expertise_and_recycled_ref.pkl'
    df_merged.to_pickle(path, compression='infer', protocol=2)
    print ("written df_reference_cite_plos_merged_with_team_expertise_and_recycled_ref.pkl", df_merged.shape)




    print ("GOOD JOB!  :)")














###################################
########################################
###################################
########################################

def get_reclycle_ref_yes_no(row, dict_plos_UT_list_references_used_prior):
    
    flag_recycled_ref = np.nan
    
    paper_UT = row.paper_UT
    ref_UT = row.reference_UT
    
    flag_recycled_ref = 0
        
    try:
        dict_plos_UT_list_references_used_prior[paper_UT]
       
        if ref_UT in dict_plos_UT_list_references_used_prior[paper_UT]:   # that is the list of papers authored by the list of authors of paper_UT until the year before of the publication of paper_UT
            flag_recycled_ref = 1
    except KeyError: pass
    
    
            
    return flag_recycled_ref

###########



######################################
######################################
######################################  
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "



############################3
#################################



