# streamlit_app.py
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from gspread_pandas import Spread,Client
import ssl
ssl._create_default_https_context=ssl._create_unverified_context
# Create a connection object.
scope=["https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"]
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope,
)
client=Client(scope=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"], creds=credentials)
spreadsheetname="test"
spread=Spread(spreadsheetname,client=client)


sh=client.open(spreadsheetname)
worksheet_list = sh.worksheets()

st.write(spread.url)
# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(f"{row.name} has a :{row.pet}:")
