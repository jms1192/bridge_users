from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import requests
import plotly.express as px



def create_premade_layout123(layout, data_link, type = ''):

    data = requests.get(data_link).json()

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
            [sum(vol_data[x]) for x in vol_data],
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
            [sum(vol_data[x]) for x in vol_data],
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





## sort all TVL data here 
tvl_api_list = [ 
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/fdf997c5-7919-457d-9a1d-1e00d9893417/data/latest', 'Bridge':'Stargate', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/83dc8c1c-c201-4db8-ae5f-f09a018b622b/data/latest', 'Bridge':'Stargate', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/be86d39e-03cd-4e64-ac15-fb73a1d465a9/data/latest', 'Bridge':'Stargate', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/921cb1e3-ac92-44b1-abd6-7fa3a28a0103/data/latest', 'Bridge':'Stargate', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/94e61d0e-94fe-4106-b0de-dbd6aed26870/data/latest', 'Bridge':'Stargate', 'Chain':'Arbitrum'},

    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/fdf997c5-7919-457d-9a1d-1e00d9893417/data/latest', 'Bridge':'Hop', 'Chain':'Ethereum'},
   
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/14a003fa-2d2c-4230-9097-1ed9093b12a0/data/latest', 'Bridge':'Hyphen', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/0e4e52c4-2446-41a3-a1a9-1903ea40e886/data/latest', 'Bridge':'Hyphen', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/d1db5ed3-9354-49d2-aedf-181427250e61/data/latest', 'Bridge':'Hyphen', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/9e8066c8-1021-4dc8-80d6-97573b725910/data/latest', 'Bridge':'Hyphen', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/1bf70037-576f-424d-8c5e-22728d7ff6d3/data/latest', 'Bridge':'Hyphen', 'Chain':'Arbitrum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/6a1c0cd6-ace1-4b8b-a585-9d1083df9c2f/data/latest', 'Bridge':'Hyphen', 'Chain':'BSC'}
]

full_tvl_list = []
for api in tvl_api_list:
    api_data_clean = sort_flipside_api(api['link'], api['Bridge'], 'TVL', api['Chain'])
    for x in api_data_clean:
        full_tvl_list.append(x)

#print(full_tvl_list)


## sort all TVL data here
volume_api_list = [ 
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/fad87264-e207-450c-a6a7-3f1cd9b850f8/data/latest', 'Bridge':'Stargate', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/127bf7b1-6e8a-491c-85be-aae215d2ba56/data/latest', 'Bridge':'Stargate', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/af4d778d-859d-481c-81ea-64a0a84737ca/data/latest', 'Bridge':'Stargate', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/29177db5-4586-431d-b79f-1ed26733f8be/data/latest', 'Bridge':'Stargate', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/80a333e4-7157-4325-ae2e-93943b3d63c6/data/latest', 'Bridge':'Stargate', 'Chain':'Arbitrum'},

    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/6434d3e9-8b87-4e74-9897-2c1eeb0d98a2/data/latest', 'Bridge':'Hop', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/28afb7ab-1233-4a14-b585-5cdb95de8f13/data/latest', 'Bridge':'Hop', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/5153b9b4-2f3b-4ebc-a427-bebcab17dce5/data/latest', 'Bridge':'Hop', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/29177db5-4586-431d-b79f-1ed26733f8be/data/latest', 'Bridge':'Hop', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/35c12ff9-e958-4e15-9675-0d655aae0303/data/latest', 'Bridge':'Hop', 'Chain':'Arbitrum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/46c97449-588d-4584-9bd0-0f6e9cc572c7/data/latest', 'Bridge':'Hop', 'Chain':'Gnosis'},

    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/65a56a90-a54a-4624-b530-3d023a062db3/data/latest', 'Bridge':'Hyphen', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/a5ffae8b-a01d-4ef1-8ff3-0001833f4f20/data/latest', 'Bridge':'Hyphen', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/0f7b41eb-2190-4f27-92b8-f0f92690cf86/data/latest', 'Bridge':'Hyphen', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/ba6fe0cf-0dbd-45e8-825a-86d94d367350/data/latest', 'Bridge':'Hyphen', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/617d10fc-1b43-4e05-9298-832ebebf2884/data/latest', 'Bridge':'Hyphen', 'Chain':'Arbitrum'},
    #{'link':'https://node-api.flipsidecrypto.com/api/v2/queries/46c97449-588d-4584-9bd0-0f6e9cc572c7/data/latest', 'Bridge':'Hyphen', 'Chain':'Gnosis'},


    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/6454ca7c-ae9c-417f-b04f-94b93a2037ab/data/latest', 'Bridge':'Synapse', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/17c9a813-3852-4763-b170-663ad644d009/data/latest', 'Bridge':'Synapse', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/f48dfb62-f170-4e90-b7ba-f67c53893be0/data/latest', 'Bridge':'Synapse', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/e01a1cb8-c265-4b00-bdd6-50c52886862a/data/latest', 'Bridge':'Synapse', 'Chain':'Avalanche'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/1f68ee80-0c70-4a42-ac06-813f3b3947b2/data/latest', 'Bridge':'Synapse', 'Chain':'Arbitrum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/5133379d-2864-46c8-b675-7c6b3ded7ca1/data/latest', 'Bridge':'Synapse', 'Chain':'BSC'},

    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/d70c08e6-6ef0-4d4b-92df-5f47c9e23765/data/latest', 'Bridge':'Across', 'Chain':'Optimism'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/33f8cfca-047b-4fc4-bc6d-1c300f76e6ad/data/latest', 'Bridge':'Across', 'Chain':'Ethereum'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/a2df7f86-560a-4d3a-9ab9-296f553f0fdd/data/latest', 'Bridge':'Across', 'Chain':'Polygon'},
    {'link':'https://node-api.flipsidecrypto.com/api/v2/queries/0921fa72-ea81-401f-832a-2c4eea1a71d9/data/latest', 'Bridge':'Across', 'Chain':'Arbitrum'}
]

full_volume_list = []
for api in volume_api_list:
    api_data_clean = sort_flipside_api(api['link'], api['Bridge'], 'VOLUME', api['Chain'])
    for x in api_data_clean:
        full_volume_list.append(x)

#for x in full_volume_list:
    #print(x)
    #print(type(x['VOLUME']))
    #data12 = 1 + x['VOLUME'] 
#    if isinstance(x['VOLUME'], float):
#        x['VOLUME'] = int(x['VOLUME'])
#    elif x['VOLUME'] == None:
#        x['VOLUME'] = 0

#### start here turn volume list to graph list  
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

final_data_list1 = sorted(final_data_list1, key=lambda  x:(x['ASSET'], x['DAY'])) 
final_data_list2 = sorted(final_data_list2, key=lambda  x:(x['BIG_CATEGORY']), reverse=True) 
#print(final_data_list)

create_premade_layout('2d-layout-1', final_data_list1)
create_premade_layout('pie-layout-1', final_data_list2)
