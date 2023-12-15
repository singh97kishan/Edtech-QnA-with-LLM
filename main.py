import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ['GOOGLE_API_KEY']

from langchain.llms import GooglePalm
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import FewShotPromptTemplate
from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.chains import RetrievalQA


llm= GooglePalm(api_key = api_key, temperature=0.1)

instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
vectordb_filepath = 'faiss_index'

def create_vector_db():
    loader = CSVLoader(file_path= 'faqs_data.csv', source_column='query')
    data = loader.load()
    vectordb = FAISS.from_documents(documents= data, embedding= instructor_embeddings)
    vectordb.save_local(vectordb_filepath)

def get_qa_chain():
    vectordb = FAISS.load_local(vectordb_filepath, instructor_embeddings)
    retriever = vectordb.as_retriever()
    prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}"""

    PROMPT = PromptTemplate(
        template = prompt_template, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT}
    chain = RetrievalQA.from_chain_type(llm=llm,
                            chain_type="stuff",
                            retriever=retriever,
                            input_key="query",
                            return_source_documents=True,
                            chain_type_kwargs=chain_type_kwargs)
    
    return chain

if __name__=="__main__":
    #create_vector_db()
    pass
