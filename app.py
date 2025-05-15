import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Load tipper data
def load_data():
    data = {
        'Tipper': ['TIPPEG-4 - APSYM/WSB1', 'TIPPEG-5 - APSYM/ASF1', 'TIPPEG-6 - APSYM/CSF2', 
                  'TIPPEG-7 - APSYM/CSF3A', 'TIPPEG-8 - APSYM/CSF4'],
        'Last_service_MMR': [1000, 1000, 1757, 0, 0],
        'Type_of_Service': ['', '', '1000hrs Service', '', ''],
        'Due_Hours': [1000, 2500, 2759, 1000, 1000],
        'Current_MMR': [2817, 2322, 1025, 1007, 1005],
        'Remaining_MMR': [-91, -172, -72, -8, 45],
        'Expires_Q1': [True, True, True, True, True],
        'Expires_QII_Filter': [True, True, True, True, True],
        'Fust_Filter': [True, True, True, True, True],
        'Parts_under_1000hrs': [True, True, True, True, True]
    }
    return pd.DataFrame(data)

# Calculate maintenance status
def calculate_status(row):
    if row['Remaining_MMR'] < 0:
        return 'OVERDUE'
    elif row['Remaining_MMR'] < 100:
        return 'DUE SOON'
    else:
        return 'OK'

# Streamlit app
def main():
    st.title('Tipper Maintenance Dashboard')
    st.subheader('May 2025 Service Schedule')
    
    # Load and process data
    df = load_data()
    df['Status'] = df.apply(calculate_status, axis=1)
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tippers", len(df))
    col2.metric("Overdue Services", len(df[df['Status'] == 'OVERDUE']))
    col3.metric("Due Soon", len(df[df['Status'] == 'DUE SOON']))
    
    # Color coding for status
    def color_status(val):
        color = 'red' if val == 'OVERDUE' else 'orange' if val == 'DUE SOON' else 'green'
        return f'background-color: {color}'
    
    # Display main table
    st.dataframe(df.style.applymap(color_status, subset=['Status']))
    
    # Maintenance alerts section
    st.subheader('Maintenance Alerts')
    
    overdue = df[df['Status'] == 'OVERDUE']
    due_soon = df[df['Status'] == 'DUE SOON']
    
    if not overdue.empty:
        st.error('⚠️ Overdue Maintenance')
        st.dataframe(overdue[['Tipper', 'Current_MMR', 'Due_Hours', 'Remaining_MMR']])
        
    if not due_soon.empty:
        st.warning('⚠️ Maintenance Due Soon')
        st.dataframe(due_soon[['Tipper', 'Current_MMR', 'Due_Hours', 'Remaining_MMR']])
    
    # Filter replacement section
    st.subheader('Filter Replacement Status')
    filter_df = df[['Tipper', 'Expires_Q1', 'Expires_QII_Filter', 'Fust_Filter']]
    st.dataframe(filter_df)
    
    # Service history and scheduling
    st.subheader('Service Scheduling')
    selected_tipper = st.selectbox('Select Tipper', df['Tipper'])
    tipper_data = df[df['Tipper'] == selected_tipper].iloc[0]
    
    st.write(f"**Current MMR:** {tipper_data['Current_MMR']}")
    st.write(f"**Next Service Due At:** {tipper_data['Due_Hours']} hours")
    st.write(f"**Remaining Hours Until Service:** {max(0, tipper_data['Remaining_MMR'])}")
    
    # Service form
    with st.form("service_form"):
        st.write(f"Log Service for {selected_tipper}")
        service_type = st.selectbox("Service Type", ["1000hrs Service", "2500hrs Service", "Other"])
        service_date = st.date_input("Service Date")
        service_notes = st.text_area("Notes")
        submitted = st.form_submit_button("Submit Service")
        
        if submitted:
            st.success(f"Service for {selected_tipper} logged successfully")
            # Here you would update your database with the new service record

if __name__ == '__main__':
    main()
