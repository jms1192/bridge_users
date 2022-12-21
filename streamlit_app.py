from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import requests
import plotly.express as px


def create_premade_layout(layout, data1, type = ''):

    data = data1

    if layout == '2d-layout-1':

        ## get symbols 
        symbols = [x['ASSET'] for x in data]
        all_symbols = []
        for i in symbols:
            if i not in all_symbols:
                all_symbols.append(i)

        ## drop text box 
        symbols = st.multiselect("", all_symbols, all_symbols[:9])
        st.text("")

        ## sort data 
        vol_data = {}
        vol_data_sum = {}
        date_data = []
        vol = []
        asset = ''
        for x in data:
            if x['ASSET'] in symbols:
                if not x['ASSET'] == asset:
                    if asset == '':
                        asset = x['ASSET']
                    else:
                        vol_data_sum[asset] = sum(vol)
                        vol_data[asset] = vol
                        asset = x['ASSET']
                        
                    vol = []
                    vol.append(x['SWAP_VOLUME'])
                    date_data = []
                    date_data.append(x['DAY'])
                else:
                    date_data.append(x['DAY'])
                    vol.append(x['SWAP_VOLUME'])

        vol_data[asset] = vol           
        symbols.sort()

        ## create data frames
        chart = pd.DataFrame(
            vol_data,
            index=date_data
        )

        chart2 = pd.DataFrame(
            [sum(vol_data[x])/12 for x in vol_data],
            index=[x for x in vol_data]
        )

        ## place data frame 
        if type == 'line':
            st.line_chart(chart)
        elif type == 'bar':
            st.bar_chart(chart)
        elif type == 'area':
            st.area_chart(chart)
        else:
            st.area_chart(chart)
            
        st.bar_chart(chart2)
        
    elif layout == 'pie-layout-1':
        ### data needs to made like {BIG_CATEGORY, SMALL_CATEGORY, VALUE}
        symbols = [x['BIG_CATEGORY'] for x in data]
        big_category = []
        for i in symbols:
            if i not in big_category:
                big_category.append(i)
                
        symbols3 = st.selectbox("", big_category)

        df = [x for x in data if x['BIG_CATEGORY'] == symbols3]
        if len(df) > 10:
            df = sorted(df, key=lambda x: x['VALUE'], reverse=True)
            df = df[0:10]
        
        fig = px.pie(df, values='VALUE', names='SMALL_CATEGORY')
        st.plotly_chart(fig, use_container_width=True)






def sort_flipside_api(link, bridge, type, chain):
    #sort TVL_data 
    if type == 'TVL':

        data = requests.get(link).json()
        data_list = []
        for x in data:
            ##data if 
            if "TVL_USD" in x:
                amount = x['TVL_USD']
            elif "TVL" in x:
                amount = x['TVL']
            elif "BALANCE" in x:
                amount = x['BALANCE']
            ## token if 
            if "TOKEN" in x:
                token = x['TOKEN']
            elif "SYMBOL" in x:
                token = x['SYMBOL']


            clean_dict = {'DAY':x['DAY'], 'TOKEN':token, 'BRIDGE':bridge, 'CHAIN':chain, 'TVL':amount}
            data_list.append(clean_dict)

        return data_list

    if type == 'VOLUME':

        data = requests.get(link).json()
        data_list = []
        for x in data:
            
                ##data if 
                if 'OUT_VOLUME' in x:
                    amount = x['OUT_VOLUME']
                if 'AMT_OUT' in x:
                    amount = x['AMT_OUT']
                if 'VOLUME' in x:
                    amount = x['VOLUME']
                if 'VOL_USD_OUT' in x:
                    amount = x['VOL_USD_OUT']

                clean_dict = {'DAY':x['DAY'], 'BRIDGE':bridge, 'CHAIN':chain, 'VOLUME':amount}
                data_list.append(clean_dict)

        return data_list

    if type == 'USERS':

        data = requests.get(link).json()
        data_list = []
        for x in data:
            
                ##data if 
                if 'USERS' in x:
                    amount = x['USERS']
                if 'USER' in x:
                    amount = x['USER']
                if 'TOTAL_UNIQUE_USERS' in x:
                    amount = x['TOTAL_UNIQUE_USERS']
                #if 'VOL_USD_OUT' in x:
                #    amount = x['VOL_USD_OUT']
                clean_dict = {'DAY':x['DAY'], 'BRIDGE':bridge, 'CHAIN':chain, 'VOLUME':amount}
                data_list.append(clean_dict)

        return data_list


