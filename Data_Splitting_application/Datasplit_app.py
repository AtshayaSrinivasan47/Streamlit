import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split

# function to preprocess the data
def preprocess_data(df):
    return

def count_features(df):
    return len(df.columns)

#function to split dataset
def split_data(df, test_size=0.2):
    train,test=train_test_split(df,test_size=test_size)
    train_percentage=len(train)/len(df)*100
    test_percentage=len(test)/len(df)*100
    return train, test, train_percentage,test_percentage

def federated_split(df,num_nodes,test_size=0.2):
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

# streamlit app
st.title('Data split analysis for ML model training and testing')

# upload dataset
uploaded_file=st.file_uploader("Choose a CSV file", type='csv')

if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    st.write(" Data Preview")
    st.write(df.head())
    
    # option to preprocess the dataset
    if st.button('Pre-process the data'):
        df=preprocess_data(df)
        st.write("Pre-processed data preview")
        st.write(df.head())
    
    # show feature count
    if st.button('Count of features'):
        st.write(f"Number of features: {count_features(df)}")
    
    # Training and testing data split
    if st.button("Train and test split data percentage"):
        st.header("Train and test Data Split")
        test_size=st.slider('Test_size (0-1)',0.0,0.5,0.2)
        if st.button("Split Data"):
            train, test, train_percentage, test_percentage = split_data(df, test_size)
            st.write(f"Training data : {train_percentage:0.2f}%")
            st.write(f"Testing data : {test_percentage:0.2f}%")
            st.write("Training data preview")
            st.write(train.head())
            st.write("Testing data preview")
            st.write(test.head())
    
    # Federated learning data split
    if st.button("Federated_learning_Data split"):
        st.header("Federated Learning Data split")
        num_nodes=st.slider('num_of_nodes', min_values=1, value=3)
        test_size=st.slider('Test_size (0-1)',0.0,0.5,0.2)
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
