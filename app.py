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
import pandas as pd
import folium
import geopandas as gpd

state_geo ='https://raw.githubusercontent.com/angyf/proyecto/main/mexico.json'
data_geo = gpd.read_file(state_geo)
data_geo = data_geo.rename(columns={'name':'Entidad'})

#Se lee el csv con las defunciones por estado
data=pd.read_csv('https://raw.githubusercontent.com/angyf/proyecto/main/Tasa_Mortalidad_Cardiovascular_Serie_Historica.csv')

#Se cambian los nombres de los estados para que coincidan con los del geojson
data=data.replace({"Coahuila de Zaragoza": "Coahuila", "Distrito Federal": "Ciudad de México","Michoacán de Ocampo":"Michoacán","Veracruz Llave":"Veracruz", "Querétaro de Arteaga":"Querétaro"})
data= data.rename(columns={'Entidad de Residencia':'Entidad'})

#Se aplica un filtro para quitar las defunciones totales a nivel nacional
data=data[data['Entidad']!="Nacional"]

#Se aplica un filtro para obtener solo los datos más recientes 
data_2013=data[data['Periodo']==2013]
data_2012=data[data['Periodo']==2012]
data_2011=data[data['Periodo']==2011]
data_2010=data[data['Periodo']==2010]
data_2009=data[data['Periodo']==2009]

#Se crea un dataframe uniendo el geojson con el csv para tener toda la información de los estados en uno solo
geo_2013=data_geo.merge(data_2013,on="Entidad")
geo_2012=data_geo.merge(data_2012,on="Entidad")
geo_2011=data_geo.merge(data_2011,on="Entidad")
geo_2010=data_geo.merge(data_2010,on="Entidad")
geo_2009=data_geo.merge(data_2009,on="Entidad")

def folium_del_legend(choropleth: folium.Choropleth):
  """A hack to remove choropleth legends.

  The choropleth color-scaled legend sometimes looks too crowded. Until there is an
  option to disable the legend, use this routine to remove any color map children
  from the choropleth.

  Args:
    choropleth: Choropleth objected created by `folium.Choropleth()`

  Returns:
    The same object `choropleth` with any child whose name starts with
    'color_map' removed.
  """
  del_list = []
  for child in choropleth._children:
    if child.startswith('color_map'):
      del_list.append(child)
  for del_item in del_list:
    choropleth._children.pop(del_item)
  return choropleth

import numpy as np
import branca
import folium
from branca.element import MacroElement
from jinja2 import Template
import sys

sys.path.insert(0, 'folium')
sys.path.insert(0, 'branca')


