import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
import tempfile

# Initialize Streamlit session state variables
if 'initialized' not in st.session_state:
    st.session_state.update({
        'initialized': True,
        'results': [],
        'questions': []
    })

# Streamlit configuration
st.title("QA Interface for PDF Documents")
st.write("Upload a PDF file, choose the model, and submit your questions.")

# Select embedding model and GPT model
model_name = st.selectbox("Choose a Hugging Face model", ["sentence-transformers/all-MiniLM-L6-v2", "sentence-transformers/all-MiniLM-L12-v2"])
gpt_model = st.selectbox("Choose a LLM model", ["llama3", "phi3", "gemma2"])
temperature = st.slider("Adjust the temperature", 0.0, 1.0, 0.3)

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Process the uploaded file
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_file_path = tmp_file.name

    with st.spinner('Loading the document...'):
        loader = UnstructuredFileLoader(temp_file_path)
        documents = loader.load()

    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=3000, chunk_overlap=200)
    text_chunks = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    knowledge_base = FAISS.from_documents(text_chunks, embeddings)
    st.success("Knowledge base ready.")

    llm = ChatOpenAI(base_url="http://localhost:11434/v1", temperature=temperature, api_key="not-needed", model_name=gpt_model)
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=knowledge_base.as_retriever())
 
    st.session_state.questions = st.text_area("Enter questions (one per line)").split('\n')

    if st.button("Get Answers"):
        st.session_state.results = []
        with st.spinner('Processing answers...'):
            for question in st.session_state.questions:
                if question.strip():
                    response = qa_chain.invoke({"query": question.strip()})
                    st.session_state.results.append((question.strip(), response["result"]))
        for question, result in st.session_state.results:
            st.write(f"**Question:** {question}")
            st.write(f"**Answer:** {result}")

# Handle saving results to a file and create a download button
filename = st.text_input("Filename to save answers:", "results.txt")
if st.button("Save answers to file"):
    if st.session_state.results:
        with open(filename, "w") as file:
            for i, (question, result) in enumerate(st.session_state.results):
                file.write(f"Question {i + 1}:\n{question}\n")
                file.write(f"Answer {i + 1}:\n{result}\n\n")

        # After saving the results, show a download button
        with open(filename, "rb") as f:
            st.download_button(
                label="Download results",
                data=f,
                file_name=filename,
                mime="text/plain"
            )
        st.success(f"Results saved in {filename}")
    else:
        st.error("No results to save.")
