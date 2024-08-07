
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

st.write("""
# Penguin species Prediction app

This app predicts the ***Penguin species***

Data obtained from DataProfessor Github data repository(https://github.com/dataprofessor/data/blob/master/penguins_cleaned.csv)

"""
)

st.sidebar.header('User Input Features')
st.sidebar.markdown(
    """
    Example CSV input file(https://github.com/dataprofessor/data/blob/master/penguins_example.csv)
    """
)

# collecting user input feature into dataframe

uploaded_file=st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
  input_df=pd.read_csv(uploaded_file)
else:
  def user_input_features():
    island=st.sidebar.selectbox('island',('Biscoe','Dream','Torgersen'))
    sex=st.sidebar.selectbox('sex',('male','female'))
    bill_length_mm=st.sidebar.number_input('Bill length (mm)',32.1,59.6,43.9)
    bill_depth_mm=st.sidebar.number_input('Bill depth (mm)', 13.1,21.5,17.2)
    flipper_length=st.sidebar.number_input('flipper length (mm)', 172.0,231.0,201.0 )
    body_mass_g=st.sidebar.number_input('body_mass (g)', 2700.0,6300.0,4207.0)
    data={'island':island,
          'bill_length':bill_length_mm,
          'bill_depth_mm':bill_depth_mm,
          'flipper_length':flipper_length,
          'body_mass':body_mass_g,
          'sex':sex}
    user_df=pd.DataFrame(data,index=[0])
    return user_df
  input_df=user_input_features()

# Ensure input_df has the correct columns
input_df.columns = ['island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex']

# Combining input features with entire penguin dataset
penguins_raw = pd.read_csv('penguins_cleaned.csv')
penguins_raw = penguins_raw[['island', 'bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex']]
df = pd.concat([input_df, penguins_raw], axis=0)

le = LabelEncoder()
df['island'] = le.fit_transform(df['island'])
df['sex'] = le.fit_transform(df['sex'])

df = df[:1]  # Selects only the user input

# displaying the user input features
st.subheader(' User Input Feature')

if uploaded_file is not None:
  st.write(df)
else:
  st.write('Awaiting CSV file to be uploaded. Currently using manual example parameters')
  st.write(df)

# Reads in saved classification model 
load_model=pickle.load(open('penguins_classification.pkl','rb'))

prediction=load_model.predict(df)
prediction_prob=load_model.predict_proba(df)

st.subheader('prediction')
st.write(prediction)

st.subheader('prediction_Probability')
st.write(prediction_prob)
  