import streamlit as st
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import OneHotEncoder

def perform_mice_imputation(df):
    # Separate numerical and categorical columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    
    # Encode categorical columns using one-hot encoding
    df_encoded = pd.get_dummies(df, columns=categorical_columns, drop_first=True)
    
    # Initialize MICE imputer for numerical columns
    imputer = IterativeImputer(random_state=0)
    df_imputed = df_encoded.copy()
    df_imputed[numeric_columns] = imputer.fit_transform(df_encoded[numeric_columns])
    
    # Fill missing values in categorical columns with mode
    for col in categorical_columns:
        mode_value = df[col].mode()[0]
        df_imputed[col].fillna(mode_value, inplace=True)
    
    return df_imputed

def main():
    st.title('MICE Imputation App')
    
    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        
        st.write("Original DataFrame:")
        st.write(df)
        
        # Perform MICE imputation
        df_imputed = perform_mice_imputation(df)
        
        st.write("Imputed DataFrame:")
        st.write(df_imputed)
        
        # Allow user to download the imputed CSV file
        csv_file = df_imputed.to_csv(index=False)
        st.download_button(label="Download Imputed CSV", data=csv_file, file_name="imputed_data.csv", mime="text/csv")

if __name__ == '__main__':
    main()
