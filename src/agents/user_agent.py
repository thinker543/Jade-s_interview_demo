"""
用户管理 Agent
使用 LangChain Agent 进行智能用户管理
"""
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from src.tools.user_tools import create_user_tools
from src.services.user_service import UserService
from src.langchain_config import LangChainConfig


def create_user_management_agent(user_service: UserService):
    """
    创建用户管理 Agent
    
    Args:
        user_service: 用户服务实例
        
    Returns:
        配置好的 Agent
    """
    # 检查配置
    if not LangChainConfig.validate_openai_config():
        raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY in .env file")
    
    # 初始化 LLM
    llm = ChatOpenAI(
        model=LangChainConfig.OPENAI_MODEL,
        temperature=LangChainConfig.OPENAI_TEMPERATURE,
        openai_api_key=LangChainConfig.OPENAI_API_KEY
    )
    
    # 创建工具
    tools = create_user_tools(user_service)
    
    # 初始化 Agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent


class UserManagementAssistant:
    """用户管理助手类"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.agent = None
        self._initialized = False
    
    def initialize(self):
        """初始化 Agent"""
        if not self._initialized:
            self.agent = create_user_management_agent(self.user_service)
            self._initialized = True
    
    def query(self, question: str) -> str:
        """
        向助手提问
        
        Args:
            question: 用户的问题
            
        Returns:
            助手的回答
        """
        if not self._initialized:
            self.initialize()
        
        try:
            result = self.agent.run(question)
            return result
        except Exception as e:
            return f"处理问题时出错: {str(e)}"
    
    async def aquery(self, question: str) -> str:
        """
        异步向助手提问
        
        Args:
            question: 用户的问题
            
        Returns:
            助手的回答
        """
        if not self._initialized:
            self.initialize()
        
        try:
            result = await self.agent.arun(question)
            return result
        except Exception as e:
            return f"处理问题时出错: {str(e)}"
