from langchain_community.chat_models.tongyi import ChatTongyi

from config import setting


class LLMInitializer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMInitializer, cls).__new__(cls)
            cls._instance.llm = None
        return cls._instance

    def get_llm(self):

        api_key = setting.TONGYI_API_KEY

        if self.llm is None:
            self.llm = ChatTongyi(api_key=api_key, max_retries=setting.MAX_RETRIES)
        return self.llm


if __name__ == '__main__':
    llm = LLMInitializer().get_llm()
    llm2 = LLMInitializer().get_llm()

    print(llm is llm2)
