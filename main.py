import streamlit as st
from datetime import datetime
import plotly.express as px
from scripts.fetch_data import fetch_apr,fetch_tvl,fetch_vault_roi,fetch_funding_rates
from streamlit_autorefresh import st_autorefresh
import webbrowser

tvl = fetch_tvl()
vault_apr = fetch_apr()
vault_roi = fetch_vault_roi()

def main():
    st.set_page_config(
        layout = "wide",
        page_title='Home',
        page_icon="random"
    )

    refresh = st_autorefresh(60000)

    ct = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.write(ct)
    if st.button("Access Hyperliquid Alpha",type = "primary"):
        webbrowser.open_new_tab("https://app.hyperliquid.xyz/join/MATSUM")
    
    st.header("Overview")
    st.warning("This data is for educational purposes only")
    st.write("Data is taken from Defi Llama or queried from the HyperLiquid Api directly")
    st.write("TVL data is updated circa 00:00 (DL updates at this time)")
    st.header("Funding Rates")
    st.write(fetch_funding_rates())

    opt_menu = st.radio("View Vaults as",['APR',"ROI"])
    c1, c2= st.columns(2)
   

    fig1 = px.line(tvl,x = tvl['date'],y=tvl['totalLiquidityUSD'],labels={'x':'Date', 'y':'TVL (USD)'},title = "Total Value Locked")
    c1.plotly_chart(fig1,use_container_width=True)
    
   
    if opt_menu.lower() == "apr":
        fig2 = px.bar(vault_apr, x = vault_apr['name'],y = vault_apr['apr'], labels={'x':'Vault Name', 'y':'APR'},title = "Vault APR")
        c2.plotly_chart(fig2,use_container_width=True)

    if opt_menu.lower() == "roi":
        fig2 = px.bar(vault_roi, x = vault_roi['name'],y = vault_roi['roi'],labels={'x':'Vault Name', 'y':'ROI'},title = "Vault ROI")
        c2.plotly_chart(fig2,use_container_width=True)

    refresh
if __name__ == "__main__":
    main()