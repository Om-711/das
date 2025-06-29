import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns

# --- PAGE TITLE ---
st.set_page_config(page_title="Solar Dashboard", layout="wide")
st.title("🔆 ML Ascend Submission Dashboard")
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
    .team-card {
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
        margin: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .team-member-image {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        margin: 0 auto 15px;
        border: 4px solid white;
    }
    .team-member-name {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .team-social-links {
        margin-top: 15px;
    }
    .social-btn {
        display: inline-block;
        width: 40px;
        height: 40px;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        margin: 0 5px;
        line-height: 40px;
        text-align: center;
        color: white;
        text-decoration: none;
        font-size: 18px;
    }
    .social-btn:hover {
        background: rgba(255,255,255,0.3);
    }
</style>
""", unsafe_allow_html=True)


# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📉 Performance Analyzer", 
    "📊 Feature Visualizations", 
    "🔁 Actual vs Estimated Analysis", 
    "📐 Correlation Matrix",
     "👥 Our Team"
])

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

# --- TAB 1: Performance Analyzer ---
with tab1:
    st.header("📉 Performance Analyzer")

    # Step 1: Time granularity
    granularity = st.radio("Select Time Granularity", ["General", "Hourly", "Daily", "Weekly"], horizontal=True)

    scope = None
    plant_number = None
    string_number = None

    if granularity != "General":
        # Step 2: Analysis Scope
        scope = st.radio("Select Scope", ["Plant Level", "String Level"], horizontal=True)

        if scope == "Plant Level":
            plant_number = st.selectbox("Select Plant", ["3", "8"])
        elif scope == "String Level":
            string_number = st.selectbox("Select String", ["8", "9", "10", "12"])

    # Define image paths
    image_paths = {
        "General": ["Images/combine_loss_hourly.png"],
        "Hourly": {
            "Plant Level": {
                "3": ["Images/plant3_hourly.png"], 
                "8": ["Images/plant8_hourly.png"]
            },
            "String Level": {
                "8": ["Images/string8_hourly.png"],
                "9": ["Images/string9_hourly.png"],
                "10": ["Images/string10_hourly.png"],
                "12": ["Images/string12_hourly.png"]
            }
        },
        "Daily": {
            "Plant Level": {
                "3": ["Images/plant3_daily.png"], 
                "8": ["Images/plant8_daily.png"]
            },
            "String Level": {
                "8": ["Images/string8_daily.png"], 
                "9": ["Images/string9_daily.png"], 
                "10": ["Images/string10_daily.png"], 
                "12": ["Images/string12_daily.png"]
            }
        },
        "Weekly": {
            "Plant Level": {
                "3": ["Images/plant3_weekly.png"], 
                "8": ["Images/plant8_weekly.png"]
            },
            "String Level": {
                "8": ["Images/string8_weekly.png"], 
                "9": ["Images/string9_weekly.png"],
                "10": ["Images/string10_weekly.png"], 
                "12": ["Images/string12_weekly.png"]
            }
        }
    }

    st.markdown("---")
    st.subheader(f"📈 Performance - {granularity} View")

    images_to_display = []

    if granularity == "General":
        images_to_display = image_paths.get("General", [])
    else:
        if granularity in image_paths:
            if scope == "Plant Level" and plant_number:
                images_to_display = image_paths[granularity]["Plant Level"].get(plant_number, [])
            elif scope == "String Level" and string_number:
                images_to_display = image_paths[granularity]["String Level"].get(string_number, [])

    if images_to_display:
        for img in images_to_display:
            st.image(img, caption=f"{granularity} - {scope or 'General'} View", width=800)
    else:
        st.info("No images available for selected configuration.")

# --- TAB 2: Feature Visualizations ---
with tab2:
    st.header("📈 Feature Visualization")

    # --- Feature group selection ---
    st.subheader("🧰 Select Feature Group")
    selected_group = st.selectbox("Feature Group", list(feature_groups.keys()))

    # --- Choose Time Granularity ---
    viz_type = st.radio(
        "Select one:",
        options=["General", "Hourly", "Daily", "Weekly"],
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
        "Datalogger Temperature (°C)": ["Images/datalogger_nan.png", "Images/datalogger_zero.png"]
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
        "Datalogger Temperature (°C)": ["Images/datalogger_hourly.png", "Images/datalogger_histogram.png"]
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
        "Datalogger Temperature (°C)": ["Images/daily_datalogger.png"]
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
        "Datalogger Temperature (°C)": ["Images/weekly_datalogger.png"]
    }

    # --- Display Visualization based on selected type ---
    st.markdown("---")
    st.subheader(f"📷 {viz_type} Visualization")

    image_map = {
        'General': raw_image_map,
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
    else:
        st.info(f"No {viz_type.lower()} images available for this feature group.")

# --- TAB 5: Our Team ---
with tab5:
    st.header("👥 Our Team")
    st.markdown("### Meet the brilliant minds behind this Solar Energy Dashboard")
    
    # Team members data
    team_members = [
        {
            "name": "Paarth Batra",
            "image": "Images/paarth.jpeg",  
            "linkedin": "https://www.linkedin.com/in/paarth7/",
            "github": "https://github.com/hydro-7"
        },
        {
            "name": "Dhruv Singh",
            "image": "Images/dhruv.jpeg", 
            "linkedin": "https://www.linkedin.com/in/dhruv-singh-b12768285/",
            "github": "https://github.com/Vurhd0"
        },
        {
            "name": "Om Chiddarwar",
            "image": "Images/om.jpeg", 
            "linkedin": "https://www.linkedin.com/in/om-chiddarwar-29a947283/",
            "github": "https://github.com/Om-711"
        }
    ]
    
    # Display team members in a row
    cols = st.columns(3)
    
    for i, member in enumerate(team_members):
        with cols[i]:
            # Create team member card using HTML
            st.markdown(f"""
            <div class="team-card">
                <div class="team-member-name">{member['name']}</div>
                <div class="team-social-links">
                    <a href="{member['linkedin']}" target="_blank" class="social-btn">
                        <i class="fab fa-linkedin"></i> in
                    </a>
                    <a href="{member['github']}" target="_blank" class="social-btn">
                        <i class="fab fa-github"></i> </>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display image if available
            try:
                st.image(member['image'], width=200, caption=member['name'])
            except:
                # Fallback if image doesn't exist
                st.info(f"Photo coming soon for {member['name']}")
    
    st.markdown("---")
    st.markdown("**Indian Institute of Information Technology Design & Manufacturing, Kurnool**")
    st.markdown("*Building sustainable energy solutions through data analytics and machine learning*")
    st.markdown("© Copyright 2025")
    
