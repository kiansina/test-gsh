# streamlit_app.py
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from gspread_pandas import Spread,Client
# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
client=Client(scope=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"], creds=credentials)
spreadsheetname="test"
spread=Spread(spreadsheetname,client=client)


sh=client.open(spreadsheetname)
worksheet_list = sh.worksheets()

st.write(spread.url)
