
import sys

import pickle
import gzip





lista_all_plos_UTs = pickle.load(open('../data/lista_all_plos_UTs.pkl', 'rb'))
new_lista_all_plos_UTs = ['000'+str(item) for item in lista_all_plos_UTs]
print (len(lista_all_plos_UTs))

lista_all_reference_UTs = pickle.load(open('../data/lista_all_reference_UTs.pkl', 'rb'))
print (len(lista_all_reference_UTs))






lista_UTs_plos_and_ref=new_lista_all_plos_UTs+ lista_all_reference_UTs
lista_UTs_plos_and_ref =  list(set(lista_UTs_plos_and_ref))
#len(lista_UTs_plos_and_ref)   #2,706,287 UTs without repetitions




lista_files=[]

for i in range(320):
    i +=1
    file_name='wos_dais_all_batch'+str(i)+'.csv.gz'    
    lista_files.append(file_name)


###########



path_disamb='/home/workspace/scibio/resources/rbusa/rbusa_main_v1_1/disambiguation/wos_dais/'





#lista_lines=[]
#tot_cont_lines=0

#ini=0
#delta=10
#fin= ini + delta


#while fin <= 320:
    
 #   lista_all_lines=[]  
  #  for file_name in lista_files[ini:fin]:

   #     print (file_name)


    #    cont =1    
     #   with gzip.open(path_disamb+file_name,'r') as f:
      #      for line in f:

       #         UT=str(line).split(",")[1]           
        #        lista_all_lines.append(str(line))

         #       cont +=1


        #print ("  done,", cont)     
        #tot_cont_lines += cont   


    ######### i process the slice of files
    #print ("  processing batch........")
    #for line in lista_all_lines:
     #   UT=str(line).split(",")[1]
      #  if UT in lista_UTs_plos_and_ref:       
       #     lista_lines.append(str(line))
    #print ("     ",len(lista_all_lines), len(lista_lines))    


    #ini +=delta
    #fin +=delta

###############




lista_lines=[]
tot_cont_lines=0


delta=10
fin= 321
ini =  fin - delta

while fin > 0:
    
    #lista_all_lines=[]  
    for file_name in lista_files[ini:fin]:

        print (file_name)


        cont =1    
        with gzip.open(path_disamb+file_name,'r') as f:
            for line in f:

                UT=str(line).split(",")[1]           
                #lista_all_lines.append(str(line))
                if UT in lista_UTs_plos_and_ref:       
                    lista_lines.append(str(line))
                    print (str(line))

                cont +=1



        tot_cont_lines += cont   
        print ("  done tot lines in file and so far", cont, tot_cont)     

   

        with open('../data/lista_lines_disambig.pkl', 'wb') as handle:
            pickle.dump(lista_lines, handle, protocol = 2)
        print ("written: ../data/lista_lines_disambig.pkl")
        print ("# lines in selected lines:", len(lista_lines))



    ini -=delta
    fin -=delta



###############





with open('../data/lista_lines_disambig.pkl', 'wb') as handle:
     pickle.dump(lista_lines, handle, protocol = 2)
print ("written: ../data/lista_lines_disambig.pkl")
print ("# lines in selected lines:", len(lista_lines))

