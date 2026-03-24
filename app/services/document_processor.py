import fitz  # PyMuPDF
from typing import List
from app.models.schemas import SourceChunk

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def process_pdf(self, file_content: bytes, doc_id: str) -> List[SourceChunk]:
        """
        Extract text from a PDF document and split it into chunks.
        """
        doc = fitz.open(stream=file_content, filetype="pdf")
        chunks = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            if not text.strip():
                continue
                
            # Basic chunking by character count
            start = 0
            while start < len(text):
                end = start + self.chunk_size
                chunk_text = text[start:end]
                if chunk_text.strip():
                    chunks.append(SourceChunk(
                        doc_id=doc_id,
                        page_number=page_num + 1,
                        text=chunk_text.strip()
                    ))
                start += (self.chunk_size - self.overlap)
                
        return chunks

document_processor = DocumentProcessor()
