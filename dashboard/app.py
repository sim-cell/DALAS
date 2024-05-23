# PROJET DALAS
## Dashboard
### Aylin Soykok et Simay Celik
### Encadrants : Laure Souiler et Nicolas Baskiotis

##uncomment if needed
#!pip install --quiet dash  
#!pip install --quiet plotly
#!pip install --quiet pandas

from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd



app = Dash()

#basically redoing eda because sinon on doit sauvegarder tous les dataframes obtenus
#YEARS DATA 
data = pd.read_csv('../data/data_annees.csv')

filtered_data = data[['Country', 'Year', 'Quality of Life Index', 'Purchasing Power Index','Pollution Index', 'Climate Index']].copy()
#curse de csv, remettre les valeurs numériques
filtered_data['Quality of Life Index'] = pd.to_numeric(filtered_data['Quality of Life Index'], errors='coerce')
filtered_data['Pollution Index'] = pd.to_numeric(filtered_data['Pollution Index'], errors='coerce')
filtered_data['Climate Index'] = pd.to_numeric(filtered_data['Climate Index'], errors='coerce')
filtered_data['Purchasing Power Index'] = pd.to_numeric(filtered_data['Purchasing Power Index'], errors='coerce')
filtered_data.dropna(subset=['Pollution Index', 'Climate Index','Quality of Life Index','Purchasing Power Index'], inplace=True)

#FASHION DATA 
fashion_data = pd.read_pickle('../apprentissage/base.pkl')
fast_fashion_data = fashion_data[fashion_data['Brand Type'] == 'Fast Fashion']
nb_fast_fashion = fast_fashion_data.shape[0]
slow_fashion_data = fashion_data[fashion_data['Brand Type'] == 'Slow Fashion']
nb_slow_fashion = slow_fashion_data.shape[0]



