import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from folium.plugins import HeatMap

from streamlit_option_menu import option_menu
from streamlit_folium import st_folium

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestClassifier

rep_images = "images/"
rep_data = "data/"

df_cyclistes_23 = pd.read_csv(rep_data+"df_cyclistes_2023.csv", sep=";") # pour les maps, uniquement la dernière année sinon trop de données
df_cyclistes_21_23 = pd.read_csv(rep_data+"df_cyclistes_2021_2023.csv", sep=";")

# victimes cyclistes, avec éventuellement plusieurs lignes pour chaque accident (car intersection de plusieurs lieux)
df_cyclistes_all = df_cyclistes_21_23[df_cyclistes_21_23['catv'].isin([1, 80])]
# victimes cyclistes mais une seule ligne par accident, avec la valeur max
df_max = df_cyclistes_21_23[df_cyclistes_21_23['catv'].isin([1, 80])].groupby('id_usager', as_index=False).max()
# victimes cyclistes mais une seule ligne par accident, avec la 1e valeur
df_first = df_cyclistes_21_23[df_cyclistes_21_23['catv'].isin([1, 80])].groupby('id_usager', as_index=False).first()

df_nb_vehicules = df_cyclistes_21_23.groupby('Num_Acc', as_index=False)['id_vehicule'].nunique()
vehicule_multiple = list(df_nb_vehicules[df_nb_vehicules['id_vehicule']>1]['Num_Acc'].unique())
cycliste_seul = list(df_nb_vehicules[df_nb_vehicules['id_vehicule']==1]['Num_Acc'].unique())

# pour les maps, uniquement année 2023 sinon trop de données à afficher : 
df_max_23 = df_cyclistes_23[df_cyclistes_23['catv'].isin([1, 80])].groupby('id_usager', as_index=False).max()
# function for folium map coordinates
def coord(df_data):
    data = [[x,y,1] for x,y,_ in zip(df_data['lat'].tolist(), df_data['long'].tolist(),range(df_data.shape[0]))]
    data = (np.array(data)).tolist()
    return data



def accueil():
      # Using object notation
    # Le bouton de déconnexion    
    
    # Using "with" notation

    with st.sidebar:        
        st.write(f"Bienvenue",)
        selection = option_menu(
            menu_title=None,
            options=["Accueil", "Choix Visu Statistiques", "Maps", "Predictions"]

        )

    
    
    if selection == "Accueil":
        st.write('Bienvenue')
        page_accueil()

        #st.image(rep_images+"home.jpg")
    elif selection == "Choix Visu Statistiques":
        page_visu() 

    elif selection == "Maps":
        page_maps() 

    elif selection == "Predictions":
        page_predictions()


