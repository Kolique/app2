import streamlit as st
import pandas as pd

st.title("🔍 Comparateur de colonnes entre 2 fichiers CSV")

# Upload des fichiers
file1 = st.file_uploader("📁 Fichier CSV 1", type=["csv"])
file2 = st.file_uploader("📁 Fichier CSV 2", type=["csv"])

if file1 and file2:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    st.subheader("🔧 Sélection des colonnes à comparer")

    col1 = st.selectbox("Colonne du fichier 1", df1.columns)
    col2 = st.selectbox("Colonne du fichier 2", df2.columns)

    if st.button("🔍 Comparer"):
        valeurs_df1 = df1[col1].astype(str)
        valeurs_df2 = df2[col2].astype(str)

        lignes_non_trouvees = df1[~valeurs_df1.isin(valeurs_df2)]

        st.write(f"### Résultat : {len(lignes_non_trouvees)} ligne(s) non trouvée(s)")
        st.dataframe(lignes_non_trouvees)

        # Génération du CSV
        csv_result = lignes_non_trouvees.to_csv(index=False)
        st.download_button("📥 Télécharger les lignes en CSV", data=csv_result, file_name="lignes_non_trouvees.csv", mime="text/csv")