app.layout = html.Div(style = {'font-family':'Arial','background-color': '#D8BFD8'}, children=[
    html.Div(id="header",children=[
    html.H1("La Pollution et les Effets de la Mode Ephémère (Fast Fashion) sur l'Environnement et les Humains Dashboard"),
    html.H2("Projet DALAS de Aylin et Simay"),
    html.Div("La mode ephémère est un créateur de pollution mais ses effets étaient souvent ignorés jusqu'à le mouvement de mode durable. Les conditions de travail dans ce secteur ne sont pas les meilleurs non plus. Dans ce dashboard, nous allons\
                  découvrir comment les indices de la qualité de vie varient au cours des années et comparer les deux types de mode."),     
    ]),
    html.Br(),
    html.Div(id="annees",style = {'border-top': '4px solid #4B0082', 'padding': '3px'},children=[
        html.H2("Données sur la pollution et les conditions de vie par année et par pays"),
        html.A("Les données sont issues de Numbeo et sont disponibles sur leur site.", href="https://www.numbeo.com/quality-of-life/rankings_by_country.jsp?title=2014"),
        html.Br(),
        html.Br(),
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
        html.Div(id='annees-container', style={'width': '100%','height':'30%','overflow': 'auto'}, children=[
            html.Div(id='map-container', style={'width': '48%','float': 'left','margin-left': '1%','border': '1px solid black', 'padding': '2px'}, children=[
                html.H3("Carte du Monde Selon l'Environnement et les Conditions des Pays par Année"),
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
                dcc.Graph(id='map-graph'),
            ]),
            html.Div(id='graph-container', style={'width': '48%', 'float': 'right', 'margin-right':'1%','border': '1px solid black', 'padding': '2px'}, children=[
                html.H3("Graphe des valeurs d'indice au cours des années par pays"),
                html.Label("Choisir le pays :"),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': country, 'value': country} for country in filtered_data['Country'].unique()],
                    value=['France', 'Bangladesh', 'Turkey', 'America', 'China'],
                    multi=True
                ),
                dcc.Graph(id='index-graph')
            ]),
        ]),
        html.Br()
    ]),
    html.Br(),
    html.Div(id="fashion",style = {'border-top': '4px solid #4B0082', 'padding': '3px'},children=[
        html.H2("La Mode :  Rapide vs Durable"),
        html.A("Données de la mode rapide sont obtenus à partir de H&M France", href="https://www2.hm.com/fr_fr/femme.html"),
        html.Br(),
        html.A("Données de la mode durable sont obtenus à partir de Everlane",href="https://www.everlane.com/womens"),
        html.Div(f"Dans cette partie, on se concentre sur les différences entre les deux types de mode. Y-a-t-il une différence de prix? Quels sont les matériaux utilisés?\
                 Tout d'abord, il y a une différence entre le nombre de produit obtenu de chaque marque, cela peut nous indiquer qu'il y a une difference entre la masse de production.\
                 Nous nous basons nos analyses sur trois types de produits, des hauts, des jeans et des pantalons."),
        html.Br(),
        html.Div(id="basic-stats", style={'width': '100%','height':'30%','overflow': 'auto'}, children=[
            html.Div(id="total-products",style={'width': '48%','float': 'left','margin-left': '1%','border': '1px solid black', 'padding': '2px'}, children=[
                dcc.Graph(id='total-products-graph')
            ]),
            html.Div(id="prices", style={'width': '48%','float': 'right','margin-right': '1%','border': '1px solid black', 'padding': '2px'},children=[
                dcc.Graph(id='price-comparison-graph')
            ]),
        ]),
        html.Br(),
        html.Div("Les  diagramme en camembert montrent les 10 matériaux les plus utilisés dans chaque type de mode. La mode durable et la mode rapide possèdent 20 et 32 matériaux uniques réspectivement. "),
        html.Br(),
        html.Div(id='material-stats',style={'overflow': 'auto'}, children=[
            html.Div(id="fast-mat",style={'width': '48%','float': 'left','margin-left': '1%','border': '1px solid black', 'padding': '2px'}, children=[
                dcc.Graph(id='fast-fashion-materials-graph'),
            ]),
            html.Div(id="slow-mat", style={'width': '48%','float': 'right','margin-right': '1%','border': '1px solid black', 'padding': '2px'},children=[
                dcc.Graph(id='slow-fashion-materials-graph')
            ]),
        ]),
        html.Br(),
        html.Div("Les pays de fabrication des produits sont aussi importants. Les histogrammes montrent les 20 pays les plus fréquents dans chaque type de mode."),
        html.Br(),
        html.Div(id='countriesstats',style={'overflow': 'auto'}, children=[
            html.Div(id="fast-mat",style={'width': '48%','float': 'left','margin-left': '1%','border': '1px solid black', 'padding': '2px'}, children=[
                dcc.Graph(id='fast-fashion-countries-graph'),
            ]),
            html.Div(id="slow-mat", style={'width': '48%','float': 'right','margin-right': '1%','border': '1px solid black', 'padding': '2px'},children=[
                dcc.Graph(id='slow-fashion-countries-graph')
            ]),
        ]),
          
    ])
       
 ])


# we need to callbact to update the slider (or anything update-able tbh)
#each output is something that is returned in an update function
@app.callback(
    [Output('map-graph', 'figure'),
     Output('index-slider', 'min'),
     Output('index-slider', 'max'),
     Output('index-slider', 'marks'),
     Output('index-slider', 'value'),
     Output('index-graph', 'figure'),
     Output('price-comparison-graph', 'figure'),
     Output('total-products-graph', 'figure'),
     Output('fast-fashion-materials-graph', 'figure'),
     Output('slow-fashion-materials-graph', 'figure'),
     Output('fast-fashion-countries-graph', 'figure'),
     Output('slow-fashion-countries-graph', 'figure'),
     ],
    [Input('year-slider', 'value'),
     Input('index-radio', 'value'),
     Input('index-slider', 'value'),
     Input('country-dropdown', 'value')]
)


