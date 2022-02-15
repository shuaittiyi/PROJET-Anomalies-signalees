import pandas
import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib import cm
from scipy.stats import kde
import seaborn as sns
import sys


# Ouverture de fichier
df=pandas.read_csv(r"C:\Users\shuai\Documents\FromationPython\anomalie-signalees\dans_ma_rue_ok.csv",sep = ';', encoding = 'unicode_escape', header = 0)
# supprimer les colonnes qui servent à rien
df = df.drop(['ADRESSE','DATE DECLARATION','geo_shape','ID DECLARATION',
         'CONSEIL DE QUARTIER','OUTIL SOURCE','INTERVENANT','ID_DMR','SOUS TYPE DECLARATION'], axis=1)
# Transformer tous les noms de colunnes en miniscule
df.columns = df.columns.str.lower()
# Remplacer les espaces de noms de colonnes par '_'
df.columns = df.columns.str.replace("[ ]", "_")


# ====================================================================================================================
# Quetion 1: Quelles sont les années pour lesquelles il y a le plus / le moins d’anomalies signalées par arrondissement ?
# ======================================================================================================================

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

# -----------------------------------histogramme---------------------------------------

for i in df_1['arrondissement'] :
    sns.set_style("ticks")
    sns.set_theme()
    df_iloc = df_1.iloc[i-1:i]
    df_iloc.plot(
        x        = "arrondissement",
        y        = [2020,2021],
        kind     = "bar",
        subplots = False,
        title    = "2020-2021 Anomalies signalées",
        xlabel   = "Arrondissement " + str(i),
        ylabel   = "Nombre d'anomalies signalées",
        color    = {2020: "#B7D6EA", 2021: "#29FAAE"},
        rot      = 0,
        xticks   = [],
        label    = [2020, 2021],
        grid = True
        )
    plt.show()

#--------------------------- cammenbert-----------------------------------------------
for i in df_1['arrondissement'] :
    df_iloc = df_1.iloc[i-1, 1:-2]
    df_iloc.plot(
        kind="pie",
        colors    = ["#B7D6EA", "#29FAAE"],
        ylabel="Arondissement "+ str(i),
        title    = "2020-2021 Anomalies signalées",
        startangle=90,
        autopct="%0.0f%%",
        rot=0,
        xticks=[],
        subplots = True,
        labels= [2020,2021]
    )
    plt.savefig("c_arrondissement. png")
    plt.show()


#==================================================================================================================
# Question 2: Quels sont les mois pour lesquels il y a le plus / le moins d’anomalie signalées, par type d’anomalie ?
# =================================================================================================================

# ce tableau affiche commme colonnes: les 12 mois de chaque annee (2020, 2021)
# et comme lignes les type_declarations et annee_declaration
dta = pandas.crosstab([df['type_declaration'], df['annee_declaration']], df['mois_declaration'])
# pour recuperer type_declaration et année_declaration en colonne
dt = dta.reset_index()
#print(dta)
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

# -----------------------------------histogramme---------------------------------------
# 2020

colonnes_mois = df_2020.columns[2:len(df_2020.columns)-4]
for i in range(len(colonnes_mois)) :
    df_iloc = df_2020.iloc[i: i+1]
    index = df_iloc['type_declaration'].index[0]
    sns.set_style("ticks")
    color = sns.color_palette("husl", 12)
    sns.set_theme()
    df_iloc.plot(
                x         = "type_declaration",
                # la hauteur de bar
                y         = colonnes_mois,
                # type de graphique
                kind      = "bar",
                subplots  = False,
                title     = " signalé(e)s en " + str(2020),
                # Nom axe des abscisses
                xlabel    = " ",
                # Nom axe des ordonnées
                ylabel    = "Nombre d'anomalies signalées",
                # La rotation de xlabel
                rot       = 0,
                # La legende
                label     = ['Semptembre', 'Octobre', 'Novembre', 'Décembre']
                )
plt.show()

#---------------------------------------------------------------------
# 2021

colonnes_mois = df_2021.columns[2:len(df_2021.columns)-4]
for i in range(len(colonnes_mois)) :
    df_iloc = df_2021.iloc[i: i+1]
    index = df_iloc['type_declaration'].index[0]
    sns.set_style("ticks")
    color = sns.color_palette("husl", 12)
    sns.set_theme()
    df_iloc.plot(
                x         = "type_declaration",
                # la hauteur de bar
                y         = colonnes_mois,
                # type de grapg$hique
                kind      = "bar",
                subplots  = False,
                title     = " signalé(e)s en " + str(2021),
                # Nom axe des abscisses
                xlabel    = " ",
                # Nom axe des ordonnées
                ylabel    = "Nombre d'anomalies signalées",
                # La rotation de xlabel
                rot       = 0,
                color     = color,
                # La legende
                label     = ['Janvrier','Février','Mars','Avril','Mai','Juin','Juille','Août','Semptembre', 'Octobre']
                )
