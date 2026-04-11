import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.intent.base import Intent
from app.config.prompts import INTENT_PROMPT, INTENT_AND_PRODUCT_PROMPT
# from app.LLMs.qwen import model, tokenizer
from app.LLMs.qwen3 import qwen3
import json
# import torch

###USING MINI QWEN LOADED MODEL
# def llm_detect_intent(user_message: str, state: str, selected_car: str | None) -> Intent:
#     prompt = INTENT_PROMPT.format(
#         state = state,
#         selected_car = selected_car or "None",
#         user_message = user_message
#     )
#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
#     with torch.no_grad():
#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=100,
#             temperature=None,
#             do_sample=False,
#             pad_token_id=tokenizer.eos_token_id
#         )

#     decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     answer = decoded[len(prompt):].strip().lower()
#     allowed = ['GREETING', 'ASK_RECOMMENDATION', 'ASK_CAR_INFO', 'FILTER_BY_PRICE', 'FILTER_BY_BRAND', 'COMPARE_CARS', 'CONFIRM_SELECTION', 'ASK_POLICY', 'GOODBYE', 'UNKNOWN']

#     for a in allowed:
#         if a.lower() in answer:
#             return Intent(a)
#     return Intent.UNKNOWN


###USING QWEN3's API
def intent_and_product_detector(user_message: str):
    prompt = INTENT_AND_PRODUCT_PROMPT.format(
        user_message=user_message
    )
    response = qwen3.chat_completion(
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )

    response = json.loads(response["choices"][0]["message"]["content"])
    return response