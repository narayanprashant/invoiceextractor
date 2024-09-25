from dotenv import load_dotenv
load_dotenv()##load all the environment variable from .env

import streamlit as st
import os 
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##function to load Gemini Pro Vision
model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input,image,prompt): ##prompt is what message i want
    response= model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data=uploaded_file.getvalue()
        image_part=[
            {
                "mime_tpye":uploaded_file.type, #get the mine type of the 
                "data":bytes_data
            }
        ]
        return image_part
    else:
        raise FileNotFoundError("No File Uploaded")
##initialize our streamlit app

st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("MultiLanguage Invoice Extractor")
input=st.text_input("Input Prompt: ", key="input")
uploaded_file= st.file_uploader("Choose an image of the invoice....",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image",use_column_width=True)
    
submit=st.button("Tell me about the image")

input_prompt=""""
You are an expert in understanding invoice.
"""

if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is ")
    st.write(response)
    