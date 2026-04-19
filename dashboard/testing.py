import streamlit as st
import pandas as pd
import joblib
import time

st.title("🧪 Testare Interactiva a Modelelor")
st.write("""
Testeaza modelele noastre in timp real! Selecteaza tipul de model, introdu detaliile 
tranzactiei si vezi daca algoritmul o clasifica drept legitima sau frauduloasa.
""")

st.markdown("---")


# ==========================================
# 1. INCARCAREA MODELELOR
# ==========================================
@st.cache_resource
def load_all_models():
    try:
        # Modele reale (CreditCard - PCA)
        model_r = joblib.load('model/best_model_real.pkl')
        scaler_r = joblib.load('model/scaler_real.pkl')

        # Modele sintetice (FraudTrain)
        model_s = joblib.load('model/best_model_synthetic.pkl')
        scaler_s = joblib.load('model/scaler_synthetic.pkl')

        return model_r, scaler_r, model_s, scaler_s
    except Exception as e:
        st.error(f"🚨 Modelele nu au putut fi incarcate. Detalii eroare: {e}")
        st.info("💡 Asigura-te ca fisierele .pkl sunt in folderul 'model/' si ca ai instalat biblioteca 'xgboost'.")
        return None, None, None, None


model_real, scaler_real, model_synth, scaler_synth = load_all_models()

