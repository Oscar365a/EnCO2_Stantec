import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go

# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression


st.set_page_config(page_title='Project Parametric Analysis', layout='wide')

CHEP_en = pd.read_csv('./data/Energy.csv')
epic = pd.DataFrame(pd.read_excel('./data/EPiC.xlsx'))
chep_co2 = pd.read_csv('./data/CO2.csv')

#CHEP_en = pd.read_csv(r'C:\Users\atabadkani\Streamlit Apps\CHEP\data\Energy.csv')
#epic = pd.DataFrame(pd.read_excel(r'C:\Users\atabadkani\Streamlit Apps\CHEP\data\EPiC.xlsx'))
#chep_co2 = pd.read_csv(r'C:\Users\atabadkani\Streamlit Apps\CHEP\data\CO2.csv')

st.title("Project Parametric Analysis - 512 Iterations")

st.markdown('---')
st.header(":red[**ENERGY SECTION**]")
st.markdown('---')

Floor_area = 2310.5  ##########
en_price = 0.2 ###$/kWh


#Energy Cost Calc

CHEP_en['Energy Cost (AU$/yr)'] = CHEP_en['EUI (kWh/m2)']*Floor_area*en_price

with st.sidebar:
    
    st.title('Choose the Design Inputs:')
    
    WWR_NS = st.select_slider('Window-to-Wall Ratio (North-South):', options = [20, 40, 60, 80], value = 40, key = 'WWR_NS')
    WWR_EW = st.select_slider('Window-to-Wall Ratio (East-West):', options = [20, 40, 60, 80], value = 60, key = 'WWR_EW')
    Shade_dep = st.select_slider('Shade Depth (mm):', options = [0, 300, 600, 900], value = 300, key = 'shadedepth')
    SHGC = st.select_slider('SHGC:', options = [0.22,0.34,0.46,0.58], value = 0.46, key = 'glass_shgc')
    exwall = st.select_slider('External Wall R-value:', options = [1.0,1.4], value = 1.4, key = 'exwall_r')
    
    
