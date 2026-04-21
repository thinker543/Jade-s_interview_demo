"""
用户 API 接口测试
测试所有用户相关的 HTTP 端点
"""
import pytest


class TestCreateUser:
    """测试创建用户接口"""
    
    def test_create_user_success(self, fresh_client, sample_user_data):
        """测试成功创建用户"""
        response = fresh_client.post('/api/users/', json=sample_user_data)
        
        # 验证响应状态码
        assert response.status_code == 201
        
        # 验证响应数据
        data = response.get_json()
        assert data['success'] is True
        assert data['message'] == 'User created successfully'
        assert 'user' in data
        
        # 验证用户字段
        user = data['user']
        assert user['username'] == sample_user_data['username']
        assert user['email'] == sample_user_data['email']
        assert user['age'] == sample_user_data['age']
        assert 'password' not in user  # 密码不应返回
        assert 'user_id' in user
        assert 'created_at' in user
        assert user['is_active'] is True
    
    def test_create_user_duplicate_username(self, fresh_client, sample_user_data):
        """测试创建重复用户名的用户"""
        # 创建第一个用户
        response1 = fresh_client.post('/api/users/', json=sample_user_data)
        assert response1.status_code == 201
        
        # 尝试创建相同用户名的用户
        duplicate_data = sample_user_data.copy()
        duplicate_data['email'] = 'different@example.com'
        response2 = fresh_client.post('/api/users/', json=duplicate_data)
        
        # 验证返回冲突错误
        assert response2.status_code == 409
        data = response2.get_json()
        assert data['error'] == 'UserAlreadyExistsError'
    
    def test_create_user_duplicate_email(self, fresh_client, sample_user_data):
        """测试创建重复邮箱的用户"""
        # 创建第一个用户
        response1 = fresh_client.post('/api/users/', json=sample_user_data)
        assert response1.status_code == 201
        
        # 尝试创建相同邮箱的用户
        duplicate_data = sample_user_data.copy()
        duplicate_data['username'] = 'different_username'
        response2 = fresh_client.post('/api/users/', json=duplicate_data)
        
        # 验证返回冲突错误
        assert response2.status_code == 409
        data = response2.get_json()
        assert data['error'] == 'UserAlreadyExistsError'
    
    def test_create_user_missing_fields(self, fresh_client):
        """测试创建用户时缺少必填字段"""
        incomplete_data = {
            'username': 'test_user'
            # 缺少 email, age, password
        }
        response = fresh_client.post('/api/users/', json=incomplete_data)
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'Missing required fields' in data['error']
    
    def test_create_user_invalid_email(self, fresh_client):
        """测试创建用户时使用无效邮箱"""
        invalid_data = {
            'username': 'test_user',
            'email': 'invalid-email',
            'age': 25,
            'password': 'TestPass123!'
        }
        response = fresh_client.post('/api/users/', json=invalid_data)
        
        assert response.status_code == 400
    
    def test_create_user_weak_password(self, fresh_client):
        """测试创建用户时使用弱密码"""
        weak_password_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'age': 25,
            'password': '123'  # 太短
        }
        response = fresh_client.post('/api/users/', json=weak_password_data)
        
        assert response.status_code == 400
    
    def test_create_user_underage(self, fresh_client):
        """测试创建未成年用户"""
        underage_data = {
            'username': 'young_user',
            'email': 'young@example.com',
            'age': 16,  # 小于 18
            'password': 'TestPass123!'
        }
        response = fresh_client.post('/api/users/', json=underage_data)
        
        assert response.status_code == 400


