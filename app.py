import os
from time import sleep
from constants import OPEN_AI

import streamlit as st
# from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain



from langchain_openai import OpenAI

os.environ['OPENAI_API_KEY'] = OPEN_AI

can_downlaod = False
st.title('Call Anaylsis Tool')
# prompt = st.text_input('Enter a prompt', '')

#include a file uplaoderr
file_uploader = st.file_uploader("Upload a call log file", type=["csv", "txt"])
if file_uploader is not None:
    # To read file as string:
    string_data = file_uploader.getvalue()
    # st.write(string_data)
    # Can be used wherever a string is needed.

# Prompt templates

default_prompt_template = PromptTemplate(input_variables=['prompt'], template="""Give a sentiment analysis on each entry in a call log. 
                                         We are focusing on the clients conversation, duration and sentiment. 
                                         
                                         Give the clients name in the data .csv file
                                         \n\n
                                        ---
                                         
                                         
                                         Example result:
                                         Client Full Name: John Murphy\n
                                         Duration: 12 minutes\n
                                         Sentiment: Happy\n
                                         Extract: "some text from the conversation in that 'converstation text''"\n
                                         
                                         Only use the data that has been supplied. Do not use external data. Do not make up data.
                                         ----
                                         Data .csv file:
                                         {prompt}
                                         -----

                                         Formate output into a csv file format.

                                         continue;
                                         """)

title_template = PromptTemplate(
    input_variables = ['topic'],
    template="Research {topic} and write summary about it, add a new line. Following the summary generate 4 questions and answers on the {topic}.",
)




script_template = PromptTemplate(
    input_variables = ['title'],
    template="Generate 4 questions and answers on the {title}. include mathematics if possible.",
)

# Llms
llm = OpenAI(temperature=0.1, openai_api_key=OPEN_AI, model="gpt-3.5-turbo-instruct", max_tokens=2000)
default_chain = LLMChain(llm=llm, prompt=default_prompt_template, verbose=True)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True)

# join chains
sequential_chain = SimpleSequentialChain(chains=[default_chain], verbose=True)




# add button to run query
if st.button('Run'):


    st.write("Processing...")

    # add progress bar
    my_bar = st.progress(10)
    response = sequential_chain.run(string_data)

    for percent_complete in range(100):
        sleep(0.1)
        my_bar.progress(percent_complete + 1)


    st.write("Complete.")

    # save response to csv file
    with open("call_analysis.csv", 'w') as f:
        f.write(response)
    can_downlaod = True
    


if(can_downlaod and response is not None):
    st.markdown("### Download File")
    st.markdown("Download your file here")

    # download a file from path = "call_analysis.csv"
    st.download_button(
        label="Download call_analysis.csv",
        data=response,
        file_name="call_analysis.csv",
        mime="text/csv",
    )

