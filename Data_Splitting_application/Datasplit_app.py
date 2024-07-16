import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split

def count_features(df):
    return len(df.columns)

#function to split dataset
def split_data(df, test_size):
    train,test=train_test_split(df,test_size=test_size)
    train_percentage=len(train)/len(df)*100
    test_percentage=len(test)/len(df)*100
    return train, test, train_percentage,test_percentage

def federated_split(df,num_nodes,test_size):
    node_splits=[]
    for _ in range(num_nodes):
        train,test=train_test_split(df,test_size=test_size)
        node_splits.append({
            'train':train,
            'test':test,
            'train_percentage':len(train)/len(df)*100,
            'test_percentage':len(test)/len(df)*100
        })
    return node_splits

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# streamlit app
st.title('Data split analysis for ML model training and testing')

# upload dataset
uploaded_file=st.file_uploader("Choose a CSV file", type='csv')

if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    st.write(" Data Preview")
    st.write(df.head())
        
    # show feature count
    if st.button('Count of features'):
        st.write(f"Number of features: {count_features(df)}")
    
    # Training and testing data split
    st.header("Train and test Data Split")
    test_size=st.slider('Test_size (0-1)',0.0,0.5,0.2,key='test_size_slider')
    if st.button("Split Data"):
        train, test, train_percentage, test_percentage = split_data(df, test_size)
        st.write(f"Training data : {train_percentage:0.2f}%")
        st.write(f"Testing data : {test_percentage:0.2f}%")
        st.write("Training data preview")
        st.write(train.head())
        st.write("Testing data preview")
        st.write(test.head())
        # provide options to download train and test csv file
        train_csv=convert_df_to_csv(train)
        test_csv=convert_df_to_csv(test)
        st.download_button(
            label="Download training data as CSV",
            data=train_csv,
            file_name='train_data.csv',
            mime='text/csv'
        )
        st.download_button(
            label="Download testing data as CSV",
            data=test_csv,
            file_name='test_data.csv',
            mime='text/csv'
        )
    
    # Federated learning data split
    st.header("Federated Learning Data split")
    num_nodes=st.slider('num_of_nodes', min_value=1,max_value=10, value=3, key='number of nodes')
    test_size=st.slider('Test_size (0-1)',0.0,0.5,0.2, key='test_size_slider_Federated')
    if st.button("Split_data"):
        node_splits=federated_split(df,num_nodes,test_size)
        for i, nodes in enumerate(node_splits):
            st.write(f"Node {i+1}")
            st.write(f"Training_data: {nodes['train_percentage']:0.2f}%")
            st.write(f"Test_data: {nodes['test_percentage']:0.2f}%")
            st.write("Train data Preview")
            st.write(nodes['train'].head())
            st.write("Test data preview")
            st.write(nodes['test'].head())
        # Provide option to download each node's split data
        for i, node in enumerate(node_splits):
            train_csv = convert_df_to_csv(node['train'])
            test_csv = convert_df_to_csv(node['test'])
            st.download_button(
                label=f"Download Node {i + 1} Training Data as CSV",
                data=train_csv,
                file_name=f'node_{i + 1}_train_data.csv',
                mime='text/csv',
            )
            st.download_button(
                label=f"Download Node {i + 1} Testing Data as CSV",
                data=test_csv,
                file_name=f'node_{i + 1}_test_data.csv',
                mime='text/csv',
            )
