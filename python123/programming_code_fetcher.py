import requests
import json
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 全局配置
BASE_URL = "https://python123.io/api/v1/student/courses"
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMTY1MzA4MzQ3MUBxcS5jb20iLCJuYW1lIjoi5aec6L-c5bCaIiwiaWQiOiIxMjQzOTYxIiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTEyODY0MjcwfSwiaWF0IjoxNzU1NTE1MjU1LCJleHAiOjE3NTY4MTEyNTV9.4CFizZ4KvcRwad7ACdvSPfG0Kf3epPQYJdwiv_YUPps",
    "Connection": "keep-alive",
    "Cookie": "Hm_lvt_6f63cfeea8c9a84040e2c4389f01bb91=1755516075; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMTY1MzA4MzQ3MUBxcS5jb20iLCJuYW1lIjoi5aec6L-c5bCaIiwiaWQiOiIxMjQzOTYxIiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTEyODY0MjcwfSwiaWF0IjoxNzU1NTE1MjU1LCJleHAiOjE3NTY4MTEyNTV9.4CFizZ4KvcRwad7ACdvSPfG0Kf3epPQYJdwiv_YUPps; io=yt1DxQoARfnmCYByABjJ",
    "Host": "python123.io",
    "Referer": "https://python123.io/student/home",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

def get_problem_code(course_id, group_id, problem_id):
    """获取指定题目的代码"""
    url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/code"
    
    try:
        response = requests.get(url, headers=HEADERS, verify=False)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"请求发生错误: {e}")
        return None

def fetch_first_programming_code():
    """获取第一个编程题的代码，跳过choice类型的题目"""
    print("=" * 60)
    print("Python123.io 编程题代码获取工具")
    print("仅供学习使用 - 跳过选择题，只获取编程题代码")
    print("=" * 60)
    
    # 使用已知的数据进行测试
    course_id = 8717
    group_id = 114918
    
    # 已知的编程题目ID列表（跳过选择题）
    programming_problems = [
        {"id": 99764, "name": "Hello World I", "type": "programming"},
        {"id": 138943, "name": "世界，你好！", "type": "programming"},
        {"id": 138944, "name": "说句心里话 A", "type": "programming"}
    ]
    
    print("已知的编程题目列表:")
    for i, problem in enumerate(programming_problems, 1):
        print(f"  {i}. {problem['name']} (ID: {problem['id']})")
    
    print(f"\n开始获取第一个编程题的代码...")
    print("-" * 50)
    
    # 获取第一个编程题的代码
    first_problem = programming_problems[0]
    problem_id = first_problem['id']
    problem_name = first_problem['name']
    
    print(f"正在获取题目: {problem_name} (ID: {problem_id})")
    print(f"请求URL: {BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/code")
    
    code_data = get_problem_code(course_id, group_id, problem_id)
    
    if code_data and 'data' in code_data:
        print("✓ 成功获取编程题代码!")
        print("=" * 50)
        
        # 提取代码内容
        actual_code = code_data['data'].get('code', '')
        update_time = code_data['data'].get('update_at', '')
        
        print(f"题目名称: {problem_name}")
        print(f"题目ID: {problem_id}")
        print(f"更新时间: {update_time}")
        print(f"代码内容:")
        print(f"```python")
        print(f"{actual_code}")
        print(f"```")
        
        print("\n完整响应数据:")
        print(json.dumps(code_data, ensure_ascii=False, indent=2))
        
        # 保存到文件
        filename = f"programming_code_{problem_id}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'problem_info': {
                        'id': problem_id,
                        'name': problem_name,
                        'type': 'programming',
                        'course_id': course_id,
                        'group_id': group_id
                    },
                    'code_info': {
                        'code': actual_code,
                        'update_at': update_time,
                        'full_response': code_data
                    },
                    'timestamp': '2025-08-18'
                }, f, ensure_ascii=False, indent=2)
            print(f"\n代码数据已保存到文件: {filename}")
        except Exception as e:
            print(f"保存文件失败: {e}")
    else:
        print("✗ 获取代码失败")

def fetch_all_programming_codes():
    """获取所有编程题的代码"""
    print("=" * 60)
    print("Python123.io 所有编程题代码获取工具")
    print("仅供学习使用 - 跳过选择题，获取所有编程题代码")
    print("=" * 60)
    
    # 使用已知的数据
    course_id = 8717
    group_id = 114918
    
    programming_problems = [
        {"id": 99764, "name": "Hello World I", "type": "programming"},
        {"id": 138943, "name": "世界，你好！", "type": "programming"},
        {"id": 138944, "name": "说句心里话 A", "type": "programming"}
    ]
    
    all_codes = {}
    
    print(f"开始获取 {len(programming_problems)} 个编程题的代码...")
    print("-" * 50)
    
    for i, problem in enumerate(programming_problems, 1):
        problem_id = problem['id']
        problem_name = problem['name']
        
        print(f"\n{i}/{len(programming_problems)} 正在获取: {problem_name} (ID: {problem_id})")
        
        code_data = get_problem_code(course_id, group_id, problem_id)
        
        if code_data and 'data' in code_data:
            actual_code = code_data['data'].get('code', '')
            print(f"  ✓ 成功获取代码: {actual_code}")
            
            all_codes[str(problem_id)] = {
                'problem_name': problem_name,
                'code': actual_code,
                'full_response': code_data
            }
        else:
            print(f"  ✗ 获取失败")
    
    # 保存所有代码到文件
    if all_codes:
        filename = "all_programming_codes.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'course_info': {
                        'course_id': course_id,
                        'group_id': group_id
                    },
                    'codes': all_codes,
                    'total_problems': len(all_codes),
                    'timestamp': '2025-08-18'
                }, f, ensure_ascii=False, indent=2)
            print(f"\n所有编程题代码已保存到文件: {filename}")
            print(f"总计获取了 {len(all_codes)} 个编程题的代码")
        except Exception as e:
            print(f"保存文件失败: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        fetch_all_programming_codes()
    else:
        fetch_first_programming_code()
        
        print("\n" + "-" * 50)
        print("提示：")
        print("  python programming_code_fetcher.py        # 获取第一个编程题代码")
        print("  python programming_code_fetcher.py --all  # 获取所有编程题代码")
