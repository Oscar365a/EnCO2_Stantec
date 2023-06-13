import streamlit as st
import pandas as pd
import plotly.express as px
from os import listdir
from PIL import Image
import numpy as np


st.set_page_config(page_title='CAIRNS Hospital Data Analysis', layout='wide')

CHEP_en = pd.read_csv('./data/Energy.csv')

#CHEP_en = pd.read_csv(r'C:\Users\atabadkani\Streamlit Apps\CHEP\data\Energy.csv')

st.title("Cairns Hospital Parametric Analysis")

with st.sidebar:
    
    st.title('Choose the Design Inputs:')
    
    WWR_NS = st.select_slider('Window-to-Wall Ratio (North-South):', options = [25, 50, 75], value = 50, key = 'WWR_NS')
    WWR_EW = st.select_slider('Window-to-Wall Ratio (East-West):', options = [25, 50, 75], value = 50, key = 'WWR_EW')
    Shade_dep = st.select_slider('Shade Depth (mm):', options = [0, 300, 600], value = 300, key = 'shadedepth')
    Shade_ori = st.select_slider('Shade Orientation (0:V, 1:H):', options = [0, 1], value = 0, key = 'shadeori')
    SHGC_VLT = st.select_slider('SHGV/VLT:', options = ['0.22/30','0.45/50','0.7/65'], value = '0.45/50', key = 'glass_shgc')
    exwall = st.select_slider('External Wall R-value:', options = [1.0,1.4], value = 1.4, key = 'exwall_r')
    
    
