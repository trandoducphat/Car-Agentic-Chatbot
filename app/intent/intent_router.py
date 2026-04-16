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
    # rule_intent = detect_rule_intent(state.user_message)
    # if rule_intent:
    #     state.intent = rule_intent
    #     return state

    intent_and_product_response = intent_and_product_detector(state.user_message)
    state.intent = Intent(intent_and_product_response["intent"])
    suitable_prods = []
    for i in intent_and_product_response["product"]:
        for name, doc in PROD_IDX.items():
            if i.lower() in name.lower():
                suitable_prods.append(doc)
                break

    if not suitable_prods:
        return state
    if len(suitable_prods) == 1:
        state.selected_car = suitable_prods[0]
    else:
        state.compared_car = suitable_prods
    return state
