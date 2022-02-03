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
# ===================================================
#               Quetion 1
# ===================================================
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

# histogramme
'''
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
    # plt.show()
    '''

# camb  
for i in df_1['arrondissement'] :
    df_iloc = df_1.iloc[i-1, 1:-2]
    df_iloc.plot(
        kind="pie",
        colors=["#B7D6EA", "#29FAAE"],
        ylabel="Arondissement "+ str(i),
        title    = "Anomalies signalées dans l'arrondissement "+ str(i),
        startangle=90,
        autopct="%0.0f%%",
        rot=0,
        xticks=[],
        subplots = True,
        labels= [2020,2021]
    )
    plt.savefig("c_arrondissement. png")
    plt.show()
# ===================================================
#               Quetion 2
# ===================================================
# ce tableau affiche commme colonnes: les 12 mois de chaque annee (2020, 2021)
# et comme lignes les type_declarations et annee_declaration
dta = pandas.crosstab([df['type_declaration'], df['annee_declaration']], df['mois_declaration'])
# pour recuperer type_declaration et année_declaration en colonne
dt = dta.reset_index()
# permet de generer le df que je souhaite 
def table_type_anomalie_par_mois(annee) :
    dt_frame = dt.groupby('annee_declaration').get_group(annee)
    # Supprimer les colonnes nulles
    # exemple: en 2020 aucune anomalie n'a été signalée entre janvier et aout
    # on suprime donc ces colonnes de la df
    colonne_a_supprimee = []
    for i in range(1, 13) :
        somme = 0
        for j in dt_frame[i] :
            somme += j
        if somme == 0 :
            colonne_a_supprimee.append(i)
    # La data qu'on va retourner
    dt_final = dt_frame.drop(colonne_a_supprimee, axis = 1)
    
    # supprimer egalement les annee_declaration et type_de_declaration
    # pour eviter de fausser les resultat de min et max
    data = dt_final.drop(['annee_declaration', 'type_declaration'], axis=1)
    
    # la valeur de min
    data['min'] = data.min(axis=1)
    # le mois sur lequel on a le min
    data['min_mois'] = data.idxmin(axis=1)

    # le mois sur lequel on a le ax
    data['max_mois'] = data.idxmax(axis=1)
    # la valeur de max
    data['max'] = data.max(axis=1)
    # min_mois correspond au mois sur lequel on le moins d'anomalie signalée
    dt_final['min_mois'] = data['min_mois']
    # valeur_min correspond au nb d'anomalie signalee de l'annee
    dt_final['valeur_min'] = data['min']

    dt_final['max_mois'] = data['max_mois']
    dt_final['valeur_max'] = data['max']
    
    return dt_final

# les 2 df qu'ontilisera
df_2020 = table_type_anomalie_par_mois(2020)
df_2021 = table_type_anomalie_par_mois(2021)

def histogramme_q2(annee, liste_mois) :
    df_2          = table_type_anomalie_par_mois(annee)
    colonnes_mois = df_2.columns[2:len(df_2.columns)-4]

    for i in range(len(colonnes_mois)) :
        df_iloc = df_2.iloc[i: i+1]
        index = df_iloc['type_declaration'].index[0]
        sns.set_style("ticks")
        sns.set_theme()
        df_iloc.plot(x         = "type_declaration",
                # la hauteur de bar
                    y         = colonnes_mois,
                    # type de grapg$hique
                    kind      = "bar",
                    subplots  = False,
                    title     = df_iloc['type_declaration'][index] + " signalé(es) en \n" + str(annee) + " de " + liste_mois[0] + " à " + liste_mois[-1], 
                    # Nom axe des abscisses
                    xlabel    = " ", 
                    # Nom axe des ordonnées
                    ylabel    = "Nombre d'anomalies signalées", 
                    # La rotation de xlabel
                    rot       = 0, 
                    # La legende
                    label     = liste_mois
            )
        plt.show()
# histogramme_q2(2020, ['Semptembre', 'Octobre', 'Novembre', 'Décembre'])
histogramme_q2(2021, ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'semptebre', 'octobre'])



['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'semptebre', 'octobre']