import pandas as pd
import streamlit as st
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

def mice_impute_missing(df, columns_to_impute, max_iter=10):
    # Perform MICE imputation on selected columns
    imputer = IterativeImputer(max_iter=max_iter)
    df_imputed = df.copy()
    df_imputed[columns_to_impute] = imputer.fit_transform(df_imputed[columns_to_impute])
    return df_imputed

def display_imputed_rows(original_df, imputed_df):
    # Identify rows that have been imputed
    imputed_rows = (original_df.isnull() & ~imputed_df.isnull())
    return original_df[imputed_rows.any(axis=1)]

def main():
    st.title("MICE Imputation App")
    
    # Allow user to upload a CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        st.write("Original DataFrame:")
        st.write(df)
        
        # Identify columns with missing values
        columns_with_missing = df.columns[df.isnull().any()].tolist()
        
        if columns_with_missing:
            st.write(f"Columns with missing values: {', '.join(columns_with_missing)}")
            
            # Multi-select widget to choose columns for imputation
            columns_to_impute = st.multiselect("Select columns to impute", columns_with_missing, default=columns_with_missing)
            
            # Slider widget to select the number of iterations
            num_iterations = st.slider("Select number of iterations", min_value=1, max_value=20, value=10)
            
            if st.button("Impute Missing Values using MICE") and columns_to_impute:
                # Perform MICE imputation on selected columns with specified iterations
                df_imputed = mice_impute_missing(df, columns_to_impute, max_iter=num_iterations)
                
                st.write("Imputed DataFrame:")
                st.write(df_imputed)
                
                # Display rows that were imputed
                imputed_rows = display_imputed_rows(df, df_imputed)
                if not imputed_rows.empty:
                    st.write("Rows with imputed values:")
                    st.write(imputed_rows)
                else:
                    st.write("No rows were imputed.")
        else:
            st.write("No columns with missing values found in the uploaded dataset.")

if __name__ == "__main__":
    main()
