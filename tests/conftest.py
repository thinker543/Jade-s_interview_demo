"""
Pytest 全局配置文件
用于定义全局 fixtures、hooks 和配置
"""
import pytest
from datetime import datetime


def pytest_configure(config):
    """Pytest 配置钩子"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )


@pytest.fixture(scope="session")
def test_session_id():
    """生成测试会话 ID"""
    return f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


@pytest.fixture
def sample_data():
    """提供示例测试数据"""
    return {
        "username": "test_user",
        "email": "test@example.com",
        "age": 25
    }
