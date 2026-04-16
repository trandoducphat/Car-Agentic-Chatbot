import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.retrievers.registry import get_policy_retriever
from app.config.prompts import POLICY_ANSWER_PROMPT
from app.LLMs.qwen import tokenizer, model
from app.LLMs.qwen3 import qwen3
import torch
from langchain_core.runnables import RunnableLambda


def detect_policy_intent(query: str):
    q = query.lower()

    mapping = {
        "POL-01": ["đặt cọc", "cọc"],
        "POL-02": ["thanh toán", "trả góp"],
        "POL-03": ["giao xe", "bàn giao", "nhận xe"],
        "POL-04": ["bảo hành", "xe mới"],
        "POL-05": ["xe cũ"],
        "POL-06": ["đổi xe", "đổi"],
        "POL-07": ["hủy", "hoàn tiền"],
        "POL-08": ["trách nhiệm", "nghĩa vụ"]
    }

    matched = []
    for code, keywords in mapping.items():
        for kw in keywords:
            if kw in q:
                matched.append(code)
                break

    return matched


def filter_by_policy(docs, policy_codes):
    if not policy_codes:
        return docs

    filtered = [
        d for d in docs
        if any(code in d.get("metadata", {}).get("code", "") for code in policy_codes)
    ]

    return filtered if filtered else docs


def boost_score(doc, query: str):
    q = query.lower()
    content = doc["content"].lower()
    code = doc.get("metadata", {}).get("code", "")

    score = doc["score"]
    bonus = 0.0

    intent_keywords = {
        "POL-01": ["đặt cọc", "cọc", "giữ xe"],
        "POL-02": ["thanh toán", "trả góp", "chuyển khoản"],
        "POL-03": ["giao xe", "bàn giao", "nhận xe"],
        "POL-04": ["bảo hành", "xe mới", "hư hỏng kỹ thuật"],
        "POL-05": ["bảo hành", "xe cũ"],
        "POL-06": ["đổi xe", "đổi", "trả xe"],
        "POL-07": ["hủy", "hoàn tiền", "trả lại tiền"],
        "POL-08": ["trách nhiệm", "nghĩa vụ", "sử dụng sai"]
    }

    for pol, keywords in intent_keywords.items():
        for kw in keywords:
            if kw in q:
                if pol in code:
                    bonus += 0.4
                else:
                    bonus -= 0.2

    for word in q.split():
        if word in content:
            bonus += 0.02 

    if "đổi xe" in q:
        if "POL-06" in code:
            bonus += 0.5
        if "POL-04" in code or "POL-05" in code:
            bonus -= 0.3

    if "bảo hành" in q:
        if "POL-04" in code or "POL-05" in code:
            bonus += 0.4
        if "POL-06" in code:
            bonus -= 0.2

    if "hủy" in q or "hoàn tiền" in q:
        if "POL-07" in code:
            bonus += 0.5

    doc["score"] = max(0.0, score + bonus)
    return doc


def rerank_with_boost(docs, query):
    boosted = []
    for d in docs:
        boosted.append(boost_score(d, query))

    boosted.sort(key=lambda x: x["score"], reverse=True)
    return boosted


def retrieve_policy_docs(state: ChatState) -> ChatState:
    policy_retriver = get_policy_retriever()
    query = state.user_message

    policy_codes = detect_policy_intent(query)

    raw_docs = policy_retriver.retrieve(query, top_k=10, score_threshold=0.0)

    if not raw_docs:
        state.retrieved_docs = []
        return state
    
    filtered_docs = filter_by_policy(raw_docs, policy_codes)

    reranked_docs = rerank_with_boost(filtered_docs, query)

    final_docs = reranked_docs[:3]

    state.retrieved_docs = final_docs
    return state


def build_policy_context(state: ChatState) -> ChatState:
    if not state.retrieved_docs:
        state.policy_context = ""
        return state
    
    blocks = [doc['content'] for doc in state.retrieved_docs]

    state.policy_context = "\n\n---\n\n".join(blocks)
    return state


def generate_policy_answer(state: ChatState) -> ChatState:
    if not state.policy_context:
        state.response = "Xin lỗi, tôi chưa tìm thấy chính sách phù hợp với đề cập của bạn."
        state.history.append(state.response)
        return state
    
    prompt = POLICY_ANSWER_PROMPT.format(
        user_message = state.user_message,
        context = state.policy_context
    )
    response = qwen3.chat_completion(
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    
    state.response = response["choices"][0]["message"]["content"]
    return state
    


retrieve_policy_chain = RunnableLambda(retrieve_policy_docs) | RunnableLambda(build_policy_context) | RunnableLambda(generate_policy_answer)