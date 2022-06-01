from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import requests
import plotly.express as px


def create_premade_layout(layout, data_link, type = ''):

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


"""
# Symmetric vs Asymmetric LPs

On THORChain, you are allowed to add liquidity in 1 of 3 ways: Rune-only, asset-only, or symmetric (both Rune + asset). What is the breakdown of liquidity being added, according to those categories? Are there any trends over time or by pool?
### What is Thorchain? 

Thorchain, which is built on the Cosmos blockchain, is a decentralized liquidity protocol that specializes in cross-chain connectivity, allowing traders to swap tokens between different networks. The native token of the Thorchain blockchian is RUNE.

### Methodology

- We are going to look at the total add liquidity events on Thorchain broken down by event type and liquidity pool.

- We are looking to see how Thorchain users have been providing liquidity in 2022. 

## Thorchain LP Metrics 

The graphs below show the weekly and total number of liquidity actions on Thorchain broken up by action type. In 2022 providing Rune-only to pools was the most popular way to provide liquidity. At the end of March there was a spike in asset-only LP actions and symmetric LP actions.   

"""

create_premade_layout('2d-layout-1', 'https://node-api.flipsidecrypto.com/api/v2/queries/57d05aaf-2994-4ad7-b310-005a6ad92c1f/data/latest')

"""
The figure below shows the LP volume breakdown by pool of the diffrent Thorchain liquidity actions. Nearly half of all Rune-only LP action volume have gone into the BTC.BTC and ETH.ETH pool, while nealy half of all asset-only deposits have gone into the TERRA.UST and the BNB.BUSD pool.  
"""
create_premade_layout('pie-layout-1', 'https://node-api.flipsidecrypto.com/api/v2/queries/513968aa-82a9-4448-b670-9466a13e6dd1/data/latest')
    
"""
## Conclusion

- In 2022 providing Rune-only liquidity has been the most popular way to provide liquidity on The Chain and asset-only liquidity seems to be the least popular way to provide liquidity.   

- People providing liquidity to in rune-only and asset-only liquidity pools seem to provide liquidity in very different ways. Most of the volume coming in rune-only are going to the BTC.BTC and the ETH.ETH pool and the assets only liquidity is coming in to the stablecoin pools TERRA.UST and BNB.BUSD. 

"""    

 
df = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(df.style.highlight_max(axis=0))
