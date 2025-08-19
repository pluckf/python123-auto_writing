#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一次性运行多个Python脚本
先运行 main.py，然后运行 all_groups_tester.py
支持传递Authorization和Cookie作为可选参数
"""

import subprocess
import sys
import os
from pathlib import Path

def run_script_with_params(script_path, auth_token=None, cookie=None):
    """
    运行指定的Python脚本，支持传递授权参数
    
    Args:
        script_path: 脚本文件路径
        auth_token: Authorization token (可选)
        cookie: Cookie字符串 (可选)
    """
    print(f"\n{'='*60}")
    print(f"开始运行脚本: {script_path}")
    print(f"{'='*60}")
    
    # 准备环境变量
    env = os.environ.copy()
    if auth_token:
        env["PYTHON123_AUTHORIZATION"] = auth_token
        print(f"设置Authorization环境变量: {auth_token[:50]}...")
    if cookie:
        env["PYTHON123_COOKIE"] = cookie
        print(f"设置Cookie环境变量: {cookie[:50]}...")
    
    # 检查脚本文件是否存在
    if not os.path.exists(script_path):
        print(f"错误: 脚本文件不存在: {script_path}")
        return False
    
    try:
        # 运行脚本
        result = subprocess.run([sys.executable, script_path], 
                              env=env, 
                              cwd=os.path.dirname(os.path.abspath(__file__)),
                              check=False)
        
        if result.returncode == 0:
            print(f"\n✓ 脚本 {script_path} 执行成功")
        else:
            print(f"\n✗ 脚本 {script_path} 执行失败，退出代码: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"\n✗ 运行脚本时发生错误: {e}")
        return False

def main():
    """
    主函数：依次运行指定的脚本
    """
    print("Python123 自动化脚本启动器")
    print("仅供学习使用")
    print("="*60)
    
    # 配置Authorization和Cookie参数 (可选)
    # 如果不需要传递参数，可以设置为None
    AUTHORIZATION_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMzEyNzkzMDAyOEBxcS5jb20iLCJuYW1lIjoicGx1Y2tmIiwiaWQiOiIxNzY4MDg5Iiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTY2NTg5NTU2fSwiaWF0IjoxNzU1NTY4MjA0LCJleHAiOjE3NTY4NjQyMDR9.CqNd9AGSdKU5Y3KBljexEOMsKnKWuoxAKJzzrd6AJgA"

    COOKIE_STRING = "Hm_lvt_6f63cfeea8c9a84040e2c4389f01bb91=1755516075,1755522844,1755532756,1755568198; HMACCOUNT=3EE86EE065B9114B; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMzEyNzkzMDAyOEBxcS5jb20iLCJuYW1lIjoicGx1Y2tmIiwiaWQiOiIxNzY4MDg5Iiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTY2NTg5NTU2fSwiaWF0IjoxNzU1NTY4MjA0LCJleHAiOjE3NTY4NjQyMDR9.CqNd9AGSdKU5Y3KBljexEOMsKnKWuoxAKJzzrd6AJgA; io=wa4O9l8Is12Qai03ACOk; Hm_lpvt_6f63cfeea8c9a84040e2c4389f01bb91=1755568208"

    # 要运行的脚本列表（按执行顺序）
    scripts = [
        "python123/main.py",
        "python123/all_groups_tester.py"
    ]
    
    success_count = 0
    total_scripts = len(scripts)
    
    # 依次运行每个脚本
    for i, script_path in enumerate(scripts, 1):
        print(f"\n[{i}/{total_scripts}] 准备运行脚本: {script_path}")
        
        success = run_script_with_params(
            script_path=script_path,
            auth_token=AUTHORIZATION_TOKEN,
            cookie=COOKIE_STRING
        )
        
        if success:
            success_count += 1
        else:
            print(f"\n警告: 脚本 {script_path} 执行失败")
            # 如果某个脚本失败，询问是否继续
            response = input("是否继续执行剩余脚本？(y/n): ").lower().strip()
            if response != 'y' and response != 'yes':
                print("用户选择终止执行")
                break
    
    # 输出执行总结
    print(f"\n{'='*60}")
    print("执行总结:")
    print(f"总脚本数: {total_scripts}")
    print(f"成功执行: {success_count}")
    print(f"执行失败: {total_scripts - success_count}")
    print(f"{'='*60}")
    
    if success_count == total_scripts:
        print("✓ 所有脚本执行完成!")
    else:
        print("⚠ 部分脚本执行失败，请检查错误信息")

if __name__ == "__main__":
    main()