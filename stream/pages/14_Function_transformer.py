import streamlit as st
import pandas as pd
import numpy as np

def apply_log_transformation(df, columns):
    """
    Apply log transformation to the specified columns in the DataFrame.
    """
    for col in columns:
        df[col + '_log'] = np.log(df[col] + 1)  # Adding 1 to handle zero and negative values
    return df

def apply_reciprocal_transformation(df, columns):
    """
    Apply reciprocal transformation to the specified columns in the DataFrame.
    """
    for col in columns:
        df[col + '_reciprocal'] = 1 / (df[col] + 1)  # Adding 1 to handle zero values
    return df

def apply_square_transformation(df, columns):
    """
    Apply square transformation to the specified columns in the DataFrame.
    """
    for col in columns:
        df[col + '_square'] = df[col] ** 2
    return df

def apply_square_root_transformation(df, columns):
    """
    Apply square root transformation to the specified columns in the DataFrame.
    """
    for col in columns:
        df[col + '_sqrt'] = np.sqrt(df[col])
    return df

def main():
    st.title("DataFrame Function Transformation App")

    # File upload
    st.sidebar.header('Upload your CSV file')
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)

        st.header("Original DataFrame")
        st.write(df)

        # Identify numerical columns
        numerical_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()

        if numerical_cols:
            st.sidebar.subheader("Select Columns for Transformation")
            selected_cols = st.sidebar.multiselect("Choose columns for transformation", numerical_cols)

            if selected_cols:
                st.header("Transformations for Selected Columns")

                # Apply log transformation
                df_log = apply_log_transformation(df.copy(), selected_cols)
                st.subheader("Log Transformation")
                st.write(df_log)

                # Apply reciprocal transformation
                df_reciprocal = apply_reciprocal_transformation(df.copy(), selected_cols)
                st.subheader("Reciprocal Transformation")
                st.write(df_reciprocal)

                # Apply square transformation
                df_square = apply_square_transformation(df.copy(), selected_cols)
                st.subheader("Square Transformation")
                st.write(df_square)

                # Apply square root transformation
                df_sqrt = apply_square_root_transformation(df.copy(), selected_cols)
                st.subheader("Square Root Transformation")
                st.write(df_sqrt)

if __name__ == "__main__":
    main()
