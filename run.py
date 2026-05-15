"""
NoteCal 应用程序入口模块

该模块提供程序的启动点，负责设置应用路径并初始化主应用程序。
"""
import sys
import os


def main() -> None:
    """程序主入口函数"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, base_dir)

    from src.main_app import main as app_main
    app_main()


if __name__ == "__main__":
    main()