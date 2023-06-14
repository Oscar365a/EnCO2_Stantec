import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image


st.set_page_config(page_title='Project Parametric Analysis', layout='wide')

CHEP_en = pd.read_csv('./data/Energy.csv')
epic = pd.DataFrame(pd.read_excel('./data/EPiC.xlsx'))
chep_co2 = pd.read_csv('./data/CO2.csv')

#CHEP_en = pd.read_csv(r'C:\Users\atabadkani\Streamlit Apps\CHEP\data\Energy.csv')
#epic = pd.DataFrame(pd.read_excel(r'C:\Users\atabadkani\Streamlit Apps\CHEP\data\EPiC.xlsx'))
#chep_co2 = pd.read_csv(r'C:\Users\atabadkani\Streamlit Apps\CHEP\data\CO2.csv')

st.title("Project Parametric Analysis - 324 Iterations")

with st.sidebar:
    
    st.title('Choose the Design Inputs:')
    
    WWR_NS = st.select_slider('Window-to-Wall Ratio (North-South):', options = [25, 50, 75], value = 50, key = 'WWR_NS')
    WWR_EW = st.select_slider('Window-to-Wall Ratio (East-West):', options = [25, 50, 75], value = 50, key = 'WWR_EW')
    Shade_dep = st.select_slider('Shade Depth (mm):', options = [0, 300, 600], value = 300, key = 'shadedepth')
    Shade_ori = st.select_slider('Shade Orientation (0=Vert, 1=Horiz):', options = [0, 1], value = 0, key = 'shadeori')
    SHGC_VLT = st.select_slider('SHGV/VLT:', options = ['0.22/30','0.45/50','0.7/65'], value = '0.45/50', key = 'glass_shgc')
    exwall = st.select_slider('External Wall R-value:', options = [1.0,1.4], value = 1.4, key = 'exwall_r')
    
    
