import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
# Aplicacion principal
app = dash.Dash(__name__)
server = app.server

colors = {
    'background': "#C9DDD3",
    'text': "#000000",
    'sub': "#8C8888",
}



##############################################################################
#MAPA Porcentajes de Prevalencia de Enfermedades  
import folium
import geopandas as gpd 

state_geo ='https://raw.githubusercontent.com/angyf/proyecto/main/mexico.json'
data_geo = gpd.read_file(state_geo)
data_geo = data_geo.rename(columns={'name':'Entidad'})


df=pd.read_csv('https://raw.githubusercontent.com/angyf/proyecto/main/Datos-porcentaje-poblacion-mayor-20.csv',index_col=0)
df=df.replace({"Coahuila de Zaragoza": "Coahuila","Michoacán de Ocampo":"Michoacán","Veracruz de Ignacio de la Llave":"Veracruz", "Querétaro de Arteaga":"Querétaro"})
geo_porc=data_geo.merge(df,on="Entidad")
#Se crea el mapa, añadiendo las coordenadas de la ubicación de México
m = folium.Map(location=[24, -102], zoom_start=5, width='100%', height='100%',tiles='Stamen Watercolor')

#Se crean los Mapas Coropléticos, manejando el geojson de forma separada

#Layer o capa que muestra los porcentajes de Obesidad
folium.Choropleth(
    geo_data=state_geo,
    name='Obesidad',
    data=df,
    columns=['Entidad', 'Obesidad'],
    key_on='feature.properties.name',
    fill_color='YlGn',
    fill_opacity=1,
    line_opacity=0.4,
    legend_name='Obesidad'
).add_to(m)

#Layer o capa que muestra los porcentajes de Hipertensión
folium.Choropleth(
    geo_data=state_geo,
    name='Hipertensión',
    data=df,
    columns=['Entidad', 'Diagnóstico previo de hipertensión'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=1,
    line_opacity=0.4,
    legend_name='Hipertensión'
).add_to(m)

#Layer o capa que muestra los porcentajes de Diabetes
folium.Choropleth(
    geo_data=state_geo,
    name='Diabetes',
    data=df,
    columns=['Entidad', 'Diagnóstico previo de diabetes'],
    key_on='feature.properties.name',
    fill_color='RdPu',
    fill_opacity=1,
    line_opacity=0.4,
    legend_name='Diabetes'
).add_to(m)


#Se crea la función con el dataframe que contiene todos los datos
#Se selecciona la información a mostrar y las etiquetas, así como su estilo

style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.7, 
                                'weight': 0.1}

