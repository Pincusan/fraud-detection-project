import streamlit as st


st.title("💳 Sistem Inteligent de Detectie a Fraudelor Bancare")
st.markdown("---")


st.markdown("## 🖐️ Bun venit!")
st.write("""
    Aceasta este o aplicatie pentru analiza si detectarea fraudelor financiare.
""")


st.markdown("### 🎯 Scopul Proiectului")
st.write("""
Obiectivul acestui proiect este detectia fraudelor intr-un set de date foarte dezechilibrat. 
Noi incercam sa cream un model capabil sa gaseasca tranzactiile suspecte, 
mentinand un numar cat mai mic de alarme false.
""")

st.markdown("### 🧩 Cum să navighezi în aplicație")
st.write("Am structurat acest dashboard în patru secțiuni principale, accesibile din meniul lateral:")

st.markdown("""
* **📖 Details:** Aici explicăm setul de date folosit, arhitectura modelelor și tehnicile folosite pentru balansarea datelor.
* **📊 Results:** Aici poți vizualiza graficele, Matricea de Confuzie, curba ROC-AUC și scorurile F1 obținute de modelele antrenate pe date reale și sintetice.
* **🧪 Testing:** Zona interactivă. Aici poți introduce caracteristicile unei tranzacții noi, iar modelul nostru salvat o va evalua și îți va oferi un verdict instant.
""")

st.markdown("---")
st.info("""
    Pentru navigare poti folosi: 
    * 👈meniul din stanga pentru a accesa direct o pagina
    * 👇butoanele de la finalul fiecarei pagini
""")








#miscare pagini
col = st.columns([2, 6, 2])
with col[-1]:
    if st.button("Următoarea pagina ➡️"):
        st.switch_page("describe.py")