def page_accueil():
    
    # cyclistes
    st.header("Statistiques 2021-2023 sur la gravité des accidents corporels de la circulation impliquant des cyclistes (accidents enregistrés en France, outre-mer compris)")
    
    # cyclistes sans autre véhicule
    
    df1 = df_cyclistes_21_23[(df_cyclistes_21_23['Num_Acc'].isin(cycliste_seul)) & (df_cyclistes_21_23['catv'].isin([1, 80]))].groupby('id_usager', as_index=False).first()

    fig1 = px.histogram(df1, x='gravity',
                    color='gravity',
                    color_discrete_map = {'Indemne':'green', 'Blessé léger': 'orange', 'Blessé hospitalisé': 'red', 'Tué': 'black' },
                    category_orders={'gravity':['Indemne', 'Blessé léger', 'Blessé hospitalisé', 'Tué']},
                    title="Cyclistes impliqués sans autre véhicule",
                    text_auto=False)

    # Calcul des pourcentages
    counts = df1['gravity'].value_counts()
    total = len(df1)
    percentages = (counts / total * 100).sort_index()

    # Ajout des annotations de pourcentages
    for cat, percentage in percentages.items():
        fig1.add_annotation(
            x=cat,
            y=counts[cat],  # Hauteur correspondante
            text=f"{percentage:.1f}%",
            showarrow=False,
            yshift=10,  # Décalage vertical pour la lisibilité
            font=dict(color="black", size=12)
        )

    # Mise en forme
    fig1.update_traces(textfont_size=12, textposition='outside', hovertemplate='%{x}<br>%{y}<br>',
                    marker_line_color= '#800020', marker_line_width=1.5,
                    opacity=0.8)
    fig1.update_layout(width=600, height=400,
                    yaxis_title="Nombre",
                    # xaxis_title="Catégorie",
                    xaxis_title=None,
                    showlegend=True,
                    legend_title_text="",
                    title = dict(font=dict(size=15), x=0.5)
                    )
    st.plotly_chart(fig1)

    # Cyclistes avec autres véhicules
    
    df2 = df_cyclistes_21_23[(df_cyclistes_21_23['Num_Acc'].isin(vehicule_multiple)) & (df_cyclistes_21_23['catv'].isin([1, 80]))].groupby('id_usager', as_index=False).first()

    fig2 = px.histogram(df2, x='gravity',
                    color='gravity',
                    color_discrete_map = {'Indemne':'green', 'Blessé léger': 'orange', 'Blessé hospitalisé': 'red', 'Tué': 'black' },
                    category_orders={'gravity':['Indemne', 'Blessé léger', 'Blessé hospitalisé', 'Tué']},
                    title="Cyclistes impliqués avec un autre véhicule",
                    text_auto=False)

    # Calcul des pourcentages
    counts = df2['gravity'].value_counts()
    total = len(df2)
    percentages = (counts / total * 100).sort_index()

    # Ajout des annotations de pourcentages
    for cat, percentage in percentages.items():
        fig2.add_annotation(
            x=cat,
            y=counts[cat],  # Hauteur correspondante
            text=f"{percentage:.1f}%",
            showarrow=False,
            yshift=10,  # Décalage vertical pour la lisibilité
            font=dict(color="black", size=12)
        )

    # Mise en forme
    fig2.update_traces(textfont_size=12, textposition='outside', hovertemplate='%{x}<br>%{y}<br>',
                    marker_line_color= '#800020', marker_line_width=1.5,
                    opacity=0.8)
    fig2.update_layout(width=600, height=400,
                    yaxis_title="Nombre",
                    # xaxis_title="Catégorie",
                    xaxis_title=None,
                    showlegend=True,
                    legend_title_text="",
                    title = dict(font=dict(size=15), x=0.5)
                    )
    st.plotly_chart(fig2)

    
    # autres usagers
    df3 = df_cyclistes_21_23[~df_cyclistes_21_23['catv'].isin([1, 80])].groupby('id_usager', as_index=False).first()

    
    fig3 = px.histogram(df3, x='gravity',
                    color='gravity',
                    color_discrete_map = {'Indemne':'green', 'Blessé léger': 'orange', 'Blessé hospitalisé': 'red', 'Tué': 'black' },
                    category_orders={'gravity':['Indemne', 'Blessé léger', 'Blessé hospitalisé', 'Tué']},
                    title="Autres usagers impliqués avec des cyclistes", text_auto=False)

    # Calcul des pourcentages
    counts = df3['gravity'].value_counts()
    total = len(df3)
    percentages = (counts / total * 100).sort_index()

    # Ajout des annotations de pourcentages
    for cat, percentage in percentages.items():
        fig3.add_annotation(
            x=cat,
            y=counts[cat],  # Hauteur correspondante
            text=f"{percentage:.1f}%",
            showarrow=False,
            yshift=10,  # Décalage vertical pour la lisibilité
            font=dict(color="black", size=12)
        )

    # Mise en forme
    fig3.update_traces(textfont_size=12, textposition='outside', hovertemplate='%{x}<br>%{y}<br>',
                    marker_line_color= '#800020', marker_line_width=1.5,
                    opacity=0.8)
    fig3.update_layout(width=600, height=400,
                    yaxis_title="Nombre",
                    # xaxis_title="Catégories",
                    xaxis_title=None,
                    showlegend=True,
                    legend_title_text="",
                    title = dict(font=dict(size=15), x=0.5)
                    )
    st.plotly_chart(fig3)


    # Par type d'endroit
    df4 = df_max
    fig4 = px.histogram(df4, x='situ', title="Cyclistes par type d'endroit", text_auto=False)

    # Calcul des pourcentages
    counts = df4['situ'].value_counts()
    total = len(df4)
    percentages = (counts / total * 100).sort_index()

    # Ajout des annotations de pourcentages
    for cat, percentage in percentages.items():
        fig4.add_annotation(
            x=cat,
            y=counts[cat],  # Hauteur correspondante
            text=f"{percentage:.1f}%",
            showarrow=False,
            yshift=10,  # Décalage vertical pour la lisibilité
            font=dict(color="black", size=12)
        )

    # Mise en forme
    fig4.update_traces(textfont_size=12, textposition='outside', hovertemplate='%{x}<br>%{y}<br>',
                    marker_line_color= '#800020', marker_line_width=1.5,
                    opacity=0.8)
    fig4.update_xaxes(tickmode="array", tickvals = [-1,0,1,2,3,4,5, 6, 8], ticktext= ['Inconnu','Aucun','Sur chaussée',  'Sur b.a.u', 'Sur accotement', 'Sur trottoir', 'Sur piste cyclable', 'Sur autre voie spéciale', 'Autres'])

    fig4.update_layout(width=800, height=400,
                    yaxis_title="Nombre",
                    # xaxis_title="Catégories",
                    xaxis_title=None,
                    showlegend=True,
                    legend_title_text="",
                    title = dict(font=dict(size=15), x=0.5)
    )

    st.plotly_chart(fig4)

    df6 = df_max
    fig6 = px.histogram(df6, x='situ', title="Gravité Cyclistes par type d'endroit",
                    color='gravity',
                    color_discrete_map = {'Indemne':'green', 'Blessé léger': 'orange', 'Blessé hospitalisé': 'red', 'Tué': 'black' },
                    category_orders={'gravity':['Indemne', 'Blessé léger', 'Blessé hospitalisé', 'Tué']},
                    text_auto=False)

    fig6.update_xaxes(tickmode="array", tickvals = [-1,0,1,2,3,4,5, 6, 8], ticktext= ['Inconnu','Aucun','Sur chaussée',  'Sur b.a.u', 'Sur accotement', 'Sur trottoir', 'Sur piste cyclable', 'Sur autre voie spéciale', 'Autres'])

    fig6.update_layout(width=800, height=400,
                    yaxis_title="Nombre",
                    # xaxis_title="Catégories",
                    xaxis_title=None,
                    showlegend=True,
                    legend_title_text="",
                    title = dict(font=dict(size=15), x=0.5)
                    )
    
    st.plotly_chart(fig6)