with st.container():
     
    st.header('Design Summary')
    
    def get_metrics():
       
        CHEP_en_RESULT = CHEP_en[CHEP_en['WWR-NS'].isin([WWR_NS]) & CHEP_en['WWR-EW'].isin([WWR_EW]) & CHEP_en['ShadeDepth'].isin([Shade_dep]) & 
                         CHEP_en['ShadeOrientation (0:V, 1:H)'].isin([Shade_ori]) & CHEP_en['SHGC/VLT'].isin([SHGC_VLT]) & CHEP_en['ExWall'].isin([exwall])]
        
        EUI_METRIC = CHEP_en_RESULT['EUI(kWh/m2)']
        NORM_HVAC = CHEP_en_RESULT['Normalized HVACp (W/m2)']
        AVE_DA =  CHEP_en_RESULT['Average DA']
        AVE_UDI = CHEP_en_RESULT['Average UDI']
        ENERGY = CHEP_en_RESULT['Energy Cost ($ kWh/yr)']
        PATIENT_NORTH_OT = CHEP_en_RESULT['OT27% - Patient North']
        PATIENT_SOUTH_OT = CHEP_en_RESULT['OT27% - Patient South']
        image = CHEP_en_RESULT['img']
        
        return EUI_METRIC, NORM_HVAC, AVE_DA, AVE_UDI, ENERGY, PATIENT_NORTH_OT, PATIENT_SOUTH_OT, image
            
    
        
    cols = st.columns(9)
    with cols[0]:
        ""
    with cols[1]:
        st.metric('EUI(kWh/m2)', get_metrics()[0])
    with cols[2]:
        st.metric('HVACp (W/m2)', get_metrics()[1])
    with cols[3]:
        st.metric('Average DA% (500lx)', get_metrics()[2])
    with cols[4]:
        st.metric('Average UDI% (>10000lx)', get_metrics()[3])
    with cols[5]:
        st.metric('Cost ($ kWh/yr)', get_metrics()[4])
    with cols[6]:
        st.metric('Patient North% (> OT 27C)', get_metrics()[5])
    with cols[7]:
        st.metric('Patient South% (> OT 27C)', get_metrics()[6])
    with cols[8]:
        ""
        
    def loadImages():
      
        img = Image.open(f'.data/images/{get_metrics()[7].iloc[0]}')
    
        return img
    
    col1,col2,col3 = st.columns([1.5,4,0.5])
    
    with col1:
        ""
    with col2:
        st.image(loadImages(), caption='Selected Design Iteration', use_column_width = False)
    
    
    
    st.subheader("**Design Inputs vs. Operational Building Performance**")

    chep_pcm = px.parallel_coordinates(CHEP_en, CHEP_en.columns, color="EUI(kWh/m2)",
                                       labels={"ShadeDepth": "ShadeDepth", "ExWall":"ExWall"},
                                       color_continuous_scale=px.colors.cyclical.Edge,
                                       color_continuous_midpoint=2, height = 650)
    
    chep_pcm.update_layout(coloraxis_showscale=False)
         
    st.plotly_chart(chep_pcm, use_container_width=True)
   
    chep_bx_01 = px.box(CHEP_en, CHEP_en["WWR-NS"], CHEP_en["EUI(kWh/m2)"], "WWR-NS", notched = True)
    chep_bx_02 = px.box(CHEP_en, CHEP_en["WWR-EW"], CHEP_en["EUI(kWh/m2)"], "WWR-EW", notched = True)
    chep_bx_03 = px.box(CHEP_en, CHEP_en["ShadeDepth"], CHEP_en["EUI(kWh/m2)"], "ShadeDepth", notched = True)
    chep_bx_04 = px.box(CHEP_en, CHEP_en["SHGC/VLT"], CHEP_en["EUI(kWh/m2)"], "SHGC/VLT", notched = True)
    chep_bx_05 = px.box(CHEP_en, CHEP_en["ExWall"], CHEP_en["EUI(kWh/m2)"], "ExWall", notched = True)
    chep_bx_06 = px.box(CHEP_en, CHEP_en["ShadeOrientation (0:V, 1:H)"], CHEP_en["EUI(kWh/m2)"], "ShadeOrientation (0:V, 1:H)", notched = True)
    
    cols = st.columns(6)
    
    with cols[0]:
        st.plotly_chart(chep_bx_01, use_container_width=True)
    with cols[1]:
        st.plotly_chart(chep_bx_02, use_container_width=True)
    with cols[2]:
        st.plotly_chart(chep_bx_03, use_container_width=True)
    with cols[3]:
        st.plotly_chart(chep_bx_04, use_container_width=True)
    with cols[4]:
        st.plotly_chart(chep_bx_05, use_container_width=True)
    with cols[5]:
        st.plotly_chart(chep_bx_06, use_container_width=True)

    chep_bx_07 = px.box(CHEP_en, CHEP_en["WWR-NS"], CHEP_en["Average DA"], "WWR-NS", notched = True)
    chep_bx_08 = px.box(CHEP_en, CHEP_en["WWR-EW"], CHEP_en["Average DA"], "WWR-EW", notched = True)
    chep_bx_09 = px.box(CHEP_en, CHEP_en["ShadeDepth"], CHEP_en['Average DA'], "ShadeDepth",  notched = True)
    chep_bx_10 = px.box(CHEP_en, CHEP_en["SHGC/VLT"], CHEP_en['Average DA'], "SHGC/VLT",  notched = True)
    chep_bx_11 = px.box(CHEP_en, CHEP_en["ExWall"], CHEP_en['Average DA'], "ExWall", notched = True)
    chep_bx_12 = px.box(CHEP_en, CHEP_en["ShadeOrientation (0:V, 1:H)"], CHEP_en['Average DA'], "ShadeOrientation (0:V, 1:H)",notched = True)
    
    cols = st.columns(6)
    
    with cols[0]:
        st.plotly_chart(chep_bx_07, use_container_width=True)
    with cols[1]:
        st.plotly_chart(chep_bx_08, use_container_width=True)
    with cols[2]:
        st.plotly_chart(chep_bx_09, use_container_width=True)
    with cols[3]:
        st.plotly_chart(chep_bx_10, use_container_width=True)
    with cols[4]:
        st.plotly_chart(chep_bx_11, use_container_width=True)
    with cols[5]:
        st.plotly_chart(chep_bx_12, use_container_width=True)
        

epic = pd.DataFrame(pd.read_excel('./data/EPiC.xlsx'))

       
def get_index(df) -> dict:
        dict_ = {df['Version: EPiC Database 2019'].iloc[i]: i for i in range(0, len(df['Version: EPiC Database 2019']))}
        return dict_

