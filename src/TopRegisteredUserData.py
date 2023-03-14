import pandas as pd
import json
import os
import logging

#Data Extraction from the Phone Pulse Git Files
#Top Transaction Data Countrywise
def getTopRegisteredUserDataIndia():
    path = "../data/json/top/user/country/india"
    year_list = [2018, 2019, 2020, 2021, 2022]
    columns = {'State': [], 'Year': [], 'Quater': [], 'State_District_Pincode_Name': [],
               'Registered_User_Number': [], 'Area_Type': []}
    
    for year in year_list:
        file_lst_path = path+'/'+str(year)+"/"
        file_lst = os.listdir(file_lst_path)
        for _file in file_lst:
            data = open(file_lst_path+_file, 'r')
            d = json.load(data)
            try:
                for z in d['data']['states']:
                    State_District_Pincode_Name = z['name']
                    reg_users = z["registeredUsers"]
                    columns['State_District_Pincode_Name'].append(State_District_Pincode_Name)
                    columns['Registered_User_Number'].append(reg_users)
                    columns['State'].append('All-India')
                    columns['Year'].append(year)
                    columns['Quater'].append('Q'+_file.strip('.json'))
                    columns['Area_Type'].append('ST')

                for z in d['data']['districts']:
                    State_District_Pincode_Name = z['name']
                    reg_users = z["registeredUsers"]
                    columns['State_District_Pincode_Name'].append(State_District_Pincode_Name)
                    columns['Registered_User_Number'].append(reg_users)
                    columns['State'].append('All-India')
                    columns['Year'].append(year)
                    columns['Quater'].append('Q'+_file.strip('.json'))
                    columns['Area_Type'].append('DT')

                for z in d['data']['pincodes']:
                    State_District_Pincode_Name = z['name']
                    reg_users = z["registeredUsers"]
                    columns['State_District_Pincode_Name'].append(State_District_Pincode_Name)
                    columns['Registered_User_Number'].append(reg_users)
                    columns['State'].append('All-India')
                    columns['Year'].append(year)
                    columns['Quater'].append('Q'+_file.strip('.json'))
                    columns['Area_Type'].append('PC')
            except Exception as ex:
                    logging.exception(str(ex))

    TopRegUsers_India = pd.DataFrame(columns)
    return TopRegUsers_India

#Top Transaction Data Stateywise
def getTopRegisteredUserDataState():
    # path for aggregated data by each state
    path = "../data/json/top/user/country/india/state/"
    user_state_list = os.listdir(path)

    columns = {'State': [], 'Year': [], 'Quater': [], 'State_District_Pincode_Name': [],
               'Registered_User_Number': [], 'Area_Type': []}
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
                        State_District_Pincode_Name = z['name']
                        reg_users = z["registeredUsers"]
                        columns['State_District_Pincode_Name'].append(State_District_Pincode_Name)
                        columns['Registered_User_Number'].append(reg_users)
                        columns['State'].append(i)
                        columns['Year'].append(year)
                        columns['Quater'].append('Q'+k.strip('.json')) 
                        columns['Area_Type'].append('DT')   

                    for z in json_data['data']['pincodes']:
                        State_District_Pincode_Name = z['name']
                        reg_users = z["registeredUsers"]
                        columns['State_District_Pincode_Name'].append(State_District_Pincode_Name)
                        columns['Registered_User_Number'].append(reg_users)
                        columns['State'].append(i)
                        columns['Year'].append(year)
                        columns['Quater'].append('Q'+k.strip('.json'))   
                        columns['Area_Type'].append('PC')                    
                except Exception as ex:
                    logging.exception(str(ex))

    TopRegUsers_State = pd.DataFrame(columns)
    return TopRegUsers_State