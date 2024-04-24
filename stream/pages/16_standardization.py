import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler

def standardize_numerical_columns(df):
    """
    Standardize numerical columns (float and int) in the DataFrame.
    """
    # Identify numerical columns
    numerical_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()

    if not numerical_cols:
        st.warning("No numerical columns found in the DataFrame.")
        return df

    # Perform standardization using StandardScaler
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    return df

def main():
    st.title("DataFrame Standardization App")

    # File upload
    st.sidebar.header('Upload your CSV file')
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)

        st.header("Original DataFrame")
        st.write(df)

        # Perform standardization on numerical columns
        df_standardized = standardize_numerical_columns(df.copy())

        st.header("Updated DataFrame after Standardization")
        st.write(df_standardized)

        # Button to download updated DataFrame as CSV
        st.sidebar.markdown("---")
        st.sidebar.header("Download Updated CSV")
        st.sidebar.download_button(
            label="Download CSV",
            data=df_standardized.to_csv(index=False),
            file_name="updated_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
