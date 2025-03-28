import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="💿Data Sweeper", layout='wide')

# Custom CSS for styling
st.markdown(
    '''
    <style>
    .stapp {
        background-color: black;
        color: white;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

# Title and description
st.title("Datasweeper Sterling By Maryam Haseeb")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Project for Quarter 3!")

# Upload files
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Load the file into a DataFrame
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File details and preview
        st.subheader(f"Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader(f"Data Cleaning Options for {file.name}")
        
        if st.checkbox(f"Enable data cleaning for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled!")

            # Column selection
            st.subheader(f"Select columns to keep in {file.name}")           
            columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

        # Data Visualization
        st.subheader(f"Data Visualization for {file.name}")
        if st.checkbox(f"Show data visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion Options
        st.subheader(f"Conversion Options for {file.name}")
        conversion_type = st.radio(f"Convert {file.name} to", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:  # Excel
                df.to_excel(buffer, index=False, engine="xlsxwriter")
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"Download {file_name} as {conversion_type}",
                data=buffer,
                filename=file_name,
                mime_type=mime_type,
            )

    st.success("🎉All files processed successfully!")
   
