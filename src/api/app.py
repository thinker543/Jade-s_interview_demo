"""
Flask 应用工厂
创建和配置 Flask 应用
"""
from flask import Flask, jsonify, redirect, render_template_string
from flask_cors import CORS
import os

from src.api.routes import user_bp
from src.exceptions.user_exceptions import (
    UserException,
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserInactiveError
)


def create_app(config=None):
    """
    创建 Flask 应用
    
    Args:
        config: 配置字典
        
    Returns:
        Flask 应用实例
    """
    app = Flask(__name__)
    
    # 配置 API 文档
    app.config.update({
        'API_TITLE': '用户管理系统 API',
        'API_VERSION': 'v1',
        'OPENAPI_VERSION': '3.0.3',
        'OPENAPI_URL_PREFIX': '/api/docs',
        'OPENAPI_SWAGGER_UI_PATH': '/swagger',
        'OPENAPI_SWAGGER_UI_URL': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/',
        'OPENAPI_REDOC_PATH': '/redoc',
        'OPENAPI_REDOC_URL': 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js',
    })
    
    # 加载额外配置
    if config:
        app.config.update(config)
    
    # 启用 CORS
    CORS(app)
    
    # 注册蓝图
    from src.api.routes import user_bp
    app.register_blueprint(user_bp)
    
    # 注册文档路由
    @app.route('/')
    def index():
        """重定向到 API 文档"""
        return redirect('/api/docs')
    
    @app.route('/api/docs')
    def api_docs():
        """API 文档页面"""
        docs_path = os.path.join(os.path.dirname(__file__), 'templates', 'api_docs.html')
        with open(docs_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    # 注册错误处理
    register_error_handlers(app)
    
    return app


def register_error_handlers(app):
    """注册全局错误处理器"""
    
    @app.errorhandler(UserNotFoundError)
    def handle_user_not_found(error):
        return jsonify({
            'error': 'UserNotFoundError',
            'message': str(error)
        }), 404
    
    @app.errorhandler(UserAlreadyExistsError)
    def handle_user_already_exists(error):
        return jsonify({
            'error': 'UserAlreadyExistsError',
            'message': str(error)
        }), 409
    
    @app.errorhandler(InvalidCredentialsError)
    def handle_invalid_credentials(error):
        return jsonify({
            'error': 'InvalidCredentialsError',
            'message': str(error)
        }), 401
    
    @app.errorhandler(UserInactiveError)
    def handle_user_inactive(error):
        return jsonify({
            'error': 'UserInactiveError',
            'message': str(error)
        }), 403
    
    @app.errorhandler(UserException)
    def handle_user_exception(error):
        return jsonify({
            'error': 'UserException',
            'message': str(error)
        }), 400
    
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            'error': 'NotFound',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({
            'error': 'InternalServerError',
            'message': 'An internal server error occurred'
        }), 500