def page_visu():
    cols = ['']
    target = "gravity"

    col1, col2 = st.columns(2)
    
    # d'une manière générale, si la variable 'x' est dans le dataset 'lieux',plusieurs lignes possibles donc alors df=df_cyclistes_all
    # sinon on peut se contenter de df=df_first car cette caractéristique ne change pas dans les différentes lignes du lieu
    vars = {'jour de la semaine': {'df':df_first, 'x': 'day_of_week', 'tickvals': [0,1,2,3,4,5,6], 'ticktext': ['Lundi','Mardi','Mercredi',  'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']},
            'sens de la circulation': {'df': df_cyclistes_all, 'x': 'circ', 'tickvals': [-1, 1,2,3,4], 'ticktext': ['Non renseigné', 'A sens unique','Bidirectionnelle','A chaussées séparées',  'Avec voies d’affectation variable']},
            'condition de surface': {'df': df_cyclistes_all, 'x': 'surf', 'tickvals': [-1, 1,2,3,4,5,6,7,8,9], 'ticktext': ['Non renseigné','Normale', 'Mouillée', 'Flaques', 'Inondée', 'Enneigée', 'Boue', 'Verglacée', 'Corps gras – huile', 'Autre']},
            'type d\'infrastructure': {'df':df_cyclistes_all, 'x': 'infra', 'tickvals': [-1, 0,1,2,3,4,5,6,7,8,9], 'ticktext': ['Non renseigné', 'Aucun', 'Souterrain - tunnel', 'Pont - autopont', 'Bretelle d’échangeur ou de raccordement', 'Voie ferrée', 'Carrefour aménagé', 'Zone piétonne', 'Zone de péage', 'Chantier', 'Autres']},
            'vitesse maximale autorisée': {'df': df_cyclistes_all, 'x': 'vma', 'xaxis_title': 'Vitesse (km/h)'},
            'condition atmosphérique': {'df': df_first, 'x': 'atm', 'tickvals': [-1, 1,2,3,4,5,6,7,8,9], 'ticktext': ['Non renseigné', 'Normale', 'Pluie légère', 'Pluie forte', 'Neige - grêle', 'Brouillard - fumée', 'Vent fort - tempête', 'Temps éblouissant', 'Temps couvert', 'Autre']},
            'type de collision': {'df': df_first, 'x': 'col', 'tickvals': [-1, 1,2,3,4,5,6,7], 'ticktext': ['Non renseigné', 'Deux véhicules - frontale', 'Deux véhicules – par l’arrière', 'Deux véhicules – par le côté', 'Trois véhicules et plus – en chaîne', 'Trois véhicules et plus - collisions multiples', 'Autre collision', 'Sans collision']},
            'situation agglomération': {'df': df_first, 'x': 'agg', 'tickvals': [1,2], 'ticktext': ['Hors agglo', 'En agglo']},
            'condition de luminosité': {'df': df_first, 'x': 'lum', 'tickvals': [1,2,3,4,5], 'ticktext': ['Plein jour', 'Crépuscule ou aube', 'Nuit sans éclairage public', 'Nuit avec éclairage public non allumé', 'Nuit avec éclairage public allumé']},
            'type d\'intersection': {'df': df_first, 'x': 'int', 'tickvals': [1,2,3,4,5,6,7,8,9], 'ticktext': ['Hors intersection', 'Intersection en X', 'Intersection en T', 'Intersection en Y', 'Intersection à plus de 4 branches', 'Giratoire', 'Place', 'Passage à niveau', 'Autre intersection']},
            }
        
           
    option = st.selectbox(
            "Quel variable voulez-vous visualiser ?",
            vars.keys(),
            index=0,
        )


    
    fig1 = px.histogram(vars[option]['df'], x=vars[option]['x'],
                        color='gravity',
                        color_discrete_map={'Indemne': 'green', 'Blessé léger': 'orange', 'Blessé hospitalisé': 'red', 'Tué': 'black' },
                        category_orders={'gravity': ['Indemne', 'Blessé léger', 'Blessé hospitalisé', 'Tué']},
                        # barnorm='percent',
                        text_auto=False)
    if not('xaxis_title' in vars[option]):
        fig1.update_xaxes(tickmode="array", tickvals=vars[option]['tickvals'], ticktext=vars[option]['ticktext'])

    fig1.update_layout(width=800, height=400,
                       yaxis_title="Nombre",
                        # xaxis_title="Jour",
                        xaxis_title=vars[option]['xaxis_title'] if 'xaxis_title' in vars[option] else None,
                        showlegend=True,
                        legend_title_text="",
                        title=dict(font=dict(size=15), x=0.5)
                        )

    fig1.update_layout(title='Nb Gravité Cyclistes par ' + option)
    st.plotly_chart(fig1)



   
    fig2 = px.histogram(vars[option]['df'], x=vars[option]['x'],
                        color='gravity',
                        color_discrete_map = {'Indemne':'green', 'Blessé léger': 'orange', 'Blessé hospitalisé': 'red', 'Tué': 'black' },
                        category_orders={'gravity':['Indemne', 'Blessé léger', 'Blessé hospitalisé', 'Tué']},
                        barnorm='percent',
                        text_auto=False)

    if not('xaxis_title' in vars[option]):
        fig2.update_xaxes(tickmode="array", tickvals=vars[option]['tickvals'], ticktext=vars[option]['ticktext'])

    fig2.update_layout(width=800, height=400,
                        yaxis_title="%",
                        # xaxis_title="Jour",
                        xaxis_title=vars[option]['xaxis_title'] if 'xaxis_title' in vars[option] else None,
                        showlegend=True,
                        legend_title_text="",
                        title = dict(font=dict(size=15), x=0.5)
                        )

    fig2.update_layout(title='% Gravité Cyclistes par ' + option)
    st.plotly_chart(fig2)


