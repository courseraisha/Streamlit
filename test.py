$pip install streamlit
$pip install pandas
$pip install numpy
$pip install plotly

import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Title for the app
st.title("RED DOT FOUNDATION")

# Sidebar title and file uploader
st.sidebar.title('File Upload')
uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=['csv', 'xlsx'])

# Selectbox for data analysis or visualization
selected_option = st.sidebar.selectbox("Select an option", ["Data Analysis", "Data Visualization","Summary"])

# If file is uploaded, read the data
if uploaded_file is not None:
    try:
        # Attempt to read the uploaded file as a DataFrame
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    except Exception as e:
        st.sidebar.error('Error: Unable to read file. Please upload a valid CSV or Excel file.')

    if 'df' in locals():
        st.write('**Uploaded Data:**')
        st.dataframe(df)

        # Perform data analysis based on the selected option
        if selected_option == "Data Analysis":
            st.write("**Performing Data Analysis...**")
            
            # Display basic statistics of the data
            st.write("**Summary Statistics:**")
            st.write(df.describe())
            
            # Sidebar for sorting data
            st.sidebar.subheader("Sort Data:")
            sort_columns = st.sidebar.multiselect("Select columns to sort by:", df.columns)
            sort_order = st.sidebar.radio("Sort order:", ["Ascending", "Descending"])
            if sort_columns:
                sorted_df = df.sort_values(by=sort_columns, ascending=sort_order == "Ascending")
                st.write("**Sorted Data:**")
                st.dataframe(sorted_df)
            else:
                st.write("Please select at least one column to sort by.")

            # Analysis based on audience
            st.subheader("Data Analysis based on Audience:")
            selected_month = st.selectbox("Select a month:", df['Month'].unique())
            selected_month_data = df[df['Month'] == selected_month]
            st.subheader(f"Audience Count for {selected_month}:")
            audience_count_for_month = selected_month_data['Audience'].value_counts()
            st.write(audience_count_for_month)

            # Distribution of languages spoken in different locations
            language_distribution = df.groupby(['Location', 'Language ']).size().unstack(fill_value=0)
            st.subheader("Distribution of Languages Spoken in Different Locations:")
            st.write(language_distribution)

        # Perform data visualization based on the selected option
        elif selected_option == "Data Visualization":
            st.write("**Performing Data Visualization...**")
            st.subheader("Month Analysis")
            months = st.multiselect("Select months:", df['Month'].unique())
            filtered_data = df[df['Month'].isin(months)]
            audience_month_count = filtered_data.groupby(['Audience', 'Month']).size().reset_index(name='Count')
            organization_month_count = filtered_data.groupby(['Organization','Month']).size().reset_index(name='Count' )
            fig = px.bar(audience_month_count, x='Audience', y='Count', color='Month', barmode='group', title='Number of Audiences by Category and Month')
            st.plotly_chart(fig)
            fig = px.bar(organization_month_count, x='Organization', y='Count', color='Month', barmode='group', title='Number of Audiences by Category and Month')
            st.plotly_chart(fig)
            st.subheader("Language Analysis")
            locations = st.multiselect("Select locations:", df['Location'].unique())
            filtered_data = df[df['Location'].isin(locations)]
            location_lang_count = filtered_data.groupby(['Language ', 'Location']).size().reset_index(name='Count')
            fig = px.bar(location_lang_count, x='Language ', y='Count', title='Language Count by Location')
            st.plotly_chart(fig)
            st.subheader("Trainer Analysis")
            cities = st.multiselect("Select Cities:", df['City'].unique())
            filtered_data = df[df['City'].isin(cities)]
            city_trainer_count = filtered_data.groupby(['Trainer ', 'City']).size().reset_index(name='Count')
            fig = px.bar(city_trainer_count, x='Trainer ', y='Count', title='Language Count by Location')
            st.plotly_chart(fig)
            st.subheader("Total Sessions by Month Analysis")
            sessions_by_month = df.groupby('Month')['Total'].sum().reset_index()
            fig = px.bar(sessions_by_month, x='Month', y='Total', title='Total Sessions by Month')
            st.plotly_chart(fig)
            st.subheader("Gender Analysis")
            gender_by_audience = df.groupby('Audience')[['Gender (M)', 'Gender (F)']].sum().reset_index()
            gender_by_audience_melted = pd.melt(gender_by_audience, id_vars='Audience', var_name='Gender', value_name='Count')
            fig = px.bar(gender_by_audience_melted, x='Audience', y='Count', color='Gender', barmode='group', title='Gender Analysis by Audience')
            st.plotly_chart(fig)

        elif selected_option == "Summary":
            data = pd.read_excel("C:/Users/Admin/Desktop/Summary.xlsx")
            st.write(data)
