"""
API 测试全局配置和 fixtures
"""
import pytest
from src.api.app import create_app
from src.api.routes import reset_user_service


@pytest.fixture(scope='module')
def app():
    """
    创建测试用的 Flask 应用
    
    Scope: module - 整个测试模块共享一个应用实例
    """
    app = create_app({
        'TESTING': True,  # 启用测试模式
    })
    yield app
    # 清理：重置用户服务
    reset_user_service()


@pytest.fixture(scope='module')
def client(app):
    """
    创建测试客户端
    
    用于发送 HTTP 请求到 Flask 应用
    Scope: module - 模块级别共享
    """
    with app.test_client() as client:
        yield client


@pytest.fixture
def fresh_app():
    """
    创建独立的 Flask 应用实例（每个测试函数独立）
    
    Scope: function - 确保状态隔离
    """
    reset_user_service()
    test_app = create_app({
        'TESTING': True,
    })
    return test_app


@pytest.fixture
def fresh_client(fresh_app):
    """
    创建独立的测试客户端（每个测试函数独立）
    
    Scope: function - 每个测试函数都有全新的客户端和服务状态
    """
    with fresh_app.test_client() as client:
        yield client


@pytest.fixture
def sample_user_data():
    """提供标准用户测试数据"""
    return {
        'username': 'test_user_001',
        'email': 'test001@example.com',
        'age': 25,
        'password': 'TestPass123!'
    }


@pytest.fixture
def sample_user_data_2():
    """提供第二个用户测试数据"""
    return {
        'username': 'test_user_002',
        'email': 'test002@example.com',
        'age': 30,
        'password': 'AnotherPass456@'
    }


@pytest.fixture
def created_user(fresh_client, sample_user_data):
    """
    创建一个已存在的用户（用于后续测试）
    
    Returns:
        创建的用户响应数据
    """
    response = fresh_client.post('/api/users/', json=sample_user_data)
    assert response.status_code == 201, f"Failed to create user: {response.get_json()}"
    return response.get_json()