## sort all data here
volume_api_list = [ 
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/ec6ca210-d16d-4996-8d4d-5e673113ced6/data/latest', 'Bridge':'Stargate', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/3ca2b8cc-9000-4757-9296-ec78f004127c/data/latest', 'Bridge':'Stargate', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/3ca2b8cc-9000-4757-9296-ec78f004127c/data/latest', 'Bridge':'Stargate', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/5168e3d4-3b12-4808-b6e9-34cdf83d7123/data/latest', 'Bridge':'Stargate', 'Chain':'Avalanche'},

    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/6434d3e9-8b87-4e74-9897-2c1eeb0d98a2/data/latest', 'Bridge':'Hop', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/28afb7ab-1233-4a14-b585-5cdb95de8f13/data/latest', 'Bridge':'Hop', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/5153b9b4-2f3b-4ebc-a427-bebcab17dce5/data/latest', 'Bridge':'Hop', 'Chain':'Polygon'},
    #{'link':'https://node-api.flipsidecrypto.com/api/v2/queries/29177db5-4586-431d-b79f-1ed26733f8be/data/latest', 'Bridge':'Hop', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/35c12ff9-e958-4e15-9675-0d655aae0303/data/latest', 'Bridge':'Hop', 'Chain':'Arbitrum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/46c97449-588d-4584-9bd0-0f6e9cc572c7/data/latest', 'Bridge':'Hop', 'Chain':'Gnosis'},

    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/65a56a90-a54a-4624-b530-3d023a062db3/data/latest', 'Bridge':'Hyphen', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/5650044b-e534-460f-8707-deabae1be9df/data/latest', 'Bridge':'Hyphen', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/0f7b41eb-2190-4f27-92b8-f0f92690cf86/data/latest', 'Bridge':'Hyphen', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/119f6358-60ee-4407-b094-7302696a2c3e/data/latest', 'Bridge':'Hyphen', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/b4cb6f97-023d-4185-92d8-8b624aa083cb/data/latest', 'Bridge':'Hyphen', 'Chain':'Arbitrum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/4d6a502c-811c-4f60-8510-84f268c5c3c9/data/latest', 'Bridge':'Hyphen', 'Chain':'BSC'},

    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/6454ca7c-ae9c-417f-b04f-94b93a2037ab/data/latest', 'Bridge':'Synapse', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/17c9a813-3852-4763-b170-663ad644d009/data/latest', 'Bridge':'Synapse', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/f48dfb62-f170-4e90-b7ba-f67c53893be0/data/latest', 'Bridge':'Synapse', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/e01a1cb8-c265-4b00-bdd6-50c52886862a/data/latest', 'Bridge':'Synapse', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/1f68ee80-0c70-4a42-ac06-813f3b3947b2/data/latest', 'Bridge':'Synapse', 'Chain':'Arbitrum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/5133379d-2864-46c8-b675-7c6b3ded7ca1/data/latest', 'Bridge':'Synapse', 'Chain':'BSC'}

    #{'link':'https://node-api.flipsidecrypto.com/api/v2/queries/d70c08e6-6ef0-4d4b-92df-5f47c9e23765/data/latest', 'Bridge':'Across', 'Chain':'Optimism'},
    #{'link':'https://node-api.flipsidecrypto.com/api/v2/queries/33f8cfca-047b-4fc4-bc6d-1c300f76e6ad/data/latest', 'Bridge':'Across', 'Chain':'Ethereum'},
    #{'link':'https://node-api.flipsidecrypto.com/api/v2/queries/a2df7f86-560a-4d3a-9ab9-296f553f0fdd/data/latest', 'Bridge':'Across', 'Chain':'Polygon'},
    #{'link':'https://node-api.flipsidecrypto.com/api/v2/queries/0921fa72-ea81-401f-832a-2c4eea1a71d9/data/latest', 'Bridge':'Across', 'Chain':'Arbitrum'}
]

