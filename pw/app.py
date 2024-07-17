import streamlit as st 

# setting title of the page
st.set_page_config(page_title="Atshaya Srinivasan - Personal Website", layout="Wide")


# sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.write("Use the links below to navigate the site")
st.sidebar.markdown("[Projects](#projects)")
st.sidebar.markdown("[Technical Blog](#technical-blog)")
st.sidebar.markdown("[Linkedin](#linkedin)")
st.sidebar.markdown("[Contact Me](#contact-me)")


# main content
st.title("Greetings!")
st.write("Welcome to my personal website")

#About me section
st.header("About me")
st.write("""Hello! My name is Atshaya Srinivasan. I am a graduate data scientist with a passion for doing research and deliver a profitable insights.
With a strong background in Data Science and Artificial Intelligence, I have been working on various projects that involve using python, snowflake, machine learning models. 
I enjoy solving complex problems and learning new technologies. When I'm not working, I love to listen investigation movie stories.
Feel free to explore my projects and read my technical blog to know more about my work. Connect with me on LinkedIn or contact me if you would like to collaborate or just have a chat!""")

# project section
st.header("Projects")
st.write("Here you can find my recent projects. click on the link below to my repositories")

#project1
with st.container():
    st.subheader("Project 1: Train and Test dataset split tool")
    st.write("""
Description: This project is about randomly splitting a provided dataset into training and testing dataset for a single model and federated learning model
Technologies used: Python, Streamlit, Pandas
Github repository: [view on Github](https://github.com/AtshayaSrinivasan47/Streamlit/tree/main/Data_Splitting_application)""")

#Technical Blog section
st.header("Technical_Blog")
st.write("Welcome to my technical blog. Here are my some of my latest post")

#Blogposts
blog_posts=[
    {
        "title":"Common mistake we do in data preprocessing",
        "description": "A discussion on the mistakes overcome while doing classification analysis on Drug Persistent project",
        "link":"https://medium.com/@atshayarakshanaa/common-mistake-we-do-in-data-preprocessing-757f6098ed71"
    },
    {
        "title":"Unleash the power of Data Augmentation for your Machine Learning Model with real world example",
        "description":" A discussion on data augmentation techniques",
        "link":"https://medium.com/@atshayarakshanaa/unleash-the-power-of-data-augmentation-for-your-machine-learning-model-with-real-world-example-72a09df6ae85"
    }
]
for posts in blog_posts:
    with st.container():
        st.subheader(posts["title"])
        st.write(posts["description"])
        st.markdown(f"[Read more]({posts["link"]})")

# Linkedin section
st.header("Linkedin")
st.write("""connect with me on Linkedin[Linkedin](https://www.linkedin.com/in/atshaya/)""")
