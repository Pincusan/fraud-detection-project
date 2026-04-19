import streamlit as st
import os
import pandas as pd
import plotly.express as px
st.header("Analiza Exploratorie a Datelor (EDA)")
tab1, tab2 = st.tabs(["Analiza datelor reale", "Analiza datelor sintetice"])


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Construim calea către 'poze_real' plecând de la EDA.py
# (Presupunând că 'poze_real' este în folderul principal, cu un nivel mai sus de 'dashboard')
POZE_DIR = os.path.join(BASE_DIR, "poze_real")
POZE_DIR2 = os.path.join(BASE_DIR, "poze_sintetic")



with tab1:
    grafic_ales = st.radio(
        "🔎 Alege vizualizarea dorita:",
        [
            "1. Distributia Claselor",
            "2. Distributia Densitatii Timpului",
            "3. Distributii V1-V4",
            "4. Matricea de Corelatie",
            "5. Gruparea Tranzactiilor",
            "6. Corelatiile Variabilelor",
            "7. Distributia variabilelor puternic corelate (V17, V14, V12, V10)",
            "8. Vizualizare t-SNE"
        ]
    )

    st.markdown("---")

    if grafic_ales == "1. Distributia Claselor":
        st.subheader("Distributia Claselor (Normal vs. Frauda)")
        st.image(os.path.join(POZE_DIR, "2Distributia_Claselor.png"), use_container_width=True)
        st.info(
            "Graficul confirma dezechilibrul extrem din acest set de date. Tranzactiile frauduloase reprezinta un procent foarte mic din totalul tranzactilor efectuate.")

    elif grafic_ales == "2. Distributia Densitatii Timpului":
        st.subheader("Distributia in timp a tranzactiilor")
        st.image(os.path.join(POZE_DIR, "3Distributia_Densitatii_Timpului.png"), use_container_width=True)
        st.info(
            "Aici putem vedea frecventa tranzactiilor legitime fata de cele frauduloase in functie de timp (secunde). Fraudele au o distributie diferita in anumite intervale orare, indicand posibile tipare ale atacatorilor.")

    elif grafic_ales == "3. Distributii V1-V4":
        st.subheader("Analiza componentelor V1-V4")
        reform = st.columns([5, 5])
        with reform[0]:
            st.image(os.path.join(POZE_DIR, "41distributie_V1.png"), use_container_width=True)
            st.image(os.path.join(POZE_DIR, "43distributie_V3.png"), use_container_width=True)
        with reform[1]:
            st.image(os.path.join(POZE_DIR, "42distributie_V2.png"), use_container_width=True)
            st.image(os.path.join(POZE_DIR, "44distributie_V4.png"), use_container_width=True)

        st.info(
            "Putem observa diferente in forma distributiei intre tranzactiile normale si cele frauduloase.")

    elif grafic_ales == "4. Matricea de Corelatie":
        st.subheader("Matricea de Corelatie Globala")
        st.image(os.path.join(POZE_DIR, "5Matricea_Corelatie.png"), use_container_width=True)
        st.info(
            "Observam ca majoritatea variabilelor (V1-V28) nu sunt corelate intre ele (valori aproape de 0). Insa, exista anumite variabile care arata o corelatie mai puternica cu variabila tinta (Class).")

    elif grafic_ales == "5. Gruparea Tranzactiilor":
        st.subheader("Gruparea Tranzactiilor (Clusterizare)")
        st.image(os.path.join(POZE_DIR, "6gruparea_tranzactiilor.png"), use_container_width=True)
        st.info(
            "Ne ajută să observăm vizual dacă fraudele (punctele portocalii) se grupează într-o zonă distinctă sau dacă se ascund printre tranzacțiile normale (punctele albastre), indicând cât de ușor îi va fi modelului să le separe.")

    elif grafic_ales == "6. Corelatiile Variabilelor":
        st.subheader("Cele mai importante corelatii")
        st.image(os.path.join(POZE_DIR, "7Corelatiile_variabilelor.png"), use_container_width=True)
        st.info(
            "Remarcăm o corelație negativă foarte puternică în special pentru V17, V14, V12 și V10 — cu alte cuvinte, pe măsură ce valorile acestor variabile scad abrupt, probabilitatea ca tranzacția să fie frauduloasă crește vertiginos. Aceste componente reprezintă cel mai clar semnal de alarmă de care se folosesc modelele noastre.")

    elif grafic_ales == "7. Distributia variabilelor puternic corelate (V17, V14, V12, V10)":
        st.subheader("Analiza detaliata: V17, V14, V12, V10")
        reform = st.columns([5, 5])
        with reform[0]:
            st.image(os.path.join(POZE_DIR, "81KDE_Distributie_V10.png"), use_container_width=True)
            st.image(os.path.join(POZE_DIR, "82KDE_Distributie_V12.png"), use_container_width=True)
        with reform[1]:
            st.image(os.path.join(POZE_DIR, "83KDE_Distributie_V14.png"), use_container_width=True)
            st.image(os.path.join(POZE_DIR, "84KDE_Distributie_V17.png"), use_container_width=True)
        st.info(
            "Analizand individual aceste caracteristici de top, se observa clar cum valorile tranzactiilor frauduloase se desprind de clopotul (distributia normala) tranzactiilor legitime.")

    elif grafic_ales == "8. Vizualizare t-SNE":
        st.subheader("Separarea claselor folosind t-SNE")
        st.image(os.path.join(POZE_DIR, "9Vizualizare_t-SNE_V2.png"), use_container_width=True)
        st.info(
            "Pe acest grafic observăm cum fraudele tind să se desprindă de masa compactă a tranzacțiilor legitime, formând mici grupuri izolate. Această grupare distinctă ne confirmă vizual că, deși datele par inseparabile la prima vedere, modelele noastre avansate pot trasa granițe clare de decizie pentru a depista anomaliile."
        )


