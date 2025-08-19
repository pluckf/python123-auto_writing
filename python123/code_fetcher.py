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

def load_problem_ids(filename="problem_ids.json"):
    """从文件加载问题ID数据"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('problem_ids', {})
    except Exception as e:
        print(f"加载问题ID文件失败: {e}")
        return {}

def get_problem_code(course_id, group_id, problem_id):
    """获取指定题目的代码"""
    url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/code"
    
    try:
        print(f"正在请求: {url}")
        response = requests.get(url, headers=HEADERS, verify=False)
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                return response.text
        else:
            print(f"请求失败，响应内容: {response.text}")
            return None
            
    except Exception as e:
        print(f"请求发生错误: {e}")
        return None

def find_first_programming_problem():
    """找到第一个编程题目并获取其代码"""
    print("=" * 60)
    print("Python123.io 题目代码获取工具")
    print("仅供学习使用")
    print("=" * 60)
    
    # 加载问题ID数据
    problem_ids = load_problem_ids()
    
    if not problem_ids:
        print("没有找到问题ID数据，请先运行 problems_fetcher.py")
        return
    
    print("正在查找第一个编程题目...")
    print("跳过 type='choice' 的选择题")
    print("-" * 50)
    
    # 遍历所有课程和组
    for course_name, course_data in problem_ids.items():
        print(f"\n检查课程: {course_name}")
        
        for group_key, problems in course_data.items():
            print(f"  检查 {group_key}...")
            
            for problem in problems:
                problem_id = problem['id']
                problem_name = problem['name']
                problem_type = problem['type']
                
                print(f"    - {problem_name} (ID: {problem_id}, 类型: {problem_type})", end="")
                
                if problem_type == 'choice':
                    print(" [跳过选择题]")
                    continue
                
                print(" [编程题，获取代码]")
                
                # 这里需要知道课程ID和组ID，我们需要从之前的数据中获取
                # 先尝试使用已知的数据进行测试
                course_id = 8717  # 从之前的测试中知道的课程ID
                group_id = 114918  # 从之前的测试中知道的组ID
                
                code_data = get_problem_code(course_id, group_id, problem_id)
                
                if code_data:
                    print("✓ 成功获取题目代码!")
                    print("=" * 50)
                    print("题目信息:")
                    print(f"  名称: {problem_name}")
                    print(f"  ID: {problem_id}")
                    print(f"  类型: {problem_type}")
                    print("=" * 50)
                    print("代码数据:")
                    print(json.dumps(code_data, ensure_ascii=False, indent=2))
                    
                    # 保存到文件
                    filename = f"problem_code_{problem_id}.json"
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump({
                                'problem_info': {
                                    'id': problem_id,
                                    'name': problem_name,
                                    'type': problem_type,
                                    'course_id': course_id,
                                    'group_id': group_id
                                },
                                'code_data': code_data,
                                'timestamp': '2025-08-18'
                            }, f, ensure_ascii=False, indent=2)
                        print(f"\n代码数据已保存到文件: {filename}")
                    except Exception as e:
                        print(f"保存文件失败: {e}")
                    
                    return  # 只获取第一个编程题目就返回
                else:
                    print("✗ 获取代码失败")
    
    print("\n没有找到可获取代码的编程题目")

def fetch_specific_problem_code(course_id, group_id, problem_id):
    """获取指定题目的代码（测试用）"""
    print("=" * 60)
    print("获取指定题目代码")
    print("=" * 60)
    
    print(f"课程ID: {course_id}")
    print(f"组ID: {group_id}")
    print(f"题目ID: {problem_id}")
    print("-" * 50)
    
    code_data = get_problem_code(course_id, group_id, problem_id)
    
    if code_data:
        print("✓ 成功获取题目代码!")
        print("=" * 50)
        print("代码数据:")
        print(json.dumps(code_data, ensure_ascii=False, indent=2))
        
        # 保存到文件
        filename = f"problem_code_{problem_id}_test.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'problem_info': {
                        'id': problem_id,
                        'course_id': course_id,
                        'group_id': group_id
                    },
                    'code_data': code_data,
                    'timestamp': '2025-08-18'
                }, f, ensure_ascii=False, indent=2)
            print(f"\n代码数据已保存到文件: {filename}")
        except Exception as e:
            print(f"保存文件失败: {e}")
    else:
        print("✗ 获取代码失败")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 4:
        # 测试模式：python code_fetcher.py <course_id> <group_id> <problem_id>
        course_id = int(sys.argv[1])
        group_id = int(sys.argv[2])
        problem_id = int(sys.argv[3])
        fetch_specific_problem_code(course_id, group_id, problem_id)
    else:
        # 默认模式：查找第一个编程题目
        find_first_programming_problem()
        
        print("\n" + "-" * 50)
        print("提示：")
        print("  python code_fetcher.py                    # 查找第一个编程题目")
        print("  python code_fetcher.py 8717 114918 99764  # 获取指定题目代码")
