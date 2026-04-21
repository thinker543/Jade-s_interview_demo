"""
API 服务器启动脚本
"""
from src.api.app import create_app

# 创建应用
app = create_app()

if __name__ == '__main__':
    # 启动开发服务器
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
