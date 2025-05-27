from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ProcessingEnum
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



class ProcessController(BaseController):

    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_name: str):
        """
        Get the file extension from the file name.
        """
        return os.path.splitext(file_name)[-1]
    
    def get_file_loader(self, file_name: str):
        """
        Get the appropriate file loader based on the file extension.
        """
        file_extension = self.get_file_extension(file_name)
        file_path = os.path.join(self.project_path, file_name)
        if file_extension == '.txt':
            return TextLoader(file_path, encoding='utf-8')
        elif file_extension in ['.pdf']:
            return PyMuPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def get_file_content(self, file_name: str):
        """
        Get the content of the file using the appropriate loader.
        """
        file_loader = self.get_file_loader(file_name=file_name)
        documents = file_loader.load()
        return documents

    def process_file_content(self, file_content: list, file_name: str, chunk_size: int = 100, overlap_size: int = 20):
        """
        Process the file content into chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
        )
        file_content_text = [
            doc.page_content for doc in file_content
        ]
        file_content_metadata = [
            doc.metadata for doc in file_content
        ]
        chunks = text_splitter.create_documents(
            file_content_text,
            metadatas=file_content_metadata  # Corrected from 'metadates' to 'metadatas'
        )

        return chunks