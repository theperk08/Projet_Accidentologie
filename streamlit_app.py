import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from streamlit_option_menu import option_menu

rep_images = "images/"
rep_data = "data/"

df_cyclistes = pd.read_csv(rep_data+"df_cyclistes_2023.csv", sep=";")

# st.dataframe(df_cyclistes)



def accueil():
      # Using object notation
    # Le bouton de déconnexion    
    
    # Using "with" notation

    with st.sidebar:        
        st.write(f"Bienvenue",)
        selection = option_menu(
            menu_title=None,
            options=["Accueil", "Visualisations des statistiques"]

        )

    
    
    if selection == "Accueil":
        st.write('Bienvenue')
        #st.image(rep_images+"home.jpg")
    elif selection == "Visualisations des statistiques":
        visu()
  
df_max = df_cyclistes[df_cyclistes['catv'].isin([1, 80])].groupby('id_usager', as_index=False).max()
df_first = df_cyclistes[df_cyclistes['catv'].isin([1, 80])].groupby('id_usager', as_index=False).first()

def visu():
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
                        title = dict(font=dict(size=15), x=0.5)
                        )

    fig2.update_layout(title='% Gravité Cyclistes par ' + option)
    st.plotly_chart(fig2)

    
accueil()