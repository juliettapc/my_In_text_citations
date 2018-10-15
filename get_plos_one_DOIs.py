
from __future__ import print_function, unicode_literals
import sys
from pymongo import MongoClient

import sys

import pickle
import os,glob
import pandas as pd
import operator

#sys.path


# This code is the MongoConnection class from the Amaral lab LabTools folder.



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
        except KeyError:
            print('Should have a collection.', end='')
            print('Starting a collection in database', end='')
            print(' for current connection as test.')
            self.collection = self.db['test']

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


# In[3]:


merged_papers_settings = {
    "host": "chicago.chem-eng.northwestern.edu",
    "port": "27017",
    "db": "web_of_science_aux",
    "collection": "merged_papers",
    "user": "mongoreader",
    "password": "emptycoffeecup"
}

papers_con = MongoConnection(merged_papers_settings)




lista_all_plos_UTs = pickle.load(open('/home/staff/julia/at_Northwestern/In_Text_Citations/In-Text-Citations-New/data/lista_all_plos_UTs.pkl', 'rb'))
new_lista_all_plos_UTs = ['000'+str(item) for item in lista_all_plos_UTs]   # i need to add the 000 so it matches the db UTs

#print (len(new_lista_all_plos_UTs))


# In[15]:




#lista_UTs=['000322590800016','000254928800015','000305349100026','000321341000076']

start=0
stop=1000
while stop <=159000:


    lista=new_lista_all_plos_UTs[start:stop]
    query = papers_con.collection.find({"UT":{"$in":lista}},{"UT":1,"AR":1}, no_cursor_timeout=True)  


    #print (start, stop)

    for item in query:  # query (cursor) is an iterator (once i iterate over it once, it is empty), and every item is a dict

        UT=item["UT"]
        doi=item['AR'][-1]
        #string =str(UT)+" "+str(doi)
        if ".pone." in doi:
            print ( doi)

    stop +=1000
    start +=1000
        
     
    query.close()  # because i am using the no_cursor_timeout=True, i need also this, or cursor keeps waiting so ur resources are used up
        
