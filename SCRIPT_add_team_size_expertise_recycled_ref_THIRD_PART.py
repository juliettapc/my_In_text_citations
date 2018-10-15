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

import datetime
import math
import itertools


from pymongo import MongoClient




def main():







                 
    ########### I load all aux. dictionaries that i need for this third part of the code:
    try:
  
        dict_DAIS_list_papers = pickle.load(open('../data/dict_DAIS_list_papers.pkl', 'rb'))   
        print ("done loading  ../data/dict_DAIS_list_papers.pkl") 
    except:        
        print ("MISSING FILE!  ../data/dict_DAIS_list_papers.pkl           FORCED EXIT.")
        exit()




                        
    try:
        tot_list_DAIS = pickle.load(open('../data/tot_list_DAIS.pkl', 'rb'))   
        print ("done loading  ../data/tot_list_DAIS.pkl")    ###   697,993   authors (of all the plos papers)

        dict_plos_paper_UT_list_DAIS = pickle.load(open('../data/dict_plos_paper_UT_list_DAIS.pkl', 'rb'))            
        print ("done loading  ../data/dict_plos_paper_UT_list_DAIS.pkl")   # 158,813   plos papers
    except:
        print ("MISSING FILE!  ../data/dict_plos_paper_UT_list_DAIS.pkl           FORCED EXIT.")
        exit()







   
    try:
        dict_all_papers_authored_publ_year = pickle.load(open('../data/dict_all_papers_authored_publ_year.pkl', 'rb'))  
        print ("done loading ../data/dict_all_papers_authored_publ_year.pkl" )   # around 12M of keys
    except:
        print ("MISSING FILE!  ../data/dict_all_papers_authored_publ_year.pkl           FORCED EXIT.")
        exit()







    list_paper_UT = pickle.load(open('../data/list_paper_UT.pkl', 'rb'))
    print ("done loading pickle list_paper_UT")







    try:
        dict_UT_plos_paper_publication_year = pickle.load(open('../data/dict_UT_plos_paper_publication_year.pkl', 'rb'))  
        print ("done loading ../data/dict_UT_plos_paper_publication_year.pkl" )   # around 12M of keys
    except:
        print ("MISSING FILE!  ../data/dict_UT_plos_paper_publication_year.pkl           FORCED EXIT.")
        exit()






    try:
        dict_all_authored_paper_UT_list_UT_references = pickle.load(open('../data/master_dict_all_authored_paper_UT_list_UT_references.pkl', 'rb'))  
        print ("done loading ../data/master_dict_all_authored_paper_UT_list_UT_references.pkl" )   # around 12M of keys
    except:
        print ("MISSING FILE!  ../data/master_dict_all_authored_paper_UT_list_UT_references.pkl           FORCED EXIT.")
        exit()

















    ###############################################################
    #####################   now i finally get the actual number of references used previously by all team members of a given paper, as well as all the papers (expertise) they have individually written


    print ("\nworking on getting  dict_plos_UT_list_references_used_prior     and     dict_plos_UT_list_papers_authored_by_team   .................. (N_tot = 158K)")

    dict_plos_UT_list_references_used_prior={}
    dict_plos_UT_list_papers_authored_by_team={}

    list_not_found_authored_papers=[]


    cont  = 1
    for paper_UT in list_paper_UT:   #### loop over all plos papers:  # tot 158K  


        if cont % 10000 == 0:

            with open('../data/dict_plos_UT_list_references_used_prior_partial'+str(cont)+'.pkl', 'wb') as handle:
                 pickle.dump(dict_plos_UT_list_references_used_prior, handle, protocol = 2)
            print ("written:",'../data/dict_plos_UT_list_references_used_prior_partial'+str(cont)+'.pkl',len(dict_plos_UT_list_references_used_prior))   
                



            with open('../data/dict_plos_UT_list_papers_authored_by_team_until_then_partial'+str(cont)+'.pkl', 'wb') as handle:
                 pickle.dump(dict_plos_UT_list_papers_authored_by_team, handle, protocol = 2)
            print ("written:",'../data/dict_plos_UT_list_papers_authored_by_team_until_then_partial'+str(cont)+'.pkl',len(dict_plos_UT_list_papers_authored_by_team))   


            dict_plos_UT_list_references_used_prior={}
            dict_plos_UT_list_papers_authored_by_team={}




            print (cont)




        plos_year = dict_UT_plos_paper_publication_year[paper_UT]

        dict_plos_UT_list_papers_authored_by_team[paper_UT] = []  # until the publication  date of the PLOS paper that is    

        list_references_prior = []

        lista_DAIS = dict_plos_paper_UT_list_DAIS[paper_UT]

        for DAIS in lista_DAIS:   ########### loop over authors of the focus PLOS paper 
            list_authored_papers_by_DAIS = dict_DAIS_list_papers[DAIS]

            for authored_paper in list_authored_papers_by_DAIS:  ############## loop over all papers authored by all authors of the focus PLOS paper

                    try:
                        authored_paper_year = dict_all_papers_authored_publ_year[authored_paper]

                        if authored_paper_year < plos_year : # it only counts towards the team's expertise if it was published before the focus plos paper                        
                            list_references_prior += dict_all_authored_paper_UT_list_UT_references[authored_paper]
                            dict_plos_UT_list_papers_authored_by_team[paper_UT].append(authored_paper)
                    except KeyError: #pass
                        list_not_found_authored_papers.append(authored_paper)



            #### i remove duplicated ref:        
            dict_plos_UT_list_references_used_prior[paper_UT] = list(set(list_references_prior))
            dict_plos_UT_list_papers_authored_by_team[paper_UT] = list(set(dict_plos_UT_list_papers_authored_by_team[paper_UT]))


        cont +=1





    with open('../data/dict_plos_UT_list_references_used_prior_last_part.pkl', 'wb') as handle:
                 pickle.dump(dict_plos_UT_list_references_used_prior, handle, protocol = 2)
    print ("written:",'../data/dict_plos_UT_list_references_used_prior.pkl',len(dict_plos_UT_list_references_used_prior))   




    with open('../data/dict_plos_UT_list_papers_authored_by_team_last_part.pkl', 'wb') as handle:
                 pickle.dump(dict_plos_UT_list_papers_authored_by_team, handle, protocol = 2)
    print ("written:",'../data/dict_plos_UT_list_papers_authored_by_team.pkl',len(dict_plos_UT_list_papers_authored_by_team))   




    list_not_found_authored_papers =  list(set(list_not_found_authored_papers))
    print ("# authored papers not found:",len(list_not_found_authored_papers ))


    print ('DONE for now (missing the last last step: i add to dataframe the new fields: team_expertise  AND    recycled_ref)')








    ########### i glue together the partial dictionaries
    path = '../data/dict_plos_UT_list_papers_authored_by_team_until_then_*'   
    lista_files=sorted(glob.glob(path))

    master_dict  = {}
    lista_all_authored_UTs=[]

    for filename in lista_files:
        dict_plos_UT_list_papers_authored_by_team = pickle.load(open(filename, 'rb'))
        lista_all_authored_UTs += list(dict_plos_UT_list_papers_authored_by_team.keys())
        print ("done loading", filename, len(dict_plos_UT_list_papers_authored_by_team), len(lista_all_authored_UTs))

        master_dict.update(dict_plos_UT_list_papers_authored_by_team)



    with open('../data/master_dict_plos_UT_list_papers_authored_by_team_until_then.pkl', 'wb') as handle:
                 pickle.dump(master_dict, handle, protocol = 2)
    print ("written:",'../data/master_dict_plos_UT_list_papers_authored_by_team_until_then.pkl',len(master_dict))   











    df_merged = pickle.load(open('../data/df_reference_cite_plos_merged_simplified_added_more_columns_no_self-cit_one_ref_per_sect_ONLY_ARTICLES.pkl', 'rb'))
    print ("done loading pickles", df_merged.shape)


    plos_df = df_merged.drop_duplicates(subset=['paper_UT'])
    plos_df = plos_df.sort_values(by=['paper_UT'])
    plos_df = plos_df[['paper_UT']]  

    list_paper_UT = list(plos_df.paper_UT.values) 
    print ("plos_df created")





    with open('../data/list_paper_UT.pkl', 'wb') as handle:
          pickle.dump(list_paper_UT, handle, protocol = 2)
    print ("written:",'../data/list_paper_UT.pkl',len(list_paper_UT))   




    with open('../data/plos_df.pkl', 'wb') as handle:
         pickle.dump(plos_df, handle, protocol = 2)
    print ("written:",'../data/plos_df.pkl',len(plos_df))   








    exit()
































































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