with st.container():
     
    st.subheader('Design Selection Summary')
    
    def get_metrics_EUI():
       
        CHEP_en_RESULT = CHEP_en[CHEP_en['WWR-NS'].isin([WWR_NS]) & CHEP_en['WWR-EW'].isin([WWR_EW]) & CHEP_en['ShadeDepth'].isin([Shade_dep]) & CHEP_en['SHGC'].isin([SHGC]) & CHEP_en['ExWall'].isin([exwall])]
        
        EUI_METRIC = CHEP_en_RESULT['EUI (kWh/m2)']
        ELEC_P = CHEP_en_RESULT['ELECp (W/m2)']
        CLG_P = CHEP_en_RESULT['CLGp (W/m2)']
        AVE_DA =  CHEP_en_RESULT['Daylight Autonomy']
        AVE_UDI = CHEP_en_RESULT['Excessive Daylight']
        ENERGY = CHEP_en_RESULT['Energy Cost (AU$/yr)']
        PATIENT_NORTH_OT = CHEP_en_RESULT['OT26% - Patient North']
        PATIENT_SOUTH_OT = CHEP_en_RESULT['OT26% - Patient South']
        image = CHEP_en_RESULT['img']
        EUI_REF = CHEP_en_RESULT['EUI Saved(-)Wasted(+)']
        ELEC_REF = CHEP_en_RESULT['REF_ELECp']
        CLG_REF = CHEP_en_RESULT['REF_CLGp']
        DA_REF = CHEP_en_RESULT['REF_DA']
        UDI_REF = CHEP_en_RESULT['REF_ExcDA']
        
        return EUI_METRIC, ELEC_P, CLG_P, AVE_DA, AVE_UDI, ENERGY, PATIENT_NORTH_OT, PATIENT_SOUTH_OT, image,EUI_REF,ELEC_REF,CLG_REF,DA_REF,UDI_REF
            
        
    cols = st.columns([0.1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.1])
    with cols[0]:
        ""
    with cols[1]:
        st.metric('EUI(kWh/m2)', int(get_metrics_EUI()[0]))
    with cols[2]:
        st.metric('ELECp(W/m2)', int(get_metrics_EUI()[1]))
    with cols[3]:
        st.metric('CLGp(W/m2)', int(get_metrics_EUI()[2])) 
    with cols[4]:
        st.metric('Daylight Autonomy% (500lx)', int(get_metrics_EUI()[3]))
    with cols[5]:
        st.metric('Excessive Daylight% (>10000lx)',round(get_metrics_EUI()[4],2))
    with cols[6]:
        st.metric('Cost (AU$/yr)', int(get_metrics_EUI()[5]))
    with cols[7]:
        st.metric('Patient North% (> OT 26C)', int(get_metrics_EUI()[6]))
    with cols[8]:
        st.metric('Patient South% (> OT 26C)', int(get_metrics_EUI()[7]))
    with cols[9]:
        ""
        
    st.subheader('Design Performance against Reference Case - % Saved (-) Wasted (+)')
    
    data_ref_eui = {'WWR':'40%','Shade Depth':'No Shades','U-Value/SHGC/VLT': '3.91 / 0.30 / 0.38', 'EXT Walls':'R1.4'}
    REF_DF_eui = pd.DataFrame([data_ref_eui], index = ['Reference Case'])
    st.dataframe(REF_DF_eui, use_container_width= True)
    
    
    cols = st.columns(7)
    
    with cols[0]:
        ""
    with cols[1]:
        st.metric('EUI(kWh/m2)', f'{get_metrics_EUI()[9].iloc[0]} %' )
    with cols[2]:
        st.metric('ELECp(W/m2)', f'{get_metrics_EUI()[10].iloc[0]} %')
    with cols[3]:
        st.metric('CLGp(W/m2)', f'{get_metrics_EUI()[11].iloc[0]} %') 
    with cols[4]:
        st.metric('Daylight Autonomy (500lx)', f'{get_metrics_EUI()[12].iloc[0]} %')
    with cols[5]:
        st.metric('Excessive Daylight (>10000lx)', f'{get_metrics_EUI()[13].iloc[0]} %')
    with cols[6]:
        ""
    
    def loadImages():
      
        #img = Image.open(rf'C:\Users\atabadkani\Streamlit Apps\CHEP\data\images\{get_metrics_EUI()[8].iloc[0]}')
        img = Image.open(f'./data/images/{get_metrics_EUI()[8].iloc[0]}')
        #ref = Image.open(r'C:\Users\atabadkani\Streamlit Apps\CHEP\data\images\WWR-NS1_WWR-EW1_ShadeDepth0_SHGCVLT1_ExWall0.png')
        ref = Image.open('./data/images/WWR-NS2_WWR-EW2_ShadeDepth0_SHGCVLT2_ExWall0.png')
        return img, ref
    
    col1,col2,col3,col4 = st.columns([1.5,4,0.5,4])
    
    with col1:
        ""
    with col2:
        st.image(loadImages()[0], caption='Selected Design Iteration', use_column_width = False)
    with col3:
        ""
    with col4:
        st.image(loadImages()[1], caption='Reference Case', use_column_width = False)
    
    
    st.subheader("**Design Inputs vs. Operational Building Performance**")
    
    columns = ['WWR-NS', 'WWR-EW', 'ShadeDepth', 
       'SHGC','VLT', 'ExWall', 'EUI (kWh/m2)', 'EUI Saved(-)Wasted(+)','CLGp (W/m2)',
       'Daylight Autonomy', 'Excessive Daylight', 'Energy Cost (AU$/yr)',
       'OT26% - Patient North', 'OT26% - Patient South', ]
    
    
    chep_pcm = px.parallel_coordinates(CHEP_en, columns, color="EUI (kWh/m2)",
                                       labels={"ShadeDepth": "ShadeDepth", "ExWall":"ExWall"},
                                       color_continuous_scale=px.colors.cyclical.Edge,
                                       color_continuous_midpoint=2, height = 650)
    chep_pcm.update_layout(coloraxis_showscale=False)
    # chep_pcm.update_traces(line_colorbar_tickangle=45)
    
    st.plotly_chart(chep_pcm, use_container_width=True)
        
 
 
    chep_bx_01 = px.box(CHEP_en, CHEP_en["WWR-NS"], CHEP_en["EUI (kWh/m2)"], "WWR-NS", notched = True)
    chep_bx_02 = px.box(CHEP_en, CHEP_en["WWR-EW"], CHEP_en["EUI (kWh/m2)"], "WWR-EW", notched = True)
    chep_bx_03 = px.box(CHEP_en, CHEP_en["ShadeDepth"], CHEP_en["EUI (kWh/m2)"], "ShadeDepth", notched = True)
    chep_bx_04 = px.box(CHEP_en, CHEP_en["SHGC"], CHEP_en["EUI (kWh/m2)"], "SHGC", notched = True)
    chep_bx_05 = px.box(CHEP_en, CHEP_en["ExWall"], CHEP_en["EUI (kWh/m2)"], "ExWall", notched = True)

    cols = st.columns(5)
    
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

    chep_bx_07 = px.box(CHEP_en, CHEP_en["WWR-NS"], CHEP_en["Daylight Autonomy"], "WWR-NS", notched = True)
    chep_bx_08 = px.box(CHEP_en, CHEP_en["WWR-EW"], CHEP_en["Daylight Autonomy"], "WWR-EW", notched = True)
    chep_bx_09 = px.box(CHEP_en, CHEP_en["ShadeDepth"], CHEP_en['Daylight Autonomy'], "ShadeDepth",  notched = True)
    chep_bx_10 = px.box(CHEP_en, CHEP_en["VLT"], CHEP_en['Daylight Autonomy'], "VLT",  notched = True)
    chep_bx_11 = px.box(CHEP_en, CHEP_en["ExWall"], CHEP_en['Daylight Autonomy'], "ExWall", notched = True)
    
    cols = st.columns(5)
    
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
        

    chep_bx_13 = px.box(CHEP_en, CHEP_en["WWR-NS"], CHEP_en["Excessive Daylight"], "WWR-NS", notched = True)
    chep_bx_14 = px.box(CHEP_en, CHEP_en["WWR-EW"], CHEP_en["Excessive Daylight"], "WWR-EW", notched = True)
    chep_bx_15 = px.box(CHEP_en, CHEP_en["ShadeDepth"], CHEP_en['Excessive Daylight'], "ShadeDepth",  notched = True)
    chep_bx_16 = px.box(CHEP_en, CHEP_en["VLT"], CHEP_en['Excessive Daylight'], "VLT",  notched = True)
    chep_bx_17 = px.box(CHEP_en, CHEP_en["ExWall"], CHEP_en['Excessive Daylight'], "ExWall", notched = True)
    
    cols = st.columns(5)
    
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

def get_index(df) -> dict:
        dict_ = {df['Version: EPiC Database 2019'].iloc[i]: i for i in range(0, len(df['Version: EPiC Database 2019']))}
        return dict_

#Correlations
#-------------------------------------------------------------------------------------------------------------------------------------

CHEP_lm = CHEP_en.drop(['img', 'REF_ELECp', 'REF_CLGp', 'REF_DA','REF_ExcDA'], axis=1)


