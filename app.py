import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparateur CSV 🔍", layout="centered")

st.markdown("""
    <style>
        .big-title {
            font-size: 2.2em;
            font-weight: bold;
            color: #3c3c3c;
        }
        .section-title {
            font-size: 1.5em;
            margin-top: 1em;
            color: #2a82e4;
        }
        .block {
            padding: 1.5em;
            border: 1px solid #ccc;
            border-radius: 12px;
            background-color: #f9f9f9;
            margin-bottom: 2em;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>🔍 Comparateur de colonnes entre 2 fichiers CSV</div>", unsafe_allow_html=True)

# Upload Section
st.markdown("<div class='section-title'>📁 Étape 1 : Téléverse tes fichiers CSV</div>", unsafe_allow_html=True)
file1 = st.file_uploader("🟠 Fichier principal (CSV 1)", type=["csv"])
file2 = st.file_uploader("🔵 Fichier de référence (CSV 2)", type=["csv"])

if file1 and file2:
    try:
        df1 = pd.read_csv(file1, sep=';')
        df2 = pd.read_csv(file2, sep=';')

        st.markdown("<div class='section-title'>🎯 Étape 2 : Choisis les colonnes à comparer</div>", unsafe_allow_html=True)

        col1 = st.selectbox("Colonne du CSV 1 📄", df1.columns)
        col2 = st.selectbox("Colonne du CSV 2 📄", df2.columns)

        st.markdown("<div class='section-title'>🚀 Étape 3 : Lance la comparaison</div>", unsafe_allow_html=True)

        if st.button("🔍 Comparer maintenant"):
            values_df1 = df1[col1].astype(str)
            values_df2 = df2[col2].astype(str)
            mask = ~values_df1.isin(values_df2)
            result = df1[mask]

            st.success(f"✅ {len(result)} ligne(s) du CSV 1 dont la valeur dans '{col1}' n’existe pas dans la colonne '{col2}' du CSV 2.")

            if len(result) > 0:
                st.markdown("<div class='section-title'>📊 Résultat de la comparaison</div>", unsafe_allow_html=True)
                st.dataframe(result, use_container_width=True)

                csv_res = result.to_csv(index=False, sep=';')
                st.download_button(
                    label="📥 Télécharger les résultats",
                    data=csv_res,
                    file_name="resultat_non_trouvees.csv",
                    mime="text/csv"
                )
            else:
                st.info("👍 Toutes les valeurs du CSV 1 existent dans le CSV 2. Rien à signaler !")

    except Exception as e:
        st.error(f"❌ Erreur lors du traitement des fichiers : {e}")
else:
    st.info("⬆️ Merci d’uploader les deux fichiers CSV pour commencer.")
