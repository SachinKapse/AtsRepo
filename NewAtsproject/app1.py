import streamlit as st
import google.generativeai as genai
import docx2txt
import PyPDF2 as pdf


key="AIzaSyDvOX2z2D7zrt5o_iEYuh_FUYEfYCqqwlk"
#Confoigure the generative ai model with the google api key
genai.configure(api_key=key)
print("2")
#set up the model configuration for text generation
generation_config={
        "temperature":0,
        "top_p":1,
        "top_k":32,
        "max_output_tokens":4096,
} 
#Define safety setting for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]
print("3")
#create the model
def generate_response_from_gemini(input_text):
    print(" i am in side : generate_response_from_gemini")
    #Create a generativeModel instance with 'gemini pro' as the model type
    llm=genai.GenerativeModel(
    model_name='gemini-1.5-flash',  #GenerativeModel('gemini-1.5-flash')
    generation_config=generation_config,
    safety_settings=safety_settings,
    )
    #generate content based on the inpyt text
    output=llm.generate_content(input_text)
    #return the generated text 
    print("theis is output of llm gemini: \n")
    output_mr_pande=output.text
    print(output.text)
    return output.text
print("4")

def extract_text_from_pdf_file(uploaded_file):
    # use pdfreader to read the text content from a PDF file
    print(" i am in side : extract_text_from_pdf_file")
    pdf_reader=pdf.PdfReader(uploaded_file)
    text_content=""
    for page in pdf_reader.pages:
        text_content +=str(page.extract_text())
                        #Locate all text drawing commands, in the order they are provided in the content stream, and extract the text.

    return text_content
print("5")

def extract_text_from_docx_file(uploaded_file):
    print(" i am in side : extract_text_from_docx_file")
    return docx2txt.process(uploaded_file)

# Prompt Template
input_prompt_template = """
As an experienced Applicant Tracking System (ATS) analyst,
with profound knowledge in technology, software engineering, data science, 
and big data engineering, your role involves evaluating resumes against job descriptions.
Recognizing the competitive job market, provide top-notch assistance for resume improvement.
Your goal is to analyze the resume against the given job description, 
assign a percentage match based on key criteria, and pinpoint missing keywords accurately.
resume:{text}
description:{job_description}
I want the response in one single string having the structure
{{"Job Description Match":"%","Missing Keywords":"","Candidate Summary":"","Experience":""}}
"""

print("6")
#Streamlit app
#initialize streamlit app
st.title("Intelligent ATS-Enhance your Resume")
st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
job_description = st.text_area("Paste the Job Description",height=300)
uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], help="Please upload a PDF or DOCX file")

submit_button =st.button("submit")

if submit_button:
    if uploaded_file is None:
        if uploaded_file.type=="application/pdf":
            resume_text = extract_text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx_file(uploaded_file)
        response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))
 # Extract Job Description Match percentage from the response
        match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0]

        # Remove percentage symbol and convert to float
        match_percentage = float(match_percentage_str.rstrip('%'))
        
        st.subheader("ATS Evaluation Result:")
        st.write(response_text)
        st.write(f'{{\n"Job Description Match": "{match_percentage}%",\n"Missing Keywords": "",\n"Candidate Summary": "",\n"Experience": ""\n}}')

        # Display message based on Job Description Match percentage
        if match_percentage >= 80:
            st.text("Move forward with hiring")
        else:
            st.text("Not a Match")

