import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.intent.base import Intent
# from app.intent.llm_intent import llm_detect_intent
from app.intent.llm_intent import intent_and_product_detector
from app.intent.rule_intent import detect_rule_intent
from app.graph.state import ChatState
from app.embeddings.embedding_manager import PROD_IDX

def dectect_intent(state: ChatState) -> ChatState:
    rule_intent = detect_rule_intent(state.user_message)
    if rule_intent:
        state.intent = rule_intent
        return state

    intent_and_product_response = intent_and_product_detector(state.user_message)
    state.intent = Intent(intent_and_product_response["intent"])
    suitable_prods = [(PROD_IDX.get(p) if PROD_IDX.get(p) is not None else None) for p in intent_and_product_response["product"]]

    if len(suitable_prods) == 0:
        return state
    elif len(suitable_prods) == 1:
        state.selected_car = suitable_prods[0]
        return state
    else:
        state.compared_car = suitable_prods
        return state
