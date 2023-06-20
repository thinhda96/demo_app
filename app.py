
import pandas as pd
import streamlit as st

from chat_sql_agent import create_openai_sqlagent
from config import db_config, open_ai_key
from database import Database
from plot import Plot

db_instance = Database(db_config)
plot_instance = Plot()


def plot_monthly_chart():
    transactions = db_instance.fetch_current_month_transactions()
    chart = plot_instance.plot_monthly_transactions(transactions)
    st.pyplot(chart)


def plot_user_transactions_pie_chart():
    transactions_by_user = db_instance.fetch_top_user_transactions()
    chart_user = plot_instance.plot_user_transactions_pie_chart(transactions_by_user)
    st.pyplot(chart_user)


if __name__ == "__main__":
    agent = create_openai_sqlagent(open_ai_key)

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
    # Create two columns for the charts
    col1, col2 = st.beta_columns(2)
    # show monthly chart in the first column
    with col1:
        plot_monthly_chart()
    # show transaction pie chart in the second column
    with col2:
        plot_user_transactions_pie_chart()

