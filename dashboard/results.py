import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POZE_DIR = os.path.join(BASE_DIR, "rez")
st.title("📊 Rezultatele Modelelor (Ploturi si Diagrame)")
st.write("""
Aici poti explora vizual performanta modelelor antrenate de noi pe cele doua seturi de date. 
Am selectat cele mai relevante grafice generate in etapa de evaluare.
""")

st.markdown("---")

# Cream coloane pentru selectori
col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    dataset_choice = st.radio(
        "Alege setul de date evaluat:",
        ("💳 Date Reale (CreditCard)", "🧪 Date Sintetice (FraudTrain)")
    )

with col_sel2:
    model_choice = st.selectbox(
        "Alege algoritmul:",
        ("Regresie Logistica", "Random Forest", "XGBoost")
    )

st.markdown(f"### Performanta pe: **{dataset_choice}** cu **{model_choice}**")

# ==========================================
# BAZA DE DATE PENTRU REZULTATE SI POZE
# ==========================================

results_db = {
    "🧪 Date Sintetice (FraudTrain)": {
        "observatie": "Pe datele sintetice am avut 1 frauda la fiecare 171 de tranzactii normale. XGBoost a obtinut cel mai bun scor general.",
        "Regresie Logistica": {
            "cm": np.array([[492567, 61007], [558, 1587]]),
            "precision": ["1.00", "0.03"], "recall": ["0.89", "0.74"], "f1": ["0.94", "0.05"],
            "support": ["553574", "2145"]
        },
        "Random Forest": {
            "cm": np.array([[553192, 382], [1071, 1074]]),
            "precision": ["1.00", "0.74"], "recall": ["1.00", "0.50"], "f1": ["1.00", "0.60"],
            "support": ["553574", "2145"]
        },
        "XGBoost": {
            "cm": np.array([[540880, 12694], [302, 1843]]),
            "precision": ["1.00", "0.98"], "recall": ["1.00", "0.95"], "f1": ["1.00", "0.96"],
            "support": ["553574", "2145"]
            }
    },
    "💳 Date Reale (CreditCard)": {
        "observatie": "Datele reale au fost mult mai dezechilibrate (1 frauda la 577 normale). Regresia Logistica si XGBoost au excelat la ROC-AUC.",
        "Regresie Logistica": {
            "cm": np.array([[55425, 1439], [8, 90]]),
            "precision": ["1.00", "0.06"], "recall": ["0.97", "0.92"], "f1": ["0.99", "0.11"],
            "support": ["56864", "98"]
        },
        "Random Forest": {
            "cm": np.array([[56861, 3], [24, 74]]),
            "precision": ["1.00", "0.96"], "recall": ["1.00", "0.76"], "f1": ["1.00", "0.85"],
            "support": ["56864", "98"]
        },
        "XGBoost": {
            "cm": np.array([[56853, 11], [15, 83]]),
            "precision": ["1.00", "0.88"], "recall": ["1.00", "0.85"], "f1": ["1.00", "0.86"],
            "support": ["56864", "98"]
        }
    }
}

# Extragem datele modelului curent
current_data = results_db[dataset_choice][model_choice]
cm = current_data["cm"]

# ==========================================
# ZONA DE GRAFICE (Matricea de Confuzie si Poza ROC)
# ==========================================

col1, col2 = st.columns([4, 6])

with col1:
    st.subheader("Matricea de Confuzie")
    fig_cm, ax_cm = plt.subplots(figsize=(5, 4))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Normal', 'Frauda'])
    disp.plot(cmap='Blues', ax=ax_cm, values_format='d')
    ax_cm.set_title(f'CM: {model_choice}')

    st.pyplot(fig_cm)
    st.caption("Axa Y: Tipul de tranzactie   | Axa X: Predictia modelului.")

with col2:
    st.subheader("Curba ROC (ROC-AUC)")
    if dataset_choice == "💳 Date Reale (CreditCard)":
        if model_choice == "Regresie Logistica":
            st.image(os.path.join(POZE_DIR, "LRR.png"), use_container_width=True)

        elif model_choice == "Random Forest":
            st.image(os.path.join(POZE_DIR, "RFR.png"), use_container_width=True)
        else:
            st.image(os.path.join(POZE_DIR, "XGR.png"), use_container_width=True)
    else:
        if model_choice == "Regresie Logistica":
            st.image(os.path.join(POZE_DIR, "LRS.png"), use_container_width=True)
        elif model_choice == "Random Forest":
            st.image(os.path.join(POZE_DIR, "RFS.png"), use_container_width=True)
        else:
            st.image(os.path.join(POZE_DIR, "XGS.png"), use_container_width=True)

    st.caption(
        "Axa Y: Rata fraudelor detectate corect (True Positive)   | Axa X: Rata alarmelor false (False Positive).")


# ==========================================
# SECTIUNE SUPLIMENTARA: RAPORT DE CLASIFICARE (Tabelar)
# ==========================================
st.markdown("---")
st.subheader("📋 Raport de Clasificare (Classification Report)")
st.write("Acestea sunt datele extrase din evaluarea algoritmului:")

data_report = {
    "Clasa": ["Normal (0)", "Frauda (1)"],
    "Precision": current_data["precision"],
    "Recall": current_data["recall"],
    "F1-Score": current_data["f1"],
    "Suport (Nr. cazuri)": current_data["support"]
}

df_report = pd.DataFrame(data_report)
st.table(df_report)

# ==========================================
# NAVIGARE PAGINI
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)  # spatiu vizual
col = st.columns([2, 6, 2])
with col[0]:
    if st.button("⬅️ Pagina anterioara"):
        st.switch_page("EDA.py")
with col[-1]:
    if st.button("Urmatoarea pagina ➡️"):
        st.switch_page("testing.py")