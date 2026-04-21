"""
单元测试示例
测试单个函数、类或模块的功能
"""
import pytest


def test_addition():
    """测试基本加法运算"""
    assert 1 + 2 == 3


def test_string_concatenation():
    """测试字符串拼接"""
    result = "Hello" + " " + "World"
    assert result == "Hello World"


def test_list_operations(sample_data):
    """测试使用 fixture 的列表操作"""
    items = [1, 2, 3, 4, 5]
    assert len(items) == 5
    assert sum(items) == 15


class TestStringMethods:
    """字符串方法测试类"""
    
    def test_upper(self):
        """测试转大写"""
        assert "hello".upper() == "HELLO"
    
    def test_isupper(self):
        """测试是否全大写"""
        assert "HELLO".isupper()
        assert not "Hello".isupper()
    
    def test_strip(self):
        """测试去除空格"""
        assert "  hello  ".strip() == "hello"


@pytest.mark.slow
def test_slow_operation():
    """标记为慢速测试的示例"""
    import time
    time.sleep(0.1)  # 模拟耗时操作
    assert True
