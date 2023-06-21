
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


def plot_spending_money_per_month_chart():
    spending_data = db_instance.fetch_spending_money_per_month()
    chart = plot_instance.plot_spending_money_per_month(spending_data)
    st.pyplot(chart)


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
    # show monthly chart
    plot_monthly_chart()

    st.write('---')
    # show transaction pie chart
    plot_user_transactions_pie_chart()

    st.write('---')
    # show spending money per month chart
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            # Add any content you want to display in the left column
            pass
        with col2:
            # show spending money per month chart
            plot_spending_money_per_month_chart()
