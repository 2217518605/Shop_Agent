import os

class Settings:

    # 数据库文件路径
    DB_PATH = 'D:\Code\Agent\Shop_Agent\shop_agent\data\orders.db'

    # JSON 文件路径
    JSON_PATH = os.path.join(os.path.dirname(__file__), "../data/orders.json")

    # 退货正常的文件路径
    DOCS_PATH = os.path.join(os.path.dirname(__file__), "../docs/policy_docs.md")

    # 分割块的大小：
    CHUNK_SIZE = 50

    # 块的 overlap：
    CHUNK_OVERLAP = 0

    # 智谱 AI 的api_key:
    ZHIPUAI_API_KEY = "32cb1399517a4bc6bf87e5b174f60557.3ApH7q0bCxxFHTqq"

    # API_KEY(通义)
    TONGYI_API_KEY = "sk-4774d23219524d1c86c9b68870e89e7c"

    # 智谱的模型：
    ZHIPUAI_MODEL = "glm-4"

    # 智谱的模型温度
    ZHIPUAI_TEMPERATURE = 0.2

    # 嵌入模型：
    ZHIPUAI_EMBEDDING_MODEL = "embedding-2"

    # 持久化数据库路径：
    CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "../chroma_db4")

    # 最大尝试次数
    MAX_RETRIES = 5


setting = Settings()