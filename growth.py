import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config (page_title="data sweeper", layout='wide')

#custom css
st.markdown(
    '''
    <style>
    .stapp{
        background-color: black:
        colour:white;
      }
      </style>
      ''',
      unsafe_allow_html=True
)

#title and description
st.title ("Datasweeper Sretling By Maryam Haseeb")

st.write("Transform your file between CSV and exel formats with build in data cleaning and vizualization creating the project for quarter3!")

#upload file
uploaded_files = st.file_uploader("upload your files(accepts CSV or exel:)",type= ["cvs,xlsx"],accept_multiple_files=(True) )

if uploaded_files:
    for file in uploaded_files:
     file_ext = os.path.splitext(file.name)[-1].lower()

    if file_ext == ".csv":
     df = pd.read_csv(file)

    elif file_ext == "xlsx":
      df = pd.read_excel(file)
    else:
         st.error(f"unsupported file {file_ext}")
  

#files details
st.write("preview the head of the data frame")
st.Dataframe(df.head())

#data cleaning
st.subheader("data cleaning options")
if st.checkbox(f"data cleaning for {file.name}"):
    col1, col2 = st.columns(2)

    with col1:
        if st.buttons(f"remove duplicate from the file {file.name}"):
            df.drop_duplicates(inplace=True)
            st.write("duplicate remove!")

            with col2:
                if st.button(f"fill missing values for {file.name}"):
                    numeric_cols =df.select_dtypes(include =['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("missing value have been filled!")

        st.subheader("select column to keep")           
        columns = st.multiselect(f"choose column for {file.name}", df.columns, default= df.columns)
        df= df[columns]

        #data visualization
        st.subheader("data visualization")
        if st.checkbox("show data visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])


            #conversion options
            st.subheader("conversion options")
            conversion_type = st.ratio(f"convert{file.name} to",["CVS","EXEL"],key = file.name)
            if st.button(f"convert{file.name}"):
                buffer = BytesIO
                if conversion_type == "CSV":
                 df.to.csv( buffer, index=False)
                 file_name = file.name.replace(file_ext,".csv")
                 mime_type = "text/csv"

            elif conversion_type == "Excel":
             df.to_excel(buffer, index=False)
             file_name = file.name.replace(file_ext, "xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"download {file_name} as {conversion_type}",
                data=buffer,
                filename=file_name,
                mimetype=mime_type,
            )
            
            st.success("All files processed successfully!")
