import pandas
import csv
import numpy
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import kde
import seaborn as sns
import json

# Ouverture de fichier
df = pandas.read_csv("C:\projet_dans_ma_rue\dans_ma_rue_ok.csv", sep = ';', encoding = 'unicode_escape', header = 0)
# Transformer tous les noms de colunnes en miniscule
df.columns = df.columns.str.lower()
# Remplacer les espaces de noms de colonnes par '_'
df.columns = df.columns.str.replace("[ ]", "_")
#-----------------------------------------------------
#                    Question 1: 
#-----------------------------------------------------
# nombre d'incendent par arrondissement par an
df_1 = pandas.crosstab([df['arrondissement']], df['annee_declaration'])
# Ajouter les colonnes min et max de chaque ligne new_df
df_1['min_idxmin'] = df_1.idxmin(axis=1)
df_1['max_idxmax'] = df_1.idxmax(axis=1)
# Afin de pouvoir appliquer la methode reset_index
# on cree des copie de colonnes min_idxmin et max_idxmax
# que l'on nomme min et max
df_1['min'] = df_1['min_idxmin'].tolist()
df_1['max'] = df_1['max_idxmax'].tolist()
# Suppression de colonnes min_idxmax et max_idx
# car elles nous servent plus à rien (on les a copié)
df_1 = df_1.drop(['min_idxmin', 'max_idxmax'],axis=1)
# la dataframe finale
df_final_1 = df_1.reset_index()

#-----------------------------------------------------
#                    Question 3: 
#-----------------------------------------------------
df_2 = pandas.crosstab([df['type_declaration']], df['mois_declaration'])
df_2['min_idxmin'] = df_2.idxmin(axis=1)
df_2['max_idxmax'] = df_2.idxmax(axis=1)

df_2['min'] = df_2['min_idxmin'].tolist()
df_2['max'] = df_2['max_idxmax'].tolist()

df_2 = df_2.drop(['min_idxmin', 'max_idxmax'],axis=1)
df_final_2 = df_2.reset_index()

#-----------------------------------------------------
#                    Question 3: 
#-----------------------------------------------------
df_3 = pandas.crosstab([df['type_declaration']], df['arrondissement'])
df_3['min_idxmin'] = df_3.idxmin(axis=1)
df_3['max_idxmax'] = df_3.idxmax(axis=1)

df_3['min'] = df_3['min_idxmin'].tolist()
df_3['max'] = df_3['max_idxmax'].tolist()

df_3 = df_3.drop(['min_idxmin', 'max_idxmax'],axis=1)
df_final_3 = df_3.reset_index()

# Une fonction qui permet generer ces 3 df 
def f_data_frame(dataFrame) :
    dataFrame['min_idxmin'] = dataFrame.idxmin(axis=1)
    dataFrame['max_idxmax'] = dataFrame.idxmax(axis=1)

    dataFrame['min'] = dataFrame['min_idxmin'].tolist()
    dataFrame['max'] = dataFrame['max_idxmax'].tolist()

    dataFrame = dataFrame.drop(['min_idxmin', 'max_idxmax'],axis=1)
    return dataFrame.reset_index()