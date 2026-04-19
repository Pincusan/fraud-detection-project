import streamlit as st
import os

home = st.Page("home.py", title="Home")
description = st.Page("describe.py", title="Details")
EDA = st.Page("EDA.py", title="Exploring Data Analysis")
results = st.Page("results.py", title="Models Results")
testing = st.Page("testing.py", title="Testing")
sectionare={"Navigare rapida:" : [home, description, EDA, results, testing]}
page = st.navigation(sectionare)

with st.sidebar:
    #ca sa poti da dowland din dashboard la data atunci trebuie sa pui cele 2 csv-uri cu numele nemodificat in data
    st.header("📂 Downland data")

    # Selectorul de dataset
    dataset_choice = st.selectbox(
        "Alege setul de date activ:",
        ["Date Reale", "Date Sintetice"]
    )

    # Logica de identificare a fisierului pentru download
    path_to_file = "data/creditcard.csv" if dataset_choice == "Date Reale" else "data/fraudTest.csv"

    if os.path.exists(path_to_file):
        with open(path_to_file, "rb") as f:
            st.download_button(
                label=f"📥 Descarca {dataset_choice}",
                data=f,
                file_name=os.path.basename(path_to_file),
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.warning("Fisierul sursa nu a fost gasit in /data.")

    st.markdown("---")
    st.caption("Proiect realizat pentru detectia fraudelor bancare folosind ML.")




page.run()