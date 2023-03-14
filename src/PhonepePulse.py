import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy import text
import dbConfig as config

connection = create_engine("mysql+mysqldb://{0}:{1}@{2}:{3}/{4}".format(config.user, 
                                                                        config.password, 
                                                                        config.host, 
                                                                        config.port, 
                                                                        config.dbname))
connection.connect() 


#Look Up DataFrames - Quarter
qryQuarters = text("SELECT DISTINCT Quater FROM phonepepulse.Aggregated_User_Transaction_Data")
df_Quarters = pd.read_sql(qryQuarters, con=connection)

#Look Up DataFrames - Year
qryYears = text("SELECT DISTINCT Year FROM phonepepulse.Aggregated_User_Transaction_Data")
df_Years = pd.read_sql(qryYears, con=connection)

#Look Up DataFrames - States
qryStates = text("SELECT DISTINCT State FROM phonepepulse.Map_Hover_User_Transaction_Data")
df_States = pd.read_sql(qryStates, con=connection)

#Bar Chart - Formation
def getAggregatedTransData(state, year, quarter, connection):
    qryAggTransData = text("SELECT * " +
                           "FROM Aggregated_Transaction_Data " +
                           "WHERE State = '" + state + "' AND Year = '" + year + "' AND Quater = '" + quarter + "'")
    df_AggTransData = pd.read_sql(qryAggTransData, con=connection)

    aggFig = px.bar(df_AggTransData, 
                      x='Transacion_type', 
                      y='Transacion_amount', 
                      color='Transacion_type', 
                      color_continuous_scale='armyrose',
                      title='Total Transacions in '+ state + ' for Quater '+ quarter + ' and for the Year -' + year )
    return aggFig

#Pie Chart - Formation
def getAggregatedUserTranData(state, year, quarter, connection):
    qryAggUsrTransData = text("SELECT * " +
                              "FROM Aggregated_User_Transaction_Data " +
                              "WHERE State = '" + state + "' AND Year = '" + year + "' AND Quater = '" + quarter + "'")
    df_AggUsrTransData = pd.read_sql(qryAggUsrTransData, con=connection)
    
    aggUsrFig = px.pie(df_AggUsrTransData, 
                       values='Transacion_count', 
                       names='User_type', 
                       title='Total User Transacion in '+ state + ' for Quater '+ quarter + ' and for the Year -' + year)
    return aggUsrFig

#Heat Map - Geo Visualization - Transaction Data
def getMapHoverTransData(state, year, quarter, connection):
    if state == 'All-India':
        qryMapHoverTransData = text("SELECT a.*, b.code, b.Latitude, b.Longitude, b.geo_state " +
                                    "FROM phonepepulse.Map_Hover_Transaction_Data a, phonepepulse.States_Longitude_Latitude b " +
                                    "WHERE a.State_District_Name = replace(b.state, '-', ' ') AND a.Year = '" + year + "' AND a.Quater = '" + quarter + "' AND a.State = 'All-India'")
    else:
        qryMapHoverTransData = text("SELECT a.*, b.Latitude, b.Longitude, c.code, c.geo_state " +
                                    "FROM phonepepulse.Map_Hover_Transaction_Data a, phonepepulse.Districts_Longitude_Latitude b, phonepepulse.States_Longitude_Latitude c " +
                                    "WHERE a.State_District_Name = b.District AND a.State = b.State AND b.State = c.State AND a.Year = '" + year + "' AND a.Quater = '" + quarter + "' AND a.State = '" + state + "'")
    df_MapHoverTransData = pd.read_sql(qryMapHoverTransData, con=connection)

    chart = df_MapHoverTransData.drop(labels='State', axis=1)

    if state == 'All-India':							
        indiaFig = px.scatter_geo(chart,
                            lon=chart['Longitude'],
                            lat=chart['Latitude'],
                            hover_name=chart['State_District_Name'],
                            text=chart['code'],
                            hover_data=['Transacion_count', 'Transacion_amount', 'Year', 'Quater'],
                            )
        indiaFig.update_traces(marker=dict(color="#f6b26b", size=0.3))
    else:
        stateFig = px.scatter_geo(chart,
                            lon=chart['Longitude'],
                            lat=chart['Latitude'],
                            hover_name=chart['State_District_Name'],
                            text=chart['code'],
                            hover_data=['Transacion_count', 'Transacion_amount', 'Year', 'Quater'],
                            title='District',
                            size_max=22,)
        stateFig.update_traces(marker={'color': "#CC0044",
                               'line_width': 1})
    
    
    mapHovfig = px.choropleth(chart,
                              geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey='properties.ST_NM',
                              locations='geo_state',
                              color='Transacion_amount',
                              color_continuous_scale='Blues',
                              hover_data=['Transacion_count', 'Transacion_amount'])

    mapHovfig.update_geos(fitbounds="locations", visible=False)
    if state == 'All-India':
        mapHovfig.add_trace(indiaFig.data[0])
    else:
        mapHovfig.add_trace(stateFig.data[0])

    mapHovfig.update_layout(height=700, width=1000)
    return mapHovfig

