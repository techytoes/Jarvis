import os

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import GoogleDriveLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from drive import get_file_id_list

# folder_id = "19OW4fYgnz3vuv4TZGSIyan7ScW4wUtXB"
file_ids = get_file_id_list()
loader = GoogleDriveLoader(
    # folder_id=folder_id,
    file_ids=file_ids,
    recursive=True
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000, chunk_overlap=0, separators=[" ", ",", "\n"]
    )

texts = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(texts, embeddings)
retriever = db.as_retriever()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="refine", retriever=retriever)

while True:
    query = input("> ")
    result = qa.run(query=query)
    print("Result:")
    print(result)