with tab2:
    grafic_ales = st.radio(
        "🔎 Alege vizualizarea dorita:",
        [
            "1. Distributia Claselor",
            "2. Media sumelor",
            "3. Observarea sumelor outlier",
            "4. Corelatia dintre latitudine si suma",
            "5. Matricea de corelatie"
        ]
    )
    if grafic_ales == "1. Distributia Claselor":
        st.subheader("Distributia Claselor (Normal vs. Frauda)")
        st.image(os.path.join(POZE_DIR2, "1Distributia_Tranzactiilor.png"), use_container_width=True)
        st.info("La fel ca in cazul datelor reale, observam dezechilibrul dintre fraude si normale.")
    elif grafic_ales == "2. Media sumelor":
        st.subheader("Media sumelor:")
        st.image(os.path.join(POZE_DIR2, "2Media_sumelor.png"), use_container_width=True)
        st.info("In cazul tranzactiilor frauduloase se observa in mod clar sume de bani mult mai mari comparativ cu tranzactiile obisnuite.")


    elif grafic_ales == "3. Observarea sumelor outlier":
        st.subheader("Observarea sumelor outlaier:")
        st.image(os.path.join(POZE_DIR2, "3Outliers.png"), use_container_width=True)
        st.info("Desi uneori platile normale ating valori uriase (valorile atinse sus), in mod obisnuit ele sunt sume foarte mici. La fraude, in schimb, majoritatea sunt situate vizibil mai sus, semn ca sunt vizate in mod constant sume mai mari de bani.")
    elif grafic_ales == "4. Corelatia dintre latitudine si suma":
        st.subheader("Corelatia dintre latitudine si suma:")
        st.image(os.path.join(POZE_DIR2, "4Axe_curate.png"), use_container_width=True)
        st.info("Acest grafic ne arata ca fraudele nu se limiteaza la o anumita zona geografica, ele fiind raspandite pe toata axa latitudinii. Totusi, vizualizarea ne reconfirma regula acestui set de date: indiferent de locatia in care au loc, tranzactiile frauduloase ocolesc sumele foarte mici, plasandu-se constant la un nivel valoric mai ridicat.")
    else:
        st.subheader("Matricea de corelatie:")
        st.image(os.path.join(POZE_DIR2, "5Matrice_corelatie.png"), use_container_width=True)
        st.info("Matricea de corelatie confirma matematic o singura legatura relevanta: valoarea tranzactiei ('amt') este singurul factor din acest set cu un impact direct si pozitiv (*0.23*) asupra probabilitatii de frauda. Caracteristicile geografice, demografice sau temporale au o corelatie apropiata de zero, demonstrand ca, luate strict individual, acestea nu ne ofera indicii clare pentru depistarea anomaliilor.")
#miscare pagini
col = st.columns([2, 6, 2])
with col[0]:
    if st.button("⬅️ Pagina anterioară"):
        st.switch_page("describe.py")
with col[-1]:
    if st.button("Următoarea pagină ➡️"):
        st.switch_page("results.py")