with st.container():
     
    st.subheader('Design Selection Summary')
    
    def get_metrics_EUI():
       
        CHEP_en_RESULT = CHEP_en[CHEP_en['WWR-NS'].isin([WWR_NS]) & CHEP_en['WWR-EW'].isin([WWR_EW]) & CHEP_en['ShadeDepth'].isin([Shade_dep]) & 
                         CHEP_en['ShadeOrientation (0:V, 1:H)'].isin([Shade_ori]) & CHEP_en['SHGC/VLT'].isin([SHGC_VLT]) & CHEP_en['ExWall'].isin([exwall])]
        
        EUI_METRIC = CHEP_en_RESULT['EUI(kWh/m2)']
        NORM_HVAC = CHEP_en_RESULT['HVACp (W/m2)']
        AVE_DA =  CHEP_en_RESULT['Daylight Autonomy']
        AVE_UDI = CHEP_en_RESULT['Excessive Daylight']
        ENERGY = CHEP_en_RESULT['Energy Cost ($ kWh/yr)']
        PATIENT_NORTH_OT = CHEP_en_RESULT['OT27% - Patient North']
        PATIENT_SOUTH_OT = CHEP_en_RESULT['OT27% - Patient South']
        image = CHEP_en_RESULT['img']
        EUI_DtS = CHEP_en_RESULT['EUI(kWh/m2)|DtS']
        NORM_HVAC_DtS = CHEP_en_RESULT['HVACp(W/m2)|DtS']
        AVE_DA_DtS = CHEP_en_RESULT['DA|DtS']
        AVE_UDI_DtS = CHEP_en_RESULT['Excessive Daylight|DtS']
        
        return EUI_METRIC, NORM_HVAC, AVE_DA, AVE_UDI, ENERGY, PATIENT_NORTH_OT, PATIENT_SOUTH_OT, image,EUI_DtS,NORM_HVAC_DtS,AVE_DA_DtS,AVE_UDI_DtS
            
        
    cols = st.columns(9)
    with cols[0]:
        ""
    with cols[1]:
        st.metric('EUI(kWh/m2)', get_metrics_EUI()[0])
    with cols[2]:
        st.metric('HVACp (W/m2)', get_metrics_EUI()[1])
    with cols[3]:
        st.metric('Daylight Autonomy% (500lx)', get_metrics_EUI()[2])
    with cols[4]:
        st.metric('Excessive Daylight% (>10000lx)', get_metrics_EUI()[3])
    with cols[5]:
        st.metric('Cost ($ kWh/yr)', get_metrics_EUI()[4])
    with cols[6]:
        st.metric('Patient North% (> OT 27C)', get_metrics_EUI()[5])
    with cols[7]:
        st.metric('Patient South% (> OT 27C)', get_metrics_EUI()[6])
    with cols[8]:
        ""
        
    st.subheader('% Design Performance against DtS Case - (-) Saved (+) Wasted')
    cols = st.columns(6)
    
    with cols[0]:
        ""
    with cols[1]:
        st.metric('EUI(kWh/m2)', get_metrics_EUI()[8])
    with cols[2]:
        st.metric('HVACp (W/m2)', get_metrics_EUI()[9])
    with cols[3]:
        st.metric('Daylight Autonomy% (500lx)', get_metrics_EUI()[10])
    with cols[4]:
        st.metric('Excessive Daylight% (>10000lx)', get_metrics_EUI()[11])
    with cols[5]:
        ""
    
    def loadImages():
      
        #img = Image.open(rf'C:\Users\atabadkani\Streamlit Apps\CHEP\data\images\{get_metrics_EUI()[7].iloc[0]}')
        img = Image.open(f'./data/images/{get_metrics_EUI()[7].iloc[0]}')
        #dts = Image.open(r'C:\Users\atabadkani\Streamlit Apps\CHEP\data\images\WWR-NS1_WWR-EW1_ShadeDepth0_ShadeOrienation0_SHGCVLT1_ExWall0.png')
        dts = Image.open('./data/images/WWR-NS1_WWR-EW1_ShadeDepth0_ShadeOrienation0_SHGCVLT1_ExWall0.png')
        return img, dts
    
    col1,col2,col3,col4 = st.columns([1.5,4,0.5,4])
    
    with col1:
        ""
    with col2:
        st.image(loadImages()[0], caption='Selected Design Iteration', use_column_width = False)
    with col3:
        ""
    with col4:
        st.image(loadImages()[1], caption='DtS Reference Case', use_column_width = False)
    
    
    st.subheader("**Design Inputs vs. Operational Building Performance**")

    columns = ['WWR-NS', 'WWR-EW', 'ShadeDepth', 'ShadeOrientation (0:V, 1:H)',
       'SHGC/VLT', 'ExWall', 'EUI(kWh/m2)', 'HVACp (W/m2)',
       'Daylight Autonomy', 'Excessive Daylight', 'Energy Cost ($ kWh/yr)',
       'OT27% - Patient North', 'OT27% - Patient South']
    
    chep_pcm = px.parallel_coordinates(CHEP_en, columns, color="EUI(kWh/m2)",
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

    chep_bx_07 = px.box(CHEP_en, CHEP_en["WWR-NS"], CHEP_en["Daylight Autonomy"], "WWR-NS", notched = True)
    chep_bx_08 = px.box(CHEP_en, CHEP_en["WWR-EW"], CHEP_en["Daylight Autonomy"], "WWR-EW", notched = True)
    chep_bx_09 = px.box(CHEP_en, CHEP_en["ShadeDepth"], CHEP_en['Daylight Autonomy'], "ShadeDepth",  notched = True)
    chep_bx_10 = px.box(CHEP_en, CHEP_en["SHGC/VLT"], CHEP_en['Daylight Autonomy'], "SHGC/VLT",  notched = True)
    chep_bx_11 = px.box(CHEP_en, CHEP_en["ExWall"], CHEP_en['Daylight Autonomy'], "ExWall", notched = True)
    chep_bx_12 = px.box(CHEP_en, CHEP_en["ShadeOrientation (0:V, 1:H)"], CHEP_en['Daylight Autonomy'], "ShadeOrientation (0:V, 1:H)",notched = True)
    
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
        

    chep_bx_13 = px.box(CHEP_en, CHEP_en["WWR-NS"], CHEP_en["Excessive Daylight"], "WWR-NS", notched = True)
    chep_bx_14 = px.box(CHEP_en, CHEP_en["WWR-EW"], CHEP_en["Excessive Daylight"], "WWR-EW", notched = True)
    chep_bx_15 = px.box(CHEP_en, CHEP_en["ShadeDepth"], CHEP_en['Excessive Daylight'], "ShadeDepth",  notched = True)
    chep_bx_16 = px.box(CHEP_en, CHEP_en["SHGC/VLT"], CHEP_en['Excessive Daylight'], "SHGC/VLT",  notched = True)
    chep_bx_17 = px.box(CHEP_en, CHEP_en["ExWall"], CHEP_en['Excessive Daylight'], "ExWall", notched = True)
    chep_bx_18 = px.box(CHEP_en, CHEP_en["ShadeOrientation (0:V, 1:H)"], CHEP_en['Excessive Daylight'], "ShadeOrientation (0:V, 1:H)",notched = True)
    
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

       
def get_index(df) -> dict:
        dict_ = {df['Version: EPiC Database 2019'].iloc[i]: i for i in range(0, len(df['Version: EPiC Database 2019']))}
        return dict_


#Material Selection and Emission Calc

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

    Glass = epic[epic['Version: EPiC Database 2019'].str.contains('glazing | glass')]
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
    
    
#Scenario Type Selection

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
    
    CHEP_co2['Total kgCO2e'] = calc_df['Total']
    
    chep_pcm_co = px.parallel_coordinates(CHEP_co2, ['WWR-NS', 'WWR-EW', 'ShadeDepth', 'ShadeOrientation (0:V, 1:H)',
       'SHGC/VLT', 'ExWall', 'Total kgCO2e', 'WoL','EUI (kWh/m2)'], color='EUI (kWh/m2)',
                                        labels={"ShadeDepth": "ShadeDepth", "ExWall":"ExWall"},
                                        color_continuous_scale=px.colors.cyclical.HSV,
                                        color_continuous_midpoint=100, height = 650)

    
    
    chep_pcm_co.update_layout(coloraxis_showscale=False)
         
    st.plotly_chart(chep_pcm_co, use_container_width=True)

#DtS CO2 Calcs

DtS_Concrete = 1055.82 #####
DtS_Glasswool = 486 #####
DtS_PB = 164.11 #####
DtS_Glass = 541.94  #####
DtS_Shade = 0 #####
DtS_EUI = 84.31 #####

if concrete_unit == 'm³':
    concrete_calc_dts = DtS_Concrete*concrete_em
elif concrete_unit == 'kg':
    concrete_ = concrete_em*concerte_density
    concrete_calc_dts = DtS_Concrete*concrete_
if  PB_unit == 'm²':
    if PB_selection == 'Plasterboard - 10 mm':
        PB_1m = 1/0.01
        PB_ = PB_1m*PB_em
        PB_calc_dts = DtS_PB*PB_
    elif PB_selection == 'Plasterboard - 13 mm':
        PB_1m = 1/0.013
        PB_ = PB_1m*PB_em
        PB_calc_dts = DtS_PB*PB_
elif PB_unit == 'kg':
        PB_ = PB_em*PB_density
        PB_calc_dts = DtS_PB*PB_
if Glass_unit == 'm²':
    Glass_calc_dts = DtS_Glass*Glass_em
if alum_unit == 'm²':
    alum_calc_dts = DtS_Shade*alum_em

embodied_dts = concrete_calc_dts+PB_calc_dts+Glass_calc_dts+alum_calc_dts
DtS_WoL = (DtS_EUI*Floor_area*grid_factor*num_years)+round(embodied_dts,2)



with st.container():
    
    
    def get_metrics_CO2():
       
        CHEP_co2_RESULT = CHEP_co2[CHEP_co2['WWR-NS'].isin([WWR_NS]) & CHEP_co2['WWR-EW'].isin([WWR_EW]) & CHEP_co2['ShadeDepth'].isin([Shade_dep]) & 
                         CHEP_co2['ShadeOrientation (0:V, 1:H)'].isin([Shade_ori]) & CHEP_co2['SHGC/VLT'].isin([SHGC_VLT]) & CHEP_co2['ExWall'].isin([exwall])]
        
        TotalCO2 = CHEP_co2_RESULT['Total kgCO2e']
        WoL_ = CHEP_co2_RESULT['WoL']
        EUI4co2 = CHEP_co2_RESULT['EUI (kWh/m2)']
        
        
        return TotalCO2, WoL_, EUI4co2, CHEP_co2_RESULT
            
    cols = st.columns(6)
    with cols[0]:
        ""
    with cols[1]:
        st.metric('Embodied CO2 (kgCO2e)', int(round(get_metrics_CO2()[0],0)))
    with cols[2]:
        st.metric(f'Whole of Life (kgCO2e/{num_years}yrs)', int(round(get_metrics_CO2()[1],0)))
    with cols[3]:
        st.metric('DtS Embodied CO2 (kgCO2e)', int(round(embodied_dts,0)))
    with cols[4]:
        st.metric(f'DtS Whole of Life (kgCO2e/{num_years}yrs)', int(round(DtS_WoL,0)))
    with cols[5]:
        ""

with st.container():
    
    cols = st.columns(4)
    with cols[0]:
        ""
    with cols[1]: 
        chep_pie_co2 = px.pie(color_discrete_sequence=px.colors.sequential.RdBu, 
                              names =['Upfront Carbon', 'Operational Carbon'], values = [get_metrics_CO2()[0].iloc[0],get_metrics_CO2()[2].iloc[0]*Floor_area*grid_factor*num_years])
        chep_pie_co2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(chep_pie_co2,use_container_width=True)
    with cols[2]:
       upfront_vs_dts = ((get_metrics_CO2()[0].iloc[0]/embodied_dts)-1)*100
       operational_vs_dts = (((DtS_EUI*Floor_area*grid_factor*num_years)/(get_metrics_CO2()[2].iloc[0]*Floor_area*grid_factor*num_years))-1)*100
       chep_pie_co2_dts = px.pie(color_discrete_sequence=px.colors.sequential.thermal, 
                             names =['Upfront Carbon vs. DtS', 'Operational Carbon vs. DtS '], values = [upfront_vs_dts,operational_vs_dts])
       chep_pie_co2_dts.update_traces(textposition='inside', textinfo='percent+label')
       st.plotly_chart(chep_pie_co2_dts,use_container_width=True)
    with cols[3]:
        ""
   

    chep_bx_19 = px.box(CHEP_co2, CHEP_co2["WWR-NS"], CHEP_co2['Total kgCO2e'], "WWR-NS", notched = True)
    chep_bx_20 = px.box(CHEP_co2, CHEP_co2["WWR-EW"], CHEP_co2['Total kgCO2e'], "WWR-EW", notched = True)
    chep_bx_21 = px.box(CHEP_co2, CHEP_co2["ShadeDepth"], CHEP_co2['Total kgCO2e'], "ShadeDepth",  notched = True)
    chep_bx_22 = px.box(CHEP_co2, CHEP_co2["SHGC/VLT"], CHEP_co2['Total kgCO2e'], "SHGC/VLT",notched = True)
    chep_bx_23 = px.box(CHEP_co2, CHEP_co2["ExWall"], CHEP_co2['Total kgCO2e'], "ExWall", notched = True)
    chep_bx_24 = px.box(CHEP_co2, CHEP_co2["ShadeOrientation (0:V, 1:H)"], CHEP_co2['Total kgCO2e'], "ShadeOrientation (0:V, 1:H)", notched = True)
        
    cols = st.columns(6)
    
    with cols[0]:
        st.plotly_chart(chep_bx_19, use_container_width=True)
    with cols[1]:
        st.plotly_chart(chep_bx_20, use_container_width=True)
    with cols[2]:
        st.plotly_chart(chep_bx_21, use_container_width=True)
    with cols[3]:
        st.plotly_chart(chep_bx_22, use_container_width=True)
    with cols[4]:
        st.plotly_chart(chep_bx_23, use_container_width=True)
    with cols[5]:
        st.plotly_chart(chep_bx_24, use_container_width=True)  
    
    
    chep_bx_25 = px.box(CHEP_co2, CHEP_co2["WWR-NS"], CHEP_co2['WoL'], "WWR-NS", notched = True)
    chep_bx_26 = px.box(CHEP_co2, CHEP_co2["WWR-EW"], CHEP_co2['WoL'], "WWR-EW", notched = True)
    chep_bx_27 = px.box(CHEP_co2, CHEP_co2["ShadeDepth"], CHEP_co2['WoL'], "ShadeDepth",  notched = True)
    chep_bx_28 = px.box(CHEP_co2, CHEP_co2["SHGC/VLT"], CHEP_co2['WoL'], "SHGC/VLT",notched = True)
    chep_bx_29 = px.box(CHEP_co2, CHEP_co2["ExWall"], CHEP_co2['WoL'], "ExWall", notched = True)
    chep_bx_30 = px.box(CHEP_co2, CHEP_co2["ShadeOrientation (0:V, 1:H)"], CHEP_co2['WoL'], "ShadeOrientation (0:V, 1:H)", notched = True)
        
    cols = st.columns(6)
    
    with cols[0]:
        st.plotly_chart(chep_bx_25, use_container_width=True)
    with cols[1]:
        st.plotly_chart(chep_bx_26, use_container_width=True)
    with cols[2]:
        st.plotly_chart(chep_bx_27, use_container_width=True)
    with cols[3]:
        st.plotly_chart(chep_bx_28, use_container_width=True)
    with cols[4]:
        st.plotly_chart(chep_bx_29, use_container_width=True)
    with cols[5]:
        st.plotly_chart(chep_bx_30, use_container_width=True)  
        
        
