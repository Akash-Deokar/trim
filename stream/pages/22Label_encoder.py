import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def main():
    st.title("Categorical Data Encoder")

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
            st.subheader("Select Categorical Columns for Encoding")
            selected_cols = st.multiselect("Choose columns", categorical_cols)

            if selected_cols:
                # Apply label encoding
                for col in selected_cols:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))

                st.header("Encoded Data")
                st.write(df)

            else:
                st.warning("Please select at least one column for encoding.")

        else:
            st.info("No categorical columns found in the dataset.")

if __name__ == "__main__":
    main()
