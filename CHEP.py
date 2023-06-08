import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Cairns Hospital Data Analysis', layout='wide')

chep = './data/CHEP.csv'

CHEP = chep.drop('img', axis =1)


with st.container():
    st.dataframe(CHEP, use_container_width=True)
    chep_pcm = px.parallel_coordinates(CHEP, CHEP.columns, color="in:WWR",
                                       labels={"in:ShadeDepth": "in:ShadeDepth"},
                                       color_continuous_scale=px.colors.diverging.Tealrose,
                                       color_continuous_midpoint=2)
    chep_pcm.update_layout(coloraxis_showscale=False)
         
    st.plotly_chart(chep_pcm, use_container_width=True)
    
    
    chep_bx_01 = px.box(CHEP, CHEP["in:WWR"], CHEP["out:EUI(kWh/m2)"], "in:WWR", labels = {"in:WWR":"WWR","out:EUI(kWh/m2)": "EUI(kWh/m2)"}, notched = True)
    chep_bx_02 = px.box(CHEP, CHEP["in:ShadeDepth"], CHEP["out:EUI(kWh/m2)"], "in:ShadeDepth", labels = {"in:ShadeDepth":"ShadeDepth", "out:EUI(kWh/m2)":"EUI(kWh/m2)"}, notched = True)
    chep_bx_03 = px.box(CHEP, CHEP["in:SHGC/VLT"], CHEP["out:EUI(kWh/m2)"], "in:SHGC/VLT", labels = {"in:SHGC/VLT":"SHGC/VLT", "out:EUI(kWh/m2)":"EUI(kWh/m2)"}, notched = True)
    chep_bx_04 = px.box(CHEP, CHEP["in:ExWall"], CHEP["out:EUI(kWh/m2)"], "in:ExWall", labels = {"in:ExWall":"ExWall", "out:EUI(kWh/m2)":"EUI(kWh/m2)"}, notched = True)
    
    
    
    cols = st.columns(4)
    
    with cols[0]:
        st.plotly_chart(chep_bx_01, use_container_width=True)
    with cols[1]:
        st.plotly_chart(chep_bx_02, use_container_width=True)
    with cols[2]:
        st.plotly_chart(chep_bx_03, use_container_width=True)
    with cols[3]:
        st.plotly_chart(chep_bx_04, use_container_width=True)
    
    
    chep_bx_05 = px.box(CHEP, CHEP["in:ExWall"], CHEP['out:Average DA'], "in:ExWall", labels = {"in:ExWall":"ExWall", 'out:Average DA':"Average DA"}, notched = True)
    chep_bx_06 = px.box(CHEP, CHEP["in:ShadeDepth"], CHEP['out:Average DA'], "in:ShadeDepth", labels = {"in:ShadeDepth":"ShadeDepth", 'out:Average DA':"Average DA"}, notched = True)
    chep_bx_07 = px.box(CHEP, CHEP["in:SHGC/VLT"], CHEP['out:Average DA'], "in:SHGC/VLT", labels = {"in:SHGC/VLT":"SHGC/VLT", 'out:Average DA':"Average DA"}, notched = True)
    chep_bx_08 = px.box(CHEP, CHEP["in:ExWall"], CHEP['out:Average DA'], "in:ExWall", labels = {"in:ExWall":"ExWall", 'out:Average DA':"Average DA"}, notched = True)
    
    cols = st.columns(4)
    
    with cols[0]:
        st.plotly_chart(chep_bx_05, use_container_width=True)
    with cols[1]:
        st.plotly_chart(chep_bx_06, use_container_width=True)
    with cols[2]:
        st.plotly_chart(chep_bx_07, use_container_width=True)
    with cols[3]:
        st.plotly_chart(chep_bx_08, use_container_width=True)
    
    chep_bx_09 = px.box(CHEP, CHEP["in:ExWall"], CHEP['out:Total KgCO2e'], "in:ExWall", labels = {"in:ExWall":"ExWall", 'out:Total KgCO2e':"Total KgCO2e"}, notched = True)
    chep_bx_10 = px.box(CHEP, CHEP["in:ShadeDepth"], CHEP['out:Total KgCO2e'], "in:ShadeDepth", labels = {"in:ShadeDepth":"ShadeDepth", 'out:Total KgCO2e':"Total KgCO2e"}, notched = True)
    chep_bx_11 = px.box(CHEP, CHEP["in:SHGC/VLT"], CHEP['out:Total KgCO2e'], "in:SHGC/VLT", labels = {"in:SHGC/VLT":"SHGC/VLT", 'out:Total KgCO2e':"Total KgCO2e"}, notched = True)
    chep_bx_12 = px.box(CHEP, CHEP["in:ExWall"], CHEP['out:Total KgCO2e'], "in:ExWall", labels = {"in:ExWall":"ExWall", 'out:Total KgCO2e':"Total KgCO2e"}, notched = True)
    
    cols = st.columns(4)
    
    with cols[0]:
        st.plotly_chart(chep_bx_09, use_container_width=True)
    with cols[1]:
        st.plotly_chart(chep_bx_10, use_container_width=True)
    with cols[2]:
        st.plotly_chart(chep_bx_11, use_container_width=True)
    with cols[3]:
        st.plotly_chart(chep_bx_12, use_container_width=True)
        
        
        
