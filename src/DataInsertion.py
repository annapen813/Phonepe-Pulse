import pandas as pd
import pymysql
import dbConfig as config
import AggregatedTransactionData as AggTransData
import AggregatedUserTransactionData as AggUsrTransData
import MapHoverTransactionData as MapHovTransData
import MapHoverUserTransactionData as MapHovUsrTransData
import TopTransactionData as TopTransData
import TopRegisteredUserData as TopUsrTransData
#SQL
from sqlalchemy import create_engine

db = pymysql.connect(host=config.host, user = config.user, password=config.password, port=config.port)
# you have cursor instance here
cursor = db.cursor()
cursor.execute("select version()")

#Creating DB for the first time
sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'phonepepulse'" 

dbIsExist = cursor.execute(sql)
if(dbIsExist == 0):
    sql = "create database phonepepulse end"
    cursor.execute(sql)
    cursor.connection.commit()

db_data = 'mysql+mysqldb://' + config.user + ':' + config.password + '@' + config.host + ':3306/' + config.dbname + '?charset=utf8mb4'

engine = create_engine(db_data)

# Dataframe formation
# Aggregated Transaction Data
df_AggTransData = pd.concat([AggTransData.getAggregatedTransactionDataIndia(),
                            AggTransData.getAggregatedTransactionDataState()], ignore_index=True)

# Aggregated User Transaction Data
df_AggUserTransData = pd.concat([AggUsrTransData.getAggregatedUserDataIndia(),
                                 AggUsrTransData.getAggregatedUserDataState()], ignore_index=True)

# Map Hover Transaction Data
df_MapHovTransData = pd.concat([MapHovTransData.getMapHoverTransactionDataIndia(),
                                MapHovTransData.getMapHoverTransactionDataState()], ignore_index=True)

# Map Hover User Transaction Data
df_MapHovUsrTransData = pd.concat([MapHovUsrTransData.getMaphoverUserDataIndia(),
                                  MapHovUsrTransData.getMapHoverUserDataState()], ignore_index=True)

# Top Transaction Data
df_TopTransData = pd.concat([TopTransData.getTopTransactionDataIndia(),
                             TopTransData.getTopTransactionDataState()], ignore_index=True)

# Top Registered User Transaction Data
df_TopUsrTransData = pd.concat([TopUsrTransData.getTopRegisteredUserDataIndia(),
                            TopUsrTransData.getTopRegisteredUserDataState()], ignore_index=True)

#Latitude Longitude table created for geoMap Vizualization for all states and distric
states_LatLong = pd.read_csv('../data/csv/States_Longitude_Latitude.csv')
districts_LatLong = pd.read_csv('../data/csv/Districts_Longitude_Latitude.csv')



# Execute the to_sql for writting DF into SQL
df_AggTransData.to_sql('Aggregated_Transaction_Data', engine, if_exists='append', index=False)  
df_AggUserTransData.to_sql('Aggregated_User_Transaction_Data', engine, if_exists='append', index=False)  
df_MapHovTransData.to_sql('Map_Hover_Transaction_Data', engine, if_exists='append', index=False)  
df_MapHovUsrTransData.to_sql('Map_Hover_User_Transaction_Data', engine, if_exists='append', index=False)  
df_TopTransData.to_sql('Top_Transaction_Data', engine, if_exists='append', index=False)  
df_TopUsrTransData.to_sql('Top_User_Transaction_Data', engine, if_exists='append', index=False)  

states_LatLong.to_sql('States_Longitude_Latitude', engine, if_exists='append', index=False)  
districts_LatLong.to_sql('Districts_Longitude_Latitude', engine, if_exists='append', index=False)