# Daca modelele s-au incarcat cu succes, afisam interfata
if model_real is not None and model_synth is not None:

    # ==========================================
    # 2. SELECTORUL DE MODEL
    # ==========================================
    tip_model = st.radio("Alege modelul pe care doresti sa-l testezi:",
                         ["💳 Tranzactie Reala (CreditCard PCA)", "🛒 Tranzactie Sintetica (FraudTrain)"])

    st.markdown("---")

    # ==========================================
    # INTERFATA PENTRU DATE REALE
    # ==========================================
    if tip_model == "💳 Tranzactie Reala (CreditCard PCA)":
        st.subheader("Introduceti datele financiare")

        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("💵 Suma Tranzactiei (Amount)", min_value=0.0, value=120.50, step=10.0)
            v1 = st.number_input("Valoare V1", value=0.0, step=1.0)
            v2 = st.number_input("Valoare V2", value=0.0, step=1.0)
        with col2:
            v3 = st.number_input("Valoare V3", value=0.0, step = 1.0)
            v4 = st.number_input("Valoare V4", value=0.0, step = 1.0)
            st.info(
                "💡 Variabilele de la **V5 la V28** vor fi completate automat cu **0.0** in fundal pentru a simplifica testarea.")

        if st.button("Evalueaza Tranzactia Reala", use_container_width=True):
            with st.spinner('Analizam tiparele tranzactiei...'):
                time.sleep(1)  # Pentru procesare

                # A. INTRODUCEM IN V1-V29 si AMOUNT
                input_data = {'V1': v1, 'V2': v2, 'V3': v3, 'V4': v4}
                for i in range(5, 29):
                    input_data[f'V{i}'] = 0.0
                input_data['Amount'] = amount

                # B. Transformam in DataFrame si scalam Suma
                df_input = pd.DataFrame([input_data])
                df_input[['Amount']] = scaler_real.transform(df_input[['Amount']])

                # C. Predictie
                prediction = model_real.predict(df_input)
                try:
                    proba = model_real.predict_proba(df_input)[0][1]
                except:
                    proba = 1.0 if prediction[0] == 1 else 0.0

                # D. Afisare rezultate
                st.markdown("### Rezultat:")
                if prediction[0] == 1:
                    st.error(
                        f"🚨 FRAUDA DETECTATA! Aceasta tranzactie prezinta tipare suspecte. (Probabilitate: {proba * 100:.2f}%)")
                else:
                    st.success(
                        f"✅ TRANZACTIE SIGURA. Nu au fost detectate anomalii. (Probabilitate frauda: {proba * 100:.2f}%)")

    # ==========================================
    # INTERFATA PENTRU DATE SINTETICE
    # ==========================================
    else:
        st.subheader("Introduceti datele sintetice")

        col1, col2 = st.columns(2)
        with col1:
            amt_synth = st.number_input("💵 Suma Tranzactiei (amt)", min_value=0.0, value=150.0, step=10.0)
            lat = 44.4
            lat = st.number_input("Latitudine client (lat)", value=44.4)
            long = st.number_input("Longitudine client (long)", value=26.0)
            city_pop = st.number_input("Populatie Oras (city_pop)", min_value=1, value=150000)

        with col2:
            merch_lat = st.number_input("Latitudine comerciant (merch_lat)", value=44.4)
            merch_long = st.number_input("Longitudine comerciant (merch_long)", value=26.1)

            # Formulare intuitive pentru utilizator (M/F si Lista de categorii)
            gender = st.radio("Genul clientului", ["M", "F"])

            categories = [
                'food_dining', 'gas_transport', 'grocery_net', 'grocery_pos',
                'health_fitness', 'home', 'kids_pets', 'misc_net', 'misc_pos',
                'personal_care', 'shopping_net', 'shopping_pos', 'travel'
            ]
            selected_category = st.selectbox("Categorie Magazin", categories)

        if st.button("Evalueaza Tranzactia Sintetica", use_container_width=True):
            with st.spinner('Analizam comportamentul...'):
                time.sleep(1)

                # 1. Initializam variabilele numerice
                synth_input_data = {
                    'amt': amt_synth,
                    'lat': lat,
                    'long': long,
                    'city_pop': city_pop,
                    'merch_lat': merch_lat,
                    'merch_long': merch_long
                }

                # 2. Convertim Categoria selectata in One-Hot Encoding (generam coloanele cu 1 si 0)
                for cat in categories:
                    col_name = f'category_{cat}'
                    synth_input_data[col_name] = 1 if cat == selected_category else 0

                # 3. Convertim Genul
                synth_input_data['gender_M'] = 1 if gender == "M" else 0

                df_synth = pd.DataFrame([synth_input_data])

                # 4. FORTAM ordinea corecta a coloanelor
                expected_cols = [
                    'amt', 'lat', 'long', 'city_pop', 'merch_lat', 'merch_long',
                    'category_food_dining', 'category_gas_transport', 'category_grocery_net',
                    'category_grocery_pos', 'category_health_fitness', 'category_home',
                    'category_kids_pets', 'category_misc_net', 'category_misc_pos',
                    'category_personal_care', 'category_shopping_net', 'category_shopping_pos',
                    'category_travel', 'gender_M'
                ]
                df_synth = df_synth[expected_cols]

                # 5. Aplicam standardizarea (daca scalerul o suporta pentru intregul dataframe)
                try:
                    df_synth_scaled = scaler_synth.transform(df_synth)
                    df_final = pd.DataFrame(df_synth_scaled, columns=expected_cols)
                except:
                    # Daca scalerul sintetic a fost folosit doar pe anumite coloane initial,
                    # trecem datele mai departe nescalate (XGBoost se descurca excelent si cu date brute).
                    df_final = df_synth

                # 6. Predictie
                try:
                    pred_synth = model_synth.predict(df_final)

                    try:
                        proba_synth = model_synth.predict_proba(df_final)[0][1]
                    except:
                        proba_synth = 1.0 if pred_synth[0] == 1 else 0.0

                    st.markdown("### Rezultat Sintetic:")
                    if pred_synth[0] == 1:
                        st.error(f"🚨 FRAUDA DETECTATA! (Probabilitate: {proba_synth * 100:.2f}%)")
                    else:
                        st.success(f"✅ Tranzactie Normala. (Probabilitate frauda: {proba_synth * 100:.2f}%)")
                except Exception as e:
                    st.error(f"Eroare in timpul predictiei: {e}")


#miscarea intre pagini:
col = st.columns([2, 6, 2])
with col[0]:
    if st.button("⬅️ Pagina anterioara"):
        st.switch_page("results.py")
with col[-1]:
    if st.button("Pagina de start!➡️"):
        st.switch_page("home.py")