CHEP_CORR_HTM = px.imshow(round(CHEP_lm.corr(),2),text_auto=True,color_continuous_scale='thermal',  width = 1000, height = 1000,title = 'Design Input Correlations with Energy/Comfort Targets')
CHEP_CORR_HTM.update_traces(textfont_size=15)

st.plotly_chart(CHEP_CORR_HTM, use_container_width=True)

st.markdown('**:red[Note:]** Numbers represent the magnitude level of variables against each other, and Negative Values mean the input impacts the target negatively.')

#Linear Regression
#-------------------------------------------------------------------------------------------------------------------------------------

# X = CHEP_lm[['WWR-NS', 'WWR-EW', 'ShadeDepth', 'SHGC', 'VLT', 'ExWall']]

# y = CHEP_lm[['EUI (kWh/m2)', 'ELECp (W/m2)', 'CLGp (W/m2)', 'Daylight Autonomy',
#        'Excessive Daylight', 'OT26% - Patient North', 'OT26% - Patient South','EUI Saved(-)Wasted(+)','Energy Cost (AU$/yr)']]

# X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.8, random_state=101)

# lm = LinearRegression()

# lm.fit(X_train,y_train)

# CHEP_en_cdf = pd.DataFrame(np.transpose(lm.coef_),X.columns,columns=[['EUI (kWh/m2)', 'ELECp (W/m2)', 'CLGp (W/m2)', 'Daylight Autonomy',
#        'Excessive Daylight', 'OT26% - Patient North', 'OT26% - Patient South','EUI Saved(-)Wasted(+)','Energy Cost (AU$/yr)']])

# st.dataframe(CHEP_en_cdf, use_container_width=True)


####################################################################################################################
#CARBON SECTION
st.markdown('---')
st.header(":red[**CARBON SECTION**]")
st.markdown('---')

#Material Selection and Emission Calc

