import dotenv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

EMAILS_CSV_PATH = "data/emails.csv"
EMAILS_CHROMA_PATH = "chroma_data"

dotenv.load_dotenv()

loader = CSVLoader(file_path=EMAILS_CSV_PATH, source_column="Content")
emails = loader.load()

emails_vector_db = Chroma.from_documents(
    emails, OpenAIEmbeddings(), persist_directory=EMAILS_CHROMA_PATH
)
