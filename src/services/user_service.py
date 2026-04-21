"""
用户服务层
处理用户相关的业务逻辑
"""
from typing import List, Optional, Dict
from datetime import datetime
import uuid
import hashlib

from src.models.user import User
from src.exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserInactiveError
)


class UserService:
    """用户管理服务"""
    
    def __init__(self):
        """初始化用户存储（模拟数据库）"""
        self._users: Dict[str, User] = {}
        self._username_index: Dict[str, str] = {}
        self._email_index: Dict[str, str] = {}
    
    def create_user(self, username: str, email: str, age: int, password: str) -> User:
        """
        创建新用户
        
        Args:
            username: 用户名
            email: 邮箱
            age: 年龄
            password: 密码
            
        Returns:
            创建的用户对象
            
        Raises:
            UserAlreadyExistsError: 用户名或邮箱已存在
        """
        # 检查用户名是否已存在
        if username.lower() in self._username_index:
            raise UserAlreadyExistsError(f"Username '{username}' already exists")
        
        # 检查邮箱是否已存在
        if email.lower() in self._email_index:
            raise UserAlreadyExistsError(f"Email '{email}' already exists")
        
        # 先创建用户对象（使用原始密码进行验证）
        user = User(
            username=username,
            email=email,
            age=age,
            password=password,  # 先使用原始密码
            user_id=str(uuid.uuid4())
        )
        
        # 验证通过后，哈希密码
        user.password = self._hash_password(password)
        
        # 存储用户
        self._users[user.user_id] = user
        self._username_index[username.lower()] = user.user_id
        self._email_index[email.lower()] = user.user_id
        
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """根据 ID 获取用户"""
        return self._users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        user_id = self._username_index.get(username.lower())
        if user_id:
            return self._users.get(user_id)
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        user_id = self._email_index.get(email.lower())
        if user_id:
            return self._users.get(user_id)
        return None
    
    def update_user(self, user_id: str, **kwargs) -> User:
        """
        更新用户信息
        
        Args:
            user_id: 用户 ID
            **kwargs: 要更新的字段
            
        Returns:
            更新后的用户对象
            
        Raises:
            UserNotFoundError: 用户不存在
            UserAlreadyExistsError: 更新的用户名或邮箱已被使用
        """
        user = self._users.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID '{user_id}' not found")
        
        # 如果要更新用户名，检查新用户名是否可用
        if 'username' in kwargs:
            new_username = kwargs['username'].lower()
            existing_id = self._username_index.get(new_username)
            if existing_id and existing_id != user_id:
                raise UserAlreadyExistsError(f"Username '{kwargs['username']}' already exists")
            
            # 删除旧的用户名索引
            del self._username_index[user.username.lower()]
        
        # 如果要更新邮箱，检查新邮箱是否可用
        if 'email' in kwargs:
            new_email = kwargs['email'].lower()
            existing_id = self._email_index.get(new_email)
            if existing_id and existing_id != user_id:
                raise UserAlreadyExistsError(f"Email '{kwargs['email']}' already exists")
            
            # 删除旧的邮箱索引
            del self._email_index[user.email.lower()]
        
        # 如果更新密码，需要先验证再哈希
        if 'password' in kwargs:
            # 临时保存原始密码用于验证
            original_password = kwargs['password']
            # 先验证密码强度（通过 User 模型）
            temp_user = User(
                username=user.username,
                email=user.email,
                age=user.age,
                password=original_password
            )
            # 验证通过后哈希
            kwargs['password'] = self._hash_password(original_password)
        
        # 更新用户信息
        user.update_info(**kwargs)
        
        # 更新索引
        if 'username' in kwargs:
            self._username_index[kwargs['username'].lower()] = user_id
        if 'email' in kwargs:
            self._email_index[kwargs['email'].lower()] = user_id
        
        return user
    
    def delete_user(self, user_id: str) -> bool:
        """
        删除用户
        
        Args:
            user_id: 用户 ID
            
        Returns:
            是否删除成功
            
        Raises:
            UserNotFoundError: 用户不存在
        """
        user = self._users.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID '{user_id}' not found")
        
        # 删除索引
        del self._username_index[user.username.lower()]
        del self._email_index[user.email.lower()]
        
        # 删除用户
        del self._users[user_id]
        
        return True
    
    def authenticate(self, username: str, password: str) -> User:
        """
        用户认证
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            认证成功的用户对象
            
        Raises:
            InvalidCredentialsError: 用户名或密码错误
            UserInactiveError: 账户已停用
        """
        user = self.get_user_by_username(username)
        
        if not user:
            raise InvalidCredentialsError("Invalid username or password")
        
        if not user.is_active:
            raise UserInactiveError("User account is inactive")
        
        hashed_password = self._hash_password(password)
        if user.password != hashed_password:
            raise InvalidCredentialsError("Invalid username or password")
        
        return user
    
    def deactivate_user(self, user_id: str) -> User:
        """停用用户账户"""
        user = self._users.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID '{user_id}' not found")
        
        user.deactivate()
        return user
    
    def activate_user(self, user_id: str) -> User:
        """激活用户账户"""
        user = self._users.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID '{user_id}' not found")
        
        user.activate()
        return user
    
    def list_users(self, active_only: bool = False) -> List[User]:
        """
        列出所有用户
        
        Args:
            active_only: 是否只返回活跃用户
            
        Returns:
            用户列表
        """
        if active_only:
            return [user for user in self._users.values() if user.is_active]
        return list(self._users.values())
    
    def count_users(self) -> int:
        """获取用户总数"""
        return len(self._users)
    
    def search_users(self, keyword: str) -> List[User]:
        """
        搜索用户（按用户名或邮箱）
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的用户列表
        """
        keyword_lower = keyword.lower()
        results = []
        
        for user in self._users.values():
            if keyword_lower in user.username.lower() or keyword_lower in user.email.lower():
                results.append(user)
        
        return results
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """哈希密码（简化版，实际项目应使用 bcrypt）"""
        return hashlib.sha256(password.encode()).hexdigest()