with st.sidebar:
    
    st.title('Material Type:')
    
    with st.expander('Roof/Ceilings'):
        
        
        roof_concrete = epic[epic['Functional unit'] =='m³'] #only m3 rows
        roof_concrete = roof_concrete[roof_concrete['Functional unit'] !='no.'] #remove unitless rows
        roof_concrete = roof_concrete[roof_concrete['Version: EPiC Database 2019'].str.contains('Concrete|AAC')]
        roof_concrete_type = roof_concrete['Version: EPiC Database 2019'].iloc[:]
        roof_concrete_selection = st.selectbox('Concrete:', options=roof_concrete_type, key='concrete-roof', index = 2)   
        roof_concrete_unit = roof_concrete['Functional unit'].iloc[int(get_index(roof_concrete)[roof_concrete_selection])]
        roof_concrete_em = roof_concrete['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(roof_concrete)[roof_concrete_selection])]
        st.markdown(f'**Unit: {roof_concrete_unit} | Emission Factor (kgCO₂e): {roof_concrete_em}**')
        # roof_concerte_density = st.number_input('Concrete Density (Kg/m3)', min_value=100, max_value=3000, value = 2300, key='concrete-roof-den')
    
        roof_PB = epic[epic['Functional unit'] =='m²']
        roof_PB = roof_PB[roof_PB['Functional unit'] !='no.']
        roof_PB = roof_PB[roof_PB['Version: EPiC Database 2019'].str.contains('Plaster|plaster')]
        roof_PB_type = roof_PB['Version: EPiC Database 2019'].iloc[:]
        roof_PB_selection = st.selectbox('Plaster Board:', options=roof_PB_type, key='PB-roof', index = 1)    
        roof_PB_unit = roof_PB['Functional unit'].iloc[int(get_index(roof_PB)[roof_PB_selection])]
        roof_PB_em = roof_PB['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(roof_PB)[roof_PB_selection])]
        st.markdown(f'**Unit: {roof_PB_unit} | Emission Factor (kgCO₂e): {roof_PB_em}**')
        # PB_density = st.number_input('Plaster Board Density (Kg/m3)', min_value=50, max_value=1500, value = 700, key='PB-roof-den')
    
        roof_insul = epic[epic['Functional unit'] =='kg']
        roof_insul = roof_insul[roof_insul['Functional unit'] !='no.']
        roof_insul = roof_insul[roof_insul['Version: EPiC Database 2019'].str.contains('insulation')]
        roof_insul_type = ['Cellulose insulation','Glasswool insulation','Rockwool insulation']
        roof_insul_selection = st.selectbox('Insulation Type:', options=roof_insul_type, key='insul-roof', index = 1)
        roof_insul_unit = roof_insul['Functional unit'].iloc[int(get_index(roof_insul)[roof_insul_selection])]
        roof_insul_em = roof_insul['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(roof_insul)[roof_insul_selection])]
        st.markdown(f'Unit: {roof_insul_unit} | Emission Factor (kgCO₂e): {roof_insul_em}')
        roof_insul_density = st.number_input('Insulation Density (Kg/m3)', min_value=10, max_value=40, value = 18, key='insul-roof-den')
        
    with st.expander('External Walls'):
        
        wall_concrete = epic[epic['Functional unit'] =='m³']
        wall_concrete = wall_concrete[wall_concrete['Functional unit'] !='no.']
        wall_concrete = wall_concrete[wall_concrete['Version: EPiC Database 2019'].str.contains('Concrete|AAC')]
        wall_concrete_type = wall_concrete['Version: EPiC Database 2019'].iloc[:]
        wall_concrete_selection = st.selectbox('Concrete:', options=wall_concrete_type, key='concrete-wall', index = 2)   
        wall_concrete_unit = wall_concrete['Functional unit'].iloc[int(get_index(wall_concrete)[wall_concrete_selection])]
        wall_concrete_em = wall_concrete['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(wall_concrete)[wall_concrete_selection])]
        st.markdown(f'**Unit: {wall_concrete_unit} | Emission Factor (kgCO₂e): {wall_concrete_em}**')
        # concerte_density = st.number_input('Concrete Density (Kg/m3)', min_value=100, max_value=3000, value = 2300, key='concrete-wall-den')
    
        wall_PB = epic[epic['Functional unit'] =='m²']
        wall_PB = wall_PB[wall_PB['Functional unit'] !='no.']
        wall_PB = wall_PB[wall_PB['Version: EPiC Database 2019'].str.contains('Plaster|plaster')]
        wall_PB_type = wall_PB['Version: EPiC Database 2019'].iloc[:]
        wall_PB_selection = st.selectbox('Plaster Board:', options=wall_PB_type, key='PB-wall', index = 1)    
        wall_PB_unit = wall_PB['Functional unit'].iloc[int(get_index(wall_PB)[wall_PB_selection])]
        wall_PB_em = wall_PB['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(wall_PB)[wall_PB_selection])]
        st.markdown(f'**Unit: {wall_PB_unit} | Emission Factor (kgCO₂e): {wall_PB_em}**')
        # PB_density = st.number_input('Plaster Board Density (Kg/m3)', min_value=50, max_value=1500, value = 700, key='PB-wall-den')
    
        wall_insul = epic[epic['Functional unit'] =='kg']
        wall_insul = wall_insul[wall_insul['Functional unit'] !='no.']
        wall_insul = wall_insul[wall_insul['Version: EPiC Database 2019'].str.contains('insulation')]
        wall_insul_type = ['Cellulose insulation','Glasswool insulation','Rockwool insulation']
        wall_insul_selection = st.selectbox('Insulation Type:', options=wall_insul_type, key='insul-wall', index = 1)
        wall_insul_unit = wall_insul['Functional unit'].iloc[int(get_index(wall_insul)[wall_insul_selection])]
        wall_insul_em = wall_insul['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(wall_insul)[wall_insul_selection])]
        st.markdown(f'Unit: {wall_insul_unit} | Emission Factor (kgCO₂e): {wall_insul_em}')
        wall_insul_density = st.number_input('Insulation Density (Kg/m3)', min_value=10, max_value=40, value = 18, key='insul-wall-den')
        
    with st.expander('Internal Walls'):
        
        inwall_PB = epic[epic['Functional unit'] =='m²']
        inwall_PB = inwall_PB[inwall_PB['Functional unit'] !='no.']
        inwall_PB = inwall_PB[inwall_PB['Version: EPiC Database 2019'].str.contains('Plaster|plaster')]
        inwall_PB_type = inwall_PB['Version: EPiC Database 2019'].iloc[:]
        inwall_PB_selection = st.selectbox('Plaster Board:', options=inwall_PB_type, key='PB-inwall', index = 1)    
        inwall_PB_unit = inwall_PB['Functional unit'].iloc[int(get_index(inwall_PB)[inwall_PB_selection])]
        inwall_PB_em = inwall_PB['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(inwall_PB)[inwall_PB_selection])]
        st.markdown(f'**Unit: {inwall_PB_unit} | Emission Factor (kgCO₂e): {inwall_PB_em}**')
        # PB_density = st.number_input('Plaster Board Density (Kg/m3)', min_value=50, max_value=1500, value = 700, key='PB-inwall-den')
    
        inwall_insul = epic[epic['Functional unit'] =='kg']
        inwall_insul = inwall_insul[inwall_insul['Functional unit'] !='no.']
        inwall_insul = inwall_insul[inwall_insul['Version: EPiC Database 2019'].str.contains('insulation')]
        inwall_insul_type = ['Cellulose insulation','Glasswool insulation','Rockwool insulation']
        inwall_insul_selection = st.selectbox('Insulation Type:', options=inwall_insul_type, key='insul-inwall', index = 1)
        inwall_insul_unit = inwall_insul['Functional unit'].iloc[int(get_index(inwall_insul)[inwall_insul_selection])]
        inwall_insul_em = inwall_insul['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(inwall_insul)[inwall_insul_selection])]
        st.markdown(f'Unit: {inwall_insul_unit} | Emission Factor (kgCO₂e): {inwall_insul_em}')
        inwall_insul_density = st.number_input('Insulation Density (Kg/m3)', min_value=10, max_value=40, value = 18, key='insul-inwall-den')
        
    with st.expander('Floors'):
        
        floor_concrete = epic[epic['Functional unit'] =='m³']
        floor_concrete = floor_concrete[floor_concrete['Functional unit'] !='no.']
        floor_concrete = floor_concrete[floor_concrete['Version: EPiC Database 2019'].str.contains('Concrete|AAC')]
        floor_concrete_type = floor_concrete['Version: EPiC Database 2019'].iloc[:]
        floor_concrete_selection = st.selectbox('Concrete:', options=floor_concrete_type, key='concrete-floor', index = 2)   
        floor_concrete_unit = floor_concrete['Functional unit'].iloc[int(get_index(floor_concrete)[floor_concrete_selection])]
        floor_concrete_em = floor_concrete['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(floor_concrete)[floor_concrete_selection])]
        st.markdown(f'**Unit: {floor_concrete_unit} | Emission Factor (kgCO₂e): {floor_concrete_em}**')
        # concerte_density = st.number_input('Concrete Density (Kg/m3)', min_value=100, max_value=3000, value = 2300, key='insul-floor-den')
        
    with st.expander('Windows'):

        Glass = epic[epic['Version: EPiC Database 2019'].str.contains('glazing | glass')]
        Glass = Glass[Glass['Functional unit'] !='no.']
        Glass_type = Glass['Version: EPiC Database 2019'].iloc[:]      
        Glass_selection = st.selectbox('Glass Type:', options=Glass_type, key='Glass', index = 1)
        Glass_unit = Glass['Functional unit'].iloc[int(get_index(Glass)[Glass_selection])]
        Glass_em = Glass['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(Glass)[Glass_selection])]
        st.markdown(f'**Unit: {Glass_unit} | Emission Factor (kgCO₂e): {Glass_em}**')
        
    with st.expander('Shades'):
        
        alum = epic[epic['Functional unit'] =='m²']
        alum = alum[alum['Functional unit'] !='no.']
        alum = alum[alum['Version: EPiC Database 2019'].str.contains('Aluminium sheet -')]
        alum_type = alum['Version: EPiC Database 2019'].iloc[:]
        alum_selection = st.selectbox('Aluminium Type:', options=alum_type, key='alum', index = 1)
        alum_unit = alum['Functional unit'].iloc[int(get_index(alum)[alum_selection])]
        alum_em = alum['Embodied Greenhouse Gas Emissions (kgCO₂e)'].iloc[int(get_index(alum)[alum_selection])]
        st.markdown(f'**Unit: {alum_unit} | Emission Factor (kgCO₂e): {alum_em}**')
    
    
#Scenario Type Selection
#-------------------------------------------------------------------------------------------------------------------------------------

with st.sidebar:
    
    
    st.title('Grid Emission Scenario:')
    
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
    
    
#CO2 PCM
#-------------------------------------------------------------------------------------------------------------------------------------

with st.container():
    
    st.subheader("**Design Inputs vs. Building Whole of Life Performance**")

    CHEP_co2 = chep_co2.drop('img', axis =1)  

    concrete_calc = []
    PB_calc = []
    Glass_calc = []
    insul_calc = []
    alum_calc  = []
    iteration_calc = []
    roof_contribution = []
    wall_contribution = []
    inwall_contribution = []
    WoL = []
    
    #Material Selection Embodied Calculations
    for i in range(0, len(CHEP_co2)):
        #Concrete
        concrete_vol = (CHEP_co2['Conc_Roof(m3)'].iloc[i]*roof_concrete_em)+(CHEP_co2['Conc_ExWall(m3)'].iloc[i]*wall_concrete_em)+(CHEP_co2['Conc_Floor(m3)'].iloc[i]*floor_concrete_em)
        concrete_calc.append(concrete_vol)
        #Plasterboard
        if (roof_PB_selection == 'Plasterboard - 10 mm'):
            PB_1m = 0.01
            PB_vol_roof = (CHEP_co2['PB_Roof(m3)'].iloc[i]*PB_1m*roof_PB_em)
            
        elif (roof_PB_selection == 'Plasterboard - 13 mm') or (wall_PB_selection == 'Plasterboard - 13 mm') or (inwall_PB_selection == 'Plasterboard - 13 mm'):
            PB_1m = 0.013
            PB_vol_roof = (CHEP_co2['PB_Roof(m3)'].iloc[i]*PB_1m*roof_PB_em)
        
        if (wall_PB_selection == 'Plasterboard - 10 mm'):
            PB_1m = 0.01
            PB_vol_exwall = (CHEP_co2['PB_ExWall(m3)'].iloc[i]*PB_1m*wall_PB_em)
        elif (wall_PB_selection == 'Plasterboard - 13 mm'):
            PB_1m = 0.013
            PB_vol_exwall = (CHEP_co2['PB_ExWall(m3)'].iloc[i]*PB_1m*wall_PB_em)
        
        if (inwall_PB_selection == 'Plasterboard - 10 mm'):
            PB_1m = 0.01
            PB_vol_inwall = (CHEP_co2['PB_IntWall(m3)'].iloc[i]*PB_1m*wall_PB_em)
        elif (inwall_PB_selection == 'Plasterboard - 13 mm'):
            PB_1m = 0.013
            PB_vol_inwall = (CHEP_co2['PB_IntWall(m3)'].iloc[i]*PB_1m*wall_PB_em)
        
        PB_vol = PB_vol_roof+PB_vol_exwall+PB_vol_inwall
        PB_calc.append(PB_vol)
        
        #Windows 
        Glass_vol = CHEP_co2['Glass(m2)'].iloc[i]*Glass_em
        Glass_calc.append(Glass_vol)
        
        #Insulation
        insul_roof = roof_insul_em*roof_insul_density
        insul_wall = wall_insul_em*wall_insul_density
        insul_inwall = inwall_insul_em*inwall_insul_density
        
        insul_vol = (CHEP_co2['ins_Roof(m3)'].iloc[i]*insul_roof)+(CHEP_co2['ins_ExWall(m3)'].iloc[i]*insul_wall)+(CHEP_co2['ins_IntWall(m3)'].iloc[i]*insul_inwall)
        insul_calc.append(insul_vol)
        
        #Shades
        alum_vol = CHEP_co2['ShadeArea(m2)'].iloc[i]*alum_em
        alum_calc.append(alum_vol)
        
        #Summing up layers for each envelope component
        roof_contribution.append(CHEP_co2['Conc_Roof(m3)'].iloc[i]*roof_concrete_em+CHEP_co2['PB_Roof(m3)'].iloc[i]*PB_1m*roof_PB_em+CHEP_co2['PB_Roof(m3)'].iloc[i]*PB_1m*roof_PB_em+insul_roof) 
        wall_contribution.append(CHEP_co2['Conc_ExWall(m3)'].iloc[i]*wall_concrete_em+CHEP_co2['PB_ExWall(m3)'].iloc[i]*PB_1m*wall_PB_em+CHEP_co2['PB_ExWall(m3)'].iloc[i]*PB_1m*wall_PB_em+insul_wall)
        inwall_contribution.append(CHEP_co2['PB_IntWall(m3)'].iloc[i]*PB_1m*inwall_PB_em+CHEP_co2['PB_IntWall(m3)'].iloc[i]*PB_1m*inwall_PB_em+insul_inwall)
        glass_contribution = Glass_calc
        shades_contribution = alum_calc
        
        #Listing single iteration values from the 'for loop'
        iteration_calc.append([concrete_vol,PB_vol,Glass_vol,alum_vol,insul_vol])
        #Summing up the values for single iteration values from the 'for loop'
        sum_contributions = concrete_vol+PB_vol+Glass_vol+alum_vol+insul_vol
        #WoL Calculations for each iteration
        WoL_value = CHEP_co2['EUI (kWh/m2)'].iloc[i]*Floor_area*grid_factor*num_years + round(sum_contributions,2)
        WoL.append(WoL_value)
        
        #For WoL line plot to compare on time basis
        Wol_scenario_one = []
        Wol_scenario_two = []
        years = []
        for yrs in range(0,21):
            
            scenario_one_grid = (ln(yrs)*-0.147) + 0.9121
            scenario_two_grid = (ln(yrs)*-0.309) + 0.9413
            
            if yrs == 0:
                years.append(f' Year {yrs}')
                Wol_scenario_one.append(round(sum_contributions,2))
                Wol_scenario_two.append(round(sum_contributions,2))
            else:
                years.append(f' Year {yrs}')
                Wol_scenario_one.append(CHEP_co2['EUI (kWh/m2)'].iloc[i]*Floor_area*scenario_one_grid*yrs)
                Wol_scenario_two.append(CHEP_co2['EUI (kWh/m2)'].iloc[i]*Floor_area*scenario_two_grid*yrs)

        
      
    calc_df_raw = pd.DataFrame([concrete_calc,PB_calc,Glass_calc,alum_calc,insul_calc])
    calc_df = calc_df_raw.transpose()
    calc_df = calc_df.rename(columns={0:'concrete_calc', 1:'PB_calc',2:'Glass_calc',3:'alum_calc',4:'insul_calc'})
    calc_df['Total'] = calc_df['concrete_calc']+calc_df['PB_calc']+calc_df['Glass_calc']+calc_df['alum_calc']+calc_df['insul_calc']
    
    CHEP_co2['roof_contribution'] = roof_contribution
    CHEP_co2['wall_contribution'] = wall_contribution
    CHEP_co2['inwall_contribution'] = inwall_contribution
    CHEP_co2['glass_contribution'] = glass_contribution
    CHEP_co2['shades_contribution'] = shades_contribution
    
    CHEP_co2['WoL (KgCO2e)'] = WoL
    
    CHEP_co2['UpfrontCO2 (KgCO2e)'] = calc_df['Total']
    
    chep_pcm_co = px.parallel_coordinates(CHEP_co2, ['WWR-NS', 'WWR-EW', 'ShadeDepth',
       'SHGC','ExWall', 'EUI (kWh/m2)', 'UpfrontCO2 (KgCO2e)', 'WoL (KgCO2e)'], color='EUI (kWh/m2)',
                                        labels={"ShadeDepth": "ShadeDepth", "ExWall":"ExWall"},
                                        color_continuous_scale=px.colors.cyclical.HSV,
                                        color_continuous_midpoint=200, height = 650)

    chep_pcm_co.update_layout(coloraxis_showscale=False)
         
    st.plotly_chart(chep_pcm_co, use_container_width=True)

#REFERENCE UPFRONT CALCS
#-------------------------------------------------------------------------------------------------------------------------------------
#Volumes
REF_roof_Concrete = 473.70 #####
REF_wall_Concrete = 126.74  #####
REF_floor_Concrete = 473.70 #####
REF_roof_insul = 307.91 ####
REF_wall_insul = 17.74 ####
REF_inwall_insul = 154.24 ####
REF_roof_PB = 30.79 ####
REF_wall_PB = 8.23 ####
REF_inwall_PB = 95.48 ###
REF_glass = 450.18 ####
REF_shade = 0
REF_EUI = 126.05 #####

REF_concrete_em = 416 #concrete 32MPA for roof/floors
REF_wall_em = 328 #concrete 20MPA
REF_PB_em = 6.5 #13mm
REF_insul_em = 72 #glasswool 18 kg/m3 (4*18)
REF_glass_em = 76.1 #Laminated glass sheet 10.38mm

data_ref_carbon = {'WWR':'40%','Shade Depth':'No Shades','U-Value/SHGC/VLT': '3.91 / 0.30 / 0.38', 'EXT Walls':'R1.4', 
            'Concrete (Roof/Floor)':f'Concrete 32MPA, Emission Factor: {REF_concrete_em}', 'Concrete (EXT Walls)':f'Concrete 20MPA, Emission Factor: {REF_wall_em}',
            'Plaster Board': f'13mm, Emission Factor: {REF_PB_em}', 'Insulation':f'Glasswool 18kg/m3, Emission Factor: {REF_insul_em}',
            'Glass':f'Laminated glass sheet 10.38mm, Emission Factor: {REF_glass_em}'}

REF_DF = pd.DataFrame([data_ref_carbon], index = ['Reference Case'])

concrete_calc_REF = (REF_roof_Concrete*REF_concrete_em)+(REF_floor_Concrete*REF_concrete_em)+(REF_wall_Concrete*REF_wall_em)

PB_calc_REF = (REF_roof_PB*REF_PB_em) + (REF_wall_PB*REF_PB_em) + (REF_inwall_PB*REF_PB_em)

insul_calc_REF = (REF_roof_insul*REF_insul_em) + (REF_wall_insul*REF_insul_em) + (REF_inwall_insul*REF_insul_em)

Glass_calc_REF = REF_glass * REF_glass_em
    

DTS_Upfront = concrete_calc_REF+PB_calc_REF+insul_calc_REF+Glass_calc_REF

DtS_WoL = (REF_EUI*Floor_area*grid_factor*num_years)+round(DTS_Upfront,2)

#CO2 Metrics
#-------------------------------------------------------------------------------------------------------------------------------------

with st.container():
    
    def get_metrics_CO2():
       
        CHEP_co2_RESULT = CHEP_co2[CHEP_co2['WWR-NS'].isin([WWR_NS]) & CHEP_co2['WWR-EW'].isin([WWR_EW]) & CHEP_co2['ShadeDepth'].isin([Shade_dep]) 
                                   & CHEP_co2['SHGC'].isin([SHGC]) & CHEP_co2['ExWall'].isin([exwall])]
        
        TotalCO2 = CHEP_co2_RESULT['UpfrontCO2 (KgCO2e)']
        WoL_ = CHEP_co2_RESULT['WoL (KgCO2e)']
        EUI4co2 = CHEP_co2_RESULT['EUI (kWh/m2)']
        iteration_index = CHEP_co2_RESULT['EUI (kWh/m2)'].index[0]
        roofcontr = CHEP_co2_RESULT['roof_contribution'].iloc[0]
        wallcontr= CHEP_co2_RESULT['wall_contribution'].iloc[0]
        inwallcontr = CHEP_co2_RESULT['inwall_contribution'].iloc[0]
        windowscontr = CHEP_co2_RESULT['glass_contribution'].iloc[0]
        shadescontr = CHEP_co2_RESULT['shades_contribution'].iloc[0]
        
        
        return TotalCO2, WoL_, EUI4co2, iteration_index, roofcontr, wallcontr, inwallcontr, windowscontr, shadescontr
            
    cols = st.columns([0.1,0.7,0.7,0.7,0.7,0.7,0.7,0.1])
    with cols[0]:
        ""
    with cols[1]:
        st.metric('Proposed Embodied CO2 (kgCO2e)', int(round(get_metrics_CO2()[0],0)))
    with cols[2]:
        st.metric(f'Proposed Whole of Life (kgCO2e/{num_years}yrs)', int(round(get_metrics_CO2()[1],0)))
    with cols[3]:
        st.metric('Reference Embodied CO2 (kgCO2e)', int(round(DTS_Upfront,0)))
    with cols[4]:
        st.metric(f'Reference Whole of Life (kgCO2e/{num_years}yrs)', int(round(DtS_WoL,0)))
    with cols[5]:
        st.metric('% Embodied CO2 Improvement (kgCO2e)', round((1 - (int(round(get_metrics_CO2()[0],0))/int(round(DTS_Upfront,0))))*100,2))
    with cols[6]:
        st.metric(f'% Whole of Life Improvement (kgCO2e/{num_years}yrs)', round((1-(int(round(get_metrics_CO2()[1],0)) / int(round(DtS_WoL,0))))*100,2))
    with cols[7]:
       ""
#Pie Charts
#-------------------------------------------------------------------------------------------------------------------------------------

with st.container():
    
    st.dataframe(REF_DF, use_container_width=True)
    
    
    cols = st.columns([0.05,3,0.5,3,0.05])
    with cols[0]:
        ""
    with cols[1]:
    
        Proposed_Upfront_CO2 = get_metrics_CO2()[0].iloc[0]
        Proposed_Opr_CO2 = get_metrics_CO2()[2].iloc[0]*Floor_area*grid_factor*num_years
        chep_pie_co2 = px.pie(color_discrete_sequence=px.colors.sequential.RdBu, 
                              names =['Upfront Carbon', 'Operational Carbon'], values = [Proposed_Upfront_CO2,Proposed_Opr_CO2])
        chep_pie_co2.update_traces(textposition='inside', textinfo='percent+label')
        chep_pie_co2.update_layout(title_text='Proposed Case')
        st.plotly_chart(chep_pie_co2,use_container_width=True)
    with cols[2]:
        ""
    with cols[3]:
        
        #WoL Scenarios
        #-------------------------------------------------------------------------------------------------------------------------------------
        
        Wol_scenarios = pd.DataFrame([Wol_scenario_one,Wol_scenario_two, years]).transpose()
        Wol_scenarios.rename(columns = {0:'Scenario One',1: 'Scenario Two'},inplace = True)
        Wol_scenarios.set_index(2,inplace = True)
        Wol_scenarios = px.line(Wol_scenarios, labels = {'index':'Years', 'value':'Carbon (KgCO2e)', '2':''}, markers = True)
        Wol_scenarios.update_layout(title_text='Carbon Impact')
        st.plotly_chart(Wol_scenarios, use_container_width=True)
    
    with cols[4]:
        ""       
        
        
    cols = st.columns([2.3,0.2,2.3,0.2,2.3])
    with cols[0]:
        
        chep_bar_CO2_contr = go.Figure(data=[
                        go.Bar(x = ['Roof/Ceiling','External Walls', 'Internal Walls', 'Windows','Shades'],
                               y = [get_metrics_CO2()[4],get_metrics_CO2()[5],get_metrics_CO2()[6],get_metrics_CO2()[7],get_metrics_CO2()[8]],
            marker_color= ['yellow','lightgreen','darkgreen','cyan','purple'])])

        chep_bar_CO2_contr.update_traces(marker_line_width=1.5, opacity=0.95)
        chep_bar_CO2_contr.update_layout(title_text='Envelope Contributions to Upfront CO2 (Proposed Selection) ')
    
        st.plotly_chart(chep_bar_CO2_contr,use_container_width=True)
        
    with cols[1]:
        ""
        
    with cols[2]: 
        
        chep_bar_CO2 = go.Figure(data=[
                        go.Bar(x = ['Concrete','Plaster Board', 'Glass','Aluminium','Insulation'],
                               y = [iteration_calc[get_metrics_CO2()[3]][0],iteration_calc[get_metrics_CO2()[3]][1],iteration_calc[get_metrics_CO2()[3]][2],iteration_calc[get_metrics_CO2()[3]][3],iteration_calc[get_metrics_CO2()[3]][4]],
            marker_color= ['brown','Grey','darkblue','lightgrey','lightyellow'])])

        chep_bar_CO2.update_traces(marker_line_width=1.5, opacity=0.95)
        chep_bar_CO2.update_layout(title_text='Material Contributions to Upfront CO2 (Proposed Selection)')
    
        st.plotly_chart(chep_bar_CO2,use_container_width=True)
        
    with cols[3]:
        ""
        
    with cols[4]:
        
        DTS_Operational_CO2 = REF_EUI*Floor_area*grid_factor*num_years
        
        chep_bar_CO2_DtS = go.Figure(data=[
                        go.Bar(x = ['Proposed Upfront','Reference Upfront', 'Proposed Operational','Reference Operational'],
                               y = [Proposed_Upfront_CO2,DTS_Upfront,Proposed_Opr_CO2,DTS_Operational_CO2],
            marker_color= ['lightblue','Red','lightblue','Red'], width=[0.5, 0.5, 0.5, 0.5, 0.5])])

        chep_bar_CO2_DtS.update_traces(marker_line_width=1.5, opacity=0.75)
        chep_bar_CO2_DtS.update_layout(title_text='Proposed Selection vs. Reference Case')
        
        st.plotly_chart(chep_bar_CO2_DtS,use_container_width=True)
        
        
#Box Plots

    chep_bx_19 = px.box(CHEP_co2, CHEP_co2["WWR-NS"], CHEP_co2['UpfrontCO2 (KgCO2e)'], "WWR-NS", notched = True)
    chep_bx_20 = px.box(CHEP_co2, CHEP_co2["WWR-EW"], CHEP_co2['UpfrontCO2 (KgCO2e)'], "WWR-EW", notched = True)
    chep_bx_21 = px.box(CHEP_co2, CHEP_co2["ShadeDepth"], CHEP_co2['UpfrontCO2 (KgCO2e)'], "ShadeDepth",  notched = True)
    chep_bx_22 = px.box(CHEP_co2, CHEP_co2["SHGC"], CHEP_co2['UpfrontCO2 (KgCO2e)'], "SHGC",notched = True)
    chep_bx_23 = px.box(CHEP_co2, CHEP_co2["ExWall"], CHEP_co2['UpfrontCO2 (KgCO2e)'], "ExWall", notched = True)

    cols = st.columns(5)
    
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
    
    
    chep_bx_25 = px.box(CHEP_co2, CHEP_co2["WWR-NS"], CHEP_co2['WoL (KgCO2e)'], "WWR-NS", notched = True)
    chep_bx_26 = px.box(CHEP_co2, CHEP_co2["WWR-EW"], CHEP_co2['WoL (KgCO2e)'], "WWR-EW", notched = True)
    chep_bx_27 = px.box(CHEP_co2, CHEP_co2["ShadeDepth"], CHEP_co2['WoL (KgCO2e)'], "ShadeDepth",  notched = True)
    chep_bx_28 = px.box(CHEP_co2, CHEP_co2["SHGC"], CHEP_co2['WoL (KgCO2e)'], "SHGC",notched = True)
    chep_bx_29 = px.box(CHEP_co2, CHEP_co2["ExWall"], CHEP_co2['WoL (KgCO2e)'], "ExWall", notched = True)
        
    cols = st.columns(5)
    
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
        
        
#Correlations
#-------------------------------------------------------------------------------------------------------------------------------------


CHEP_co2_lm = CHEP_co2.drop(['VLT','Conc_Roof(m3)', 'Conc_ExWall(m3)', 'Conc_Floor(m3)','ins_Roof(m3)', 'ins_ExWall(m3)', 'ins_IntWall(m3)', 
                             'PB_Roof(m3)','PB_ExWall(m3)', 'PB_IntWall(m3)', 'Glass(m2)', 'ShadeArea(m2)','roof_contribution', 
                             'wall_contribution', 'inwall_contribution', 'glass_contribution', 'shades_contribution','UpfrontCO2 (KgCO2e)'], axis=1)


CHEP_co2_CORR_HTM = px.imshow(round(CHEP_co2_lm.corr(),2),text_auto=True,color_continuous_scale='greens',  width = 1000, height = 1000,title = 'Design Input Correlations with Carbon Targets')
CHEP_co2_CORR_HTM.update_traces(textfont_size=15)

st.plotly_chart(CHEP_co2_CORR_HTM, use_container_width=True)

st.markdown('**:red[Note:]** Numbers represent the magnitude level of variables against each other, and Negative Values mean the input impacts the target negatively.')

