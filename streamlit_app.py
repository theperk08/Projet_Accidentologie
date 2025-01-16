import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from streamlit_option_menu import option_menu

rep_images = "images/"
rep_data = "data/"

df_cyclistes = pd.read_csv(rep_data+"df_cyclistes_2023.csv", sep=";")

df_max = df_cyclistes[df_cyclistes['catv'].isin([1, 80])].groupby('id_usager', as_index=False).max()
df_first = df_cyclistes[df_cyclistes['catv'].isin([1, 80])].groupby('id_usager', as_index=False).first()
df_nb_vehicules = df_cyclistes.groupby('Num_Acc', as_index=False)['id_vehicule'].nunique()
vehicule_multiple = list(df_nb_vehicules[df_nb_vehicules['id_vehicule']>1]['Num_Acc'].unique())
cycliste_seul = list(df_nb_vehicules[df_nb_vehicules['id_vehicule']==1]['Num_Acc'].unique())


def accueil():
      # Using object notation
    # Le bouton de déconnexion    
    
    # Using "with" notation

    with st.sidebar:        
        st.write(f"Bienvenue",)
        selection = option_menu(
            menu_title=None,
            options=["Accueil", "Choix Visu Statistiques"]

        )

    
    
    if selection == "Accueil":
        st.write('Bienvenue')
        page_accueil()

        #st.image(rep_images+"home.jpg")
    elif selection == "Choix Visu Statistiques":
        page_visu()  


def page_accueil():
    
    # cyclistes
    st.header("Statistiques 2023 sur la gravité des accidents corporels de la circulation impliquant des cyclistes (accidents enregistrés en France, outre-mer compris)")
    
    # cyclistes sans autre véhicule
    
    df1 = df_cyclistes[(df_cyclistes['Num_Acc'].isin(cycliste_seul)) & (df_cyclistes['catv'].isin([1, 80]))].groupby('id_usager', as_index=False).first()

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
    
    df2 = df_cyclistes[(df_cyclistes['Num_Acc'].isin(vehicule_multiple)) & (df_cyclistes['catv'].isin([1, 80]))].groupby('id_usager', as_index=False).first()

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
    df3 = df_cyclistes[~df_cyclistes['catv'].isin([1, 80])].groupby('id_usager', as_index=False).first()

    
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
    
    vars = {'jour de la semaine': {'df':df_max, 'x': 'day_of_week', 'tickvals': [0,1,2,3,4,5,6], 'ticktext': ['Lundi','Mardi','Mercredi',  'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']},
             'sens de la circulation' : {'df': df_first, 'x': 'circ', 'tickvals': [-1, 1,2,3,4], 'ticktext': ['Non renseigné', 'A sens unique','Bidirectionnelle','A chaussées séparées',  'Avec voies d’affectation variable']},
             'condition de surface': {'df': df_first, 'x': 'surf', 'tickvals': [-1, 1,2,3,4,5,6,7,8,9], 'ticktext': ['Non renseigné','Normale', 'Mouillée', 'Flaques', 'Inondée', 'Enneigée', 'Boue', 'Verglacée', 'Corps gras – huile', 'Autre']},
             'type d\'infrastructure':{'df': df_first, 'x': 'infra', 'tickvals': [-1, 0,1,2,3,4,5,6,7,8,9], 'ticktext': ['Non renseigné', 'Aucun', 'Souterrain - tunnel', 'Pont - autopont', 'Bretelle d’échangeur ou de raccordement', 'Voie ferrée', 'Carrefour aménagé', 'Zone piétonne', 'Zone de péage', 'Chantier', 'Autres']},
            }
    option = st.selectbox(
            "Quel variable veux-tu visualiser ?",
            vars.keys(),
            index=0,
        )


    
    fig1 = px.histogram(vars[option]['df'], x=vars[option]['x'],
                        color='gravity',
                        color_discrete_map={'Indemne': 'green', 'Blessé léger': 'orange', 'Blessé hospitalisé': 'red', 'Tué': 'black' },
                        category_orders={'gravity': ['Indemne', 'Blessé léger', 'Blessé hospitalisé', 'Tué']},
                        # barnorm='percent',
                        text_auto=False)

    fig1.update_xaxes(tickmode="array", tickvals=vars[option]['tickvals'], ticktext=vars[option]['ticktext'])

    fig1.update_layout(width=800, height=400,
                       yaxis_title="Nombre",
                        # xaxis_title="Jour",
                        xaxis_title=None,
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


    fig2.update_xaxes(tickmode="array", tickvals=vars[option]['tickvals'], ticktext=vars[option]['ticktext'])

    fig2.update_layout(width=800, height=400,
                        yaxis_title="%",
                        # xaxis_title="Jour",
                        xaxis_title=None,
                        showlegend=True,
                        legend_title_text="",
                        title = dict(font=dict(size=15), x=0.5)
                        )

    fig2.update_layout(title='% Gravité Cyclistes par ' + option)
    st.plotly_chart(fig2)

    
accueil()