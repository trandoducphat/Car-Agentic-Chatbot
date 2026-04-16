import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

import re
from app.intent.base import Intent

RULE_PATTERNS = {
    Intent.CONFIRM_SELECTION: [
        r"\b(chốt|chọn)\b.*(xe|mẫu này)",
        r"\b(tôi chốt|chốt mua)\b",
    ],
    Intent.COMPARE_CARS:[
        r"\b(so sánh)"
    ],
    Intent.ASK_POLICY: [
        r"\b(chính sách|điều khoản)"
    ],
    Intent.GOODBYE: [
        r"\b(cảm ơn|bye|tạm biệt)\b",
    ],
}


def detect_rule_intent(text: str) -> Intent | None:
    text = text.lower()

    for intent, patterns in RULE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return intent
    
    return None