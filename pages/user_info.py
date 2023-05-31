from scripts.fetch_data import fetch_positions,fetch_open_orders
import streamlit as st
st.warning("This page is currently under maintenance ")
c1,c2 = st.columns(2)
c2.markdown("Glossary:")
c2.markdown("sz = Size")
c2.markdown("limitpx = Limit Price")
c2.markdown("side = If long or short where A stands for ask (short) and B stands for Bid (long)")
            
lookup = c1.text_input(label="Enter Address below",placeholder="0x00")
c1.header("Open Positions")
c1.write(fetch_positions(lookup=lookup))

c1.header("Open Orders")
c1.write(fetch_open_orders(lookup=lookup))