with st.sidebar:
    
    st.title('Choose the Material Type:')
    
    concrete = epic[epic['Version: EPiC Database 2019'].str.contains('Concrete|AAC')]
    concrete = concrete[concrete['Functional unit'] !='no.']
    concrete_type = concrete['Version: EPiC Database 2019'].iloc[:]
    
    concrete_selection = st.selectbox('Concrete:', options=concrete_type, key='concrete', index = 2)   
    concrete_unit = concrete['Functional unit'].iloc[int(get_index(concrete)[concrete_selection])]
    concrete_em = concrete['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(concrete)[concrete_selection])]
    st.markdown(f'**Unit: {concrete_unit} | Emission Factor (kgCO₂e): {concrete_em}**')
    concerte_density = st.number_input('Concrete Density', min_value=100, max_value=3000, value = 2300)

    
    PB = epic[epic['Version: EPiC Database 2019'].str.contains('Plaster|plaster')]
    PB = PB[PB['Functional unit'] !='no.']
    PB_type = PB['Version: EPiC Database 2019'].iloc[:]
    
    PB_selection = st.selectbox('Plaster Board:', options=PB_type, key='PB', index = 1)    
    PB_unit = PB['Functional unit'].iloc[int(get_index(PB)[PB_selection])]
    PB_em = PB['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(PB)[PB_selection])]
    st.markdown(f'**Unit: {PB_unit} | Emission Factor (kgCO₂e): {PB_em}**')
    PB_density = st.number_input('Plaster Board Density', min_value=50, max_value=1500, value = 700)

    Glass = epic[epic['Version: EPiC Database 2019'].str.contains('glazing')]
    Glass = Glass[Glass['Functional unit'] !='no.']
    Glass_type = Glass['Version: EPiC Database 2019'].iloc[:]
    
    Glass_selection = st.selectbox('Glass Type:', options=Glass_type, key='Glass', index = 1)
    Glass_unit = Glass['Functional unit'].iloc[int(get_index(Glass)[Glass_selection])]
    Glass_em = Glass['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(Glass)[Glass_selection])]
    st.markdown(f'**Unit: {Glass_unit} | Emission Factor (kgCO₂e): {Glass_em}**')
    
    # insul = epic[epic['Version: EPiC Database 2019'].str.contains('insulation')]
    # insul = insul[insul['Functional unit'] !='no.']
    # insul_type = insul['Version: EPiC Database 2019'].iloc[:]
    
    # insul_selection = st.selectbox('Insulation Type:', options=insul_type, key='insul', index = 1)
    # insul_unit = insul['Functional unit'].iloc[int(get_index(insul)[insul_selection])]
    # insul_em = insul['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(insul)[insul_selection])]
    # st.markdown(f'Unit: {insul_unit} | Emission Factor (kgCO₂e): {insul_em}')
    
    alum = epic[epic['Version: EPiC Database 2019'].str.contains('Aluminium')]
    alum = alum[alum['Functional unit'] !='no.']
    alum_type = alum['Version: EPiC Database 2019'].iloc[:]
    
    alum_selection = st.selectbox('Aluminium Type:', options=alum_type, key='alum', index = 20)
    alum_unit = alum['Functional unit'].iloc[int(get_index(alum)[alum_selection])]
    alum_em = alum['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(alum)[alum_selection])]
    st.markdown(f'**Unit: {alum_unit} | Emission Factor (kgCO₂e): {alum_em}**')
    
    
with st.sidebar:
    Floor_area = 2310.5  ##########
    
    st.title('Choose the Grid Emission Scenario:')
    
    scenario = st.selectbox('Scenario:', options=['Scenario One', 'Scenario Two'], key='grid')
    
    num_years = st.number_input('Years to Predict WoL:', min_value=1, max_value=20, value = 7)
    
    def ln(x):
        n = 1000.0
        return n * ((x ** (1/n)) - 1)

    if scenario == 'Scenario One':
        grid_factor = (ln(num_years)*-0.147) + 0.9121
    
    elif scenario == 'Scenario Two':
        grid_factor = (ln(num_years)*-0.309) + 0.9413
    
    st.markdown(f'**Grid Emission Factor is {round(grid_factor,2)}.**')
    
with st.container():
    
    st.subheader("**Design Inputs vs. Building Whole of Life Performance**")

    chep_co2 = pd.read_csv('./data/CO2.csv')
    
    CHEP_co2 = chep_co2.drop('img', axis =1)  
    
    concrete_calc = []
    PB_calc = []
    Glass_calc = []
    alum_calc  = []
    
    
    for i in range(0, len(CHEP_co2)):
        if concrete_unit == 'm³':
            concrete_vol = CHEP_co2['Concrete m3'].iloc[i]*concrete_em
            concrete_calc.append(concrete_vol)
        elif concrete_unit == 'kg':
            concrete_ = concrete_em*concerte_density
            concrete_vol = CHEP_co2['Concrete m3'].iloc[i]*concrete_
            concrete_calc.append(concrete_vol)
        if  PB_unit == 'm²':
            if PB_selection == 'Plasterboard - 10 mm':
                PB_1m = 1/0.01
                PB_ = PB_1m*PB_em
                PB_vol = CHEP_co2['PB m3'].iloc[i]*PB_
                PB_calc.append(PB_vol)
            elif PB_selection == 'Plasterboard - 13 mm':
                PB_1m = 1/0.013
                PB_ = PB_1m*PB_em
                PB_vol = CHEP_co2['PB m3'].iloc[i]*PB_
                PB_calc.append(PB_vol)
        elif PB_unit == 'kg':
                PB_ = PB_em*PB_density
                PB_vol = CHEP_co2['PB m3'].iloc[i]*PB_
                PB_calc.append(PB_vol)
        if Glass_unit == 'm²':
            Glass_vol = CHEP_co2['Glass Area m2'].iloc[i]*Glass_em
            Glass_calc.append(Glass_vol)
        if alum_unit == 'm²':
            alum_vol = CHEP_co2['Shades Area m2'].iloc[i]*alum_em
            alum_calc.append(alum_vol)
    
    calc_df_raw = pd.DataFrame([concrete_calc , PB_calc,Glass_calc,alum_calc])
    calc_df = calc_df_raw.transpose()
    calc_df = calc_df.rename(columns={0:'concrete_calc', 1:'PB_calc',2:'Glass_calc',3:'alum_calc'})
    calc_df['Total'] = calc_df['concrete_calc']+calc_df['PB_calc']+calc_df['Glass_calc']+calc_df['alum_calc']
    
    CHEP_co2['WoL'] = ((CHEP_co2['EUI (kWh/m2)'].iloc[i]*Floor_area*grid_factor*num_years)+round(calc_df['Total'],2))
    
    chep_pcm_co = px.parallel_coordinates(CHEP_co2, ['WWR-NS', 'WWR-EW', 'ShadeDepth', 'ShadeOrientation (0:V, 1:H)',
       'SHGC/VLT', 'ExWall', 'WoL','EUI (kWh/m2)'], color='EUI (kWh/m2)',
                                        labels={"ShadeDepth": "ShadeDepth", "ExWall":"ExWall"},
                                        color_continuous_scale=px.colors.cyclical.HSV,
                                        color_continuous_midpoint=100, height = 650)

    
    
    chep_pcm_co.update_layout(coloraxis_showscale=False)
         
    st.plotly_chart(chep_pcm_co, use_container_width=True)

with st.container():
    chep_bx_13 = px.box(CHEP_co2, CHEP_co2["WWR-NS"], CHEP_co2['WoL'], "WWR-NS", notched = True)
    chep_bx_14 = px.box(CHEP_co2, CHEP_co2["WWR-EW"], CHEP_co2['WoL'], "WWR-EW", notched = True)
    chep_bx_15 = px.box(CHEP_co2, CHEP_co2["ShadeDepth"], CHEP_co2['WoL'], "ShadeDepth",  notched = True)
    chep_bx_16 = px.box(CHEP_co2, CHEP_co2["SHGC/VLT"], CHEP_co2['WoL'], "SHGC/VLT",notched = True)
    chep_bx_17 = px.box(CHEP_co2, CHEP_co2["ExWall"], CHEP_co2['WoL'], "ExWall", notched = True)
    chep_bx_18 = px.box(CHEP_co2, CHEP_co2["ShadeOrientation (0:V, 1:H)"], CHEP_co2['WoL'], "ShadeOrientation (0:V, 1:H)", notched = True)
        
    cols = st.columns(6)
    
    with cols[0]:
        st.plotly_chart(chep_bx_13, use_container_width=True)
    with cols[1]:
        st.plotly_chart(chep_bx_14, use_container_width=True)
    with cols[2]:
        st.plotly_chart(chep_bx_15, use_container_width=True)
    with cols[3]:
        st.plotly_chart(chep_bx_16, use_container_width=True)
    with cols[4]:
        st.plotly_chart(chep_bx_17, use_container_width=True)
    with cols[5]:
        st.plotly_chart(chep_bx_18, use_container_width=True)  
        
        
