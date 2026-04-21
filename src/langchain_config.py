"""
LangChain 配置模块
管理 LLM 提供商、API 密钥等配置
"""
import os
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class LangChainConfig:
    """LangChain 配置类"""
    
    # OpenAI 配置
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL: str = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_TEMPERATURE: float = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # Azure OpenAI 配置（可选）
    AZURE_OPENAI_API_KEY: str = os.getenv('AZURE_OPENAI_API_KEY', '')
    AZURE_OPENAI_ENDPOINT: str = os.getenv('AZURE_OPENAI_ENDPOINT', '')
    AZURE_OPENAI_DEPLOYMENT: str = os.getenv('AZURE_OPENAI_DEPLOYMENT', '')
    
    # Anthropic Claude 配置（可选）
    ANTHROPIC_API_KEY: str = os.getenv('ANTHROPIC_API_KEY', '')
    ANTHROPIC_MODEL: str = os.getenv('ANTHROPIC_MODEL', 'claude-2')
    
    # 向量数据库配置
    VECTOR_STORE_TYPE: str = os.getenv('VECTOR_STORE_TYPE', 'chroma')  # chroma, faiss, pinecone
    CHROMA_PERSIST_DIR: str = os.getenv('CHROMA_PERSIST_DIR', './data/chroma_db')
    
    # Embedding 配置
    EMBEDDING_MODEL: str = os.getenv('EMBEDDING_MODEL', 'text-embedding-ada-002')
    
    @classmethod
    def validate_openai_config(cls) -> bool:
        """验证 OpenAI 配置是否完整"""
        return bool(cls.OPENAI_API_KEY)
    
    @classmethod
    def get_openai_config(cls) -> dict:
        """获取 OpenAI 配置字典"""
        return {
            'api_key': cls.OPENAI_API_KEY,
            'model': cls.OPENAI_MODEL,
            'temperature': cls.OPENAI_TEMPERATURE,
        }
