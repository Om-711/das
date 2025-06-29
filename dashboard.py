import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns

# --- PAGE TITLE ---
st.set_page_config(page_title="Solar Dashboard", layout="wide")
st.title("🔆 Solar Energy Dashboard")
st.markdown("""
<style>
    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
        padding: 12px;
    }
    .metric-label {
        font-weight: bold;
        font-size: 16px;
    }
    .block-container {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3,tab5 = st.tabs(["📊 Performance Analyzer", "📈 Feature Visualizations", "📉 Performance Analyzer", "📐 Correlation Matrix"])

# --- Feature Groups for Visualization ---
feature_groups = {
    'SCB Current (A)': [
        'inversores_ctin03_strings_string8_pv_i9', 'inversores_ctin03_strings_string8_pv_i13',
        'inversores_ctin03_strings_string8_pv_i1', 'inversores_ctin03_strings_string8_pv_i6',
        'inversores_ctin03_strings_string8_pv_i4', 'inversores_ctin03_strings_string8_pv_i11',
        'inversores_ctin03_strings_string8_pv_i10', 'inversores_ctin03_strings_string8_pv_i2',
        'inversores_ctin03_strings_string8_pv_i5', 'inversores_ctin03_strings_string8_pv_i7',
        'inversores_ctin03_strings_string8_pv_i12', 'inversores_ctin03_strings_string8_pv_i3',
        'inversores_ctin03_strings_string8_pv_i8',
        'inversores_ctin03_strings_string10_pv_i4', 'inversores_ctin03_strings_string10_pv_i9',
        'inversores_ctin03_strings_string10_pv_i7', 'inversores_ctin03_strings_string10_pv_i12',
        'inversores_ctin03_strings_string10_pv_i8', 'inversores_ctin03_strings_string10_pv_i13',
        'inversores_ctin03_strings_string10_pv_i10', 'inversores_ctin03_strings_string10_pv_i6',
        'inversores_ctin03_strings_string10_pv_i11', 'inversores_ctin03_strings_string10_pv_i5',
        'inversores_ctin03_strings_string10_pv_i1', 'inversores_ctin03_strings_string10_pv_i3',
        'inversores_ctin03_strings_string10_pv_i2',
        'inversores_ctin08_strings_string9_pv_i12', 'inversores_ctin08_strings_string9_pv_i13',
        'inversores_ctin08_strings_string9_pv_i1', 'inversores_ctin08_strings_string9_pv_i7',
        'inversores_ctin08_strings_string9_pv_i8', 'inversores_ctin08_strings_string9_pv_i6',
        'inversores_ctin08_strings_string9_pv_i10', 'inversores_ctin08_strings_string9_pv_i9',
        'inversores_ctin08_strings_string9_pv_i11', 'inversores_ctin08_strings_string9_pv_i4',
        'inversores_ctin08_strings_string9_pv_i5', 'inversores_ctin08_strings_string9_pv_i2',
        'inversores_ctin08_strings_string9_pv_i3',
        'inversores_ctin08_strings_string12_pv_i4', 'inversores_ctin08_strings_string12_pv_i1',
        'inversores_ctin08_strings_string12_pv_i5', 'inversores_ctin08_strings_string12_pv_i7',
        'inversores_ctin08_strings_string12_pv_i3', 'inversores_ctin08_strings_string12_pv_i6',
        'inversores_ctin08_strings_string12_pv_i2', 'inversores_ctin08_strings_string12_pv_i8',
        'inversores_ctin08_strings_string12_pv_i9', 'inversores_ctin08_strings_string12_pv_i10'
    ],
    'SCB Voltage (V)': [
        'inversores_ctin03_strings_string8_pv_v', 'inversores_ctin03_strings_string10_pv_v',
        'inversores_ctin08_strings_string9_pv_v', 'inversores_ctin08_strings_string12_pv_v'
    ],
    'Solar Irradiation (W/m²)': [
        'meteorolgicas_em_03_02_gii', 'meteorolgicas_em_08_01_gii',
        'meteorolgicas_em_03_02_ghi', 'meteorolgicas_em_08_01_ghi',
        'meteorolgicas_em_08_01_gii_rear', 'meteorolgicas_em_03_02_gii_rear'
    ],
    'Temperature (°C)': [
        'meteorolgicas_em_03_02_t_amb', 'meteorolgicas_em_08_01_t_amb',
        'celulas_ctin08_cc_08_2_t_amb', 'celulas_ctin03_cc_03_1_t_amb',
        'celulas_ctin08_cc_08_1_t_amb', 'celulas_ctin03_cc_03_2_t_amb',
        'celulas_ctin03_cc_03_1_t_mod', 'celulas_ctin08_cc_08_2_t_mod',
        'celulas_ctin03_cc_03_2_t_mod', 'celulas_ctin08_cc_08_1_t_mod'
    ],
    'Humidity (%)': ['meteorolgicas_em_03_02_h_r', 'meteorolgicas_em_08_01_h_r'],
    'Wind Speed (m/s)': ['meteorolgicas_em_03_02_ws', 'meteorolgicas_em_08_01_ws'],
    'Wind Direction (°)': ['meteorolgicas_em_03_02_wd', 'meteorolgicas_em_08_01_wd'],
    # 'Shading Sensor (IR)': [
    #     'celulas_ctin08_cc_08_1_ir_cel_1', 'celulas_ctin08_cc_08_2_ir_cel_1',
    #     'celulas_ctin03_cc_03_1_ir_cel_1', 'celulas_ctin03_cc_03_2_ir_cel_1',
    #     'celulas_ctin03_cc_03_1_ir_cel_2', 'celulas_ctin03_cc_03_2_ir_cel_2',
    #     'celulas_ctin08_cc_08_1_ir_cel_2', 'celulas_ctin08_cc_08_2_ir_cel_2'
    # ],
    'Energy Generation': [
        'inversores_ctin03_inv_03_03_eact_tot', 'inversores_ctin08_inv_08_08_eact_tot'
    ],
    'DC Input Power': [
        'inversores_ctin03_inv_03_03_p_dc', 'inversores_ctin08_inv_08_08_p_dc'
    ],
    'AC Output Power': [
        'inversores_ctin03_inv_03_03_p', 'inversores_ctin08_inv_08_08_p'
    ],
    
    'Datalogger Temperature (°C)': [
        'meteorolgicas_em_03_02_t_dlogger',
        'meteorolgicas_em_08_01_t_dlogger'
    ]

}

with tab1:
    st.header("📊 Data Analytics")

    # --- Monthly Energy Loss Plot (Image) ---
    st.markdown("---")
    st.subheader("📆 Monthly Energy Loss")

    st.image("Images/energy_loss.png", caption="Monthly Energy Loss", width=850)



# # --- TAB 1: Data Analytics ---
# with tab1:
#     st.header("📊 Data Analytics")
   
#     df = pd.read_csv("Dataset 1.csv", parse_dates=["datetime"])
#     df["Energy Loss"] = df["ttr_potenciaproducible"] - df["ppc_p_tot"]

#     # --- Metric Display ---
#     st.metric("📉 Avg. Loss per Hour", f"{df['Energy Loss'].mean():.2f} kWh")

#     # --- Monthly Energy Loss Plot ---
#     st.markdown("---")
#     st.subheader("📆 Monthly Energy Loss")
#     df["month"] = df["datetime"].dt.to_period("M").astype(str)
#     monthly_loss = df.groupby("month")["Energy Loss"].sum()

#     fig_month, ax_month = plt.subplots(figsize=(12, 4))  # Approx. 800px wide
#     ax_month.bar(monthly_loss.index, monthly_loss.values, color="orange")
#     ax_month.set_title("Total Energy Loss per Month")
#     ax_month.set_xlabel("Month")
#     ax_month.set_ylabel("Energy Loss (kWh)")
#     ax_month.tick_params(axis='x', rotation=45)
#     st.pyplot(fig_month)


# --- TAB 2: Visualizations ---
with tab2:
    st.header("📈 Feature Visualization")

    # --- Feature group selection ---
    st.subheader("🧰 Select Feature Group")
    selected_group = st.selectbox("Feature Group", list(feature_groups.keys()))


    # --- Choose Time Granularity (Only one) ---
    # st.subheader("⏱ Choose Visualization Granularity")
    viz_type = st.radio(
        "Select one:",
        options=["Raw", "Hourly", "Daily", "Weekly"],
        horizontal=True
    )

    raw_image_map = {
        "SCB Current (A)": ["Images/SCB_current_nan.png", "Images/SCB_current_zero.png"],
        "SCB Voltage (V)": ["Images/scb_voltage_nan.png", "Images/voltage_zero.png"],
        "Energy Generation": ["Images/energy_generation_nan.png", "Images/energy_generation_zero.png"],
        "DC Input Power": ["Images/dc_input_nan.png", "Images/dc_input_zero.png"],
        "AC Output Power": ["Images/ac_input_nan.png", "Images/ac_input_zero.png"],
        "Solar Irradiation (W/m²)": ["Images/nonzero_nighttime_iradiance.png"],
        "Temperature (°C)": ["Images/temperature_nan.png", "Images/temperature_zero.png", "Images/temp_min_max.png"],
        "Wind Speed (m/s)": ["Images/windspeed_nan.png", "Images/windspeed_zero.png"],
        "Wind Direction (°)": ["Images/winddir_nan.png", "Images/winddi_zero.png"],
        "Humidity (%)": ["Images/humidity_nan.png", "Images/humidity_zero.png"],
        "Datalogger Temperature (°C)": ["Images/datalogger_nan.png", "Images/datalogger_zero.png"],
        # "shading": ["Images/shading_nan.png", "Images/shading_zero.png"]
    }



    # --- Image mapping for each granularity ---
    hourly_image_map = {
        "SCB Current (A)": ["Images/Average_SCB_Current.png"],
        "SCB Voltage (V)": ["Images/Average_SCB_Voltage.png"],
        "Energy Generation": ["Images/hourly_energy_generation.png"],  
        "DC Input Power": ["Images/hourly_dc_input.png"],              
        "AC Output Power": ["Images/hourly_ac_output.png"],            
        "Solar Irradiation (W/m²)": ["Images/hourly_solar_iradiance.png"],  
        "Temperature (°C)": ["Images/hourly_temp_station.png", "Images/hourly_temp.png"],         
        "Wind Speed (m/s)": ["Images/windspeed_hourly.png", "Images/windspeed_histogram.png"],
        "Wind Direction (°)": ["Images/winddir_hourly.png", "Images/winddir_histogram.png"],
        "Humidity (%)": ["Images/humidity_hourly.png", "Images/humidity_histogram.png"],
        "Datalogger Temperature (°C)": ["Images/datalogger_hourly.png", "Images/datalogger_histogram.png"],
        # "shading": ["Images/hourly_shading.png"]
    }


    daily_image_map = {
        "SCB Current (A)": ["Images/daily_scb_current.png"],
        "SCB Voltage (V)": ["Images/daily_scb_voltage.png"],
        "Energy Generation": ["Images/daily_energy_generation.png"],
        "DC Input Power": ["Images/daily_dc_input.png"],
        "AC Output Power": ["Images/daily_ac_output.png"],
        "Solar Irradiation (W/m²)": ["Images/daily_solar_iradiance.png"],
        "Temperature (°C)": ["Images/daily_temp_station.png", "Images/daily_temp.png"],
        "Wind Speed (m/s)": ["Images/daily_windspeed.png"],
        "Wind Direction (°)": ["Images/daily_winddir.png"],
        "Humidity (%)": ["Images/daily_humidity.png"],
        "Datalogger Temperature (°C)": ["Images/daily_datalogger.png"],
        # "shading": ["Images/daily_shading.png"]
    }

    weekly_image_map = {
        "SCB Current (A)": ["Images/weekly_scb_current.png"],
        "SCB Voltage (V)": ["Images/weekly_scb_voltage.png"],
        "Energy Generation": ["Images/weekly_energy_generation.png"],
        "DC Input Power": ["Images/weekly_dc_input.png"],
        "AC Output Power": ["Images/weekly_ac_output.png"],
        "Solar Irradiation (W/m²)": ["Images/iradiance_weekly.png"],
        "Temperature (°C)": [
            "Images/weekly_temp.png",
            "Images/weekly_temp_dstation.png",
            "Images/ambient_temp.png"
        ],
        "Wind Speed (m/s)": ["Images/weekly_windspeed.png"],
        "Wind Direction (°)": ["Images/weekly_winddir.png"],
        "Humidity (%)": ["Images/weekly_humidity.png"],
        "Datalogger Temperature (°C)": ["Images/weekly_datalogger.png"],
        # "shading": ["Images/weekly_shading.png"]
    }


    # --- Display Visualization based on selected type ---
    st.markdown("---")
    st.subheader(f"📷 {viz_type} Visualization")

    image_map = {
        'Raw' : raw_image_map,
        "Hourly": hourly_image_map,
        "Daily": daily_image_map,
        "Weekly": weekly_image_map
    }

    images = image_map[viz_type].get(selected_group, [])

    if images:
        for i in range(0, len(images), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(images):
                    with cols[j]:
                        st.image(images[i + j], caption=f"{selected_group} — {viz_type} Plot {i + j + 1}", width=680)


    # if images:
    #     for i, img_path in enumerate(images):
    #         st.image(img_path, caption=f"{selected_group} — {viz_type} Plot {i+1}", width=800)  # 👈 set width here (e.g., 800px)
    # else:
    #     st.info(f"No {viz_type.lower()} images available for this feature group.")


# --- TAB 3: Performance Analyzer ---
with tab3:
    st.header("📉 Performance Analyzer")

    # Step 1: Time granularity
    granularity = st.radio("Select Time Granularity", ["Raw", "Hourly", "Daily", "Weekly"], horizontal=True)

    scope = None
    plant_number = None
    string_number = None

    if granularity != "Raw":
        # Step 2: Analysis Scope
        scope = st.radio("Select Scope", ["Plant Level", "String Level"], horizontal=True)

        if scope == "Plant Level":
            plant_number = st.selectbox("Select Plant", ["3", "8"])
        elif scope == "String Level":
            string_number = st.selectbox("Select String", ["8", "9", "10", "12"])

    # Define image paths
    image_paths = {
        "Raw": ["Images/combine_loss_hourly.png"],
        "Hourly": {
            "Plant Level": {"3": ["Images/plant3_hourly.png"], 
                            "8": ["Images\plant8_hourly.png"]},
            
            "String Level": {"8": ["Images/string8_hourly.png"],
                             "9": ["Images/string9_hourly.png"],
                             "10": ["Images/string10_hourly.png"],
                             "12": ["Images/string12_hourly.png"]}
        },
        "Daily": {
            "Plant Level": {"3": ["Images/plant3_daily.png"], 
                            "8": ["Images/plant8_daily.png"]},

            "String Level": {"8": ["Images/string8_daily.png"], 
                             "9": ["Images/string9_daily.png"], 
                             "10": ["Images/string10_daily.png"], 
                             "12": ["Images/string12_daily.png"]}
        },
        "Weekly": {
            "Plant Level": {"3": ["Images/plant3_weekly.png"], 
                            "8": ["Images/plant8_weekly.png"]},

            "String Level": {"8": ["Images/string8_weekly.png"], 
                             "9": ["Images/string9_weekly.png"],
                            "10": ["Images/string10_weekly.png"], 
                            "12": ["Images/string12_weekly.png"]}
        }
    }

    st.markdown("---")
    st.subheader(f"📈 Performance - {granularity} View")

    images_to_display = []

    if granularity == "Raw":
        images_to_display = image_paths.get("Raw", [])
    else:
        if granularity in image_paths:
            if scope == "Plant Level" and plant_number:
                images_to_display = image_paths[granularity]["Plant Level"].get(plant_number, [])
            elif scope == "String Level" and string_number:
                images_to_display = image_paths[granularity]["String Level"].get(string_number, [])

    if images_to_display:
        for img in images_to_display:
            st.image(img, caption=f"{granularity} - {scope or 'Raw'} View", width=800)
    else:
        st.info("No images available for selected configuration.")

# # --- TAB 4: Model Insights ---
# with tab4:
#     st.header("🧮 Model Insights")
#     st.write("You can show model predictions here or SHAP value explanations.")
#     st.info("This section is placeholder for ML models or advanced analytics.")


# --- TAB 5: Correlation Matrix ---
with tab5:
    # st.header("📐 Feature Correlation Matrix")

    st.subheader("🖼️ Correlation by Feature Group")

    # Define feature group with appropriate image names
    corr_image_map = {
        "SCB Current (A)": ["Images/corr_string.png"],
        "SCB Voltage (V)": ["Images/corr_string.png"],
        "Energy Generation": ["Images/corr_ac.png"],
        "DC Input Power": ["Images/corr_ac.png"],
        "AC Output Power": ["Images/corr_ac.png"],
        "Solar Irradiation (W/m²)": ["Images/corr_solar_iradiance.png"],
        "Temperature (°C)": ["Images/corr_solar_iradiance.png"],
        "Wind Speed (m/s)": ["Images/corr_windspeed.png"],
        "Wind Direction (°)": ["Images/corr_winddir.png"],
        "Humidity (%)": ["Images/corr_humidity.png"],
        "Datalogger Temperature (°C)": ["Images/corr_datalogger.png"]
    }

    # Create one tab per feature group
    feature_tabs = st.tabs(list(corr_image_map.keys()))

    for tab, feature_name in zip(feature_tabs, corr_image_map.keys()):
        with tab:
            st.markdown(f"### 📊 {feature_name}")
            for i, img_path in enumerate(corr_image_map[feature_name]):
                st.image(img_path, caption=f"{feature_name} - Correlation View {i + 1}", width=700)
