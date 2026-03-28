from models.rag import RAGSystem
from langchain.tools import tool

rag = RAGSystem()

@tool(description="查询知识库，回答用户问题，当用户问退货政策与优惠规则时，可以调用此工具")
def query_knowledge(question: str):
    """
    查询知识库，回答用户问题
   当用户问退货政策与优惠规则时，可以调用此工具
   :param question: 用户问题
   :return: 回答
    """

    if not question:
        return "请提供一个问题"

    # 使用 RAG 系统回答问题：
    result = rag.qa_chain.invoke({"input": question})
    return result["answer"] if result else "我目前还不会这个哦，请您找我们的人工客服哦！"
