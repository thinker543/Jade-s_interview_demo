"""
用户管理系统演示
展示系统的功能和使用方法
"""
from src.services.user_service import UserService
from src.exceptions.user_exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError


def main():
    """演示用户管理系统的功能"""
    print("=== 用户管理系统演示 ===\n")
    
    # 创建用户服务实例
    user_service = UserService()
    
    # 1. 创建用户
    print("1. 创建用户:")
    try:
        user1 = user_service.create_user(
            username="john_doe",
            email="john@example.com",
            age=25,
            password="SecurePass123!"
        )
        print(f"   ✓ 创建用户成功: {user1.username} ({user1.email})")
        
        user2 = user_service.create_user(
            username="jane_smith",
            email="jane@example.com",
            age=30,
            password="AnotherPass456@"
        )
        print(f"   ✓ 创建用户成功: {user2.username} ({user2.email})")
        
    except UserAlreadyExistsError as e:
        print(f"   ✗ 创建用户失败: {e}")
    
    # 2. 获取用户
    print("\n2. 获取用户:")
    user = user_service.get_user_by_username("john_doe")
    if user:
        print(f"   ✓ 找到用户: {user.username}, 邮箱: {user.email}")
    
    # 3. 列出所有用户
    print("\n3. 列出所有用户:")
    all_users = user_service.list_users()
    for u in all_users:
        print(f"   - {u.username} ({u.email}), 年龄: {u.age}")
    
    # 4. 认证用户
    print("\n4. 用户认证:")
    try:
        authenticated_user = user_service.authenticate("john_doe", "SecurePass123")
        print(f"   ✓ 认证成功: {authenticated_user.username}")
    except (InvalidCredentialsError, UserNotFoundError) as e:
        print(f"   ✗ 认证失败: {e}")
    
    # 5. 更新用户
    print("\n5. 更新用户信息:")
    try:
        updated_user = user_service.update_user(
            user1.user_id,
            age=26,
            email="john.doe@example.com"
        )
        print(f"   ✓ 更新成功: {updated_user.username}, 新邮箱: {updated_user.email}")
    except Exception as e:
        print(f"   ✗ 更新失败: {e}")
    
    # 6. 搜索用户
    print("\n6. 搜索用户 (关键词: john):")
    search_results = user_service.search_users("john")
    for user in search_results:
        print(f"   - 找到: {user.username}")
    
    # 7. 统计信息
    print(f"\n7. 用户统计: 总共 {user_service.count_users()} 个用户")
    
    print("\n=== 演示完成 ===")


if __name__ == "__main__":
    main()
