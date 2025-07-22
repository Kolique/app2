import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparateur de colonnes CSV", layout="centered")
st.title("🔍 Comparateur de colonnes entre 2 fichiers CSV")

file1 = st.file_uploader("📁 Upload du fichier principal (CSV 1)", type=["csv"])
file2 = st.file_uploader("📁 Upload du fichier de référence (CSV 2)", type=["csv"])

if file1 and file2:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    st.subheader("🎯 Choisis les colonnes à comparer")
    col1 = st.selectbox("🔸 Colonne du CSV 1", df1.columns)
    col2 = st.selectbox("🔹 Colonne du CSV 2", df2.columns)

    if st.button("🚀 Comparer"):
        values_df1 = df1[col1].astype(str)
        values_df2 = df2[col2].astype(str)
        mask = ~values_df1.isin(values_df2)
        result = df1[mask]

        st.success(f"{len(result)} ligne(s) du CSV 1 dont la valeur dans '{col1}' n’est pas dans '{col2}'")
        st.dataframe(result)

        csv_res = result.to_csv(index=False)
        st.download_button("📥 Télécharger le résultat", data=csv_res,
                           file_name="resultat_non_trouvees.csv", mime="text/csv")
