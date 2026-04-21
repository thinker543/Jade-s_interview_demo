"""
测试数据工厂
使用 factory-boy 生成测试数据
"""
from factory import Factory, Sequence, Faker


class UserFactory(Factory):
    """用户数据工厂示例"""
    
    class Meta:
        model = dict
    
    username = Sequence(lambda n: f'user_{n}')
    email = Faker('email')
    age = Faker('random_int', min=18, max=80)


class ProductFactory(Factory):
    """产品数据工厂示例"""
    
    class Meta:
        model = dict
    
    name = Faker('word')
    price = Faker('pyfloat', min_value=1.0, max_value=1000.0, right_digits=2)
    description = Faker('sentence')
