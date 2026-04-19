import streamlit as st

st.title("📖 Descrierea Proiectului si Detalii Tehnice")
st.write("""
Aici exploram provocarile tehnice, deciziile de preprocesare si conceptele de Machine Learning 
care stau la baza modelelor noastre de detectie a fraudelor.
""")

st.markdown("---")

# Creăm 4 tab-uri pentru a organiza informația elegant
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Seturile de Date",
    "⚖️ Problema Dezechilibrului",
    "⚙️ Fluxul de Antrenare",
    "📈 Metode de Evaluare"
])

with tab1:
    st.header("Date Reale vs. Date Sintetice")

    st.write("""
    Pentru a construi acest sistem de detectie, am adoptat o abordare robusta,
    bazata pe doua seturi de date cu caracteristici complet diferite. Astfel,
    am putut analiza si compara performanta modelelor de Machine Learning in scenarii variate:
    """)

    st.markdown("## 1. Setul de Date Real")
    st.write("""
    Acesta este un set de date bancar clasic, care contine **284.807** tranzactii. 
    * **Anatomia datelor:** Setul este format din 30 de caracteristici (features) de intrare, plus o ultima coloana care specifica tipul tranzactiei (variabila tinta). 
    * **Continut:** Din motive de confidentialitate a clientilor, majoritatea datelor originale au fost deja transformate matematic, rezultand 28 de variabile numerice abstracte (`V1` pana la `V28`). Singurele atribute pastrate in formatul brut sunt `Time` si `Amount` (suma tranzactionata).
    """)

    st.markdown("## 2. Setul de Date Sintetic")
    st.write("""
        Spre deosebire de setul real puternic anonimizat, setul sintetic ne ofera **contextul clar al tranzactiilor**, punandu-ne la dispozitie initial 23 de atribute detaliate.
        * **Preprocesare si selectie:** Deoarece nu toate informatiile brute erau relevante pentru analiza noastra (unele putand genera chiar confuzie pentru algoritm), o parte dintre aceste atribute au fost eliminate, pastrandu-se doar caracteristicile cu o putere reala de predictie a fraudelor.
        """)
    st.info(
        "💡 **Eticheta (Class / is_fraud):** In ambele seturi, valoarea **0** reprezinta o tranzactie normala (legitima), iar **1** reprezinta o frauda.")

with tab2:
    st.header("Datele Dezechilibrate")
    st.write("""
    Detectia fraudelor este un exemplu clasic de date extrem de dezechilibrate (*Highly Imbalanced Data*). 
    In setul real de date, din cele aprox. 284.800 de tranzactii, **doar 492 sunt fraude (0.17%)**.
    """)

    st.markdown("### De ce este o problema?")
    st.write("""
    Daca un algoritm prezice mereu „0” (Normal), va avea o acuratete de 99.83%. La prima vedere pare un model perfect, 
    dar in realitate este complet inutil, deoarece va rata absolut toate fraudele.
    """)

    st.markdown("### Solutiile noastre:")
    st.markdown("### Solutia noastra pentru dezechilibrul datelor:")

    st.write("""
    Deoarece fraudele reprezinta un procent infim din totalul tranzactiilor (mai putin de 0.2%), ne-am confruntat cu o provocare majora: un algoritm standard ar tinde sa ignore complet fraudele. 

    Pentru a rezolva aceasta problema, am analizat doua abordari principale:
    """)

    st.write("""    
    1. **Cost-Sensitive Learning (Solutia implementata):** Aceasta este metoda pe care am aplicat-o la antrenarea modelelor noastre. Am modificat direct functia de invatare a algoritmilor. Mai exact, am calculat raportul de dezechilibru si am aplicat o „greutate” matematica. Astfel, algoritmul este penalizat mult mai sever daca rateaza o frauda autentica decat daca declanseaza o alarma falsa pentru o tranzactie legitima.

    2. **Oversampling / Undersampling (Alte metoda):** O abordare clasica ce implica generarea de date sintetice pentru fraude (ex: algoritmul SMOTE) sau stergerea tranzactiilor normale.
    """)

