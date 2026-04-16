import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.retrievers.registry import get_product_retriever
from langchain_core.runnables import RunnableLambda

def retrieve_products_docs(state: ChatState) -> ChatState:
    if len(state.compared_car)>=2:
        return state
    product_retriver = get_product_retriever()
    retrieved_products = product_retriver.retrieve(state.user_message, 2, 0.0)

    state.compared_car = retrieved_products
    return state

def normalize_product(p):
    if hasattr(p, "metadata") and isinstance(p.metadata, dict):
        return p.metadata

    if isinstance(p, dict) and "metadata" in p and isinstance(p["metadata"], dict):
        return p["metadata"]

    if isinstance(p, dict):
        return p



def build_compare_table(state: ChatState) -> ChatState:
    if not state.compared_car or len(state.compared_car) < 2:
        state.response = "Tôi chưa xác định được 2 sản phẩm mà bạn đang so sánh. Vui lòng mô tả rõ nhất về thông tin (tên hãng + tên mẫu) của sản phẩm mà bạn đang muốn nói đến."

    products = [normalize_product(p) for p in state.compared_car]

    # lấy tất cả field union
    fields = sorted(set().union(*[p.keys() for p in products]))

    # tạo title từng sản phẩm
    def get_title(p: dict) -> str:
        brand = str(p.get("brand", ""))
        model = str(p.get("model", ""))
        title = f"{brand} {model}".strip()
        return title if title else "Sản phẩm"

    titles = [get_title(p) for p in products]

    # width cho cột thông số
    col_widths = []

    # cột 0: tên field
    col0_width = max(len("Thông số"), *(len(f) for f in fields))

    # các cột sản phẩm
    for i, p in enumerate(products):
        col_widths.append(
            max(len(titles[i]), *(len(str(p.get(f, ""))) for f in fields))
        )

    def line():
        return "+" + "+".join(["-" * (col0_width + 2)] +
                              ["-" * (w + 2) for w in col_widths]) + "+"

    rows = []

    # header
    rows.append(line())

    header = "| " + "Thông số".ljust(col0_width) + " |"
    for i, t in enumerate(titles):
        header += " " + t.ljust(col_widths[i]) + " |"
    rows.append(header)

    rows.append(line())

    # data rows
    for f in fields:
        row = "| " + f.ljust(col0_width) + " |"
        for i, p in enumerate(products):
            row += " " + str(p.get(f, "")).ljust(col_widths[i]) + " |"
        rows.append(row)

    rows.append(line())

    compare_table = "\n".join(rows)

    state.response = (
        f"Đây là bảng so sánh thông số giữa {len(products)} sản phẩm:\n"
        f"{compare_table}"
    )
    state.compared_car = []
    return state


retrieve_products_chain = RunnableLambda(retrieve_products_docs) | RunnableLambda(build_compare_table)