def update_everything(selected_year, selected_index, slider_value, selected_countries):
    # map
    year_data = filtered_data[filtered_data['Year'] == selected_year]

    min_val = year_data[selected_index].min()
    max_val = year_data[selected_index].max()

    filtered_year_data = year_data[(year_data[selected_index] >= slider_value[0]) & (year_data[selected_index] <= slider_value[1])]

    fig1 = px.choropleth(filtered_year_data, locations="Country",
                        locationmode='country names',
                        color=selected_index,
                        hover_name="Country",
                        hover_data={'Country': False, selected_index: True},
                        #normalement on doit mettre le titre en francais mais j'ai vraiment pas envie
                        title=f'{selected_index} dans {selected_year}',
                        color_continuous_scale=px.colors.sequential.YlOrRd)
    
    fig1.update_layout(geo=dict(showframe=False, showcoastlines=False))

    marks = {int(val): str(int(val)) for val in range(int(min_val), int(max_val)+1, (int(max_val)-int(min_val)) // 10)}

    ## graphe au cours des années
    filtered_country_data = filtered_data[filtered_data['Country'].isin(selected_countries)]

    fig2 = px.line(filtered_country_data, x='Year', y=selected_index, color='Country', title=f'{selected_index} Au Cours des Années')

    ## comparaison des prix
    average_price_per_item_type_fast = fast_fashion_data.groupby('Product Type')['Price'].mean()
    average_price_per_item_type_slow = slow_fashion_data.groupby('Product Type')['Price'].mean()

    fig3 = go.Figure(data=[
        go.Bar(name='Fast Fashion', x=average_price_per_item_type_fast.index, y=average_price_per_item_type_fast.values),
        go.Bar(name='Slow Fashion', x=average_price_per_item_type_slow.index, y=average_price_per_item_type_slow.values)
    ])

    fig3.update_layout(barmode='group', title='Comparaison des Prix Moyen', xaxis_title='Type de Produit', yaxis_title='Prix Moyen')

    ## comparison in mass
    total_fast_fashion = len(fast_fashion_data)
    total_slow_fashion = len(slow_fashion_data)

    fig4 = go.Figure(data=[
        go.Bar(name='Fast Fashion', x=['Total Products'], y=[total_fast_fashion]),
        go.Bar(name='Slow Fashion', x=['Total Products'], y=[total_slow_fashion])
    ])

    fig4.update_layout(barmode='group', title='Nombre Total des Produits', yaxis_title='Nombre de Produits')

    #materials
    material_counts_fast_fashion = fast_fashion_data['Materials'].explode().value_counts()[:10]
    material_counts_slow_fashion = slow_fashion_data['Materials'].explode().value_counts()[:10]
    fig5 = go.Figure(data=[
        go.Pie(labels=material_counts_fast_fashion.index, values=material_counts_fast_fashion.values)
    ])

    fig5.update_layout(title='Top 10 Matériaux dans Mode Rapide')
    fig6 = go.Figure(data=[
        go.Pie(labels=material_counts_slow_fashion.index, values=material_counts_slow_fashion.values)
    ])

    fig6.update_layout(title='Top 10 Matériaux dans Mode Durable')

    #countries
    country_counts_fast_fashion = fast_fashion_data['Country'].explode().value_counts()[:20]
    country_counts_slow_fashion = slow_fashion_data['Country'].explode().value_counts()[:20]
    fig7 = go.Figure(data=[
        go.Bar(x=country_counts_fast_fashion.index, y=country_counts_fast_fashion.values),
    ])

    fig7.update_layout(title='Top 20 Pays de Fabrication - Mode Rapide')
    fig8 = go.Figure(data=[
        go.Bar(x=country_counts_slow_fashion.index, y=country_counts_slow_fashion.values),
    ])

    fig8.update_layout(title='Pays de Fabrication - Mode Durable')

    fig9 = px.box(fashion_data, x="Brand Type", y="Price")
    fig9.update_layout(title='Comparaison des Prix')
    norm_fashion_data = fashion_data.copy()

    return fig1, min_val, max_val, marks, slider_value, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9




#this thing just runs the app
if __name__ == '__main__':
    app.run_server(debug=True)
