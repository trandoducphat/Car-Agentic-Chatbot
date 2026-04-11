from app.embeddings.embedding_manager import PROD_DOCS, POL_DOCS, EmbeddingManager
from app.config.settings import EMBEDDINGS_DIR, DATA_DIR
from app.retrievers.vector_store import VectorStore
from app.retrievers.retriever import RAGRetriever
import os
from app.intent.base import Intent
from app.intent.intent_router import dectect_intent
from app.graph.state import ChatState
from app.embeddings.build_vector_store import load_all_collections
from app.retrievers.registry import init_retrievers, get_policy_retriever, get_product_retriever
from app.graph.nodes.retrieve_policy import retrieve_policy_node
from app.graph.nodes.retrieve_product import retrieve_product_node
from app.graph.nodes.retrieve_info import retrieve_info_node
from app.intent.intent_router import dectect_intent
from app.graph.graph_builder import build_graph

def main():
    embedding_manager = EmbeddingManager()
    policy_store = VectorStore("policy")
    product_store = VectorStore("product")

    if policy_store.collection.count() == 0 or product_store.collection.count() == 0:
        load_all_collections()
    
    policy_retriever = RAGRetriever(policy_store, embedding_manager)
    product_retriever = RAGRetriever(product_store, embedding_manager)

    init_retrievers(policy_retriever=policy_retriever, product_retriever=product_retriever)

def test1():
    s1 = ChatState("tôi muốn hỏi về chính sách đổi trả của công ty mình", None, [], "", [], [], "", "")
    print(dectect_intent(s1).intent)
    print("---------")
    s2 = ChatState("bình xăng của xe Toyota Vios là bao nhiêu lít", None, [], "", [], [], "", "")
    print(dectect_intent(s2).intent)
    print("---------")
    s3 = ChatState("tôi muốn biết xe VinFast VF9 dùng động cơ gì", None, [], "", [], [], "", "")
    print(dectect_intent(s3).intent)
    print("---------")
    s4 = ChatState("so sánh sự khác nhau giữa VF9 và Land Cruiser là gì", None, [], "", [], [], "", "")
    print(dectect_intent(s4).intent)


def test2():
    print("------Testing Embeddings and Vector Store------")
    pol_retriever =  get_policy_retriever()
    prod_retriever = get_product_retriever()
    print(pol_retriever.retrieve("chính sách đổi trả", 1))
    print("------")
    print(prod_retriever.retrieve("tôi đang thắc mắc về số chỗ ngồi của xe Toyota Vios", 1, 0.0))
    print("------")
    print(prod_retriever.retrieve("xe, chỗ ngồi, động cơ MG dòng ZS", 1, 0.0))


def test3():
    build_graph()
    s1 = ChatState("Tôi muốn chốt con xe này", None, [], "", [], [], "", "")
    graph = build_graph()
    s1 = graph.invoke(s1)
    print(s1["response"])
    print("-------")
    s2 = ChatState("Sự khác biệt giữa VF9 và Vios", None, [], "", [], [], "", "")
    graph = build_graph()
    s2 = graph.invoke(s2)
    print(s2["response"])
    print("-------")
    s3 = ChatState("Tôi đang cần xe điện, phân khúc suv e, tầm giá dưới 2 tỷ", None, [], "", [], [], "", "")
    graph = build_graph()
    s3 = graph.invoke(s3)
    print(s3["response"])


############Testing node###################


def test4():
    print("Testing Policy node")
    test_policy_state1 = ChatState("tôi muốn hỏi về chính sách đổi trả của công ty mình", Intent.ASK_POLICY, [], "", [], [], "", "")
    test_policy_state1 = retrieve_policy_node(test_policy_state1)
    print("1: Chính sách đổi trả: ",test_policy_state1.response)

    test_policy_state2 = ChatState("tôi muốn hỏi về các điều khoản đặt cọc và giao dịch của công ty", Intent.ASK_POLICY, [], "", [], [], "", "")
    test_policy_state2 = retrieve_policy_node(test_policy_state2)
    print("2: Điều khoản đặt cọc: ",test_policy_state2.response)

    test_policy_state3 = ChatState("vậy về chính sách giao xe và hồ sơ của công ty thì như thế nào?", Intent.ASK_POLICY, [], "", [], [], "", "")
    test_policy_state3 = retrieve_policy_node(test_policy_state3)
    print("3: Giao xe và hồ sơ: ",test_policy_state3.response)


def test5():
    test_compare_state = ChatState("tôi phân vân giữa xe Toyota Vios  và Land Cruiser Prado", Intent.COMPARE_CARS, [], "", [], [], "", "")
    test_compare_state = retrieve_product_node(test_compare_state)
    print(test_compare_state.response)

def test6():
    test_info_state = ChatState("tôi đang thắc mắc về số chỗ ngồi và nhiên liệu của xe Toyota Land Cruiser Prado và Toyota Vios", Intent.ASK_CAR_INFO, [], "", [], [], "", "")
    test_info_state = retrieve_info_node(test_info_state)
    print(test_info_state.response)
    print("------------")
    test_info_state.user_message = "tôi muốn biết thêm về hãng, đời xe, và nhiên liệu sử dụng của Toyota Vios"
    print(retrieve_info_node(test_info_state).response)

def test7():
    ...



if __name__ == "__main__":
    main()
    # test1()
    # test2()
    test3()
    # test4()
    # test5()
    # test6()