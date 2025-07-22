import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparateur de colonnes CSV", layout="centered")

st.title("🔍 Comparateur de colonnes entre 2 fichiers CSV")

# Étape 1 : Upload des deux fichiers
file1 = st.file_uploader("📁 Upload du **fichier principal** (CSV 1)", type=["csv"])
file2 = st.file_uploader("📁 Upload du **fichier de référence** (CSV 2)", type=["csv"])

if file1 and file2:
    # Lecture des fichiers
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    st.subheader("🎯 Choisis les colonnes à comparer")

    col1 = st.selectbox("🔸 Colonne du fichier 1 (celle à vérifier)", df1.columns)
    col2 = st.selectbox("🔹 Colonne du fichier 2 (référence)", df2.columns)

    if st.button("🚀 Lancer la comparaison"):
        # Convertir en chaînes pour éviter les problèmes de type
        values_df1 = df1[col1].astype(str)
        values_df2 = df2[col2].astype(str)

        # Obtenir un masque des lignes à conserver (valeurs pas trouvées dans la colonne de référence)
        mask_non_trouvees = ~values_df1.isin(values_df2)
        lignes_non_trouvees = df1[mask_non_trouvees]

        st.success(f"✅ {len(lignes_non_trouvees)} ligne(s) du fichier 1 ont une valeur dans '{col1}' qui n'existe pas dans '{col2}'.")

        st.dataframe(lignes_non_trouvees)

        # Télécharger le résultat
        csv_result = lignes_non_trouvees.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger les lignes filtrées",
            data=csv_result,
            file_name="resultat_non_trouvees.csv",
            mime="text/csv"
        )