def page_maps():  
    
    # Choix de la carte à afficher
    option = st.selectbox(
            "Quelle carte voulez-vous afficher ?",
            ['Répartition globale', 'Localisation exacte'],
            index=None,
        )
    
    legend_txt = '<span style="color: {col};">{txt}</span>'
    df1 = df_max_23

    if option == "Répartition globale":
        # Heatmap
        st.write('Répartition géographique des gravités des accidents corporels des cyclistes')
        
        df_grav1 = coord(df1[df1['gravity']=='Indemne'])
        df_grav2 = coord(df1[df1['gravity']=='Blessé léger'])
        df_grav3 = coord(df1[df1['gravity']=='Blessé hospitalisé'])
        df_grav4 = coord(df1[df1['gravity']=='Tué'])

        m_heat = folium.Map([47, 3], zoom_start=6)
        
        HeatMap(df_grav1).add_to(folium.FeatureGroup(name=legend_txt.format(txt='Indemne', col='green'), show=False).add_to(m_heat))
        HeatMap(df_grav2).add_to(folium.FeatureGroup(name=legend_txt.format(txt='Blessé léger', col='orange'), show=False).add_to(m_heat))
        HeatMap(df_grav3).add_to(folium.FeatureGroup(name=legend_txt.format(txt='Blessé hospitalisé', col='red'), show=False).add_to(m_heat))
        HeatMap(df_grav4).add_to(folium.FeatureGroup(name=legend_txt.format(txt='Tué', col='black')).add_to(m_heat))
        folium.LayerControl().add_to(m_heat)

        # call to render Folium map in Streamlit
        st_data_heatmap = st_folium(m_heat, width=725)

    elif option == "Localisation exacte":
        # Localisation exacte des accidents
        st.write("Localisation exacte des accidents des cyclistes")
        group_1 = folium.FeatureGroup(name=legend_txt.format(txt='Indemne', col='green'), show=False)
        group_2 = folium.FeatureGroup(name=legend_txt.format(txt='Blessé léger', col='orange'), show=False)
        group_3 = folium.FeatureGroup(name=legend_txt.format(txt='Blessé hospitalisé', col='red'), show=False)
        group_4 = folium.FeatureGroup(name=legend_txt.format(txt='Tué', col='black'))
        dico_group = {'Indemne':group_1, 'Blessé léger':group_2, 'Blessé hospitalisé':group_3, 'Tué':group_4}
        dico_color = {'Indemne':'green', 'Blessé léger':'orange', 'Blessé hospitalisé':'red', 'Tué':'black'}

        m_markers = folium.Map([47, 3], zoom_start=6)

        for k in range(df1.shape[0]):
            lat, long = df1.loc[k, ['lat', 'long']]
            point = (lat, long) # (float(lat.replace(',', '.')), float(long.replace(',', '.')))
            #print(point)

            # création d'un bel affichage popup
            html = 'Heure : ' + str(df1.loc[k, 'hrmn']) + '<br>Gravité : ' + str(df1.loc[k, 'gravity']) + '<br>Sexe : ' + str(df1.loc[k, 'sexe']) + '<br>Situation : ' + str(df1.loc[k, 'situ'])  + '<br>Département : ' + str(df1.loc[k, 'dep']) + '<br>Commune : ' + str(df1.loc[k, 'com'])
            iframe = folium.IFrame(html,
                            width=200,
                            height=100)
            popup = folium.Popup(iframe,
                            max_width=200)
            
            # ajout du marker avec son popup personnalisé
            folium.Marker(
                location = point,
                popup = popup ,    
                icon=folium.Icon(color=dico_color[df1.loc[k, 'gravity']], prefix='fa',icon='bicycle')
                            ).add_to(dico_group[df1.loc[k,'gravity']])


        group_1.add_to(m_markers)
        group_2.add_to(m_markers)
        group_3.add_to(m_markers)
        group_4.add_to(m_markers)

        folium.LayerControl().add_to(m_markers)

        st_data_markers = st_folium(m_markers, width=725)
    

