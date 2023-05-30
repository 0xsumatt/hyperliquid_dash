import httpx

import streamlit as st

import pandas as pd


url = "https://api.hyperliquid.xyz/info"
headers = {"Content-Type": "application/json"}

def fetch_apr():
    
    data = {"type": "vaults"}
    client = httpx.Client()
    req = client.post(url, headers=headers, json=data).json()
    df = pd.DataFrame(req)
    df_refined = df[["name", "apr"]].astype({"name": "string", "apr": "float64"})
    client.close()
    return df_refined

def fetch_tvl():
    client = httpx.Client()
    url = "https://api.llama.fi/updatedProtocol/hyperliquid"
    fetch_info = client.get(url).json()['chainTvls']['Arbitrum']['tvl']
    df = pd.DataFrame(fetch_info)
    df['date'] = pd.to_datetime(df['date'], unit='s').dt.strftime('%Y-%m-%d')
    df['totalLiquidityUSD'] = df['totalLiquidityUSD'].astype(float)
    
    client.close()
    return df

def fetch_vault_roi():
    client = httpx.Client()
    data = {"type": "vaults"}
    req = client.post(url, headers=headers, json=data).json()
    df = pd.DataFrame(req)
    refined_df = df[["name", "roi"]].astype({"name": "string", "roi": "float64"})
    client.close()
    return refined_df

def fetch_funding_rates():
    client = httpx.Client()
    data = {"type": "metaAndAssetCtxs"}
    req = client.post(url= url, headers=headers, json=data).json()
    # Extract 'ame values dynamically from the first item of the list in the response
    token_names = [item['name'] for item in req[0]['universe']]
    # Extract funding rates for each token in name
    new_dict = {
        'Token Name': token_names,
        'Funding Rate': [float(item['funding']) * 100 for item in req[1]],
        'Open Interest (in token)': [float(item['openInterest']) for item in req[1]]
    }
    rates_df = pd.DataFrame(new_dict).astype({"Token Name": "string", "Funding Rate": "float64", "Open Interest (in token)": "float64"})
    
    # Set index to 'Token Name' and transpose the DataFrame
    rates_df = rates_df.set_index('Token Name').T
    
    client.close()
    return rates_df
    

def fetch_positions(lookup):
    if len(lookup) != 0:
        client = httpx.Client()
        data = {
            "type": "clearinghouseState",
            "user": lookup
        }

        req = client.post(url=url, headers=headers, json=data).json()['assetPositions']
        positions_list = []

        for position in req:
            try:
                entry_px = position["position"]["entryPx"]

                if entry_px and entry_px != '0.0':
                    coin = position["position"]["coin"]
                    liquidation_px = position["position"]["liquidationPx"]
                    position_value = position["position"]["positionValue"]
                    unrealized_pnl = position["position"]["unrealizedPnl"]

                    position_dict = {
                        "Coin": coin,
                        "Entry Price": float(entry_px),
                        "liquidation Price": float(liquidation_px) if liquidation_px and liquidation_px != '0.0' else None,
                        "Position Value": float(position_value) if position_value and position_value != '0.0' else None,
                        "Unrealized Pnl": float(unrealized_pnl) if unrealized_pnl and unrealized_pnl != '0.0' else None
                    }
                    positions_list.append(position_dict)

            except KeyError :
                st.write("No Positions Found")

        df = pd.DataFrame(positions_list).astype({
            "Coin": "string",
            "Entry Price": "float64",
            "liquidation Price": "float64",
            "Position Value": "float64",
            "Unrealized Pnl": "float64",
        })

        client.close()
        return df

def fetch_open_orders(lookup):
    if len(lookup) != 0:
        data = {
            "type": "openOrders",
            "user": lookup
        }

        req = httpx.post(url=url, headers=headers, json=data).json()

        if not req:
            st.header("no open orders")
        else:
            df = pd.DataFrame(req)
            df["timestamp"] = pd.to_datetime(df["timestamp"] / 1000, unit="s").dt.strftime("%Y-%m-%d %H:%M:%S")
            df_dtype = df.astype({
                "timestamp": "string",
                "coin": "string",
                "limitPx": "float64",
                "oid": "Int64",
                "side": "string",
                "sz": "float64",
            })

            return df_dtype
   
   

def fetch_historic_funding():
    client = httpx.Client()
    data = {"type":"meta"}
    
    init_req = client.post(url=url,headers=headers,json=data).json()
    token_names = [item['name'] for item in init_req['universe']]
    option = st.selectbox("Select a Coin",token_names)


    hist_data = {
        "type":"fundingHistory",
        "coin":option,
        "startTime":1684512000000
        }
    get_hist_rate = client.post(url=url,headers=headers,json= hist_data).json()
    import pandas as pd
    df = pd.DataFrame(get_hist_rate)
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['time'] = df['time'].dt.floor('s')

    # Set 'time' as the index
    df.set_index('time', inplace=True)
    df =df.drop('coin',axis=1)
    client.close()
    return df