full_volume_list = []
full_volume_list2 = []
for api in volume_api_list:
    api_data_clean = sort_flipside_api(api['link'], api['Bridge'], 'USERS', api['Chain'])
    for x in api_data_clean:
        full_volume_list.append(x)




restructure_group_dict = {}
final_data_list1 = []
final_data_list2 = []
for x in full_volume_list:
    if x['VOLUME'] == None:
        x['VOLUME'] = 0
    if not x['DAY'] in restructure_group_dict:
        restructure_group_dict[x['DAY']] = {x['BRIDGE']:x['VOLUME']}
    else:
        if not x['BRIDGE'] in restructure_group_dict[x['DAY']]:
            restructure_group_dict[x['DAY']][x['BRIDGE']] = x['VOLUME']
        else:
            restructure_group_dict[x['DAY']][x['BRIDGE']] = restructure_group_dict[x['DAY']][x['BRIDGE']] + x['VOLUME']

for x in restructure_group_dict.keys():
    for y in restructure_group_dict[x].keys():
        final_dict = {'DAY':x, 'ASSET':y, 'SWAP_VOLUME': restructure_group_dict[x][y]}
        final_dict2 = {'BIG_CATEGORY':x, 'SMALL_CATEGORY':y, 'VALUE': restructure_group_dict[x][y]}
        final_data_list1.append(final_dict)
        final_data_list2.append(final_dict2)

final_data_list1 = sorted(final_data_list1, key=lambda  x:(x['ASSET'], x['DAY']), reverse=True) 
final_data_list2 = sorted(final_data_list2, key=lambda  x:(x['BIG_CATEGORY']), reverse=True) 
## make diffrent graph 

restructure_group_dict2 = {}
final_data_list3 = []
for x in full_volume_list:
    if x['VOLUME'] == None:
        x['VOLUME'] = 0
    if not x['BRIDGE'] in restructure_group_dict2:
        restructure_group_dict2[x['BRIDGE']] = {x['CHAIN']:x['VOLUME']}
    else:
        if not x['CHAIN'] in restructure_group_dict2[x['BRIDGE']]:
            restructure_group_dict2[x['BRIDGE']][x['CHAIN']] = x['VOLUME']
        else:
            restructure_group_dict2[x['BRIDGE']][x['CHAIN']] = restructure_group_dict2[x['BRIDGE']][x['CHAIN']] + x['VOLUME']

for x in restructure_group_dict2.keys():
    for y in restructure_group_dict2[x].keys():
        final_dict = {'DAY':x, 'ASSET':y, 'SWAP_VOLUME': restructure_group_dict2[x][y]}
        final_dict3 = {'BIG_CATEGORY':x, 'SMALL_CATEGORY':y, 'VALUE': restructure_group_dict2[x][y]}
        
        final_data_list3.append(final_dict3)
        
"""
# Cross Chain Bridge User Metrics 
Welcome to our on-chain analysis dashboard! In this dashboard, you can view the weekly users of the cross-chain bridges Hyphen, Hop, Stargate, Across, and Synaps. Additionally, you can see the breakdown of each bridge's weekly transfer volume by the chain where the bridge originated. In this analysis, a user is defined as a wallet. If a person uses a bridge from multiple chains, they will get double-counted."""

create_premade_layout('2d-layout-1', final_data_list1)
"""
### Description  
The graphs above shows the weekly and weekly average users of cross chain bridges Hyphen, Hop, Stargate, Across, and Synaps
"""

create_premade_layout('pie-layout-1', final_data_list3)
"""
### Description  
The graph above shows the weekly users of assets broken down by cross chain bridges Hyphen, Hop, Stargate, Across, and Synaps
"""

create_premade_layout('pie-layout-1', final_data_list2)
"""
### Description  
The graph above shows the users of each bridge broken down by the chain where the bridge event strated. 
"""