class TestGetUser:
    """测试获取用户接口"""
    
    def test_get_user_by_id_success(self, created_user, client):
        """测试通过 ID 成功获取用户"""
        user_id = created_user['user']['user_id']
        response = client.get(f'/api/users/{user_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'user' in data
        assert data['user']['user_id'] == user_id
    
    def test_get_user_not_found(self, client):
        """测试获取不存在的用户"""
        response = client.get('/api/users/non-existent-id')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'UserNotFoundError'


class TestListUsers:
    """测试获取用户列表接口"""
    
    def test_list_users_empty(self, fresh_client):
        """测试空用户列表"""
        response = fresh_client.get('/api/users/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['count'] == 0
        assert data['users'] == []
    
    def test_list_users_with_data(self, client, sample_user_data, sample_user_data_2):
        """测试获取包含数据的用户列表"""
        # 创建两个用户
        client.post('/api/users/', json=sample_user_data)
        client.post('/api/users/', json=sample_user_data_2)
        
        response = client.get('/api/users/')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['count'] >= 2
        assert len(data['users']) >= 2
    
    def test_list_active_users_only(self, client, sample_user_data):
        """测试只获取活跃用户"""
        # 创建用户
        create_response = client.post('/api/users/', json=sample_user_data)
        user_id = create_response.get_json()['user']['user_id']
        
        # 停用用户
        client.post(f'/api/users/{user_id}/deactivate')
        
        # 获取活跃用户列表
        response = client.get('/api/users/?active_only=true')
        
        assert response.status_code == 200
        data = response.get_json()
        # 停用的用户不应在列表中
        user_ids = [u['user_id'] for u in data['users']]
        assert user_id not in user_ids


class TestUpdateUser:
    """测试更新用户接口"""
    
    def test_update_user_success(self, created_user, client):
        """测试成功更新用户"""
        user_id = created_user['user']['user_id']
        update_data = {
            'age': 26,
            'email': 'updated@example.com'
        }
        response = client.put(f'/api/users/{user_id}', json=update_data)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['user']['age'] == 26
        assert data['user']['email'] == 'updated@example.com'
    
    def test_update_user_not_found(self, client):
        """测试更新不存在的用户"""
        response = client.put('/api/users/non-existent-id', json={'age': 30})
        
        assert response.status_code == 404
    
    def test_update_user_duplicate_email(self, client, sample_user_data, sample_user_data_2):
        """测试更新为已存在的邮箱"""
        # 创建两个用户
        response1 = client.post('/api/users/', json=sample_user_data)
        user1_id = response1.get_json()['user']['user_id']
        
        client.post('/api/users/', json=sample_user_data_2)
        
        # 尝试将 user1 的邮箱更新为 user2 的邮箱
        update_data = {'email': sample_user_data_2['email']}
        response = client.put(f'/api/users/{user1_id}', json=update_data)
        
        assert response.status_code == 409


class TestDeleteUser:
    """测试删除用户接口"""
    
    def test_delete_user_success(self, created_user, client):
        """测试成功删除用户"""
        user_id = created_user['user']['user_id']
        response = client.delete(f'/api/users/{user_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        
        # 验证用户已被删除
        get_response = client.get(f'/api/users/{user_id}')
        assert get_response.status_code == 404
    
    def test_delete_user_not_found(self, client):
        """测试删除不存在的用户"""
        response = client.delete('/api/users/non-existent-id')
        
        assert response.status_code == 404


class TestAuthenticate:
    """测试用户认证接口"""
    
    def test_authenticate_success(self, client, sample_user_data):
        """测试成功认证"""
        # 创建用户
        client.post('/api/users/', json=sample_user_data)
        
        # 认证
        auth_data = {
            'username': sample_user_data['username'],
            'password': sample_user_data['password']
        }
        response = client.post('/api/users/authenticate', json=auth_data)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message'] == 'Authentication successful'
        assert 'user' in data
    
    def test_authenticate_wrong_password(self, client, sample_user_data):
        """测试密码错误的认证"""
        # 创建用户
        client.post('/api/users/', json=sample_user_data)
        
        # 使用错误密码认证
        auth_data = {
            'username': sample_user_data['username'],
            'password': 'WrongPassword123!'
        }
        response = client.post('/api/users/authenticate', json=auth_data)
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['error'] == 'InvalidCredentialsError'
    
    def test_authenticate_nonexistent_user(self, client):
        """测试认证不存在的用户"""
        auth_data = {
            'username': 'nonexistent',
            'password': 'TestPass123!'
        }
        response = client.post('/api/users/authenticate', json=auth_data)
        
        assert response.status_code == 401
    
    def test_authenticate_inactive_user(self, client, sample_user_data):
        """测试认证已停用的用户"""
        # 创建用户
        create_response = client.post('/api/users/', json=sample_user_data)
        user_id = create_response.get_json()['user']['user_id']
        
        # 停用用户
        client.post(f'/api/users/{user_id}/deactivate')
        
        # 尝试认证
        auth_data = {
            'username': sample_user_data['username'],
            'password': sample_user_data['password']
        }
        response = client.post('/api/users/authenticate', json=auth_data)
        
        assert response.status_code == 403
        data = response.get_json()
        assert data['error'] == 'UserInactiveError'


class TestUserActivation:
    """测试用户激活/停用接口"""
    
    def test_deactivate_user_success(self, created_user, client):
        """测试成功停用用户"""
        user_id = created_user['user']['user_id']
        response = client.post(f'/api/users/{user_id}/deactivate')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['user']['is_active'] is False
    
    def test_activate_user_success(self, created_user, client):
        """测试成功激活用户"""
        user_id = created_user['user']['user_id']
        
        # 先停用
        client.post(f'/api/users/{user_id}/deactivate')
        
        # 再激活
        response = client.post(f'/api/users/{user_id}/activate')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['user']['is_active'] is True
    
    def test_deactivate_nonexistent_user(self, client):
        """测试停用不存在的用户"""
        response = client.post('/api/users/non-existent-id/deactivate')
        
        assert response.status_code == 404


class TestSearchUsers:
    """测试搜索用户接口"""
    
    def test_search_users_success(self, client, sample_user_data):
        """测试成功搜索用户"""
        # 创建用户
        client.post('/api/users/', json=sample_user_data)
        
        # 搜索
        response = client.get('/api/users/search?keyword=test')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['count'] >= 1
        assert data['keyword'] == 'test'
    
    def test_search_users_no_keyword(self, client):
        """测试搜索时缺少关键词"""
        response = client.get('/api/users/search')
        
        assert response.status_code == 400
    
    def test_search_users_no_results(self, client):
        """测试搜索无结果"""
        response = client.get('/api/users/search?keyword=nonexistent')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 0
        assert data['users'] == []


class TestCountUsers:
    """测试用户计数接口"""
    
    def test_count_users(self, client, sample_user_data):
        """测试获取用户数量"""
        # 创建用户
        client.post('/api/users/', json=sample_user_data)
        
        response = client.get('/api/users/count')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['count'] >= 1
