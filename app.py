
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
    transactions_by_user = db_instance.fetch_top_10_user_transactions()
    chart_user = plot_instance.plot_user_transactions_pie_chart(transactions_by_user)
    st.pyplot(chart_user)

def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            # Validate the uploaded CSV file
            if not {'user_id', 'product_id', 'transaction_date', 'transaction_amount', 'payment_method'}.issubset(df_uploaded.columns):
                st.error("Invalid CSV file format. Please upload a file with the correct columns.")
                return

            # Process the uploaded CSV file
            db_instance.insert_transactions(df_uploaded)
            st.success("Transactions imported successfully.")
        except Exception as e:
            st.error(f"Error processing the uploaded file: {e}")

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

        st.write("---")
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        process_uploaded_file(uploaded_file)


    st.title("Dashboard builder")

    all_data = db_instance.fetch_all_transactions()
    df = pd.DataFrame(all_data,
                      columns=['id', 'user_id', 'product_id', 'transaction_date', 'transaction_amount',
                               'payment_method'])
    st.subheader('Transaction Data')
    st.write(df)
    
    all_users = db_instance.fetch_all_users()
    df_users = pd.DataFrame(all_users, columns=['id', 'username', 'email', 'created_at'])
    st.subheader('User Data')
    st.write(df_users)

    st.write('---')
    # show monthly chart
    plot_monthly_chart()

    st.write('---')
    # show transaction pie chart
    plot_user_transactions_pie_chart()

    st.write('---')
    plot_spending_money_per_month_chart()
