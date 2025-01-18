from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from load_system_prompt import load_system_prompt
from langchain_community.document_loaders import TextLoader

import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')


load_dotenv()

folder_path= r"/home/danish/Desktop/hf_bot/dataset"


llm = ChatOpenAI(
    model='gpt-4o-mini'
)
model_kwargs = {'device': 'cpu'}
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", model_kwargs=model_kwargs)
vector_db_file_path = "faiss_index_database"


def create_vector_db(folder_path):
    try:
        vectordb = FAISS.load_local(vector_db_file_path, embeddings_model, allow_dangerous_deserialization=True)
        print("Existing vector database loaded.")
    except:
        print("No existing vector database found, creating a new one.")
        vectordb = None

    # Get all files from the input folder
    import os
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Process each file in the folder
    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
#             with open(file_path, "r", encoding="utf-8") as file:
#                 data = file.read()
#             Load and process the file
#             loader = UnstructuredMarkdownLoader(file_path)
#             data = loader.load()
            loader = TextLoader(file_path)
            data = loader.load()

            # Splitting
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,  # chunk size (characters)
                chunk_overlap=200,  # chunk overlap (characters)
                add_start_index=True,  # track index in original document
            )
            all_splits = text_splitter.split_documents(data)
            print(f"Split {file} into {len(all_splits)} sub-documents.")

            if vectordb:
                # Add new documents to the existing vector database
                vectordb.add_documents(all_splits)
            else:
                # Create a new FAISS instance if it doesn't exist yet
                vectordb = FAISS.from_documents(documents=all_splits, embedding=embeddings_model)
                
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")
            continue
    type(vectordb)
    # Save the updated vector database
    vectordb.save_local(vector_db_file_path)
    print("Vector database saved successfully.")


def get_QA_chain():
    
    # Load the vector database from the local folder
    try:
        vectordb = FAISS.load_local(vector_db_file_path, embeddings_model,allow_dangerous_deserialization=True)

        # Create a retriever for querying the vector database
        retriever = vectordb.as_retriever(
                        search_type="similarity_score_threshold", 
                        search_kwargs={
                            "score_threshold": 0.2,
                            "k": 15
                            }
                        )
        system_prompt_string = load_system_prompt()

        system_prompt = (system_prompt_string)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        chain = create_retrieval_chain(retriever, question_answer_chain)
        return chain

    except Exception as e:
        print("Error creating QA chain: ")
        raise


if __name__ == "__main__":
    # create_vector_db(folder_path)
    chain = get_QA_chain()