import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64  # For handling file download

def analyze_dataframe(df):
    # Display the uploaded DataFrame
    st.subheader("Uploaded DataFrame:")
    st.write(df)

    # Show columns with missing values and their counts
    st.subheader("Columns with Missing Values:")
    missing_counts = df.isnull().sum()
    missing_info_df = pd.DataFrame({
        'Missing Value Count': missing_counts,
        'Missing Value Percentage': (missing_counts / df.shape[0]) * 100
    })
    st.write(missing_info_df[missing_info_df['Missing Value Count'] > 0])

    # Show value counts for each categorical column
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    st.subheader("Value Counts for Categorical Columns:")
    for col in categorical_columns:
        st.write(f"Column: {col}")
        st.write(df[col].value_counts())

    # Calculate mode for categorical columns
    st.subheader("Mode for Categorical Columns:")
    mode_values = df[categorical_columns].mode().iloc[0]
    st.write(mode_values)

    # Fill missing values with mode for categorical columns
    filled_df = df.copy()
    filled_df[categorical_columns] = filled_df[categorical_columns].fillna(mode_values)

    # Show updated DataFrame after filling missing values with mode
    st.subheader("Updated DataFrame after Filling Missing Values with Mode:")
    st.write(filled_df)

    # Download option to download updated DataFrame as CSV
    if st.button("Download Updated DataFrame as CSV"):
        download_csv(filled_df, filename='updated_dataframe.csv')

def download_csv(df, filename='data.csv'):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)


def main():
    st.title("DataFrame Analysis Tool")

    # Retrieve uploaded DataFrame from session state
    #df = st.session_state.df

    # Check if DataFrame is available
    if "df" in st.session_state:
        # Analyze the DataFrame
        df = st.session_state.df
        analyze_dataframe(df)
        
    else:
        st.warning("Please upload a CSV file first on the input page.")

if __name__ == "__main__":
    main()
