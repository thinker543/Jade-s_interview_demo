"""
API 文档和 Schema 定义
使用 Marshmallow 定义数据模型，用于生成 OpenAPI 文档
"""
from marshmallow import Schema, fields, validate


class UserRequestSchema(Schema):
    """用户创建/更新请求 Schema"""
    username = fields.String(
        required=True,
        validate=validate.Length(min=3, max=20),
        metadata={
            "description": "用户名（3-20个字符，只能包含字母、数字和下划线）",
            "example": "john_doe"
        }
    )
    email = fields.Email(
        required=True,
        metadata={
            "description": "邮箱地址",
            "example": "john@example.com"
        }
    )
    age = fields.Integer(
        required=True,
        validate=validate.Range(min=18, max=150),
        metadata={
            "description": "年龄（18-150岁）",
            "example": 25
        }
    )
    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=8),
        metadata={
            "description": "密码（至少8位，需包含大小写字母和数字）",
            "example": "SecurePass123!"
        }
    )


class UserUpdateSchema(Schema):
    """用户更新请求 Schema（所有字段可选）"""
    username = fields.String(
        validate=validate.Length(min=3, max=20),
        metadata={
            "description": "用户名（可选）",
            "example": "john_doe_updated"
        }
    )
    email = fields.Email(
        metadata={
            "description": "邮箱地址（可选）",
            "example": "newemail@example.com"
        }
    )
    age = fields.Integer(
        validate=validate.Range(min=18, max=150),
        metadata={
            "description": "年龄（可选）",
            "example": 26
        }
    )
    password = fields.String(
        load_only=True,
        validate=validate.Length(min=8),
        metadata={
            "description": "密码（可选）",
            "example": "NewPass456!"
        }
    )


class UserResponseSchema(Schema):
    """用户响应 Schema（不包含密码）"""
    user_id = fields.String(
        metadata={
            "description": "用户唯一标识符",
            "example": "550e8400-e29b-41d4-a716-446655440000"
        }
    )
    username = fields.String(
        metadata={
            "description": "用户名",
            "example": "john_doe"
        }
    )
    email = fields.Email(
        metadata={
            "description": "邮箱地址",
            "example": "john@example.com"
        }
    )
    age = fields.Integer(
        metadata={
            "description": "年龄",
            "example": 25
        }
    )
    created_at = fields.DateTime(
        metadata={
            "description": "创建时间",
            "example": "2024-01-15T10:30:00"
        }
    )
    updated_at = fields.DateTime(
        allow_none=True,
        metadata={
            "description": "更新时间",
            "example": "2024-01-16T15:45:00"
        }
    )
    is_active = fields.Boolean(
        metadata={
            "description": "账户是否激活",
            "example": True
        }
    )


class AuthRequestSchema(Schema):
    """认证请求 Schema"""
    username = fields.String(
        required=True,
        metadata={
            "description": "用户名",
            "example": "john_doe"
        }
    )
    password = fields.String(
        required=True,
        load_only=True,
        metadata={
            "description": "密码",
            "example": "SecurePass123!"
        }
    )


class ErrorResponseSchema(Schema):
    """错误响应 Schema"""
    error = fields.String(
        metadata={
            "description": "错误类型",
            "example": "UserNotFoundError"
        }
    )
    message = fields.String(
        metadata={
            "description": "错误详情",
            "example": "User with ID 'xxx' not found"
        }
    )


class SuccessResponseSchema(Schema):
    """成功响应基础 Schema"""
    success = fields.Boolean(
        metadata={
            "description": "操作是否成功",
            "example": True
        }
    )
    message = fields.String(
        metadata={
            "description": "操作消息",
            "example": "User created successfully"
        }
    )
