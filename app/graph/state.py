import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.intent.base import Intent
from dataclasses import dataclass, field
from langchain_core.documents.base import Document

@dataclass
class ChatState:
    user_message: str

    intent: Intent | None = None

    history: list[str] = field(default_factory=list)

    selected_car: Document | None = None

    compared_car: list[Document] = field(default_factory=list)

    retrieved_docs: list[dict] = field(default_factory=list)

    policy_context: str = ""

    response: str = ""