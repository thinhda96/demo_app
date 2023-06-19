import pandas as pd
import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase

from config import db_config, open_ai_key
from database import Database
from plot import Plot


def create_db_query_agent():
    # This code initializes a connection to a MySQL database using the provided configuration, creates a ChatOpenAI
    # instance with the GPT-4 model, and then sets up an SQL agent with the database and language model for natural
    # language processing tasks.
    db = SQLDatabase.from_uri(
        f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=open_ai_key)

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_db_query_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )
    return agent


db_instance = Database(db_config)
plot_instance = Plot()


# plot_monthly_chart fetches the current month's transactions from the database, creates a chart to visualize these
# transactions, and then displays the chart using Streamlit.
def plot_monthly_chart():
    transactions = db_instance.fetch_current_month_transactions()
    chart = plot_instance.plot_monthly_transactions(transactions)
    st.pyplot(chart)


# plot_user_transactions_pie_chart fetches the top user transactions from the database, creates a pie chart to visualize these transactions,
# and displays the chart using Streamlit.
def plot_user_transactions_pie_chart():
    transactions_by_user = db_instance.fetch_top_user_transactions()
    chart_user = plot_instance.plot_user_transactions_pie_chart(transactions_by_user)
    st.pyplot(chart_user)


if __name__ == "__main__":
    agent = create_db_query_agent()

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

    all_data = db_instance.fetch_all_transactions()
    df = pd.DataFrame(all_data,
                      columns=['id', 'user_id', 'product_id', 'transaction_date', 'transaction_amount',
                               'payment_method'])
    st.subheader('Transaction Data')
    st.write(df)

    st.write('---')
    plot_monthly_chart()

    st.write('---')
    plot_user_transactions_pie_chart()
