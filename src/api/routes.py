"""
用户 API 路由
定义所有用户相关的 HTTP 接口
"""
from flask import Blueprint, request, jsonify
from src.services.user_service import UserService
from src.exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserInactiveError
)

# 创建蓝图
user_bp = Blueprint('users', __name__)

# 全局用户服务实例（将在应用创建时初始化）
_user_service = None


def get_user_service():
    """获取用户服务实例"""
    global _user_service
    if _user_service is None:
        _user_service = UserService()
    return _user_service


def reset_user_service():
    """重置用户服务（用于测试）"""
    global _user_service
    _user_service = UserService()


@user_bp.route('/', methods=['GET'])
def list_users():
    """
    获取用户列表
    
    Query Parameters:
        active_only: 是否只返回活跃用户 (true/false)
        
    Returns:
        JSON 用户列表
    """
    user_service = get_user_service()
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    users = user_service.list_users(active_only=active_only)
    
    return jsonify({
        'success': True,
        'count': len(users),
        'users': [user.to_dict() for user in users]
    }), 200


@user_bp.route('/search', methods=['GET'])
def search_users():
    """
    搜索用户
    
    Query Parameters:
        keyword: 搜索关键词（必填）
        
    Returns:
        JSON 匹配的用户列表
    """
    user_service = get_user_service()
    keyword = request.args.get('keyword', '')
    
    if not keyword:
        return jsonify({
            'success': False,
            'error': 'Keyword parameter is required'
        }), 400
    
    users = user_service.search_users(keyword)
    
    return jsonify({
        'success': True,
        'count': len(users),
        'keyword': keyword,
        'users': [user.to_dict() for user in users]
    }), 200


@user_bp.route('/count', methods=['GET'])
def count_users():
    """
    获取用户总数
    
    Returns:
        JSON 包含用户数量
    """
    user_service = get_user_service()
    count = user_service.count_users()
    
    return jsonify({
        'success': True,
        'count': count
    }), 200


@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    根据 ID 获取用户详情
    
    Args:
        user_id: 用户 ID
        
    Returns:
        JSON 用户详情
    """
    user_service = get_user_service()
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise UserNotFoundError(f"User with ID '{user_id}' not found")
    
    return jsonify({
        'success': True,
        'user': user.to_dict()
    }), 200


@user_bp.route('/', methods=['POST'])
def create_user():
    """
    创建新用户
    
    Request Body:
        {
            "username": "string (3-20 chars)",
            "email": "string (valid email)",
            "age": "integer (18-150)",
            "password": "string (min 8 chars, with upper, lower, digit)"
        }
        
    Returns:
        JSON 创建的用户信息（不含密码）
    """
    user_service = get_user_service()
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['username', 'email', 'age', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'success': False,
            'error': f'Missing required fields: {", ".join(missing_fields)}'
        }), 400
    
    try:
        user = user_service.create_user(
            username=data['username'],
            email=data['email'],
            age=int(data['age']),
            password=data['password']
        )
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
        
    except UserAlreadyExistsError:
        raise
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'ValidationError',
            'message': str(e)
        }), 400


@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    更新用户信息
    
    Args:
        user_id: 用户 ID
        
    Request Body:
        {
            "username": "string (optional)",
            "email": "string (optional)",
            "age": "integer (optional)",
            "password": "string (optional)"
        }
        
    Returns:
        JSON 更新后的用户信息
    """
    user_service = get_user_service()
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    try:
        user = user_service.update_user(user_id, **data)
        
        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except UserNotFoundError:
        raise


@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    删除用户
    
    Args:
        user_id: 用户 ID
        
    Returns:
        JSON 删除结果
    """
    user_service = get_user_service()
    try:
        user_service.delete_user(user_id)
        
        return jsonify({
            'success': True,
            'message': f'User {user_id} deleted successfully'
        }), 200
        
    except UserNotFoundError:
        raise


@user_bp.route('/authenticate', methods=['POST'])
def authenticate():
    """
    用户认证（登录）
    
    Request Body:
        {
            "username": "string",
            "password": "string"
        }
        
    Returns:
        JSON 用户信息（认证成功）
    """
    user_service = get_user_service()
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            'success': False,
            'error': 'Username and password are required'
        }), 400
    
    try:
        user = user_service.authenticate(
            username=data['username'],
            password=data['password']
        )
        
        return jsonify({
            'success': True,
            'message': 'Authentication successful',
            'user': user.to_dict()
        }), 200
        
    except (InvalidCredentialsError, UserInactiveError):
        raise


@user_bp.route('/<user_id>/deactivate', methods=['POST'])
def deactivate_user(user_id):
    """
    停用用户账户
    
    Args:
        user_id: 用户 ID
        
    Returns:
        JSON 操作结果
    """
    user_service = get_user_service()
    try:
        user = user_service.deactivate_user(user_id)
        
        return jsonify({
            'success': True,
            'message': 'User deactivated successfully',
            'user': user.to_dict()
        }), 200
        
    except UserNotFoundError:
        raise


@user_bp.route('/<user_id>/activate', methods=['POST'])
def activate_user(user_id):
    """
    激活用户账户
    
    Args:
        user_id: 用户 ID
        
    Returns:
        JSON 操作结果
    """
    user_service = get_user_service()
    try:
        user = user_service.activate_user(user_id)
        
        return jsonify({
            'success': True,
            'message': 'User activated successfully',
            'user': user.to_dict()
        }), 200
        
    except UserNotFoundError:
        raise
