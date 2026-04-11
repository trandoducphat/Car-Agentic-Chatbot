import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
QWEN3_API_KEY = os.getenv("QWEN3_API_KEY")
qwen3 = InferenceClient(
    model="Qwen/Qwen3-235B-A22B-Instruct-2507",
    token=QWEN3_API_KEY
)