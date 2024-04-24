import pandas as pd
import streamlit as st
from sklearn.impute import KNNImputer

def knn_impute_missing(df, columns_to_impute, n_neighbors=5, weights='uniform'):
    # Perform KNN imputation on selected numerical columns with missing values
    imputer = KNNImputer(n_neighbors=n_neighbors, weights=weights)
    df_imputed = df.copy()
    df_imputed[columns_to_impute] = imputer.fit_transform(df_imputed[columns_to_impute])
    return df_imputed

def display_imputed_rows(original_df, imputed_df):
    # Identify rows that have been imputed
    imputed_rows = (original_df.isnull() & ~imputed_df.isnull()).any(axis=1)
    return original_df[imputed_rows]

def main():
    st.title("KNN Imputation App")
    
    # Allow user to upload a CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        st.write("Original DataFrame:")
        st.write(df)
        
        # Identify numerical columns with missing values
        numerical_cols = df.select_dtypes(include=['int', 'float']).columns.tolist()
        numerical_cols_with_missing = [col for col in numerical_cols if df[col].isnull().any()]
        
        if numerical_cols_with_missing:
            st.write(f"Numerical columns with missing values: {', '.join(numerical_cols_with_missing)}")
            
            # Multi-select widget to choose columns for imputation
            columns_to_impute = st.multiselect("Select columns to impute", numerical_cols_with_missing, default=numerical_cols_with_missing)
            
            # Slider widget to select the value of k
            k_value = st.slider("Select the value of k", min_value=1, max_value=10, value=5)
            
            # Radio button widget to select the weight function
            weights_option = st.radio("Select weight function", options=['uniform', 'distance'], index=0)
            
            if st.button("Impute Missing Values using KNN") and columns_to_impute:
                # Perform KNN imputation on selected columns with specified parameters
                df_imputed = knn_impute_missing(df, columns_to_impute, n_neighbors=k_value, weights=weights_option)
                
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
            st.write("No numerical columns with missing values found in the uploaded dataset.")

if __name__ == "__main__":
    main()
