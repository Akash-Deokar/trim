import streamlit as st
import pandas as pd
from sklearn.impute import KNNImputer

def perform_knn_imputation(df, n_neighbors=5):
    # Separate numerical and categorical columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    
    # Initialize KNN imputer
    imputer = KNNImputer(n_neighbors=n_neighbors)
    
    # Create a copy of the DataFrame for imputation
    df_imputed = df.copy()
    
    # Perform KNN imputation only on numerical columns
    df_imputed[numeric_columns] = imputer.fit_transform(df[numeric_columns])
    
    return df_imputed

def main():
    st.title('KNN Imputation App')
    
    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Read CSV file
            df = pd.read_csv(uploaded_file)
            
            st.write("Original DataFrame:")
            st.write(df)
            
            # Perform KNN imputation
            df_imputed = perform_knn_imputation(df)
            
            st.write("Imputed DataFrame:")
            st.write(df_imputed)
            
            # Allow user to download the imputed CSV file
            csv_file = df_imputed.to_csv(index=False)
            st.download_button(label="Download Imputed CSV", data=csv_file, file_name="imputed_data.csv", mime="text/csv")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
