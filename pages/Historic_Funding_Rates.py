from scripts.fetch_data import fetch_historic_funding
import streamlit as st
import plotly.express as px 
df = fetch_historic_funding()

st.write(df)

fig1 = px.line(df,y=df['fundingRate'],title = "Historic Funding Rates")
fig1.update_layout(xaxis_title='Date', yaxis_title='Funding Rate (%)')
st.plotly_chart(fig1)