def page_predictions():

    st.write('Choisissez un exemple précis :')

    options = {'obs': {0: 'sans objet', 1 : 'Véhicule en stationnement', 2 : 'Arbre', 3 : 'Glissière métallique', 4 : 'Glissière béton', 5 : 'Autre glissière', 6 : 'Bâtiment, mur, pile de pont',
                             7 : 'Support de signalisation verticale ou poste d’appel d’urgence', 8 : 'Poteau', 9 : 'Mobilier urbain', 10 : 'Parapet', 11 : 'Ilot, refuge, borne haute',
                             12 : 'Bordure de trottoir', 13 : 'Fossé, talus, paroi rocheuse', 14 : 'Autre obstacle fixe sur chaussée', 15 : 'Autre obstacle fixe sur trottoir ou accotement',
                             16 : 'Sortie de chaussée sans obstacle', 17 : 'Buse – tête d’aqueduc'},
                'obsm':{0 : 'Aucun', 1 : 'Piéton', 2 : 'Véhicule', 4 : 'Véhicule sur rail', 5 : 'Animal domestique', 6 : 'Animal sauvage', 9 : 'Autre'},
                'choc': {0 : 'Aucun', 1 : 'Avant', 2 : 'Avant droit', 3 : 'Avant gauche', 4 : 'Arrière', 5 : 'Arrière droit', 6 : 'Arrière gauche', 7 : 'Côté droit', 8 : 'Côté gauche', 9 : 'Chocs multiples (tonneaux)'},
                'manv':{1 : 'Sans changement de direction', 2 : 'Même sens, même file', 3 : 'Entre 2 files', 4 : 'En marche arrière', 5 : 'A contresens', 6 : 'En franchissant le terre-plein central',
                              7 : 'Dans le couloir bus, dans le même sens', 8 : 'Dans le couloir bus, dans le sens inverse', 9 : 'En s’insérant', 10 : 'En faisant demi-tour sur la chaussée',
                              11 : 'Changeant de file à gauche', 12 : 'Changeant de file à droite', 13 : 'Déporté à gauche', 14 : 'Déporté à droite',  15 : 'Tournant à gauche', 16 :  'Tournant à droite',
                              17 : 'Dépassant à gauche', 18 : 'Dépassant à droite', 19 : 'Traversant la chaussée', 20 : 'Manœuvre de stationnement', 21 : 'Manœuvre d’évitement',
                              22 : 'Ouverture de porte', 23 : 'Arrêté (hors stationnement)', 24 : 'En stationnement (avec occupants)', 25 : 'Circulant sur trottoir', 26 : 'Autres manœuvres'},
                'catu': {1 : 'Conducteur', 2 : 'Passager', 3 : 'Piéton'},
                'secu1' : {0 : 'Aucun équipement', 1 : 'Ceinture', 2 : 'Casque', 3 : 'Dispositif enfants', 4 : 'Gilet réfléchissant', 5 : 'Airbag (2RM/3RM)', 6  : 'Gants (2RM/3RM)',
                             7 : 'Gants + Airbag (2RM/3RM)', 8 : 'Non déterminable',  9 : 'Autre'},
                'lum': {1 :'Plein jour', 2 :'Crépuscule ou aube', 3 : 'Nuit sans éclairage public', 4 : 'Nuit avec éclairage public non allumé', 5 : 'Nuit avec éclairage public allumé'},
                'agg': {1 : 'Hors agglomération', 2 : 'En agglomération'},
                'int': {1 : 'Hors intersection', 2 : 'Intersection en X', 3 : 'Intersection en T', 4 : 'Intersection en Y', 5 : 'Intersection à plus de 4 branches', 6 : 'Giratoire', 7 : 'Place', 8 : 'Passage à niveau', 9 : 'Autre intersection'},
                'atm' : {1  : 'Normale', 2 : 'Pluie légère', 3 : 'Pluie forte', 4 : 'Neige - grêle', 5 : 'Brouillard - fumée', 6 : 'Vent fort - tempête', 7 : 'Temps éblouissant', 8 : 'Temps couvert', 9 : 'Autre'},
                'col': {1 : 'Deux véhicules - frontale', 2 : 'Deux véhicules – par l’arrière', 3 : 'Deux véhicules – par le coté', 4 : 'Trois véhicules et plus – en chaîne', 5 : 'Trois véhicules et plus - collisions multiples', 6 : 'Autre collision', 7 : 'Sans collision' },
                'catr': {1:'Autoroute', 2: 'Route nationale', 3:'Route Départementale', 4:'Voie Communale', 5:'Hors réseau public', 6:'Parc de stationnement ouvert à la circulation publique', 7:'Routes de métropole urbaine', 9:'autre'},
                'circ':{1:'Sens unique', 2:'Bidirectionnelle', 3:'À chaussées séparées', 4:'Voies d\'affectation variable'},
                'prof': {1:'Plat', 2:'Pente', 3 :'Sommet de côte', 4:'Bas de côte'},
                'plan': {1 :'Partie rectiligne', 2:'En courbe à gauche', 3:'En courbe à droite', 4:'En « S »'},
                'surf': {1:'Normale', 2:'Mouillée', 3:'Flaques', 4 :'Inondée', 5:'Enneigée', 6:'Boue', 7:'Verglacée', 8:'Corps gras – huile', 9 :'Autre'},
                'infra':{0 :'Aucun', 1:'Souterrain - tunnel' , 2:'Pont - autopont', 3: 'Bretelle d’échangeur ou de raccordement', 4: 'Voie ferrée', 5:'Carrefour aménagé', 6 :'Zone piétonne', 7 :'Zone de péage', 8:'Chantier', 9 :'Autres'},
                 'situ':{1:'Sur chaussée',  2:'Sur bande d’arrêt d’urgence', 3:'Sur accotement', 4:'Sur trottoir', 5:'Sur piste cyclable', 6:'Sur autre voie spéciale'}
                 }
    
    for k in options.keys():
        if k not in st.session_state:
            st.session_state[k] = None
        list_options = [str(nb)+' - ' + str(v) for nb,v in options[k].items()]
        st.session_state[k] = st.selectbox(k, list_options, index=0)

    if "run_function" not in st.session_state:
        st.session_state.run_function = False  # Flag pour exécuter la fonction


    df_cyclistes_seuls = df_cyclistes_all 

    



    # les features intéressantes
    features_cat = ['obs', 'obsm', 'choc', 'manv', 'catu', 'secu1', 'lum', 'agg', 'int', 'atm',
             'col', 'catr', 'circ', 'prof', 'plan', 'surf', 'infra', 'situ', ]
    features_total = features_cat + ['nbv', 'vma']

    # encodage en catégories
    df_encoded = pd.get_dummies(df_cyclistes_seuls[features_total],columns=features_cat)
    # y = df_cyclistes_seuls['gravity']
    
    # Normalisation des features
    standard_scaler = StandardScaler()
    X_scaled = pd.DataFrame(standard_scaler.fit_transform(df_encoded), columns=df_encoded.columns)
    
    # Target en 2 catégories uniquement
    y2 = df_cyclistes_seuls['gravity'].apply(lambda x : 'grave' if x in ("Blessé hospitalisé", "Tué") else 'léger')

   
    # Train test split
    X_train2, X_test2, y_train2, y_test2 = train_test_split(X_scaled, y2, random_state=36, train_size = 0.8, stratify=y2)

    
    # Modèle
    model_rfc = RandomForestClassifier(random_state=36)

    # Entraîner le modèle sur les données d'entraînement.
    model_rfc.fit(X_train2, y_train2)

    # Faire des prédictions sur les ensembles d'entraînement et de test.
    # y_train_pred2 = model_rfc.predict(X_train2)
    # y_test_pred2 = model_rfc.predict(X_test2)

    # Calculer et afficher la précision (accuracy) sur les deux ensembles.
    # print('Précision sur l\'ensemble d\'entraînement : ', accuracy_score(y_train2, y_train_pred2))
    # print('Précision sur l\'ensemble de test : ', accuracy_score(y_test2, y_test_pred2))

    # HTML(pd.DataFrame(confusion_matrix(y_test2, y_test_pred2),
    #            index = model_rl.classes_ + " REAL",
    #            columns = model_rl.classes_ + " PREDICTED").to_html())

    if st.button("Exécuter la prédiction"):
        st.session_state.run_function = True 

    if st.session_state.run_function:
        result = prediction_simple(model_rfc, features_cat,  df_encoded.columns, standard_scaler,
                                    st.session_state['obs'],
                                    st.session_state['obsm'],
                                    st.session_state['choc'],
                                    )
        dico_result = {'grave' : 'dans un état grave ou tuée', 'léger' : 'indemne ou blessé léger'}
        st.write("La personne se retrouvera " + dico_result[result])
        st.session_state.run_function = False  # Reset du flag après exécution
    

