"""
用户模型
包含用户数据结构和验证逻辑
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import re


@dataclass
class User:
    """用户数据模型"""
    username: str
    email: str
    age: int
    password: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    is_active: bool = True
    user_id: Optional[str] = None
    
    def __post_init__(self):
        """初始化后验证"""
        self.validate_username()
        self.validate_email()
        self.validate_age()
        self.validate_password()
    
    def validate_username(self):
        """验证用户名：3-20位，只能包含字母、数字、下划线"""
        if not self.username or len(self.username) < 3 or len(self.username) > 20:
            raise ValueError("Username must be between 3 and 20 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', self.username):
            raise ValueError("Username can only contain letters, numbers, and underscores")
    
    def validate_email(self):
        """验证邮箱格式"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email format")
    
    def validate_age(self):
        """验证年龄：18-150岁"""
        if not isinstance(self.age, int) or self.age < 18 or self.age > 150:
            raise ValueError("Age must be between 18 and 150")
    
    def validate_password(self):
        """验证密码：至少8位，包含大小写字母和数字"""
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r'[A-Z]', self.password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', self.password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', self.password):
            raise ValueError("Password must contain at least one digit")
    
    def update_info(self, **kwargs):
        """更新用户信息"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['user_id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now()
        
        # 重新验证更新的字段
        if 'username' in kwargs:
            self.validate_username()
        if 'email' in kwargs:
            self.validate_email()
        if 'age' in kwargs:
            self.validate_age()
        if 'password' in kwargs:
            self.validate_password()
    
    def deactivate(self):
        """停用账户"""
        self.is_active = False
        self.updated_at = datetime.now()
    
    def activate(self):
        """激活账户"""
        self.is_active = True
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """转换为字典（不包含密码）"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'age': self.age,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
