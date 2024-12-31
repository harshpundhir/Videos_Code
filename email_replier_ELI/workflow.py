import json
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain.docstore.document import Document
from pathlib import Path
from pprint import pprint as pp
from langchain_community.vectorstores import FAISS


os.chdir(os.path.dirname(os.path.abspath(__file__)))

embeddings = OpenAIEmbeddings()

file_path = "emails_100.json"

data = json.loads(Path(file_path).read_text())

documents = [
    Document(
        page_content=entry["Body"],  # Main content for the document
        metadata={
            "From": entry["From"],
            "Email": entry["Email"],
            "Subject": entry["Subject"],
            "Date": entry["Date"]
        }
    )
    for entry in data
]

if not os.path.exists("email_replier_ELI_vs"):
    os.makedirs("email_replier_ELI_vs")
    vs: FAISS = FAISS.from_documents(documents, embeddings)
    vs.save_local("email_replier_ELI_vs")
else:
    vs = FAISS.load_local("email_replier_ELI_vs", embeddings, allow_dangerous_deserialization=True)

pp(vs.similarity_search("linkedin friend", k=3))

