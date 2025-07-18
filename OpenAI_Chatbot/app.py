import os
import json , traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.MCQgenerator import generate_eval_chain
from src.mcqgenerator.logger import logging

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# loading the json response
with open("/workspaces/GenAI-Projects/response.json","r") as file:
    RESPONSE_JSON = json.load(file)

#title of the app
st.title("MCQ Generator App")

#creating a form 
with st.form("User Inputs"):
    #file upload
    uploaded_file = st.file_uploader("Upload a pdf or txt file")

    #input fields
    mcq_count = st.number_input("No. of MCQs" , min_value=5,max_value=50)

    topic = st.text_input("Topic" , max_chars=20)

    tone = st.text_input("Tone of MCQ : Precise or Lenient" , max_chars=20 , placeholder="Simple")

    level = st.text_input("Difficulty level : Easy , Intermediate , Hardcore" , max_chars=20,placeholder="Simple")

    button = st.form_submit_button("Generate MCQ")

    #check if the button is clicked and all the fields have inputs
    if button and uploaded_file is not None and mcq_count and topic and tone and level :
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response = generate_eval_chain(
                        {
                            "text" : text,
                            "number_of_questions":mcq_count,
                            "topic":topic,
                            "level":level,
                            "tone":tone
                        }
                    )
                st.write(response)
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            
            else:
                print(cb) #callback info
                if isinstance(response,dict):
                    #getting the quiz data
                    quiz = response.get("quiz",None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index  = df.index+1
                            st.table(df)
                            #display review in a text box
                            st.text_area(label="Review",value = response["review"])
                        else:
                            st.error("Error in the table data")
                        
                    else:
                        st.write(response)
