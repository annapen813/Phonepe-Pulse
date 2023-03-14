import pandas as pd
import json
import os
import logging

#Data Extraction from the Phone Pulse Git Files
#Aggregated User Data Countrywise
def getAggregatedUserDataIndia():
    path = "../data/json/aggregated/user/country/india"
    year_list = [2018, 2019, 2020, 2021, 2022]
    columns = {'State': [], 'Year': [], 'Quater': [], 'User_type': [],
               'Transacion_count': [], 'Transacion_percentage': []}
    
    for year in year_list:
        file_lst_path = path+'/'+str(year)+"/"
        file_lst = os.listdir(file_lst_path)
        for _file in file_lst:
            data = open(file_lst_path+_file, 'r')
            d = json.load(data)
            try:
                for z in d['data']['usersByDevice']:
                    Brand = z['brand']
                    count = z['count']
                    percentage = z['percentage']
                    columns['User_type'].append(Brand)
                    columns['Transacion_count'].append(count)
                    columns['Transacion_percentage'].append(percentage)
                    columns['State'].append('All-India')
                    columns['Year'].append(year)
                    columns['Quater'].append('Q'+_file.strip('.json'))
            except Exception as ex:
                logging.exception(str(ex))

    Agg_User_Trans_India = pd.DataFrame(columns)
    return Agg_User_Trans_India


#Aggregated User Data Statewise
def getAggregatedUserDataState():
    # path for aggregated data by each state
    path = "../data/json/aggregated/user/country/india/state/"
    user_state_list = os.listdir(path)

    columns = {'State': [], 'Year': [], 'Quater': [], 'User_type': [],
        'Transacion_count': [], 'Transacion_percentage': []}
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
                    for z in json_data['data']['usersByDevice']:
                        #print(z)
                        Brand = z['brand']
                        count = z['count']
                        percentage = z['percentage']
                        columns['User_type'].append(Brand)
                        columns['Transacion_count'].append(count)
                        columns['Transacion_percentage'].append(percentage)
                        columns['State'].append(i)
                        columns['Year'].append(year)
                        columns['Quater'].append('Q'+k.strip('.json'))
                except Exception as ex:
                    logging.exception(str(ex))
    
    Agg_User_Trans_States = pd.DataFrame(columns)
    return Agg_User_Trans_States