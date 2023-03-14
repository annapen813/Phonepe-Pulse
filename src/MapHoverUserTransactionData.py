import pandas as pd
import json
import os
import logging

#Data Extraction from the Phone Pulse Git Files
#Map Hover User Transaction Data Countrywise
def getMaphoverUserDataIndia():
    path = "../data/json/map/user/hover/country/india"
    year_list = [2018, 2019, 2020, 2021, 2022]
    columns = {'State': [], 'Year': [], 'Quater': [], 'State_District_Name': [],
               'Registered_User_count': [], 'App_Open_count': []}
    
    for year in year_list:
        file_lst_path = path+'/'+str(year)+"/"
        file_lst = os.listdir(file_lst_path)
        for _file in file_lst:
            data = open(file_lst_path+_file, 'r')
            d = json.load(data)
            try:
                for z in d['data']['hoverData']:
                    State_District_Name = z
                    reg_users = d['data']['hoverData'][z]["registeredUsers"]
                    app_open_count = d['data']['hoverData'][z]["appOpens"]
                    columns['State_District_Name'].append(State_District_Name)
                    columns['Registered_User_count'].append(reg_users)
                    columns['App_Open_count'].append(app_open_count)
                    columns['State'].append('All-India')
                    columns['Year'].append(year)
                    columns['Quater'].append('Q'+_file.strip('.json'))
            except Exception as ex:
                    logging.exception(str(ex))
    
    MapHov_User_India = pd.DataFrame(columns)
    return MapHov_User_India

#Map Hover User Transaction Data Statewise
def getMapHoverUserDataState():
    # path for aggregated data by each state
    path = "../data/json/map/user/hover/country/india/state/"
    user_state_list = os.listdir(path)

    columns = {'State': [], 'Year': [], 'Quater': [], 'State_District_Name': [],
               'Registered_User_count': [], 'App_Open_count': []}
    for i in user_state_list:
        path_i = path+i+"/"
        Agg_years = os.listdir(path_i)
        for year in Agg_years:
            path_i_year = path_i+year+"/"
            Agg_yr_list = os.listdir(path_i_year)
            for k in Agg_yr_list:
                path_i_year_file = path_i_year+k
                data = open(path_i_year_file, 'r')
                json_data = json.load(data)
                try:
                    for z in json_data['data']['hoverData']:
                        State_District_Name = z
                        reg_users = json_data['data']['hoverData'][z]["registeredUsers"]
                        app_open_count = json_data['data']['hoverData'][z]["appOpens"] 
                        columns['State_District_Name'].append(State_District_Name)
                        columns['Registered_User_count'].append(reg_users)
                        columns['App_Open_count'].append(app_open_count)
                        columns['State'].append(i)
                        columns['Year'].append(year)
                        columns['Quater'].append('Q'+k.strip('.json'))                       
                except Exception as ex:
                    logging.exception(str(ex))

    MapHov_User_States = pd.DataFrame(columns)
    return MapHov_User_States