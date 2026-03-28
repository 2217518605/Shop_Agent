import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain

from models.llm import LLMInitializer
from config import setting

class RAGSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.qa_chain = None
            cls._instance.initialize()

        return cls._instance

    def initialize(self):

        if self.qa_chain is not None:
            return self.qa_chain

        # 加载数据
        DOC_PATH = setting.DOCS_PATH

        # 收集数据
        loader = TextLoader(DOC_PATH, encoding='utf-8')
        document = loader.load()

        # 分割数据：
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=setting.CHUNK_SIZE,  # 适合中文段落，段落大小
            chunk_overlap=setting.CHUNK_OVERLAP,  # 避免上下文缺失
            separators=["\n\n", "\n", "(?<=\. )", " ", ""]
        )
        splits = text_splitter.split_documents(document)

        # 选择文本嵌入模型
        os.environ["ZHIPUAI_API_KEY"] = setting.ZHIPUAI_API_KEY

        chat = ChatZhipuAI(model=setting.ZHIPUAI_MODEL, temperature=setting.ZHIPUAI_TEMPERATURE)
        embeddings = ZhipuAIEmbeddings(model=setting.ZHIPUAI_EMBEDDING_MODEL)

        # 初始化向量数据库
        # 创建向量数据库
        db = Chroma.from_documents(documents=splits,
                                   embedding=embeddings,
                                   persist_directory=setting.CHROMA_DB_PATH)

        # 创建提示词模板
        rag_prompt_template = '''
             你是一个专业的电商客服助手，根据以下商品政策信息，用自然友好的对话风格回答用户问题，就像在聊天一样。
             
             已知信息:
             {context} # 检索出来的原始文档
             
             用户问题:
             {input} # 用户的问题
             如果已知信息中不包含用户问题的答案，或者已知信息无法回答用户问题，请直接返回"这个问题暂时我还不会。您可以联系人工客服"。
             请不要输出已知信息中不包含的信息或者答案。
             请用中文回答用户问题。
             '''

        rag_prompt = PromptTemplate(
            template=rag_prompt_template,
            input_variables=["context", "input"]
        )

        # 获取 LLM：
        llm = LLMInitializer().get_llm()

        combine_docs_chain = create_stuff_documents_chain(llm, rag_prompt)
        self.qa_chain = create_retrieval_chain(db.as_retriever(), combine_docs_chain)
        return self.qa_chain

    def get_chain(self):
        return self.qa_chain
