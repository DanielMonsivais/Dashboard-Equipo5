import dash
import dash_core_components as ddc
import dash_html_components as html
import plotly.express as px
import pandas as pd
# Aplicacion principal
app = dash.Dash(__name__)
server = app.server

colors = {
    'background': "#C9DDD3",
    'text': "#000000"
}

# Datos de pandas
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
df_2 = px.data.election()

# Graficas de plotly
fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='stack')
fig_2 = px.scatter_3d(df_2, x="Joly", y="Coderre", z="Bergeron", color="winner", size="total", hover_name="district",
                      symbol="result", color_discrete_map = {"Joly": "blue", "Bergeron": "green", "Coderre":"red"})

##############################################################################

import folium
import geopandas as gpd 

state_data=pd.read_csv('https://raw.githubusercontent.com/DanielMonsivais/PRUEBAM/main/dataset/Tasa%20de%20Obesidad%202018.csv')
state_data=state_data.replace({"Coahuila de Zaragoza": "Coahuila","Michoacán de Ocampo":"Michoacán","Veracruz de Ignacio de la Llave":"Veracruz"})
state_geo ='https://raw.githubusercontent.com/DanielMonsivais/PRUEBAM/main/mexico.json'

data_geo = gpd.read_file(state_geo)
data_geo = data_geo.rename(columns={'name':'Entidad'})
geo=data_geo.merge(state_data,on="Entidad")

#Ubicación de México en el mapa
m = folium.Map(location=[24, -102], zoom_start=5, width='70%', height='70%',tiles='Stamen Watercolor')
#Tiles [OpenStreetMap, Mapbox Bright, Mapbox Control Room, Stamen Terrain, Stamen Toner, Stamen Watercolor, CartoDB positron, CartoDB dark_matter]


#Mapa Coroplético de la tasa de obesidad 

folium.Choropleth(
    geo_data=state_geo,
    name='Tasa de Obesidad',
    data=state_data,
    columns=['Entidad', 'Tasa de obesidad'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.4,
    legend_name='Tasa de Obesidad'
).add_to(m)

style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.7, 
                                'weight': 0.1}
NIL = folium.features.GeoJson(
    geo,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['Entidad','Tasa de obesidad'],
        aliases=['Estado: ','Tasa de obesidad: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
m.add_child(NIL)
m.keep_in_front(NIL)
folium.LayerControl().add_to(m)

loc = 'Tasa de Obesidad'
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(loc) 

m.get_root().html.add_child(folium.Element(title_html))

m.save('map-with-title.html')

##############################################################################




# Layout HTML
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children='Dashboard Prueba',
           style={
            'textAlign': 'center',
            'color': colors['text']
        }),
     dcc.Markdown(children="""
    En México, así como en el mundo, las defunciones causadas por enfermedades cardiovasculares (ECV) han ocupado el primer lugar entre las 
    principales causas durante varios años, entre ellas, destacan las enfermedades isquémicas del corazón que presentan una alta incidencia 
    entre la población que fallece a partir de los 45 años.
    Entre los factores de riesgo que se asocian con la enfermedad coronaria se tiene: la edad, sexo, tabaquismo, diabetes, hipertensión 
    arterial, obesidad, sobrepeso y sedentarismo.
    """, style={
        'color': colors['text']
    }),
    html.Iframe(id='map', srcDoc=open('map-with-title.html','r').read(),width='100%', height='600'),
    ddc.Graph(id='example-graph', figure=fig),
    ddc.Graph(id='example-3d', figure=fig_2)
])

if __name__ == '__main__':
    app.run_server(debug=True)
