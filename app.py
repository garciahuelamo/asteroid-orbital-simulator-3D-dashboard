import streamlit as st
import pandas as pd

st.set_page_config(
    page_title='Asteroid Data Hub',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title('Asteroid Exploration Hub')

#Pages

hpage= st.Page('./streamlit/homepage.py', title='Homepage')
dashboard = st.Page('./streamlit/data_dashboard.py', title='Dashboard')
simulator = st.Page('./streamlit/simulator.py', title='Orbital Simulator 3D')

pg = st.navigation([hpage, dashboard, simulator])

pg.run()