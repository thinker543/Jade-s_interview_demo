"""
工具函数
包含各种辅助功能
"""
import re
from typing import List
from datetime import datetime, timedelta


def validate_email_format(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        是否为有效邮箱
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def calculate_age_group(age: int) -> str:
    """
    根据年龄计算年龄段
    
    Args:
        age: 年龄
        
    Returns:
        年龄段描述
    """
    if age < 18:
        return "未成年"
    elif age < 30:
        return "青年"
    elif age < 50:
        return "中年"
    else:
        return "老年"


def format_user_report(users: List[dict]) -> str:
    """
    格式化用户报告
    
    Args:
        users: 用户字典列表
        
    Returns:
        格式化的报告字符串
    """
    if not users:
        return "No users to report."
    
    report_lines = ["=" * 50, "USER REPORT", "=" * 50]
    
    for i, user in enumerate(users, 1):
        report_lines.append(f"\nUser {i}:")
        report_lines.append(f"  Username: {user.get('username', 'N/A')}")
        report_lines.append(f"  Email: {user.get('email', 'N/A')}")
        report_lines.append(f"  Age: {user.get('age', 'N/A')}")
        report_lines.append(f"  Active: {'Yes' if user.get('is_active') else 'No'}")
        
        created_at = user.get('created_at')
        if created_at:
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at)
            report_lines.append(f"  Created: {created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    report_lines.append("\n" + "=" * 50)
    report_lines.append(f"Total Users: {len(users)}")
    report_lines.append("=" * 50)
    
    return "\n".join(report_lines)


def filter_users_by_age(users: List[dict], min_age: int, max_age: int) -> List[dict]:
    """
    按年龄范围过滤用户
    
    Args:
        users: 用户列表
        min_age: 最小年龄
        max_age: 最大年龄
        
    Returns:
        过滤后的用户列表
    """
    return [
        user for user in users
        if min_age <= user.get('age', 0) <= max_age
    ]


def get_active_users(users: List[dict]) -> List[dict]:
    """
    获取活跃用户
    
    Args:
        users: 用户列表
        
    Returns:
        活跃用户列表
    """
    return [user for user in users if user.get('is_active', False)]


def sort_users_by_creation_date(users: List[dict], reverse: bool = False) -> List[dict]:
    """
    按创建日期排序用户
    
    Args:
        users: 用户列表
        reverse: 是否倒序
        
    Returns:
        排序后的用户列表
    """
    def parse_date(user):
        created_at = user.get('created_at')
        if isinstance(created_at, str):
            return datetime.fromisoformat(created_at)
        return created_at or datetime.min
    
    return sorted(users, key=parse_date, reverse=reverse)


def generate_username_suggestions(base_name: str, count: int = 5) -> List[str]:
    """
    生成用户名建议
    
    Args:
        base_name: 基础名称
        count: 建议数量
        
    Returns:
        用户名建议列表
    """
    suggestions = []
    for i in range(1, count + 1):
        suggestion = f"{base_name}_{i}"
        if len(suggestion) <= 20:  # 确保不超过最大长度
            suggestions.append(suggestion)
    
    return suggestions


def is_strong_password(password: str) -> bool:
    """
    检查密码强度
    
    Args:
        password: 密码
        
    Returns:
        是否为强密码
    """
    if len(password) < 8:
        return False
    
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    # 强密码需要至少包含三种字符类型
    types_count = sum([has_upper, has_lower, has_digit, has_special])
    return types_count >= 3


def calculate_password_strength_score(password: str) -> int:
    """
    计算密码强度分数（0-100）
    
    Args:
        password: 密码
        
    Returns:
        强度分数
    """
    score = 0
    
    # 长度评分（最多40分）
    length = len(password)
    if length >= 8:
        score += 20
    if length >= 12:
        score += 10
    if length >= 16:
        score += 10
    
    # 字符类型评分（每种15分，最多60分）
    if re.search(r'[A-Z]', password):
        score += 15
    if re.search(r'[a-z]', password):
        score += 15
    if re.search(r'\d', password):
        score += 15
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 15
    
    return min(score, 100)
