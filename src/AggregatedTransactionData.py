import pandas as pd
import json
import os
import logging

#Data Extraction from the Phone Pulse Git Files
#Aggregated Transaction Data Countrywise
def getAggregatedTransactionDataIndia():
    path = "../data/json/aggregated/transaction/country/india"
    year_list = [2018, 2019, 2020, 2021, 2022]
    columns = {'State': [], 'Year': [], 'Quater': [], 'Transacion_type': [],
       'Transacion_count': [], 'Transacion_amount': []}
    
    for year in year_list:
        file_lst_path = path+'/'+str(year)+"/"
        file_lst = os.listdir(file_lst_path)
        for _file in file_lst:
            data = open(file_lst_path+_file, 'r')
            d = json.load(data)
            try:
                for z in d['data']['transactionData']:
                    Name = z['name']
                    count = z['paymentInstruments'][0]['count']
                    amount = z['paymentInstruments'][0]['amount']
                    columns['Transacion_type'].append(Name)
                    columns['Transacion_count'].append(count)
                    columns['Transacion_amount'].append(amount)
                    columns['State'].append('All-India')
                    columns['Year'].append(year)
                    columns['Quater'].append('Q'+_file.strip('.json'))
            except Exception as ex:
                    logging.exception(str(ex))

    Agg_Trans_India = pd.DataFrame(columns)
    return Agg_Trans_India

#Aggregated Transaction Data Statewise
def getAggregatedTransactionDataState():
    # path for aggregated data by each state
    path = "../data/json/aggregated/transaction/country/india/state/"
    user_state_list = os.listdir(path)

    columns = {'State': [], 'Year': [], 'Quater': [], 'Transacion_type': [],
        'Transacion_count': [], 'Transacion_amount': []}
    for i in user_state_list:
        path_i = path+i+"/"
        Agg_years = os.listdir(path_i)
        for year in Agg_years:
            path_i_year = path_i+year+"/"
            Agg_yr_list = os.listdir(path_i_year)
            for k in Agg_yr_list:
                path_i_year_file = path_i_year+k
                #print(path_i_year_file)
                data = open(path_i_year_file, 'r')
                json_data = json.load(data)
                try:
                    for z in json_data['data']['transactionData']:
                        Name = z['name']
                        count = z['paymentInstruments'][0]['count']
                        amount = z['paymentInstruments'][0]['amount']
                        columns['Transacion_type'].append(Name)
                        columns['Transacion_count'].append(count)
                        columns['Transacion_amount'].append(amount)
                        columns['State'].append(i)
                        columns['Year'].append(year)
                        columns['Quater'].append('Q'+k.strip('.json'))
                except Exception as ex:
                    logging.exception(str(ex))

    Agg_Trans_State = pd.DataFrame(columns)
    return Agg_Trans_State