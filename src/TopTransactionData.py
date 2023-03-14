import pandas as pd
import json
import os
import logging

#Data Extraction from the Phone Pulse Git Files
#Top Transaction Data Countrywise
def getTopTransactionDataIndia():
    path = "../data/json/top/transaction/country/india"
    year_list = [2018, 2019, 2020, 2021, 2022]
    columns = {'State': [], 'Year': [], 'Quater': [], 'State_District_PinCode_Data': [],
       'Transacion_count': [], 'Transacion_amount': [], 'Area_Type': []}
    
    for year in year_list:
        file_lst_path = path+'/'+str(year)+"/"
        file_lst = os.listdir(file_lst_path)
        for _file in file_lst:
            data = open(file_lst_path+_file, 'r')
            d = json.load(data)
            try:
                for z in d['data']['states']:
                    Name = z['entityName']
                    count = z['metric']['count']
                    amount = z['metric']['amount']
                    columns['State_District_PinCode_Data'].append(Name)
                    columns['Transacion_count'].append(count)
                    columns['Transacion_amount'].append(amount)
                    columns['State'].append('All-India')
                    columns['Year'].append(year)
                    columns['Quater'].append('Q'+_file.strip('.json'))
                    columns['Area_Type'].append('ST')

                for z in d['data']['districts']:
                    Name = z['entityName']
                    count = z['metric']['count']
                    amount = z['metric']['amount']
                    columns['State_District_PinCode_Data'].append(Name)
                    columns['Transacion_count'].append(count)
                    columns['Transacion_amount'].append(amount)
                    columns['State'].append('All-India')
                    columns['Year'].append(year)
                    columns['Quater'].append('Q'+_file.strip('.json'))
                    columns['Area_Type'].append('DT')

                for z in d['data']['pincodes']:
                    Name = z['entityName']
                    count = z['metric']['count']
                    amount = z['metric']['amount']
                    columns['State_District_PinCode_Data'].append(Name)
                    columns['Transacion_count'].append(count)
                    columns['Transacion_amount'].append(amount)
                    columns['State'].append('All-India')
                    columns['Year'].append(year)
                    columns['Quater'].append('Q'+_file.strip('.json'))
                    columns['Area_Type'].append('PC')
            except Exception as ex:
                    logging.exception(str(ex))

    TopTrans_India = pd.DataFrame(columns)
    return TopTrans_India

#Top Transaction Data Statewise
def getTopTransactionDataState():
    # path for aggregated data by each state
    path = "../data/json/top/transaction/country/india/state/"
    user_state_list = os.listdir(path)

    columns = {'State': [], 'Year': [], 'Quater': [], 'State_District_PinCode_Data': [],
        'Transacion_count': [], 'Transacion_amount': [], 'Area_Type': []}
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
                    for z in json_data['data']['districts']:
                        Name = z['entityName']
                        count = z['metric']['count']
                        amount = z['metric']['amount']
                        columns['State_District_PinCode_Data'].append(Name)
                        columns['Transacion_count'].append(count)
                        columns['Transacion_amount'].append(amount)
                        columns['State'].append(i)
                        columns['Year'].append(year)
                        columns['Quater'].append('Q'+k.strip('.json'))
                        columns['Area_Type'].append('DT')

                    for z in json_data['data']['pincodes']:
                        Name = z['entityName']
                        count = z['metric']['count']
                        amount = z['metric']['amount']
                        columns['State_District_PinCode_Data'].append(Name)
                        columns['Transacion_count'].append(count)
                        columns['Transacion_amount'].append(amount)
                        columns['State'].append(i)
                        columns['Year'].append(year)
                        columns['Quater'].append('Q'+k.strip('.json'))
                        columns['Area_Type'].append('PC')
                except Exception as ex:
                    logging.exception(str(ex))

    TopTrans_State = pd.DataFrame(columns)
    return TopTrans_State