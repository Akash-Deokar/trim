import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import boxcox, yeojohnson

def apply_boxcox_transformation(df, columns):
    """
    Apply Box-Cox transformation to the specified columns in the DataFrame.
    """
    for col in columns:
        df[col + '_boxcox'], _ = boxcox(df[col] + 1)  # Adding 1 to handle zero and negative values
    return df

def apply_yeojohnson_transformation(df, columns):
    """
    Apply Yeo-Johnson transformation to the specified columns in the DataFrame.
    """
    for col in columns:
        df[col + '_yeojohnson'], _ = yeojohnson(df[col] + 1)  # Adding 1 to handle zero and negative values
    return df

def main():
    st.title("DataFrame Power Transformation App")

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
                st.header("Power Transformations for Selected Columns")

                # Apply Box-Cox transformation
                df_boxcox = apply_boxcox_transformation(df.copy(), selected_cols)
                st.subheader("Box-Cox Transformation")
                st.write(df_boxcox)

                # Apply Yeo-Johnson transformation
                df_yeojohnson = apply_yeojohnson_transformation(df.copy(), selected_cols)
                st.subheader("Yeo-Johnson Transformation")
                st.write(df_yeojohnson)

if __name__ == "__main__":
    main()
