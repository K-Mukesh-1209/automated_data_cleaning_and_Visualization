import streamlit as st
import pandas as pd

# Define possible data types and country information
DATA_TYPES = ["primary", "date", "time", "phone", "email", 
              "string", "integer","categorical", "weights", "distance"]

WEIGHT_UNITS = ["gram", "kilogram", "pound", "ounce"]
DISTANCE_UNITS = ["meter", "kilometer", "mile", "foot"]

COUNTRIES = {
    "USA": {"time_zones": ["America/New_York", "America/Chicago", "America/Los_Angeles"], "phone_code": "+1"},
    "India": {"time_zones": ["Asia/Kolkata"], "phone_code": "+91"},
    "UK": {"time_zones": ["Europe/London"], "phone_code": "+44"},
    "Germany": {"time_zones": ["Europe/Berlin"], "phone_code": "+49"},
    "Japan": {"time_zones": ["Asia/Tokyo"], "phone_code": "+81"}
}

# Initialize session state for storing selections
if 'column_config' not in st.session_state:
    st.session_state.column_config = {}

st.title("Advanced File Attribute Configuration")

# File upload section
uploaded_file = st.file_uploader("Upload your file (CSV or Excel)", type=["csv", "xlsx"])

def show_country_selections(column, col_container):
    """Show country and specific configurations based on data type"""
    config = st.session_state.column_config.get(column, {})
    
    country = col_container.selectbox(f"Select country for {column}:",
                                      options=list(COUNTRIES.keys()),
                                      index=list(COUNTRIES.keys()).index(config.get("country", "USA")),
                                      key=f"country_{column}")
    st.session_state.column_config[column]["country"] = country
    
    if config["type"] == "time":
        time_zone = col_container.selectbox(f"Select time zone for {column}:",
                                            options=COUNTRIES[country]["time_zones"],
                                            key=f"tz_{column}")
        st.session_state.column_config[column]["time_zone"] = time_zone
        
    elif config["type"] == "phone":
        phone_code = col_container.text_input(f"Phone code for {column}:",
                                              value=COUNTRIES[country]["phone_code"],
                                              key=f"pc_{column}")
        st.session_state.column_config[column]["phone_code"] = phone_code

def show_unit_selection(column, col_container, unit_options, unit_type):
    """Show unit selection for weights or distance"""
    unit = col_container.selectbox(f"Select {unit_type} unit for {column}:",
                                   options=unit_options,
                                   key=f"unit_{column}")
    st.session_state.column_config[column]["unit"] = unit

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file, engine='openpyxl')
        
        with st.expander("File Preview", expanded=True):
            st.write(f"Dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
            st.dataframe(df.head(3))

        with st.expander("Column Configuration", expanded=True):
            st.markdown("**Configure column types and regional settings**")
            
            for column in df.columns:
                col_container = st.container()
                col1, col2 = col_container.columns([2, 3])
                
                current_type = col1.selectbox(f"**{column}** type:",
                                              options=DATA_TYPES,
                                              index=DATA_TYPES.index(st.session_state.column_config.get(column, {}).get("type", "string")),
                                              key=f"type_{column}")
                
                if column not in st.session_state.column_config:
                    st.session_state.column_config[column] = {"type": current_type}
                else:
                    st.session_state.column_config[column]["type"] = current_type
                
                if current_type in ["time", "phone"]:
                    show_country_selections(column, col2)
                elif current_type == "weights":
                    show_unit_selection(column, col2, WEIGHT_UNITS, "weight")
                elif current_type == "distance":
                    show_unit_selection(column, col2, DISTANCE_UNITS, "distance")
                else:
                    st.session_state.column_config[column].pop("country", None)
                    st.session_state.column_config[column].pop("time_zone", None)
                    st.session_state.column_config[column].pop("phone_code", None)
                    st.session_state.column_config[column].pop("unit", None)

        with st.expander("Review Configuration", expanded=True):
            st.markdown("**Current Configuration:**")
            for col, config in st.session_state.column_config.items():
                if config["type"] in ["time", "phone"]:
                    st.write(f"""
                    - **{col}**: {config['type']}  
                      Country: {config.get('country', 'N/A')}  
                      {'Time Zone' if config['type'] == 'time' else 'Phone Code'}: 
                      {config.get('time_zone', 'N/A') if config['type'] == 'time' else config.get('phone_code', 'N/A')}
                    """)
                elif config["type"] in ["weights", "distance"]:
                    st.write(f"- **{col}**: {config['type']} ({config.get('unit', 'N/A')})")
                else:
                    st.write(f"- **{col}**: {config['type']}")
    
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
else:
    st.info("Please upload a CSV or Excel file to begin")

# Sidebar with country reference
with st.sidebar:
    st.markdown("**Country Reference Data**")
    for country, info in COUNTRIES.items():
        st.markdown(f"""
        **{country}**  
        - Phone Code: {info['phone_code']}  
        - Time Zones: {', '.join(info['time_zones'])}
        """)


import json
with open("shared_config.json", "w") as f:
    json.dump(st.session_state.column_config, f)