#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试获取测试用例结果的脚本
直接调用 testcases/result API查看返回数据结构
"""
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API配置
BASE_URL = "https://python123.io/api/v1/student/courses"
HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMTY1MzA4MzQ3MUBxcS5jb20iLCJuYW1lIjoi5aec6L-c5bCaIiwiaWQiOiIxMjQzOTYxIiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTEyODY0MjcwfSwiaWF0IjoxNzU1NTE1MjU1LCJleHAiOjE3NTY4MTEyNTV9.4CFizZ4KvcRwad7ACdvSPfG0Kf3epPQYJdwiv_YUPps",
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Cookie": "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMTY1MzA4MzQ3MUBxcS5jb20iLCJuYW1lIjoi5aec6L-c5bCaIiwiaWQiOiIxMjQzOTYxIiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTEyODY0MjcwfSwiaWF0IjoxNzU1NTE1MjU1LCJleHAiOjE3NTY4MTEyNTV9.4CFizZ4KvcRwad7ACdvSPfG0Kf3epPQYJdwiv_YUPps; Hm_lvt_6f63cfeea8c9a84040e2c4389f01bb91=1755516075,1755522844; HMACCOUNT=3EE86EE065B9114B; Hm_lpvt_6f63cfeea8c9a84040e2c4389f01bb91=1755528898; io=VqDxjqf6eE8qFv9cABv0"
}

def test_testcase_result(course_id, group_id, problem_id, problem_name):
    """测试获取测试用例结果"""
    url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/testcases/result"
    
    print(f"🧪 测试题目: {problem_name}")
    print(f"🔗 API URL: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS, verify=False)
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result_data = response.json()
                print("✅ JSON响应数据:")
                print(json.dumps(result_data, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("⚠️  非JSON响应:")
                print(f"响应内容: {response.text}")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"错误内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print("-" * 80)

def main():
    """主函数 - 测试几个已提交的题目"""
    print("🚀 测试 testcases/result API")
    print("=" * 80)
    
    # 测试数据 - 使用刚才提交成功的题目
    test_cases = [
        {
            'course_id': 8717,
            'group_id': 114921,
            'problem_id': '99800',
            'name': '任意累积'
        },
        {
            'course_id': 8717,
            'group_id': 114921,
            'problem_id': '99801',
            'name': '【函和代1】斐波那契数列 II'
        },
        {
            'course_id': 8717,
            'group_id': 114921,
            'problem_id': '100501',
            'name': '【函和代1】阶乘累加求和'
        }
    ]
    
    for test_case in test_cases:
        test_testcase_result(
            test_case['course_id'],
            test_case['group_id'], 
            test_case['problem_id'],
            test_case['name']
        )
    
    print("✅ 测试完成！")

if __name__ == "__main__":
    main()
