from langchain_core.documents import Document
import json
from pathlib import Path
import re
from typing import List

class JSONLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
    
    def load(self) -> list[Document]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        documents = []
        for item in data:
            content = item.get("description", "")
            metadata = {k: v for k, v in item.items() if k != "description"}
            documents.append(Document(page_content=content, metadata=metadata))
        
        return documents


def load_policy_as_documents(file_path: str) -> List[Document]:
    """
    Đọc file txt chính sách và trả về list[Document].
    Mỗi điều khoản POL-XX thành 1 Document.
    """
    documents = []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    clauses = re.split(r"(POL-\d{2}:)", content)

    for i in range(1, len(clauses), 2):
        code = clauses[i].strip()   
        text = clauses[i+1].strip()   
        full_text = f"{code} {text}"    

        documents.append(
            Document(
                page_content=full_text,
                metadata={
                    "code": code,
                    "source": str(file_path)
                }
            )
        )

    return documents