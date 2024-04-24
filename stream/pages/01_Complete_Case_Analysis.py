import streamlit as st
import pandas as pd

def main():
    st.title("Complete Case Analysis and Null Value Analysis")

    # Check if the DataFrame exists in session state
    if "df" in st.session_state:
        df = st.session_state.df

        # Display explanation of Complete Case Analysis (CCA)
        display_cca_explanation()

        # Calculate and display null value percentages
        null_summary = calculate_null_percentages(df)
        st.write("### Uploaded Dataframe:")
        st.write(df.head(5))
        st.write("### Null Value Percentages:")
        
        st.write(null_summary)
    else:
        st.warning("Please upload a CSV file first on the input page.")

def display_cca_explanation():
    st.write("""
    **What is Complete Case Analysis (CCA)?**

    Complete case analysis (CCA), also called 'listwise deletion' of cases, consists in discarding rows
    where values in any of the columns are missing.

    Complete case analysis means literally analyzing only those observations for
    which there is information in all of the variables in the dataset.

    **Assumptions for CCA:**

    1. Data should be missing completely at random (MCAR).
    2. Missing data should be less than 5%.

    **Advantages of CCA:**

    1. Easy to implement as no data manipulation is required.
    2. Preserves variable distribution (if data is MCAR, then the distribution of the variables
       of the reduced dataset should match the distribution in the original dataset).

    **Disadvantages of CCA:**

    1. It can exclude a large fraction of the original dataset (if missing data is abundant).
    2. Excluded observations could be informative for the analysis (if data is not missing at random).
    3. When using our models in production, the model will not know how to handle missing data.
    """)
    #st.write(.head(5))
def calculate_null_percentages(df):
    # Calculate total number of rows
    total_rows = df.shape[0]

    # Calculate number of null values in each column
    null_counts = df.isnull().sum()

    # Calculate percentage of null values for each column
    null_percentages = (null_counts / total_rows) * 100

    # Create a DataFrame to store the results
    null_summary = pd.DataFrame({
        'Column': null_counts.index,
        'Null Count': null_counts.values,
        'Null Percentage': null_percentages.values
    })

    return null_summary

if __name__ == "__main__":
    main()
