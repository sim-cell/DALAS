# PROJET DALAS
## Dashboard
### Aylin Soykok et Simay Celik
### Encadrants : Laure Souiler et Nicolas Baskiotis

#!pip install --quiet dash   ##uncomment if needed
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px

import pandas as pd


app = Dash()


data = pd.read_csv('../data/data_annees.csv')
filtered_data = data[['Country', 'Year', 'Quality of Life Index', 'Purchasing Power Index','Pollution Index', 'Climate Index']].copy()
#curse de csv, remettre les valeurs numériques
filtered_data['Quality of Life Index'] = pd.to_numeric(filtered_data['Quality of Life Index'], errors='coerce')
filtered_data['Pollution Index'] = pd.to_numeric(filtered_data['Pollution Index'], errors='coerce')
filtered_data['Climate Index'] = pd.to_numeric(filtered_data['Climate Index'], errors='coerce')
filtered_data['Purchasing Power Index'] = pd.to_numeric(filtered_data['Purchasing Power Index'], errors='coerce')
filtered_data.dropna(subset=['Pollution Index', 'Climate Index','Quality of Life Index','Purchasing Power Index'], inplace=True)

fast_fashion_data = pd.read_pickle('../data/fastfashion_clean.pkl')
slow_fashion_data = pd.read_pickle('../data/slowfashion_clean.pkl')

app.layout = html.Div(style = {'font-family':'Arial'}, children=[
    html.H1("La Pollution et les Effets de la Mode Ephémère (Fast Fashion) sur l'Environnement et les Humains Dashboard"),
    html.H2("Projet DALAS de Aylin et Simay"),
    html.Div(children=[
        html.Label("Choisir l'indice à afficher :"),
        dcc.RadioItems(
            id='index-radio',
            options=[
                {'label': 'Indice de Pollution', 'value': 'Pollution Index'},
                {'label': 'Indice du Climat', 'value': 'Climate Index'},
                {'label': 'Indice de Qualité de la Vie', 'value': 'Quality of Life Index'},
                {'label': 'Indice du Pouvoir d\'Achat', 'value': 'Purchasing Power Index'}
            ],
            value='Pollution Index'
        ),
        html.Br(),
        html.Div(id='map-container', style={'width': '45%', 'float': 'left','margin-right': '2%','border': '1px solid black', 'padding': '2px'}, children=[
            html.H2("Carte du Monde Selon l'Environnement et les Conditions des Pays par Année"),
            html.Label("Choisir une année :"),
            dcc.Slider(
                id='year-slider',
                min=filtered_data['Year'].min(),
                max=filtered_data['Year'].max(),
                value=filtered_data['Year'].min(),
                marks={str(year): str(year) for year in filtered_data['Year'].unique()},
                step=None
            ),
            html.Div(id='index-slider-container', children=[
                html.Label("Set Index Value Range:"),
                dcc.RangeSlider(
                    id='index-slider',
                    marks={}, 
                    min=filtered_data['Pollution Index'].min(),
                    max=filtered_data['Pollution Index'].max(),
                    value=[filtered_data['Pollution Index'].min(), filtered_data['Pollution Index'].max()],  
                    step=1)
                ]
            ),
            dcc.Graph(id='map-graph')
        ]),
        html.Div(id='graph-container', style={'width': '45%', 'float': 'right', 'margin-left':'2%','border': '1px solid black', 'padding': '2px'}, children=[
            html.H2("Graphe des valeurs d'indice au cours des années par pays"),
            html.Label("Choisir le pays :"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in filtered_data['Country'].unique()],
                value=['France', 'Bangladesh', 'Turkey', 'America', 'China'],
                multi=True
            ),
            dcc.Graph(id='index-graph')
        ])
    ])
 ])


# we need to callbact to update the slider (or anything update-able tbh)
#each output is something that is returned in an update function
@app.callback(
    [Output('map-graph', 'figure'),
     Output('index-slider', 'min'),
     Output('index-slider', 'max'),
     Output('index-slider', 'marks'),
     Output('index-slider', 'value')],
    [Input('year-slider', 'value'),
     Input('index-radio', 'value'),
     Input('index-slider', 'value')]
)


def update_map(selected_year, selected_index, slider_value):
    year_data = filtered_data[filtered_data['Year'] == selected_year]

    min_val = year_data[selected_index].min()
    max_val = year_data[selected_index].max()

    filtered_year_data = year_data[(year_data[selected_index] >= slider_value[0]) & (year_data[selected_index] <= slider_value[1])]

    fig = px.choropleth(filtered_year_data, locations="Country",
                        locationmode='country names',
                        color=selected_index,
                        hover_name="Country",
                        hover_data={'Country': False, selected_index: True},
                        #normalement on doit mettre le titre en francais mais j'ai vraiment pas envie
                        title=f'{selected_index} dans {selected_year}',
                        color_continuous_scale=px.colors.sequential.YlOrRd)
    
    fig.update_layout(geo=dict(showframe=False, showcoastlines=False))

    marks = {int(val): str(int(val)) for val in range(int(min_val), int(max_val)+1, (int(max_val)-int(min_val)) // 10)}

    return fig, min_val, max_val, marks, slider_value

@app.callback(
    Output('index-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('index-radio', 'value')]
)
def update_index_graph(selected_countries, selected_index):
    filtered_country_data = filtered_data[filtered_data['Country'].isin(selected_countries)]

    fig = px.line(filtered_country_data, x='Year', y=selected_index, color='Country', title=f'{selected_index} Au Cours des Années')

    return fig



#this thing just runs the app
if __name__ == '__main__':
    app.run_server(debug=True)