def prediction_simple(modele, features_cat, cols, normalisation, obs, obsm, choc ):
    data_cycl = {'obs':[obs], 'obsm':[obsm], 'choc': [choc], 'manv':[1], 'place':[1], 'catu':[1], 'secu1':[2], 'lum':[1],
             'agg':[1], 'int': [1], 'atm':[1], 'col':[7], 'catr':[3], 'circ':[2], 'prof':[1], 'plan':[1],
             'surf':[1], 'infra':[0], 'situ':[1], 'nbv':[1], 'vma':[80]}
    X_cycl = pd.DataFrame(data=data_cycl, index=[0])
    X_cycl_encoded= pd.get_dummies(X_cycl, columns=features_cat)

    # Get missing columns in the training test
    missing_cols = set( cols ) - set( X_cycl_encoded.columns )
    # Add a missing column in test set with default value equal to 0
    for c in missing_cols:
        X_cycl_encoded[c] = False
    # Ensure the order of column in the test set is in the same order than in train set
    X_cycl_encoded = X_cycl_encoded[cols]
   
    X_cycl_scaled = pd.DataFrame(normalisation.transform(X_cycl_encoded), columns=X_cycl_encoded.columns)

    y_cycl_predict = modele.predict(X_cycl_scaled)

    return str(y_cycl_predict[0])
    # st.write('je te prédis une gravité = ', str(y_cycl_predict[0]))



accueil()