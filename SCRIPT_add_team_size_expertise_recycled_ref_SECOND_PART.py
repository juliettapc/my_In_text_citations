import sys
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




    #############################

    merged_papers_settings = {
        "host": "chicago.chem-eng.northwestern.edu",
        "port": "27017",
        "db": "web_of_science_aux",
        "collection": "merged_papers",
        "user": "mongoreader",
        "password": "emptycoffeecup"
    }

    papers_con = MongoConnection(merged_papers_settings)




    #############################

    dais_settings = {
        "host": "chicago.chem-eng.northwestern.edu",
        "port": "27017",
        "db": "web_of_science_aux",
        "collection": "ut_dais_all",
        "user": "mongoreader",
        "password": "emptycoffeecup"
    }

    dais_con = MongoConnection(dais_settings)

    ##############################










    list_paper_UT = pickle.load(open('../data/list_paper_UT.pkl', 'rb'))
    print ("done loading pickle list_paper_UT")


   










             
        
    ##############################     i get the dict plos paper_UT list of DAIS (disambiguated authors)



    ##### i get the list of all DAIS (disambiguated authors) for the list of PLOS papers
    try:
        tot_list_DAIS = pickle.load(open('../data/tot_list_DAIS.pkl', 'rb'))   
        print ("done loading  ../data/tot_list_DAIS.pkl") 
        dict_plos_paper_UT_list_DAIS = pickle.load(open('../data/dict_plos_paper_UT_list_DAIS.pkl', 'rb'))            
        print ("done loading  ../data/dict_plos_paper_UT_list_DAIS.pkl")


    except:    

        cont  = 1
        tot_list_DAIS=[]
        dict_plos_paper_UT_list_DAIS = {}
        for paper_UT in list_paper_UT:

            if cont % 10000 == 0:
               print (cont)
            #### i get the list of disambiguated author IDs for the paper plos
            result_query = papers_con.collection.find_one({"UT":paper_UT},{"AU":1})  
             #  print (result_query) ##  example: {'_id': ObjectId('54d3bdcdec29bd464368e4a8'), 'AU': [{'AU': 'Loffler, S', 'DAIS': 19993061}, {'AU': 'Jessen, J', 'DAIS': 37335135}, {'AU': 'Schmid, T', 'DAIS': 30805206}, {'AU': 'Porksen, U', 'DAIS': 63190680}]}



            list_DAIS=[]
            for dict_author in result_query['AU']:  # the result of find_one is a dictionary, NOT an iterator!  And the, result_query['AU'] is a list of dict with info on all the authors of the paper_UT        
                try:
                    DAIS = dict_author['DAIS']
                    #list_DAIS.append(DAIS)
                    tot_list_DAIS.append(DAIS)
                    list_DAIS.append(DAIS)
                except :
                    pass#print ("author without DAIS",dict_author, "  in paper:", paper_UT)
                    #input()




            ########## alternative, more pythonic 
            #### example: [d['value'] for d in l if 'value' in d]
            #lista_of_dict =  result_query['AU'] 
            #list_DAIS = [d['DAIS'] for d in lista_of_dict if 'DAIS' in d]


            dict_plos_paper_UT_list_DAIS[paper_UT] = list_DAIS
            cont += 1


        tot_list_DAIS = list(set(tot_list_DAIS))  # i remove duplicates
        with open('../data/tot_list_DAIS.pkl', 'wb') as handle:
                 pickle.dump(tot_list_DAIS, handle, protocol = 2)
        print ("written:",'../data/tot_list_DAIS.pkl')




        with open('../data/dict_plos_paper_UT_list_DAIS.pkl', 'wb') as handle:
                 pickle.dump(dict_plos_paper_UT_list_DAIS, handle, protocol = 2)
        print ("written:",'../data/dict_plos_paper_UT_list_DAIS.pkl')


    print ("# unique DAIS: ",len(tot_list_DAIS), len(dict_plos_paper_UT_list_DAIS))    #  697,993    158,813









    ############## i get dict of DAIS list of all authored papers by that DAIS (disambiguated authors from all PLOS papers) 
    try:
        tot_list_papers_authored = pickle.load(open('../data/tot_list_papers_authored.pkl', 'rb'))   
        print ("done loading ../data/tot_list_papers_authored.pkl") 
        dict_DAIS_list_papers = pickle.load(open('../data/dict_DAIS_list_papers.pkl', 'rb'))    
        print ("done loading ../data/dict_DAIS_list_papers.pkl") 

    except:        

        cont  = 1   
        tot_list_papers_authored=[]    
        dict_DAIS_list_papers = {}



        for DAIS in tot_list_DAIS:    # tot:  697993                      


            if cont % 10000 == 0:
                print (cont)


            #####  i get all the papers by a given disambiguated author
            cursor = dais_con.collection.find({"DAIS":DAIS},{"UT":1}) 

            list_papers=[]
            for item in cursor:  # I iterate over all papers by all the authors of paper_UT
                UT=item["UT"]
                tot_list_papers_authored.append(UT)
                list_papers.append(UT)

            dict_DAIS_list_papers[DAIS] = list_papers

            cont += 1




        tot_list_papers_authored = list(set(tot_list_papers_authored))  # i remove duplicates
        with open('../data/tot_list_papers_authored.pkl', 'wb') as handle:  # I dont really need this list
                  pickle.dump(tot_list_papers_authored, handle, protocol = 2)
        print ("written:",'../data/tot_list_papers_authored.pkl')



        with open('../data/dict_DAIS_list_papers.pkl', 'wb') as handle:
            pickle.dump(dict_DAIS_list_papers, handle, protocol = 2)
        print ("written:",'../data/dict_DAIS_list_papers.pkl')



    print ("# unique authored papers by all those DAIS:  ",len(tot_list_papers_authored), len(dict_DAIS_list_papers))









    #### now i get the publication year of all papers author by the list of DAIS (from the list of all plos papers)
    try:
        dict_all_papers_authored_publ_year = pickle.load(open('../data/dict_all_papers_authored_publ_year.pkl', 'rb'))  
        print ("done loading ../data/dict_all_papers_authored_publ_year.pkl" )
    except:

        cont  = 1  
        dict_all_papers_authored_publ_year = {}
        for paper in tot_list_papers_authored:
            if cont % 10000 == 0:
                print (cont)

            dict_result_query = papers_con.collection.find_one({"UT":paper},{"issue.PY":1})  

            try:
                year = dict_result_query['issue']['PY']
                dict_all_papers_authored_publ_year[paper]=year
            except: pass # if the paper does not exist or doesnt have a publication year

            cont += 1


        with open('../data/dict_all_papers_authored_publ_year.pkl', 'wb') as handle:
                     pickle.dump(dict_all_papers_authored_publ_year, handle, protocol = 2)
        print ("written:",'../data/dict_all_papers_authored_publ_year.pkl',len(dict_all_papers_authored_publ_year))   










    ########################### next, i get the dictionary of all authored paper UTs vs the list of the R9 references they use  (later i need to convert R9s into UTs)


    #try:  ####   OJOOOO !  replace by the final dict and list once it is done (instead of the partial)
        #dict_all_authored_paper_UT_list_R9_references = pickle.load(open('../data/dict_all_authored_paper_UT_list_R9_references.pkl', 'rb'))  
        #list_all_R9s = pickle.load(open('../data/list_all_R9s.pkl', 'rb'))  



    dict_all_authored_paper_UT_list_R9_references = pickle.load(open('../data/dict_all_authored_paper_UTs_list_R9_references_partial.pkl', 'rb'))  
    print ("done loading  ../data/dict_all_authored_paper_UTs_list_R9_references_partial.pkl")    
    list_all_R9s = pickle.load(open('../data/list_all_R9s_partial.pkl', 'rb'))  
    print ("done loading  ../data/list_all_R9s_partial.pkl")    




    partial_list_keys_so_far = pickle.load(open('../data/partial_list_keys.pkl', 'rb'))      
    print ("done loading  ../data/partial_list_keys.pkl", len(partial_list_keys_so_far))    


    aux_list_authored_papers = set(dict_all_papers_authored_publ_year.keys()) - set(partial_list_keys_so_far)
    aux_list_authored_papers = sorted(list(aux_list_authored_papers))
    print ("size of aux_list_authored_papers  (remaining)", len(aux_list_authored_papers), flush=True)
   








    list_all_R9s = pickle.load(open('../data/list_all_R9s_partial.pkl', 'rb'))  
    print ("done loading  ../data/list_all_R9s_partial.pkl")  


    

   

    try:
        dict_R9_UT = pickle.load(open('../data/dict_R9_UT.pkl', 'rb'))
        print ("done loading pickle dict_R9_UT", len(dict_R9_UT))


        dict_UT_R9 = pickle.load(open('../data/dict_UT_R9.pkl', 'rb'))
        print ("done loading pickle dict_UT_R9", len(dict_UT_R9))


    except:






        ##########################     transform R9 from list of references of papers into UT
        print ("\nworking on getting  dict_R9_UT    and    dict_UT_R9    ..................")
        dict_R9_UT = {}
        dict_UT_R9 = {}
        cont = 1
        list_missing_R9s =[]
        for R9 in list_all_R9s:
            #print (cont)

            dict_result = papers_con.collection.find_one({"T9":R9},{"UT":1})    ### keys of the resulting dict_result dictioray:   '_id', 'UT'
            try:
                UT = dict_result['UT']
                dict_R9_UT[R9] = UT
                dict_UT_R9[UT] = R9

            except : 
                list_missing_R9s.append(R9)

            if cont % 10000 == 0:
                print (cont)
            cont +=1        




        with open('../data/dict_R9_UT.pkl', 'wb') as handle:
                     pickle.dump(dict_R9_UT, handle, protocol = 2)
        print ("written:",'../data/dict_R9_UT.pkl',len(dict_R9_UT))   



        with open('../data/dict_UT_R9.pkl', 'wb') as handle:
                     pickle.dump(dict_UT_R9, handle, protocol = 2)
        print ("written:",'../data/dict_UT_R9.pkl',len(dict_UT_R9))   





        list_missing_R9s =  set(list(list_missing_R9s))
        print ("# missing R9s without a UT correspondence:",len(list_missing_R9s))








    list_names_partial_dict = ['dict_all_authored_paper_UT_list_R9_references_partial4000000.pkl','dict_all_authored_paper_UT_list_R9_references_partial10000000.pkl','dict_all_authored_paper_UT_list_R9_references_partial5000000.pkl','dict_all_authored_paper_UT_list_R9_references_partial1000000.pkl','dict_all_authored_paper_UT_list_R9_references_partial6000000.pkl','dict_all_authored_paper_UT_list_R9_references_partial11000000.pkl','dict_all_authored_paper_UT_list_R9_references_partial7000000.pkl', 'dict_all_authored_paper_UT_list_R9_references_partial12000000.pkl','dict_all_authored_paper_UT_list_R9_references_partial8000000.pkl','dict_all_authored_paper_UT_list_R9_references_partial2000000.pkl','dict_all_authored_paper_UT_list_R9_references_partial9000000.pkl', 'dict_all_authored_paper_UT_list_R9_references_partial3000000.pkl','dict_all_authored_paper_UT_list_R9_references_last_bit.pkl']





    #####################      i create a new dict of paper_UT : list of ref_UT from the auxiliary dict_all_authored_paper_UT_list_R9_references:
    print ("\nworking on getting   dict_all_authored_paper_UT_list_UT_references    ..................")
    
    cont = 1

    for filename in list_names_partial_dict :
   
        dict_all_authored_paper_UT_list_UT_references = {}

        dict_all_authored_paper_UT_list_R9_references =  pickle.load(open('../data/'+filename, 'rb'))
        print ("done loading", filename)


        for paper_UT in dict_all_authored_paper_UT_list_R9_references:
            list_ref_R9 = dict_all_authored_paper_UT_list_R9_references[paper_UT]

            list_aux_ref_UT = []
            for R9 in list_ref_R9:
                try:
                    UT = dict_R9_UT[R9]
                    list_aux_ref_UT.append(UT)
                except: pass

            dict_all_authored_paper_UT_list_UT_references[paper_UT] = list_aux_ref_UT

            if cont % 100000 == 0:

                with open('../data/dict_all_authored_paper_UT_list_UT_references_partial'+str(cont)+'.pkl', 'wb') as handle:
                     pickle.dump(dict_all_authored_paper_UT_list_UT_references, handle, protocol = 2)
                print ("written:",'../data/dict_all_authored_paper_UT_list_UT_references_partial'+str(cont)+'.pkl',len(dict_all_authored_paper_UT_list_UT_references))   


                print (cont)
            cont +=1  




    with open('../data/dict_all_authored_paper_UT_list_UT_references_last_part.pkl', 'wb') as handle:
                 pickle.dump(dict_all_authored_paper_UT_list_UT_references, handle, protocol = 2)
    print ("written:",'../data/dict_all_authored_paper_UT_list_UT_references_last_part.pkl',len(dict_all_authored_paper_UT_list_UT_references))   







    plos_df = pickle.load(open('../data/plos_paper_dataframe_more_columns.pkl', 'rb'))  
    print ("done loading pickles", plos_df.shape)
  
    plos_simple = plos_df[['paper_UT','plos_pub_year']]
    dict_aux_UT_year = dict(zip(plos_simple.paper_UT, plos_simple.plos_pub_year))
    for UT in dict_aux_UT_year:
        dict_aux_UT_year[UT] = int(dict_aux_UT_year[UT])





    with open('../data/dict_UT_plos_paper_publication_year.pkl', 'wb') as handle:
         pickle.dump(dict_aux_UT_year, handle, protocol = 2)
         print ("written:",'../data/dict_UT_plos_paper_publication_year.pkl',len(dict_aux_UT_year))   












    print ("good job! now continue running the code from line:   \nnow i finally get the actual number of references used previously by all team members of a given paper, as well as all the papers (expertise) they have individually written")

    exit()













































































    #####################   now i finally get the actual number of references used previously by all team members of a given paper, as well as all the papers (expertise) they have individually written






    print ("\nworking on getting  dict_plos_UT_list_references_used_prior     and     dict_plos_UT_list_papers_authored_by_team   ..................")

    dict_plos_UT_list_references_used_prior={}
    dict_plos_UT_list_papers_authored_by_team={}

    cont  = 1
    for paper_UT in list_paper_UT:   # tot 158K  plos papers
        if cont % 10000 == 0:


            with open('../data/dict_plos_UT_list_references_used_prior_partial.pkl', 'wb') as handle:
                 pickle.dump(dict_plos_UT_list_references_used_prior, handle, protocol = 2)
            print ("written:",'../data/dict_plos_UT_list_references_used_prior_partial.pkl',len(dict_plos_UT_list_references_used_prior))   




            with open('../data/dict_plos_UT_list_papers_authored_by_team_partial.pkl', 'wb') as handle:
                 pickle.dump(dict_plos_UT_list_papers_authored_by_team, handle, protocol = 2)
            print ("written:",'../data/dict_plos_UT_list_papers_authored_by_team_partial.pkl',len(dict_plos_UT_list_papers_authored_by_team))   

            print (cont)


        plos_year = dict_aux_UT_year[paper_UT]

        dict_plos_UT_list_papers_authored_by_team[paper_UT] = []  # until the date of the PLOS paper that is    
        list_references_prior = []

        try:
            lista_DAIS = dict_plos_paper_UT_list_DAIS[paper_UT]
            for DAIS in list_DAIS:
                list_authored_papers_by_DAIS = dict_DAIS_list_papers[DAIS]

                for authored_paper in list_authored_papers_by_DAIS:

                    try:
                        authored_paper_year = dict_all_papers_authored_publ_year[authored_paper]
                        if authored_paper_year < plos_year : # it only counts towards the team's expertise if it was published before the focus plos paper                        

                            list_references_prior += dict_all_authored_paper_UT_list_UT_references[authored_paper_year]
                            dict_plos_UT_list_papers_authored_by_team[paper_UT].append(authored_paper)

                    except KeyError:  # if no publication year

                        try:
                            dict_aux_UT_year[authored_paper]  # in case the authored paper is a plos
                            if authored_paper_year < plos_year : # it only counts towards the team's expertise if it was published before the focus plos paper                        

                                list_references_prior += dict_all_authored_paper_UT_list_UT_references[authored_paper_year]
                                dict_plos_UT_list_papers_authored_by_team[paper_UT].append(authored_paper)

                        except KeyError: pass 






            #### i remove duplicates:        
            dict_plos_UT_list_references_used_prior[paper_UT] = list(set(list_references_prior))
            dict_plos_UT_list_papers_authored_by_team[paper_UT] = list(set(dict_plos_UT_list_papers_authored_by_team[paper_UT]))


        except KeyError: pass

        cont +=1





    with open('../data/dict_plos_UT_list_references_used_prior.pkl', 'wb') as handle:
                 pickle.dump(dict_plos_UT_list_references_used_prior, handle, protocol = 2)
    print ("written:",'../data/dict_plos_UT_list_references_used_prior.pkl',len(dict_plos_UT_list_references_used_prior))   




    with open('../data/dict_plos_UT_list_papers_authored_by_team.pkl', 'wb') as handle:
                 pickle.dump(dict_plos_UT_list_papers_authored_by_team, handle, protocol = 2)
    print ("written:",'../data/dict_plos_UT_list_papers_authored_by_team.pkl',len(dict_plos_UT_list_papers_authored_by_team))   












    ####### i add the team's expertise to the dataframe:




    df_merged = pickle.load(open('../data/df_reference_cite_plos_merged_simplified_added_more_columns.pkl', 'rb'))
    print ("done loading pickles", df_merged.shape)

 


    print ("\n adding team_expertise to pandas df  ..................")
    list_expertise_papers= []
    for paper_UT in list_paper_UT:
        list_expertise_papers.append(len(dict_plos_UT_list_papers_authored_by_team[paper_UT]))


    plos_df['team_expertise'] = list_expertise_papers

    plos_simple = plos_df[['paper_UT','team_expertise']]
    df_merged = pd.merge(df_merged, plos_simple, on='paper_UT', how='left')






    path = '../data/df_reference_cite_plos_merged_simplified_added_more_columns_.pkl'
    df_merged.to_pickle(path, compression='infer', protocol=2)
    print ("written df_reference_cite_plos_merged_simplified_added_more_columns_.pkl")




    ############ i add the recycled_ref label to the plos_ref database:
    print ("\n adding recycled_ref label to pandas df  ..................")
    df_merged['recycled_ref'] = df_merged.apply (lambda row: get_reclycle_ref_yes_no(row, dict_plos_UT_list_references_used_prior),axis=1)




    path = '../data/df_reference_cite_plos_merged_simplified_added_more_columns__.pkl'
    df_merged.to_pickle(path, compression='infer', protocol=2)
    print ("written df_reference_cite_plos_merged_simplified_added_more_columns__.pkl")




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




