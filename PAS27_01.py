import pandas
import csv
import numpy

#  import data
df=pandas.read_csv(r"C:\Users\shuai\Documents\FromationPython\anomalie-signalees\dans_ma_rue_ok.csv",sep = ';', encoding = 'unicode_escape', header = 0)

print("--------------------- nettoyage data--------------------------")


df.info()   # data information

df[df.isnull().values==True]  #  rechercher NAN

# enlever les colonnes qui on n'a pas besoin et créer un DataFrame

df_propre=df.drop(['ADRESSE','DATE DECLARATION','geo_shape','ID DECLARATION',
         'CONSEIL DE QUARTIER','OUTIL SOURCE','INTERVENANT','ID_DMR','SOUS TYPE DECLARATION'], axis=1)

df_propre.rename(columns={'geo_point_2d':'GEOLOCALISATION'})

df_propre.info()


 #  lower()-- miniscule, upper()--majscule
df_propre['TYPE DECLARATION']= df_propre['TYPE DECLARATION'].str.lower()

#df_propre['TYPE DECLARATION']= df_propre['TYPE DECLARATION'].str.strip()  # enlever les espaces


print("----------------------question 1---------------------------------")
'''
   Quelles sont les années pour lesquelles il y a le plus / le moins d’anomalies signalées par arrondissement ?
'''
# nombre d'incendent par arrondissement par an
# cette df affiche un tableau avec comme colonne arrondissement, 2020 et 2021
# et comme ligne le nombres d'indicent signalé dans chaque arrondissemnt

new1_df = pandas.crosstab([df_propre['ARRONDISSEMENT']], df_propre['ANNEE DECLARATION'])
print(new1_df)

# Rajouter la colonne max de chaque ligne new1_df
# Rajouter la colonne min de chaque ligne new1_df
new1_df['Min_idx'] = new1_df.idxmin(axis=1)
new1_df['Max_idx'] = new1_df.idxmax(axis=1)
print(new1_df)

print("-----------------------question 2--------------------------")

'''
Quels sont les mois pour lesquels il y a le plus / le moins d’anomalie signalées, par type d’anomalie ?
'''

new2_df = pandas.crosstab([df_propre['TYPE DECLARATION']], df_propre['MOIS DECLARATION'])
print(new2_df)

new2_df['Min_idx'] = new2_df.idxmin(axis=1)
new2_df['Max_idx'] = new2_df.idxmax(axis=1)
print(new2_df)


print("------------------------question 3--------------------------")

'''
Quel(s) arrondissement(s) comportent le plus / le moins d’anomalies signalées, par type d’anomalie ?
'''

new3_df = pandas.crosstab([df_propre['TYPE DECLARATION']], df_propre['ARRONDISSEMENT'])
print(new3_df)

new3_df['Min_idx'] = new3_df.idxmin(axis=1)
new3_df['Max_idx'] = new3_df.idxmax(axis=1)
print(new3_df)

