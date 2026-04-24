# Fraud detection project

## Despre ce este proiectul

Acest proiect este o solutie completa pentru detectarea tranzactiilor bancare frauduloase. Obiectivul principal este de a oferi un sistem capabil sa identifice activitatile suspecte folosind algoritmi de Machine Learning.

Proiectul utilizeaza doua tipuri de seturi de date:
1. **Date Reale:** Un set de date anonimizat, continand tranzactii reale.
2. **Date Sintetice:** Un set de date generat care simuleaza tranzactii din viata reala.
Ambele seturi pot fi descarcate accesand link-urile din `data_source.txt` aflat in directorul `data`.

## Cum sa rulezi dashboard-ul

**Pasi:**
1. In caz ca nu ai instalate toate modulele care sunt folosite in fisierele .py din directorul `dashboard`, acestea pot fi instalate prin comanda `pip install [numele modulului]`
2. Pentru run, trebuie sa scrii in terminal `streamlit run` urmat de `[app.py  SAU  intre ghilimele toata calea catre app.py]` ex: `streamlit run "C:\Users\cale\app.py"`

## Antrenarea modelului

### 1. Preprocesarea Datelor
* **Pentru Datele Sintetice:** Am eliminat coloanele care nu aduc valoare predictiva, cum ar fi numele posesorului, numarul cardului, adresa exacta sau numarul tranzactiei. De asemenea, am transformat variabilele categorice folosind **One-Hot Encoding**.
* **Pentru Datele Reale:** Fiind deja preprocesate prin PCA, am intervenit doar asupra coloanei `Amount` (suma tranzactiei).

### 2. Scalarea Caracteristicilor
Pentru ca algoritmii sa nu fie influentati de unitatile de masura diferite, am folosit **StandardScaler**. Acesta centreaza datele in jurul valorii 0 si le scaleaza la o unitate standard, asigurand o antrenare corecta si eficienta.

### 3. Selectia si Antrenarea Modelelor
Am ales sa testam si sa comparam trei algoritmi diferiti pentru a vedea care se comporta cel mai bine pe date dezechilibrate:
1.  **Logistic Regression:** Folosit ca model de baza pentru simplitatea sa.
2.  **Random Forest:** Un model de tip ansamblu care gestioneaza bine datele complexe si relatiile non-liniare.
3.  **XGBoost:** Un algoritm de Gradient Boosting extrem de performant, care a oferit cele mai bune rezultate.

### 4. Evaluarea Performantei
Nu ne-am uitat doar la acuratete (care poate fi inselatoare in cazul fraudelor), ci am urmarit:
* **Precision & Recall:** Cat de multi dintre cei marcati ca "fraudatori" sunt reali si cati am ratat.
* **Matricea de Confuzie:** Pentru a vedea clar numarul de alarme false versus fraude detectate corect.
* **Scorul ROC-AUC:** Indicatorul principal pentru capacitatea modelului de a distinge intre cele doua clase.

### 5. Exportul Modelelor
Dupa compararea rezultatelor, scriptul identifica automat modelul "castigator" pentru fiecare set de date. Modelele selectate, impreuna cu scalerele folosite in etapa de preprocesare, sunt salvate in folderul `model/` folosind libraria `joblib`.
