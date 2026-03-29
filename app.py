import streamlit as st
from pathlib import Path
from langchain_community.agent_toolkits import create_sql_agent   
from langchain_classic.sql_database import SQLDatabase
from langchain_classic.agents.agent_types import AgentType
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq


st.set_page_config(page_title="LangChain:Chat with SQL DB",page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

INJECTION_WARNING = """
SQL agents can be
"""

LOCALDB  = "USE_LOCALDB"
MYSQL ="USE_MYSQL"

radio_opt = ["Use SQLlite 3 Database - Student.db","Connect to you SQL Database"]
selected_opt = st.sidebar.radio(label="Choose the DB which you want to chat",options=radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_url = MYSQL
    mysql_host = st.sidebar.text_input("Provide MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL Username")
    mysql_password = st.sidebar.text_input("MySQL password",type="password")
    mysql_db = st.sidebar.text_input("MySQL database")

else:
    db_url= LOCALDB

api_key = st.sidebar.text_input("Enter a Groq API KEY",type="password")

if not db_url:
    st.info("Please enter the database informatiom and URL")

if not api_key:
    st.info("Please add the Groq API KEY")

## LLM Model
model_name = st.sidebar.selectbox(
    "Select Model",
    [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
    ]
)

llm = ChatGroq(
    api_key=api_key,
    model=model_name,
    temperature=0,
    streaming=True
)

@st.cache_resource(ttl="2h")
def configure_db(db_url,mysql_host = None,mysql_user=None,mysql_password = None,mysql_db = None):
    if db_url == LOCALDB:
        db_file_path = (Path(__file__).parent/"student.db").absolute()
        print(db_file_path)
        creator = lambda: sqlite3.connect(f"file:{db_file_path}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))
    
    elif db_url == MYSQL:
        if not (mysql_user and mysql_db and mysql_host and mysql_password):
            st.error("Please provide all MySQL connection details")
            st.stop()

        if "@" in mysql_host:
            st.error("❌ Host should NOT contain '@'. Just write 127.0.0.1")
            st.stop()   

        from urllib.parse import quote_plus

        encoded_password = quote_plus(mysql_password)

        connection_string = f"mysql+pymysql://{mysql_user}:{encoded_password}@{mysql_host}/{mysql_db}"

        return SQLDatabase(create_engine(connection_string))
    
if db_url == MYSQL:
    db = configure_db(db_url,mysql_host,mysql_user,mysql_password,mysql_db)
else:
    db = configure_db(db_url)

## Tool kit

toolkit = SQLDatabaseToolkit(db=db,llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose =True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True 
)
if "messages" not in st.session_state or st.sidebar.button("Clear message History"):
    st.session_state["messages"] = [{"role":"assistant","content":"How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

user_query = st.chat_input(placeholder="Ask anything from the Database")

if user_query:
    st.session_state.messages.append({"role":"user","content":user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)
