import streamlit as st
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

def main():
    st.title("Custom Ordinal Encoding App")

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
            st.subheader("Select Categorical Columns for Custom Ordinal Encoding")
            selected_cols = st.multiselect("Choose columns", categorical_cols)

            if selected_cols:
                # Custom mapping for each selected column
                for col in selected_cols:
                    st.subheader(f"Custom Mapping for '{col}'")
                    unique_values = df[col].unique()
                    value_mapping = {}

                    for value in unique_values:
                        default_value = value  # Default mapping is the same as category value
                        custom_value = st.text_input(f"Enter value for '{value}' (default: {default_value}):", value=default_value)
                        value_mapping[value] = custom_value

                    # Apply custom ordinal encoding
                    df[col] = df[col].map(value_mapping)

                st.header("Encoded Data")
                st.write(df)

            else:
                st.warning("Please select at least one column for encoding.")

        else:
            st.info("No categorical columns found in the dataset.")

if __name__ == "__main__":
    main()
