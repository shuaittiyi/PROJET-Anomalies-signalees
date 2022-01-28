#-------------------------------------------------------------------------------
# Name:        Dans ma rue / projet paris
# Purpose:
#
# Author:      Bem
#
# Created:     25/01/2022
#-------------------------------------------------------------------------------

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

# Question 1: 
# nombre d'incendent par arrondissement par an
df_1 = pandas.crosstab([df['ARRONDISSEMENT']], df['ANNEE DECLARATION'])
# Ajouter les colonnes min et max de chaque ligne new_df
df_1['min'] = df_1.idxmin(axis=1)
df_1['max'] = df_1.idxmax(axis=1)
# Pour rendre df_1 pratique 
# on le transforme en dict
df_quest_1 = dict(df_1) # Un dictionnaire avec comme clés
                        # min, max, 2020, 2021
                        # et la valeur de chacune de ces clés
                        # est une serie qui a pour clés
                        # les arrondissemnt: 1, 2,..., 20
                        # ex: df_quest_1['min] renvoie une serie:
                        # 1     2020
                        # 2     2020
                        # 3     2020
                        # 4     2020
                        # 5     2020
                        # 6     2020
                        # 7     2020
                        # 8     2020
                        # 9     2020
                        # 10    2020
                        # 11    2020
                        # 12    2020
                        # 13    2020
                        # 14    2020
                        # 15    2020
                        # 16    2020
                        # 17    2020
                        # 18    2020
                        # 19    2020
                        # 20    2020
                        # et dr['min][20] renvoit 2020

# Transformer en dict le df_1
dict_df_1 = dict(df_1)
# Creation d'un nnouveau dict qui va nous permettre de
# créer une nouvelle df
data_frame = {'arrondissement' : list(range(1,21)), 2020 : [], 2021: [], 'Min' : [], 'Max': []}
# iterer sur le dict afin de condtruire une matrice
# qui sera ensuite transformer en df
for cle, serie in dict_df_1.items():
    for key, value in data_frame.items() :
        if key == cle :
            data_frame[key] = serie.tolist()
# création de la df finale
df_final_1 = pandas.DataFrame(data = data_frame)