with tab3:
    st.header("Cum a invatat modelul?")
    st.write(
        "Fluxul nostru de lucru a urmat pasii clasici din Data Science, trecand de la pregatirea datelor la antrenarea efectiva a algoritmilor:")

    st.markdown("""
    ### 1. Impartirea si Pregatirea Datelor
    * **Train / Test Split:** Pentru a simula conditii reale, am separat datele in doua categorii: **setul de Antrenare** si **setul de Testare**. 
    * **Standardizarea:** Inainte de antrenare, sumele tranzactiilor au fost aduse la aceeasi scara matematica, asigurandu-ne ca modelul nu este influentat gresit de diferentele mari dintre sume.
    """)

    st.markdown("""
    ### 2. Algoritmii de Machine Learning Antrenati
    Odata ce datele au fost pregatite, am testat si comparat mai multe tipuri de modele pentru a-l gasi pe cel optim:
    """)

    algorithms_choice = st.radio(
        "Tipul modelului: ",
        ("Logistic regresion", "Random Forest", "XGBoost")
    )
    if algorithms_choice == "Logistic regresion":

        st.markdown("""
        * **Logistic Regression:**
            * *Cum functioneaza:* Structura sa este foarte asemanatoare cu un perceptron (elementul de baza al retelelor neuronale): combina datele de intrare printr-o suma ponderata, iar rezultatul trece prin functia Sigmoid (care poate lua valori intre 0 si 1). Modelul este antrenat repetat pana cand aceste ponderi ating un punct optim, trasand astfel granita matematica de decizie.
            * *Rolul lui:* L-am folosit ca model de **baza**. Ne ajuta sa vedem cat de bine putem detecta fraudele cu o metoda simpla si matematica, stabilind un standard minim de performanta pentru ceilalti algoritmi.
        """)
    elif algorithms_choice == "Random Forest":

        st.markdown("""
        * **Random Forest:**
            * *Cum functioneaza:* La nivel tehnic, se bazeaza pe un mecanism numit **Bagging**. In loc sa antreneze un singur model urias, algoritmul construieste in fundal sute de arbori de decizie mai mici, care proceseaza datele complet independent (in paralel). Secretul consta in aplicarea aleatorului: fiecare arbore invata dintr-un subset diferit de date si, cand ia decizii, are acces doar la o anumita parte din caracteristicile tranzactiei (coloane). Asta forteaza arborii sa nu se copieze intre ei. La final, pentru o tranzactie noua, toate aceste modele individuale "voteaza", iar decizia majoritatii devine verdictul final.
            * *Rolul lui:* L-am ales tocmai pentru capacitatea sa de a pune in evidenta fraudele. Analizand tranzactiile prin diferiti arborii, algoritmul reuseste sa detecteze tranzactiile frauduloase chiar daca acestea sunt rare in setul de date.
        """)

    else:
        st.markdown("""        
        * **XGBoost (Extreme Gradient Boosting):**
            * *Cum functioneaza:* Se bazeaza pe o tehnica diferita, numita **Boosting**. Daca la Random Forest arborii lucreaza independent, XGBoost ii construieste secvential, ca intr-o cursa de stafeta. Fiecare arbore nou este creat cu un singur scop precis: sa invete si sa corecteze greselile (fraudele ratate) facute de arborii dinaintea lui. Prin aceasta concentrare continua pe cazurile dificile, modelul invata pas cu pas din propriile erori, devenind extrem de "ascutit".
            * *Rolul lui:* L-am utilizat ca un "upgrade" la modelele anterioare, pentru a impinge precizia la maximum. Fiind optimizat sa se concentreze fix pe fraudele cel mai greu de detectat (pe care restul modelelor le rateaza), XGBoost ofera rezultate excelente, mai ales pe date cu dezechilibru extrem.
        """)
with tab4:
    st.header("Cum masuram succesul?")
    st.write("""
    Deoarece acuratetea clasica ne minte, ne bazam pe urmatoarele metrici avansate pentru a selecta cel mai bun model:
    """)

    st.markdown("""
    * **Matricea de Confuzie (Confusion Matrix):** Ne arata exact cate fraude au fost prinse (True Positives), cate au fost ratate (False Negatives) si cati clienti au fost deranjati degeaba (False Positives).
    * **Recall (Sensibilitatea):** Dintre toate fraudele reale, cate a reusit sa descopere modelul nostru?
    * **Precision (Precizia):** Cand modelul nostru striga "Frauda!", de cate ori are dreptate? 
    * **F1-Score:** Media armonica dintre Precision si Recall, excelenta pentru a gasi un echilibru intre tranzactiile frauduloase si cele normale.
    * **ROC-AUC (Area Under the Receiver Operating Characteristic Curve):** Masoara capacitatea generala a modelului de a distinge clar intre clasa 0 si clasa 1. Un scor cat mai aproape de 1.0 indica un model excelent.
    """)




#miscare pagini
col = st.columns([2, 6, 2])
with col[0]:
    if st.button("⬅️ Pagina anterioara"):
        st.switch_page("home.py")
with col[-1]:
    if st.button("Următoarea pagina ➡️"):
        st.switch_page("EDA.py")