"""
Flask 应用工厂
创建和配置 Flask 应用
"""
from flask import Flask, jsonify
from flask_cors import CORS

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
    
    # 启用 CORS
    CORS(app)
    
    # 加载配置
    if config:
        app.config.update(config)
    
    # 注册蓝图
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
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
