import streamlit as st
import pandas as pd

# Function to load and process data from multiple sheets
def load_and_process_data(file):
    sheets = ["Jan", "Feb", "Mar", "Apr"]
    data_frames = []

    for sheet in sheets:
        data = pd.read_excel(file, sheet_name=sheet, usecols=['Nama', 'Bulan', 'Jabatan', 'Rata-rata hasil kerja', 'Rata-rata perilaku', 'Nilai rata-rata', 'Predikat kinerja', 'Status'])
        data_frames.append(data)

    # Concatenate all data frames
    data = pd.concat(data_frames)

    # Map months to quarters
    quarter_mapping = {
        "Januari": "Q1", "Februari": "Q1", "Maret": "Q1",
        # "April": "Q2", "Mei": "Q2", "Juni": "Q2",
        # "Juli": "Q3", "Agustus": "Q3", "September": "Q3",
        # "Oktober": "Q4", "November": "Q4", "Desember": "Q4"
    }
    data['Triwulan'] = data['Bulan'].map(quarter_mapping)

    # Aggregate individual performance by quarter
    individu_performance = data.groupby(['Nama']).agg({
        'Rata-rata hasil kerja': 'mean',
        'Rata-rata perilaku': 'mean',
        'Nilai rata-rata': 'mean'
    }).reset_index()

    # Aggregate job role performance by quarter
    jabatan_performance = data.groupby(['Jabatan']).agg({
        'Rata-rata hasil kerja': 'mean',
        'Rata-rata perilaku': 'mean',
        'Nilai rata-rata': 'mean'
    }).reset_index()

    # Aggregate quarterly performance
    triwulan_performance = data.groupby(['Triwulan', 'Nama']).agg({
        'Rata-rata hasil kerja': 'mean',
        'Rata-rata perilaku': 'mean',
        'Nilai rata-rata': 'mean'
    }).reset_index()

    return individu_performance, jabatan_performance, triwulan_performance

# Function to get top 6 performers
def get_top_performers_by_quarter(triwulan_performance, quarter):
    # Filter by the selected quarter
    filtered_data = triwulan_performance[triwulan_performance['Triwulan'] == quarter]
    top_performers = individu_performance.sort_values(by='Nilai rata-rata', ascending=False).head(6)
    return top_performers

# Streamlit app
st.title('Performance Data Analysis')

# File uploader
uploaded_file = st.file_uploader('Upload your Excel file', type='xlsx')

if uploaded_file:
    individu_performance, jabatan_performance, triwulan_performance = load_and_process_data(uploaded_file)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Go to", ["Individual Performance", "Job Role Performance", "Quarterly Performance", "Top 6 Performers"])
    
    if option == "Individual Performance":
        st.subheader('Individual Performance')
        st.write(individu_performance)
    elif option == "Job Role Performance":
        st.subheader('Job Role Performance')
        st.write(jabatan_performance)
    elif option == "Quarterly Performance":
        st.subheader('Quarterly Performance')
        
        # Additional navigation for quarters with descriptions
        quarter_options = {
            "Q1 (Januari - Maret)": "Q1",
            "Q2 (April - Juni)": "Q2",
            "Q3 (Juli - September)": "Q3",
            "Q4 (Oktober - Desember)": "Q4"
        }
        quarter_label = st.sidebar.radio("Select Quarter", list(quarter_options.keys()))
        selected_quarter = quarter_options[quarter_label]
        quarter_data = triwulan_performance[triwulan_performance['Triwulan'] == selected_quarter]
        st.write(quarter_data)
    elif option == "Top 6 Performers":
        st.subheader('Top 6 Performers')
         # Additional navigation for quarters with descriptions
        quarter_options = {
            "Q1 (Januari - Maret)": "Q1",
            "Q2 (April - Juni)": "Q2",
            "Q3 (Juli - September)": "Q3",
            "Q4 (Oktober - Desember)": "Q4"
        }
        quarter_label = st.sidebar.radio("Select Quarter", list(quarter_options.keys()))
        selected_quarter = quarter_options[quarter_label]
        top_performers = get_top_performers_by_quarter(triwulan_performance, selected_quarter)
        st.write(top_performers)

    # Option to download the processed data
    individu_csv = individu_performance.to_csv(index=False).encode('utf-8')
    jabatan_csv = jabatan_performance.to_csv(index=False).encode('utf-8')
    triwulan_csv = triwulan_performance.to_csv(index=False).encode('utf-8')

    st.sidebar.download_button(
        label='Download Individual Performance Data as CSV',
        data=individu_csv,
        file_name='individu_performance.csv',
        mime='text/csv'
    )

    st.sidebar.download_button(
        label='Download Job Role Performance Data as CSV',
        data=jabatan_csv,
        file_name='jabatan_performance.csv',
        mime='text/csv'
    )

    st.sidebar.download_button(
        label='Download Quarterly Performance Data as CSV',
        data=triwulan_csv,
        file_name='triwulan_performance.csv',
        mime='text/csv'
    )

    if option == "Top 6 Performers":
        top_performers_csv = top_performers.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label='Download Top Performers Data as CSV',
            data=top_performers_csv,
            file_name='top_performers.csv',
            mime='text/csv'
        )
