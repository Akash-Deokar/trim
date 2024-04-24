import streamlit as st
import pandas as pd

def perform_one_hot_encoding(df, columns_to_encode):
    """
    Perform one-hot encoding on specified columns of the DataFrame using pandas' get_dummies().
    Returns the DataFrame with one-hot encoded columns.
    """
    # Perform one-hot encoding using pd.get_dummies()
    encoded_df = pd.get_dummies(df, columns=columns_to_encode, drop_first=True)
    
    return encoded_df

def main():
    st.title("One-Hot Encoding App with pandas")

    # File upload
    st.sidebar.header('Upload your CSV file')
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)

        st.header("Original Data")
        st.write(df)

        # Identify categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

        if categorical_cols:
            st.subheader("Select Columns for One-Hot Encoding")
            selected_cols = st.multiselect("Choose columns to encode", categorical_cols)

            if selected_cols:
                # Perform one-hot encoding
                encoded_df = perform_one_hot_encoding(df, selected_cols)

                st.header("Encoded Data")
                st.write(encoded_df)

            else:
                st.warning("Please select at least one column for encoding.")

        else:
            st.info("No categorical columns found in the dataset.")

if __name__ == "__main__":
    main()