class MongoConnection(object):
    def __init__(self, cxnSettings, **kwargs):
        self.settings = cxnSettings
        self.mongoURI = self._constructURI()
        self.connect(**kwargs)
        self.ensure_index()

    def _constructURI(self):
        '''
        Construct the mongo URI
        '''
        mongoURI = 'mongodb://'
        #User/password handling
        if 'user'in self.settings and 'password' in self.settings:
            mongoURI += self.settings['user'] + ':' + self.settings['password']
            mongoURI += '@'
        elif 'user' in self.settings:
            print('Missing password for given user, proceeding without either')
        elif 'password' in self.settings:
            print('Missing user for given passord, proceeding without either')
        #Host and port
        try:
            mongoURI += self.settings['host'] + ':'
        except KeyError:
            print('Missing the hostname. Cannot connect without host')
            sys.exit()
        try:
            mongoURI += str(self.settings['port'])
        except KeyError:
            print('Missing the port. Substituting default port of 27017')
            mongoURI += str('27017')
        return mongoURI

    def connect(self, **kwargs):
        '''
        Establish the connection, database, and collection
        '''
        self.connection = MongoClient(self.mongoURI, **kwargs)
        #########
        try:
            self.db = self.connection[self.settings['db']]
        except KeyError:
            print("Must specify a database as a 'db' key in the settings file")
            sys.exit()
        #########
        try:
            self.collection = self.db[self.settings['collection']]
        except KeyError: pass
            #print('Should have a collection.', end='')
            #print('Starting a collection in database', end='')
            #print(' for current connection as test.')
            #self.collection = self.db['test']

    def tearDown(self):
        '''
        Closes the connection
        '''
        self.connection.close()

    def ensure_index(self):
        '''
        Ensures the connection has all given indexes.
        indexes: list of (`key`, `direction`) pairs.
            See docs.mongodb.org/manual/core/indexes/ for possible `direction`
            values.
        '''
        if 'indexes' in self.settings:
            for index in self.settings['indexes']:
                self.collection.ensure_index(index[0], **index[1])




          


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



