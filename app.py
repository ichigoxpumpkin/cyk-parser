import streamlit as st
from CYK_Paser import Grammar
import pandas as pd

st.title("CYK KELOMPOK 1")
sentence = st.text_input("Kalimat : ")


def display_parsing_table(table):
    df = pd.DataFrame(table)
    st.dataframe(df.transpose())

if st.button("Continue"):
  g = Grammar()
  try:
      if g.parse(sentence):
        st.success(f"Kalimat '{sentence}' Valid")
      else:
        st.error(f"Kalimat '{sentence}' Tidak Valid")
      display_parsing_table(g.print_parse_table())
  except(ValueError):
     st.warning("Kata tidak ada di rules")