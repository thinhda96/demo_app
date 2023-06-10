import pandas as pd
import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.chat_models import ChatOpenAI
from config import db_config, open_ai_key
from database import Database
from plot import Plot
import os

db = SQLDatabase.from_uri(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=open_ai_key)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

db_instance = Database(db_config)
plot_instance = Plot()

with st.sidebar:
    question = st.text_area("Question")
    if st.button("Ask"):
        if question == "":
            st.warning("Please enter a question")
        else:
            with st.spinner('Thinking...'):
                result = agent.run(question)
            st.success(f'Result:\n {result}')

st.title("Dashboard builder")

all_data = db_instance.query_all()
df = pd.DataFrame(all_data, columns=['id', 'user_id', 'product_id', 'transaction_date', 'transaction_amount','payment_method'])
st.subheader('Transaction Data')
st.write(df)

st.write('---')

transactions = db_instance.fetch_transactions()
chart = plot_instance.plot_transactions(transactions)
st.pyplot(chart)

st.write('---')

transactions_by_user = db_instance.fetch_total_transactions_by_user()
chart_user = plot_instance.plot_total_transactions_by_user(transactions_by_user)
st.pyplot(chart_user)