#Heat Map - Geo Visualization - User Transaction Data
def getMapHoverUserTransData(state, year, quarter, connection):
    if state == 'All-India':
        qryMapHoverUserTransData = text("SELECT a.*, b.code, b.Latitude, b.Longitude, b.geo_state " +
                                    "FROM phonepepulse.Map_Hover_User_Transaction_Data a, phonepepulse.States_Longitude_Latitude b " +
                                    "WHERE a.State_District_Name = replace(b.state, '-', ' ') AND a.Year = '" + year + "' AND a.Quater = '" + quarter + "' AND a.State = 'All-India'")
    else:
        qryMapHoverUserTransData = text("SELECT a.*, b.Latitude, b.Longitude, c.code, c.geo_state " +
                                    "FROM phonepepulse.Map_Hover_User_Transaction_Data a, phonepepulse.Districts_Longitude_Latitude b, phonepepulse.States_Longitude_Latitude c " +
                                    "WHERE a.State_District_Name = b.District AND a.State = b.State AND b.State = c.State AND a.Year = '" + year + "' AND a.Quater = '" + quarter + "' AND a.State = '" + state + "'")
    df_MapHoverUserTransData = pd.read_sql(qryMapHoverUserTransData, con=connection)
    
    chart = df_MapHoverUserTransData.drop(labels='State', axis=1)

    if state == 'All-India':							
        indiaFig = px.scatter_geo(chart,
                                  lon=chart['Longitude'],
                                  lat=chart['Latitude'],
                                  hover_name=chart['State_District_Name'],
                                  text=chart['code'],
                                  hover_data=['Registered_User_count', 'Year', 'Quater'],)
        indiaFig.update_traces(marker=dict(color="#f6b26b", size=0.3))
    else:
        stateFig = px.scatter_geo(chart,
                                  lon=chart['Longitude'],
                                  lat=chart['Latitude'],
                                  hover_name=chart['State_District_Name'],
                                  text=chart['code'],
                                  hover_data=['Registered_User_count', 'Year', 'Quater'],
                                  title='District',
                                  size_max=22,)
        stateFig.update_traces(marker={'color': "#CC0044",
                               'line_width': 1})
    
    
    mapHovUsrfig = px.choropleth(chart,
                                 geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                 featureidkey='properties.ST_NM',
                                 locations='geo_state',
                                 color='Registered_User_count',
                                 color_continuous_scale='Greens',
                                 hover_data=['Registered_User_count'])

    mapHovUsrfig.update_geos(fitbounds="locations", visible=False)
    if state == 'All-India':
        mapHovUsrfig.add_trace(indiaFig.data[0])
    else:
        mapHovUsrfig.add_trace(stateFig.data[0])

    mapHovUsrfig.update_layout(height=700, width=1000)
    return mapHovUsrfig

def Header(title, colorCode):
     st.markdown(f'<h1 style="color:{colorCode};font-size:32px;border-radius:2%;">{title}</h1>', unsafe_allow_html=True)

def subHeader(title, colorCode):
     st.markdown(f'<h3 style="color:{colorCode};font-size:24px;border-radius:2%;">{title}</h3>', unsafe_allow_html=True)


# ------------------------------------------ Data Visualizations Using Streamlit and Plotly Express----------------------------
with st.container():
    Header('PhonePe Pulse Data Visualization(2018-2022)📈', '#4B0082')
    st.image('../img/dv.jpg')

    st.sidebar.header("Category List")
    menu = ["📈 Aggregated Data","📈 Map Hover Data"]
    choice = st.sidebar.selectbox(":black[Visualization Category]",menu)
    

    col1, col2, col3 = st.columns(3)
    with col1:
        st_year = st.selectbox('Year', df_Years["Year"])
        st.write(' ')
    with col2:
        st_state = st.selectbox('State', df_States["State"], index=0)
        st.write(' ')
    with col3:
        st_quater = st.selectbox('Quater', df_Quarters["Quater"])
        st.write(' ')
   
    if choice == "📈 Aggregated Data":
        subHeader('Statewise Transaction Data','#191970')
        st.plotly_chart(getAggregatedTransData(st_state, st_year, st_quater, connection))

        subHeader('Statewise User Transaction Data', '#800000')
        st.plotly_chart(getAggregatedUserTranData(st_state, st_year, st_quater, connection))

    if choice == "📈 Map Hover Data":    
        subHeader('Statewise and Districtwise Transaction Data through Map Hovering', '#000080')
        st.plotly_chart(getMapHoverTransData(st_state, st_year, st_quater, connection))

        subHeader('Statewise and Districtwise User Transaction Data through Map Hovering', '#006400')
        st.plotly_chart(getMapHoverUserTransData(st_state, st_year, st_quater, connection))