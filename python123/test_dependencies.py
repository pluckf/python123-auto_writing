#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖包测试脚本
验证Python123.io项目所需的所有依赖包是否正确安装
"""

import sys

def test_dependencies():
    """测试所有项目依赖包"""
    print("🚀 Python123.io 项目依赖测试")
    print("=" * 50)
    
    # 核心依赖测试
    dependencies = [
        # HTTP请求相关
        ("requests", "HTTP客户端库"),
        ("urllib3", "HTTP连接池库"),
        
        # GUI相关  
        ("tkinter", "图形界面库"),
        
        # 标准库
        ("json", "JSON处理库"),
        ("re", "正则表达式库"),
        ("time", "时间处理库"),
        ("datetime", "日期时间库"),
        ("os", "操作系统接口库"),
        ("sys", "系统特定参数库"),
        ("subprocess", "子进程管理库"),
        ("threading", "多线程库"),
        ("queue", "队列库"),
        ("glob", "文件通配符库"),
    ]
    
    success_count = 0
    total_count = len(dependencies)
    
    for module_name, description in dependencies:
        try:
            if module_name == "tkinter":
                # tkinter 在不同Python版本中可能有不同的导入方式
                try:
                    import tkinter
                except ImportError:
                    import Tkinter as tkinter
                    
            else:
                __import__(module_name)
            
            print(f"✅ {module_name:12} - {description}")
            success_count += 1
            
        except ImportError as e:
            print(f"❌ {module_name:12} - {description} (缺失)")
            print(f"   错误: {e}")
    
    print("-" * 50)
    print(f"📊 测试结果: {success_count}/{total_count} 个依赖包可用")
    
    if success_count == total_count:
        print("🎉 所有依赖包都已正确安装！")
        return True
    else:
        print("⚠️ 有些依赖包缺失，请安装后重试")
        print("\n安装命令:")
        print("pip install -r requirements.txt")
        return False

def test_version_info():
    """显示关键依赖包的版本信息"""
    print("\n📋 版本信息:")
    print("-" * 30)
    
    try:
        import requests
        print(f"requests: {requests.__version__}")
    except (ImportError, AttributeError):
        print("requests: 未安装或无法获取版本")
    
    try:
        import urllib3
        print(f"urllib3: {urllib3.__version__}")
    except (ImportError, AttributeError):
        print("urllib3: 未安装或无法获取版本")
    
    print(f"Python: {sys.version}")

if __name__ == "__main__":
    print(f"Python版本: {sys.version}")
    print(f"平台: {sys.platform}\n")
    
    # 运行依赖测试
    success = test_dependencies()
    
    # 显示版本信息
    test_version_info()
    
    # 退出状态
    if success:
        print("\n🎯 项目已就绪，可以运行所有工具！")
        sys.exit(0)
    else:
        print("\n❗ 请先安装缺失的依赖包")
        sys.exit(1)
