import streamlit as st
import pandas as pd

def main():
    st.title("Upload CSV File")

    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Store the DataFrame in session state
        st.session_state.df = df

        st.success("File uploaded successfully!")

        # Link to navigate to the display page
        #st.markdown("[Go to Display Page](/dis)")

if __name__ == "__main__":
    main()
