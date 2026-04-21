"""
集成测试示例
测试多个模块之间的交互
"""
import pytest


@pytest.mark.integration
def test_database_connection():
    """测试数据库连接（示例）"""
    # 实际项目中这里会测试真实的数据库连接
    connection_status = True
    assert connection_status is True


@pytest.mark.integration
def test_api_integration():
    """测试 API 集成（示例）"""
    # 实际项目中这里会调用真实的 API
    response_data = {"status": "success", "code": 200}
    assert response_data["status"] == "success"
    assert response_data["code"] == 200


@pytest.mark.integration
def test_service_interaction(sample_data):
    """测试服务间交互（示例）"""
    # 模拟多个服务之间的数据传递
    user_data = sample_data
    processed_data = {
        "username": user_data["username"].upper(),
        "email": user_data["email"],
        "validated": True
    }
    
    assert processed_data["username"] == "TEST_USER"
    assert processed_data["validated"] is True
