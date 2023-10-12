import streamlit as st
from st_pages import Page, show_pages, add_page_title
from services.upload_data import *
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
from streamlit_extras.switch_page_button import switch_page

show_pages(
  [
    Page("pages/principal.py", "Depois te pago", ":money_with_wings:"),
    Page("pages/adicionar_role.py", "Adicionar role", ":heavy_plus_sign:"),
    Page("pages/transferir_valor.py", "Transferir valor", ":heavy_dollar_sign:"),
    Page("pages/checar_transferencias.py", "Checar transferencias", ":moneybag:")
  ]
)



if __name__ == "__main__":
  switch_page("Depois te pago")