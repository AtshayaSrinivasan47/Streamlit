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

def federated_split(df, num_nodes, test_size):
    node_splits = []
    node_data = df.sample(frac=1).reset_index(drop=True)  # Shuffle the data

    # Calculate the size of each node's data
    node_size = len(df) // num_nodes

    for i in range(num_nodes):
        start = i * node_size
        end = start + node_size if i < num_nodes - 1 else len(df)
        node_subset = node_data[start:end]
        train, test = train_test_split(node_subset, test_size=test_size, random_state=42)
        node_splits.append({
            'train': train,
            'test': test,
            'train_percentage': len(train) / len(node_subset) * 100,
            'test_percentage': len(test) / len(node_subset) * 100
        })
    return node_splits

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# streamlit app
st.title('Data split analysis for ML model training and testing')

# Reset session state
st.sidebar.header("Settings")
if st.sidebar.button("Re-upload Dataset"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# upload dataset
uploaded_file=st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx', 'xls'], key='file_uploader')

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            try:
                df=pd.read_csv(uploaded_file)
            except:
                df=pd.read_csv(uploaded_file,encoding='ISO-8859-1')
        else:
            df=pd.read_excel(uploaded_file)
        st.session_state['df']=df
        st.write(" Data Preview")
        st.write(df.head())
    except Exception as e:
        st.error(f"Error reading the file: {e}")

# ensure the dataframe in session state

if 'df' in st.session_state:
    df=st.session_state['df']
    
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
    st.header("Federated Learning Data Split")
    num_nodes = st.slider('Number of Nodes', min_value=1, max_value=10, value=3, key='federated_num_nodes_slider')
    test_size = st.slider('Test Size (0-1)', 0.0, 0.5, 0.2, key='federated_test_size_slider')
    if st.button("Split Data for Federated Learning"):
        node_splits = federated_split(df, num_nodes, test_size)
        for i, node in enumerate(node_splits):
            st.write(f"Node {i + 1}")
            st.write(f"Training data: {node['train_percentage']:.2f}%")
            st.write(f"Test data: {node['test_percentage']:.2f}%")
            st.write("Training data preview")
            st.write(node['train'].head())
            st.write("Test data preview")
            st.write(node['test'].head())
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
