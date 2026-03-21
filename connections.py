import streamlit as st
from langchain_community.utilities import SQLDatabase
import tempfile

# Function to connect to Local db or user input file
def SQlite_Connection(uploaded_file)->SQLDatabase:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name
    
    db = SQLDatabase.from_uri(f"sqlite:///{tmp_file_path}")
    return db

# Connection with MYSQL 
def MYSQL_Connection(username:str, password:str, host:str, port:str, database:str)->SQLDatabase:
    MYSQL_db_uri=f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
    MYSQL_db=SQLDatabase.from_uri(MYSQL_db_uri)
    return MYSQL_db