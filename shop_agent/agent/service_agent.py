from langchain.agents import create_agent

from models.llm import LLMInitializer
from tools.order_tools import get_order_status, return_order, complain_order
from tools.knowledge_tools import query_knowledge



class ServiceAgent:
    def __init__(self):
        # 初始化LLM
        self.llm = LLMInitializer().get_llm()
        # 初始化工具类
        self.tools = [
            get_order_status,
            return_order,
            complain_order,
            query_knowledge
        ]
        # 初始化代理对象
        self.agent_executor = self._create_agent_executor()

    def _create_agent_executor(self):
        '''
         返回代理对象
         '''
        agent_executor = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt="你是电商平台客服助手，优先调用工具获取订单信息并用简洁中文回复。",
            debug = True
        )
        return agent_executor

    def chat(self, user_input: str):
        resp = self.agent_executor.invoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        messages = resp.get("messages", [])
        if not messages:
            return ""
        last_message = messages[-1]
        if hasattr(last_message, "content"):
            return last_message.content
        if isinstance(last_message, dict):
            return last_message.get("content", "")
        return str(last_message)


customer_service_agent = ServiceAgent()