plt.show()

#--------------------------- cammenbert-----------------------------------------------
'''
colonnes_mois = df_2021.columns[2:len(df_2021.columns)-4]
for i in range(len(colonnes_mois)) :

    df_iloc = df_2021.iloc[i-1, 1:-2]
    df_iloc.plot(
        kind="pie",
        ylabel="df_iloc['type_declaration'][i]",
        title = "signalé(e)s en " + str(2021)
        startangle=90,
        autopct="%0.0f%%",
        rot=0,
        xticks=[],
        subplots = True)
    plt.show()

'''
#------------------------------------------------------------------------------------#
'''
def table_type_anomalie_par_mois(annee) :
    dt_frame = dt.groupby('annee_declaration').get_group(annee)
    # Supprimer les colonnes nulles
    # exemple: en 2020 aucune anomalie n'a été signalée entre janvier et aout
    # on suprime donc ces colonnes de la df
    colonne_a_supprimee = []
    for colonne in range(1, 13) :
        somme = 0
        for j in dt_frame[colonne] :
            somme += j
        if somme == 0 :
            colonne_a_supprimee.append(colonne)
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

def histogramme_q2(annee, liste_legende) :
    df_2          = table_type_anomalie_par_mois(annee)
    colonnes_mois = df_2.columns[2:len(df_2.columns)-4]

    for i in range(len(colonnes_mois)) :
        df_iloc = df_2.iloc[i: i+1]
        index = df_iloc['type_declaration'].index[0]
        sns.set_style("ticks")
        color = sns.color_palette("husl", 12)
        sns.set_theme()
        df_iloc.plot(x         = "type_declaration",
                    # la hauteur de bar
                    y         = colonnes_mois,
                    # type de grapg$hique
                    kind      = "bar",
                    subplots  = False,
                    xlabel    = " signalé(e)s en " + str(annee),
                    # Nom axe des ordonnées
                    ylabel    = "Nombre d'anomalies signalées",
                    # La rotation de xlabel
                    rot       = 0,
                    color     = color,

            ).legend(liste_legende)
        # plt.savefig("c_anomalie_q2_" + str(annee) + str(index) + ".png")
        plt.show()


histogramme_q2(2020, ['Septembre','Octobre', 'Novembre', 'Décembre'])
histogramme_q2(2021, ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'juillet','Aout','Septembre','Octobre'])

'''

#------------------------------------------------------------------------------------#

# ===============================================================================================================
# Question 3: Quel(s) arrondissement(s) comportent le plus / le moins d’anomalies signalées, par type d’anomalie ?
# ===============================================================================================================

df_3 = f_data_frame(pandas.crosstab([df['type_declaration']], df['arrondissement']))
#print(df_3)


#------------------------histogramme & cammenbert-----------------------------------#


colonnes_arrondissement = df_3.columns[1:len(df_3.columns)-2]

for i in range(len(colonnes_arrondissement)):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    if i < 10:
        df_iloc = df_3.iloc[i : i + 1]
        print("bar", df_iloc)
        sns.set_style("ticks")
        sns.set_theme()
        df_iloc.plot(
            x="type_declaration",
            y=colonnes_arrondissement,
            kind="bar",
            ax=axes[1],
            subplots=False,
            title="Anomalies signalées",
            xlabel=df_iloc["type_declaration"][i],
            ylabel="Nombre d'anomalies signalées",
            rot=0,
            xticks=[],
             # deux couleur au choix
            colormap = 'rainbow',
            #colormap = "RdBu",
            grid=True,
        )
        plt.legend(bbox_to_anchor=(1, 1.05), loc="upper left")


        df_iloc = df_3.iloc[i, 1:-2]
        print(df_iloc)
        df_iloc.plot(
            kind="pie",
            ax=axes[0],
            title="Anomalies signalées",
            startangle=90,
            autopct="%0.1f%%",
            rot=0,
            xticks=[],
            subplots=True,
            colormap="RdBu",
            grid=True,
        )

        axes[0].set_aspect(
            "equal"
        )  # make aspect equal (such that circle is not eliptic)
        plt.savefig(p + "\pie_bar_question3_" + str(i) + ".png")
        plt.show()



