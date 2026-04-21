"""
用户管理工具
提供对用户服务的工具化访问
"""
from langchain.tools import BaseTool
from typing import Optional
from src.services.user_service import UserService


class UserSearchTool(BaseTool):
    """用户搜索工具"""
    
    name = "user_search"
    description = "搜索用户，按用户名或邮箱查找。输入应该是搜索关键词。"
    user_service: UserService = None
    
    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service
    
    def _run(self, query: str) -> str:
        """执行用户搜索"""
        try:
            users = self.user_service.search_users(query)
            if not users:
                return f"未找到包含 '{query}' 的用户"
            
            result = f"找到 {len(users)} 个用户:\n"
            for user in users:
                result += f"- {user.username} ({user.email}), 年龄: {user.age}\n"
            return result
        except Exception as e:
            return f"搜索失败: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """异步执行（暂不支持）"""
        raise NotImplementedError("UserSearchTool does not support async")


class UserCountTool(BaseTool):
    """用户计数工具"""
    
    name = "user_count"
    description = "获取系统中的用户总数。不需要输入参数。"
    user_service: UserService = None
    
    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service
    
    def _run(self, query: str = "") -> str:
        """获取用户数量"""
        try:
            count = self.user_service.count_users()
            return f"系统中共有 {count} 个用户"
        except Exception as e:
            return f"获取用户数量失败: {str(e)}"
    
    async def _arun(self, query: str = "") -> str:
        """异步执行（暂不支持）"""
        raise NotImplementedError("UserCountTool does not support async")


def create_user_tools(user_service: UserService) -> list:
    """创建用户管理工具列表"""
    return [
        UserSearchTool(user_service=user_service),
        UserCountTool(user_service=user_service),
    ]
