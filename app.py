
import streamlit as st
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