class BindColormap(MacroElement):
    """Binds a colormap to a given layer.

    Parameters
    ----------
    colormap : branca.colormap.ColorMap
        The colormap to bind.
    """
    def __init__(self, layer, colormap):
        super(BindColormap, self).__init__()
        self.layer = layer
        self.colormap = colormap
        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
            {{this._parent.get_name()}}.on('overlayadd', function (eventLayer) {
                if (eventLayer.layer == {{this.layer.get_name()}}) {
                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
                }});
            {{this._parent.get_name()}}.on('overlayremove', function (eventLayer) {
                if (eventLayer.layer == {{this.layer.get_name()}}) {
                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'none';
                }});
        {% endmacro %}
        """)  # noqa
        
direcc=pd.read_csv('https://raw.githubusercontent.com/angyf/proyecto/main/Direcc-coord.csv')
datos=[['2009',data_2009,geo_2009],['2010',data_2010,geo_2010],['2011',data_2011,geo_2011],['2012',data_2012,geo_2012],['2013',data_2013,geo_2013]]

map = folium.Map(location=[24, -102], zoom_start=5, width='70%', height='70%')

for dat in datos:
  cm1 = branca.colormap.linear.BuPu_09.to_step(12).scale(dat[1]['Defunciones por Enfermedades Cardiovasculares'].min(),dat[1]['Defunciones por Enfermedades Cardiovasculares'].max()).add_to(map)
  cm1.caption = "Defunciones por Enfermedades Cardiovasculares"

  if (dat[0]=='2013'):
        mostrar=True
  else:
        mostrar=False


  colorm= folium_del_legend(folium.Choropleth(
      geo_data=state_geo,
      name=dat[0],
      data=dat[1],
      columns=['Entidad', 'Defunciones por Enfermedades Cardiovasculares'],
      key_on='feature.properties.name',
      fill_color='BuPu',
      fill_opacity=1,
      line_opacity=0.4,
      legend_name='Defunciones por Enfermedades Cardiovasculares',
      show=mostrar
  )).add_to(map)


  style_function = lambda x: {'fillColor': '#ffffff', 
                              'color':'#000000', 
                              'fillOpacity': 0.1, 
                              'weight': 0.1}
  highlight_function = lambda x: {'fillColor': '#000000', 
                                  'color':'#000000', 
                                  'fillOpacity': 0.7, 
                                  'weight': 0.1}
  NIL = folium.features.GeoJson(
      dat[2],
      style_function=style_function, 
      control=True,
      highlight_function=highlight_function, 
      tooltip=folium.features.GeoJsonTooltip(
          fields=['Entidad','Poblacion Total','Defunciones por Enfermedades Cardiovasculares', 'Tasa de Mortalidad por Enfermedades Cardiovasculares','Periodo'],
          aliases=['Estado: ','Población: ','Defunciones: ','Tasa de Mortalidad: ','Periodo: '],
          style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
      )
  )
  colorm.add_child(NIL)
  map.add_child(BindColormap(colorm, cm1))


feature_group = folium.FeatureGroup(name="Ubicaciones")
for i in direcc.index:
    folium.Marker(
    location=[direcc['latitud'][i],direcc['longitud'][i]],
    popup=direcc['Centro'][i],
    icon=folium.Icon(color="red", icon="heartbeat",prefix='fa')
    ).add_to(feature_group)
    feature_group.add_to(map)
#Más íconos en https://fontawesome.com/v4.7/icons/
#heart, heart-o, medkit, hospital-o


loc = 'Tasa de Mortalidad por Enfermedades Cardiovasculares 2009-2013'
title_html = '''
             <h3 style="font-size:20px"><b>{}</b></h3><br>
             '''.format(loc)
map.get_root().html.add_child(folium.Element(title_html))







folium.LayerControl().add_to(map)

map.save('defunciones.html')

##############################################################################
#GRAFICA 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

url='https://drive.google.com/file/d/1Q_ywhZHAJ1XDNlWsMe4ru2N9-Wqny_ZW/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path)

#filtramos solo a partir de 2010
df=df[df['PERIODO']>2009]

#Creamos el gráfico

#Definimos un estilo oscuro para nuestros gráficos
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(8,5))
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: format(int(x))))

for i in ['TOTAL','HOMBRE','MUJER']:
  ax.plot_date(df['PERIODO'],df[i],ls='-')

ax.set_xlabel("Año",fontsize=18)
ax.set_ylabel("Total",fontsize=18)
ax.set_title("Mortalidad en México por enfermedades del corazón\n",fontsize=18, weight='bold')
ax.legend(['Total','Hombres','Mujeres']);

fig.savefig("grafica.jpg")


##############################################################################
##############################################################################



# Layout HTML
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px','margin-top' : '-20px', 'width':'100%','padding-top': '30px'}, children=[
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
     México. En él se observan porcentajes alarmantes, sobre todo en obesidad. \n\n
     """
    , style={
        'color': colors['text']
    }),
    html.Iframe(id='map', srcDoc=open('map-porcentajes.html','r').read()),
    dcc.Markdown(children="""
     Asimismo se tiene un mapa que muestra el número de defunciones por estado a causa de enfermedades cardiovasculares durante el año 2013, así
     como la ubicación de los principales centros de salud especializados en cardiología a lo largo de todo el territorio nacional, donde se puede
     apreciar una clara concordancia.\n\n
     """
    , style={
        'color': colors['text']
    }),
    html.Iframe(id='map2', srcDoc=open('defunciones.html','r',encoding="utf8").read(),width='927', height='490',style={
            'display':'flex', 'justify-content':'center'}),
    dcc.Markdown(children="""
     \n\n Para mostrar estos resultados, se utilizó [Dash](https://dash.plotly.com/) y [Heroku](https://dashboard.heroku.com) para subir este código a la nube. Para obtener los datos de las ubicaciones se utilizó la API de Bing Maps.              .
     Código fuente: https://github.com/DanielMonsivais/Dashboard-Equipo5 
     """, style={
        'color': colors['text']
    }),
    html.Img(id = 'plot', src = 'grafica.jpg')
    
])

if __name__ == '__main__':
    app.run_server(debug=True)
