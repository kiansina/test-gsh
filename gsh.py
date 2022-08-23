import streamlit as st
import pandas as pd
#import psycopg2
import random
import time

from google.oauth2 import service_account
from gspread_pandas import Spread,Client
import ssl
ssl._create_default_https_context=ssl._create_unverified_context
scope=["https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets"]
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope,
)
client=Client(scope=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"], creds=credentials)
spreadsheetname="Questionnaire_test"
s=Spread(spreadsheetname,client=client)


questions = {
  "1": "2+2=?",
  "2": "√81=?",
  "3": "Quale non è un colore?",
  "4": "la mela ad frutta è come pizza ad?",
  "5": "chi è la mamma di fratello della sorella di tua madre?",
  "6": "1, 4, 9, ?",
  "7": "1, 4, 5, 9, ?",
  "8": "2, 3, 5, 7, 11, ?",
  "9": "quale è il capitale di Italia?",
  "10": "se giusto è sbaglio è sbaglio è sbaglio, che cosa è giusto?"
}

if "list" not in st.session_state:
    st.session_state['list']=[]

def check_password():
    """Returns `True` if the user had a correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            #del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if "t0" not in st.session_state:
    st.session_state["t0"] = time.time()
if "st" not in st.session_state:
    st.session_state["st"]= True
if "usercheck" not in st.session_state:
    st.session_state['usercheck']="sina"

if check_password():
    @st.cache(allow_output_mutation=True)
    def get_data():
        return []
    if "rn" not in st.session_state:
        st.session_state["rn"] = random.sample(range(1, 10), 5)
    Username=st.text_input("Username:")
    if st.button("check"):
        if Username not in st.session_state["list"]:
            st.session_state['usercheck']=True
            st.session_state['st']=True
        else:
            st.session_state['usercheck']=False
    if st.session_state['usercheck']==True:
        if st.session_state["st"]==True:
            Nome = st.text_input("Nome:")
            Cognome = st.text_input("Cognome:")
            sodisfazione = st.slider("Sodisfazione", 0, 100)
            Qa=st.text_input(questions[str(st.session_state["rn"][0])])
            Qb=st.text_input(questions[str(st.session_state["rn"][1])])
            Qc=st.text_input(questions[str(st.session_state["rn"][2])])
            Qd=st.text_input(questions[str(st.session_state["rn"][3])])
            Qe=st.text_input(questions[str(st.session_state["rn"][4])])
            if st.button("Submit"):
                get_data().append({"Username":Username,"Nome": Nome,"Cognome":Cognome, "Livello sodisfazione": sodisfazione, "q1": Qa, "q2": Qb, "q3": Qc, "q4": Qd, "q5": Qe, "time":time.time()-st.session_state["t0"]})
                st.write(pd.DataFrame(get_data()))
                A=pd.DataFrame(get_data())
                if st.button("Confirm"):
                    s.df_to_sheet(A,sheet='test', start='A1', replace=True, freeze_headers=1)
                st.title('la sua esame è finito 😊.')
                st.title("Grazie per la collaborazione! 😍")
                st.session_state["st"]=False
                st.stop()
        else:
            st.title('l\'esame gia registrato 😊.')
            st.session_state["list"].append(Username)
    else:
        st.title('Il username non è giusto')