NIL = folium.features.GeoJson(
    geo_porc,
    style_function=style_function,
    overlay=True, 
    show=True,
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['Entidad','Obesidad','Diagnóstico previo de hipertensión','Diagnóstico previo de diabetes'],
        aliases=['Entidad: ','Obesidad: ','Hipertensión: ','Diabetes: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
m.add_child(NIL)
m.keep_in_front(NIL)



#Se añade un título
loc = 'Porcentajes de Prevalencia de enfermedades 2018.'
title_html = '''
            <h3 style="font-size:20px"><b>{}</b></h3><br>
             '''.format(loc)
m.get_root().html.add_child(folium.Element(title_html))

#Se quitan los botones de zoom para que no se empalmen con las leyendas
m.zoom_control=False
m.objects_to_stay_in_front

#Se añade la opción para cambiar entre las capas del mapa
folium.LayerControl().add_to(m)

m.save('map-porcentajes.html')


##############################################################################
#Código para obtener el csv a través de la API
#irecc=pd.read_csv('https://raw.githubusercontent.com/angyf/proyecto/main/Direcciones.csv')
#from geopy.geocoders import Bing
#geolocator = Bing("AhzzZWFo6COn8x2J_HbNv6eancFFyXmgCqU9LEJ5Emsk1yW2flEZpbF2-oMNgVxN")

#longitud=[]
#latitud=[]
#for i in direcc.index: 
#     location = geolocator.geocode(direcc['Dirección'][i])
#     lat=[location.latitude]
#     lon=[location.longitude]
#     longitud.append(lon)
#     latitud.append(lat)

#longit=[]
#for i in range(0,len(longitud)):
#  longit.append(longitud[i][0])

#latit=[]
#for i in range(0,len(latitud)):
#  latit.append(latitud[i][0])

#direcc['longitud']=longit
#direcc['latitud']=latit
#direcc.to_csv('Direcc-coord.csv')

##############################################################################
#Mapa Defunciones
data=pd.read_csv('https://raw.githubusercontent.com/angyf/proyecto/main/Tasa_Mortalidad_Cardiovascular_Serie_Historica.csv')

data=data.replace({"Coahuila de Zaragoza": "Coahuila", "Distrito Federal": "Ciudad de México","Michoacán de Ocampo":"Michoacán","Veracruz Llave":"Veracruz", "Querétaro de Arteaga":"Querétaro"})
data= data.rename(columns={'Entidad de Residencia':'Entidad'})
data=data[data['Entidad']!="Nacional"]

data_2013=data[data['Periodo']==2013]
geo_2013=data_geo.merge(data_2013,on="Entidad")


direcc=pd.read_csv('https://raw.githubusercontent.com/angyf/proyecto/main/Direcc-coord.csv')

#Se crea el mapa de igual forma al anterior

n = folium.Map(location=[24, -102], zoom_start=5, width='100%', height='100%')

folium.Choropleth(
    geo_data=state_geo,
    name='2013',
    data=data_2013,
    columns=['Entidad', 'Defunciones por Enfermedades Cardiovasculares'],
    key_on='feature.properties.name',
    fill_color='RdPu',
    fill_opacity=1,
    line_opacity=0.4,
    legend_name='Defunciones por Enfermedades Cardiovasculares'
).add_to(n)


style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.7, 
                                'weight': 0.1}

NIL = folium.features.GeoJson(
    geo_2013,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['Entidad','Poblacion Total','Defunciones por Enfermedades Cardiovasculares', 'Tasa de Mortalidad por Enfermedades Cardiovasculares'],
        aliases=['Estado: ','Población: ','Defunciones: ','Tasa de Mortalidad: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
n.add_child(NIL)
n.keep_in_front(NIL)

loc = 'Tasa de Mortalidad por Enfermedades Cardiovasculares 2013'
title_html = '''
             <h3 style="font-size:20px"><b>{}</b></h3><br>
             '''.format(loc)
n.get_root().html.add_child(folium.Element(title_html))


folium.LayerControl().add_to(n)

for i in direcc.index:
  folium.Marker(
    location=[direcc['latitud'][i],direcc['longitud'][i]],
    popup=direcc['Centro'][i],
    ).add_to(n)


#Se añade un for que va añadiendo los marcadores, tomando las coordenadas y el nombre del dataframe


n.save('defunciones.html')

##############################################################################



# Layout HTML
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children='Dashboard Enfermedades Cardiovasculares',
           style={
            'textAlign': 'center',
            'color': colors['text']
        }),
     html.H4(children='BEDU--EQUIPO 5--DATA SCIENCE--SANTANDER',
           style={
            'textAlign': 'center',
            'color': colors['sub']
        }),
    dcc.Markdown(children="""
     En México, así como en el mundo, las defunciones causadas por enfermedades cardiovasculares (ECV) han ocupado el primer lugar entre las 
     principales causas durante varios años, entre ellas, destacan las enfermedades isquémicas del corazón que presentan una alta incidencia 
     entre la población que fallece a partir de los 45 años.
     Entre los factores de riesgo que se asocian con la enfermedad coronaria se tiene: la edad, sexo, tabaquismo, diabetes, hipertensión 
     arterial, obesidad, sobrepeso y sedentarismo.
     A continuación, se muestra un mapa de los porcentajes de los principales factores de risgo asociados a la población de cada estado de 
     México. \n\n
     """
    , style={
        'color': colors['text']
    }),
    html.Iframe(id='map', srcDoc=open('map-porcentajes.html','r').read(),width='1329', height='597'),
    dcc.Markdown(children="""
     Asimismo se tiene un mapa que muestra el número de defunciones por estado a causa de enfermedades cardiovasculares durante el año 2013, así
     como la ubicación de los principales centros de salud especializados en cardiología a lo largo de todo el territorio nacional, donde se puede
     apreciar una clara concordancia.\n\n
     """
    , style={
        'color': colors['text']
    }),
    html.Iframe(id='map2', srcDoc=open('defunciones.html','r',encoding="utf8").read(),width='1329', height='580'),
    dcc.Markdown(children="""
     \n\n Para mostrar estos resultados, se utilizó [Dash](https://dash.plotly.com/) y [Heroku](https://dashboard.heroku.com) para subir este código 
     a la nube. Para obtener los datos de las ubicaciones se utilizó la API de Bing Maps.
    Código fuente: https://github.com/DanielMonsivais/Dashboard-Equipo5 \n\n\n\n\n\n
     """
    , style={
        'color': colors['text']
    }),
    
])

if __name__ == '__main__':
    app.run_server(debug=True)
