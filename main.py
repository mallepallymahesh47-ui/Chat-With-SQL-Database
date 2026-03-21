import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from connections import SQlite_Connection, MYSQL_Connection
load_dotenv()

# set up the LLM Model
LLM=ChatGroq(model="llama-3.1-8b-instant", temperature=0, streaming=True)

# Function to generate sql query
def get_sql_chain(db):
    table_names = ", ".join(db.get_usable_table_names())

    template = f"""
    You are a sharp data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question.
    
    <SCHEMA>{{schema}}</SCHEMA>
    
    Available tables (use EXACT names): {table_names}
    
    Conversation History: {{chat_history}}
    
    IMPORTANT RULES:
    - Write ONLY the SQL query and nothing else.
    - Do NOT wrap the SQL query in backticks.
    - Use EXACT table/column names from the schema.
    - The sample rows in schema are just examples — the real table has MORE rows.
    - Always query the full table, never assume data is limited to sample rows shown.
    
    Question: {{question}}
    SQL Query:
    """
    prompt=ChatPromptTemplate.from_template(template)
    
    # Tool to return sql query
    def get_schema(_):
        return db.get_table_info()
    
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | LLM
        | StrOutputParser()
    )

# Function to run and get response
def full_chain(user_input:str, db, chat_history):
    sql_chain=get_sql_chain(db)
    template=""" 
    You are a sharp data analyst giving a concise answer to a user's database question.
    Based on the table schema below, question, sql query, and sql response, write a concise answer in natural language.

    <SCHEMA>{schema}</SCHEMA>

    Conversational History : {chat_history}

    SQL Query : <SQL>{query}</SQL>

    User Question : {question}

    SQL Response : {response}

    Give a clear, concise, friendly answer in natural language based on the SQL result.
    Do NOT repeat the SQL query in your answer.
    """

    # Tool to run the query on database
    def run_query(query):
        try:
            return db.run(query)
        except Exception as e:
            return f"Query failed with error : {str(e)}"
        
    prompt=ChatPromptTemplate.from_template(template)
    chain=(
        RunnablePassthrough.assign(query=sql_chain).assign(schema=lambda _:db.get_table_info(), response= lambda var : run_query(var["query"]))
        | prompt
        | LLM
        | StrOutputParser()
    )

    return chain.invoke({"question":user_input, "chat_history":chat_history})

# Set the environment Variables
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")



# Landing Page
st.set_page_config(page_title="Chat with Database", page_icon="🐬", layout="wide")
 

st.title("Chat with SQL Databases 🐬")
st.caption("· Groq · LangChain · SQLite / MySQL")
    

st.sidebar.header("⚙️ Database Connection")


# User option to choose
choice=["Chat with SQlite File","Chat with MySQL"]
options=st.sidebar.selectbox("Select your database",choice)

if options=="Chat with SQlite File":
    uploaded_file=st.sidebar.file_uploader("Upload SQlite file", type=["db"])
    if uploaded_file is not None:
        with st.spinner("Connecting to SQlite Database..."):
            db=SQlite_Connection(uploaded_file)
            st.session_state.db=db
            st.sidebar.success("Connected to SQlite Database")


else:
    username=st.sidebar.text_input("Enter Username", key="Username")
    password=st.sidebar.text_input("Enter Password", type="password", key="Password")
    host=st.sidebar.text_input("Enter Host", key="Host")
    port=st.sidebar.text_input("Enter Port", key="Port")
    database=st.sidebar.text_input("Enter Database", key="Database")
    if st.sidebar.button("Connect"):
        if all([username, password, host, port, database]):
            with st.spinner("Connecting…"):
                try:
                    db = MYSQL_Connection(username, password, host, port, database)
                    st.session_state.db = db
                    st.sidebar.success("Connected to MySQL Database")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
        else:
                st.warning("Please fill in all fields.")



# Display the schema
if "db" in st.session_state:
    with st.sidebar.expander("View Database Schema"):
        st.code(st.session_state.db.get_table_info())


#Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[
        AIMessage(content="Hello! I am a helpful assistant Upload Database & Ask anything...")
    ]

# Conversational History and Display both the messages of AI and User
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("User"):
            st.markdown(message.content)

user_input=st.chat_input("Ask a question about your database...")
if user_input is not None and user_input.strip()!="":
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.chat_message("User"):
        st.markdown(user_input)

    with st.chat_message("AI"):
        response=full_chain(user_input, st.session_state.db, st.session_state.chat_history)
        st.markdown(response)
    st.session_state.chat_history.append(AIMessage(content=response))

# Button to clear the History
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = [
        AIMessage(content="Hello! I am a helpful assistant Upload Database & Ask anything...")
    ]

