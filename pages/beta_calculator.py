import streamlit as st
from scripts.beta import *

st.header("How To Use")
st.markdown("""
To use this tool simply enter a date range for the data and 2 tickers, usually ticker 1 would be something like SPY or BTC and ticker 2 is the "riskier" asset.
Data is taken from yahoo finance so you'll need to use the same ticker formats as they use eg for crypto add "-USD" suffix.

""")


c1,c2 = st.columns(2)
start_date = c1.text_input(label="Start Date",placeholder="2023-01-01")
end_date = c2.text_input(label="End Date",placeholder="2023-05-09")
token1 = c1.text_input(label="ticker 1",placeholder="BTC-USD")
token2 = c2.text_input(label="ticker 2",placeholder="SOL-USD")

if len(start_date and end_date and token1 and token2) != 0:
    beta=beta_calculator(start_date = start_date,end_date =end_date,ticker_1=token1,ticker_2=token2).calc_beta()
    st.write(f"Beta = {beta}")
   