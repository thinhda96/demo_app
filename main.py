import streamlit as st
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

db_user = "root"
db_password = "password"
db_host = "localhost:3306"
db_name = "payment"
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
from langchain.chat_models import ChatOpenAI
open_ai_key = st.sidebar.text_input("OpenAI API Key", value='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')
# open_ai_key ='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'
llm = ChatOpenAI(model_name="gpt-4",openai_api_key=open_ai_key)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)


toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)
db_config = {
        'user': 'root',
        'password': 'password',
        'host': 'localhost',
        'database': 'payment'
    }

def fetch_transactions():
    # Replace these with your database credentials


    # Connect to the database
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Fetch the transaction data for the current month
    query = f"""
    SELECT transaction_date, transaction_amount
    FROM transactions
    WHERE MONTH(transaction_date) = {current_month} AND YEAR(transaction_date) = {current_year}
    """

    cursor.execute(query)
    data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    cnx.close()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data, columns=['transaction_date', 'transaction_amount'])

    return df

def plot_transactions(df):
    # Group the data by date and sum the transaction amounts
    df['transaction_amount'] = pd.to_numeric(df['transaction_amount'])
    daily_totals = df.groupby('transaction_date').sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    daily_totals.plot(kind='bar', ax=ax)
    ax.set_title('Total Transactions This Month')
    ax.set_xlabel('Date')
    ax.set_ylabel('Transaction Amount')
    return fig

def plot_total_transactions_by_user(df):
    # Connect to the database
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # Fetch the transaction data
    query = """
       SELECT user_id, SUM(transaction_amount) as transaction_amount
       FROM transactions
       GROUP BY user_id
       LIMIT 10
       """

    cursor.execute(query)
    data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    cnx.close()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data, columns=['user_id', 'transaction_amount'])
    df['transaction_amount'] = pd.to_numeric(df['transaction_amount'])

    # Group the data by user_id and sum the transaction amounts
    user_totals = df.groupby('user_id').sum()

    # Plot the pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    user_totals.plot(kind='pie', y='transaction_amount', ax=ax, legend=False, autopct='%1.1f%%')
    ax.set_title('Total Transactions by User')
    ax.set_ylabel('')

    return fig


with st.sidebar:
    question = st.text_area("Question")
    if st.button("Ask"):
        result = agent.run(question)
        st.markdown(result)

# Streamlit app
st.title("Dashboard builder")
transactions = fetch_transactions()
chart = plot_transactions(transactions)
st.pyplot(chart)

chart_user = plot_total_transactions_by_user(transactions)
st.pyplot(chart_user)