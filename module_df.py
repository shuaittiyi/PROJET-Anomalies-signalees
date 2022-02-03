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
# supprimer les colonnes qui servent à rien
df = df.drop(['ADRESSE','DATE DECLARATION','geo_shape','ID DECLARATION',
         'CONSEIL DE QUARTIER','OUTIL SOURCE','INTERVENANT','ID_DMR','SOUS TYPE DECLARATION'], axis=1)
# Transformer tous les noms de colunnes en miniscule
df.columns = df.columns.str.lower()
# Remplacer les espaces de noms de colonnes par '_'
df.columns = df.columns.str.replace("[ ]", "_")

# Une fonction qui permet nos df
def f_data_frame(dataFrame) :
    # Ajouter les colonnes min et max de chaque ligne new_df
    dataFrame['min_idxmin'] = dataFrame.idxmin(axis=1)
    dataFrame['max_idxmax'] = dataFrame.idxmax(axis=1)
    # on cree des copie de colonnes min_idxmin et max_idxmax  que l'on nomme min et max
    dataFrame['min'] = dataFrame['min_idxmin'].tolist()
    dataFrame['max'] = dataFrame['max_idxmax'].tolist()
    # Suppression de colonnes min_idxmax et max_idx
    # car elles nous servent à rien (on les a copié)
    dataFrame = dataFrame.drop(['min_idxmin', 'max_idxmax'],axis=1)
    # la dataframe finale
    return dataFrame.reset_index()

df_1 = f_data_frame(pandas.crosstab([df['arrondissement']], df['annee_declaration']))
df_2 = f_data_frame(pandas.crosstab([df['type_declaration']], df['mois_declaration']))
df_3 = f_data_frame(pandas.crosstab([df['type_declaration']], df['arrondissement']))

for i in df_1['arrondissement'] :
    sns.set_style("ticks")
    sns.set_theme()
    df_iloc = df_1.iloc[i-1:i]
    df_iloc.plot(
        x        = "arrondissement",
        y        = [2020,2021],
        kind     = "bar",
        subplots = False,
        title    = "Anomalies signalées", 
        xlabel   = "Arrondissement " + str(i), 
        ylabel   = "Nombre d'anomalies signalées", 
        color    = {2020: "#B7D6EA", 2021: "#29FAAE"},
        rot      = 0, 
        xticks   = [],
        label    = [2020, 2021], 
        grid = True
        )
    plt.show()
# print(df_2)
# print(df_3['type_declaration'].count())
for i in range(len(df_3['type_declaration'])) :
# for i in [1, 2]:
    # print([1, 2].index(i))
    # sns.set_style("ticks")
    # sns.set_theme()
    
    df_iloc = df_3.iloc[i: i+1]
    df_iloc.plot(
        x        = list(range(1, 21)),
        # y        = ['min', 'max'],
        y        = "type_declarartion",
        kind     = "bar",
        subplots = False,
        title    = "Anomalies signalées", 
        xlabel   = "Arrondissements ", 
        ylabel   = "Nombre d'anomalies signalées", 
        # color    = {2020: "#B7D6EA", 2021: "#29FAAE"},
        rot      = 0, 
        # xticks   = list(range(1, 21)),
        # label    = [], 
        grid = True,
        linewidth = 6,
        )
    # plt.xticks(list(range(1, 21)), list(range(1, 21)))
    plt.show()

colors = ["#2BDD84", "#78DEFC", "#E6177E", "#C0340C", "#B2A3E9", "#A56B4D", "#BFCA8D", "#FE474C", "#912230","#72ED64","#D9DC0E","#553A64", "#B4A218","#69E9FC","#2AEEB2","#BAE7A1","#689FB0", "#22D6B3","#2E053A","#6E1C14"]

for i in range(len(df_3['type_declaration'])) :

    sns.set_style("ticks")
    sns.set_theme()
    df_iloc = df_3.iloc[i: i+1]
    bar1 = plt.bar(np.arange(len(df_iloc['type_declaration'])) + 0.3, df_iloc['type_declaration'] , 0.3, align='center', color='b', label='Fast <= 6 sec.')
    df_iloc.plot(
        x        = "type_declaration",
        y        = list(range(1, 21)),
        kind     = "bar",
        subplots = False,
        title    = "Anomalies signalées", 
        xlabel   = "Arrondissements ", 
        ylabel   = "Nombre d'anomalies signalées", 
        color    = colors,
        rot      = 0, 
        # xticks   = list(range(1, 21)),
        label    = [], 
        grid = True,
        
        )
    # plt.xticks(list(range(1, 21)), list(range(1, 21)))

    plt.show()
