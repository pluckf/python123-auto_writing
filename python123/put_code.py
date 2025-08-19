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
    "sec-ch-ua-platform": '"Windows"',
    "Content-Type": "application/json"  # PUT请求需要设置Content-Type
}

def get_problem_code(course_id, group_id, problem_id):
    """获取指定题目的代码"""
    url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/code"
    
    try:
        response = requests.get(url, headers=HEADERS, verify=False)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"GET请求失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"GET请求发生错误: {e}")
        return None

def put_problem_code(course_id, group_id, problem_id, code_content):
    """通过PUT请求发送代码"""
    url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/code"
    
    # 构建PUT请求的数据
    put_data = {
        "code": code_content
    }
    
    try:
        print(f"正在发送PUT请求到: {url}")
        print(f"发送的代码内容: {code_content}")
        print("-" * 50)
        
        response = requests.put(url, headers=HEADERS, json=put_data, verify=False)
        
        print(f"PUT响应状态码: {response.status_code}")
        print(f"PUT响应头Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code in [200, 201, 204]:  # 常见的成功状态码
            print("✓ PUT请求成功!")
            try:
                response_data = response.json()
                print("PUT响应内容:")
                print(json.dumps(response_data, ensure_ascii=False, indent=2))
                return response_data
            except json.JSONDecodeError:
                print("PUT响应内容 (文本格式):")
                print(response.text)
                return response.text
        else:
            print(f"✗ PUT请求失败，状态码: {response.status_code}")
            print("响应内容:")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"PUT请求发生错误: {e}")
        return None

def load_problem_ids(filename="problem_ids.json"):
    """从文件加载问题ID数据"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('problem_ids', {})
    except Exception as e:
        print(f"加载问题ID文件失败: {e}")
        return {}

def test_put_specific_problem():
    """测试PUT请求发送指定题目的代码"""
    print("=" * 60)
    print("Python123.io 代码PUT请求测试工具")
    print("仅供学习使用")
    print("=" * 60)
    
    # 使用已知的编程题目数据
    course_id = 8717
    group_id = 114919
    problem_id = 99798
    
    print(f"测试题目信息:")
    print(f"  课程ID: {course_id}")
    print(f"  组ID: {group_id}")
    print(f"  题目ID: {problem_id}")
    print("-" * 50)
    
    # 第1步：获取当前代码
    print("第1步：获取当前代码")
    current_code_data = get_problem_code(course_id, group_id, problem_id)
    
    if not current_code_data or 'data' not in current_code_data:
        print("获取当前代码失败，无法继续测试")
        return
    
    current_code = current_code_data['data'].get('code', '')
    print(f"当前代码内容:")
    print(f"```python")
    print(f"{current_code}")
    print(f"```")
    
    # 第2步：准备要发送的代码（为了测试，我们可以稍微修改一下代码）
    print(f"\n第2步：准备PUT请求的代码")
    
    # 为了测试，我们在现有代码基础上添加一行注释
    test_code = current_code + "\n# PUT测试注释 - " + "2025-08-18"
    
    print(f"要发送的代码内容:")
    print(f"```python")
    print(f"{test_code}")
    print(f"```")
    
    # 第3步：发送PUT请求
    print(f"\n第3步：发送PUT请求")
    put_response = put_problem_code(course_id, group_id, problem_id, test_code)
    
    # 第4步：验证结果
    if put_response:
        print(f"\n第4步：验证PUT请求结果")
        print("-" * 50)
        
        # 重新获取代码验证是否更新成功
        updated_code_data = get_problem_code(course_id, group_id, problem_id)
        
        if updated_code_data and 'data' in updated_code_data:
            updated_code = updated_code_data['data'].get('code', '')
            print(f"更新后的代码内容:")
            print(f"```python")
            print(f"{updated_code}")
            print(f"```")
            
            if test_code.strip() == updated_code.strip():
                print("✓ 代码更新成功！PUT请求工作正常")
            else:
                print("⚠ 代码内容不完全匹配，可能存在格式差异")
                print("但PUT请求已成功执行")
        else:
            print("✗ 无法验证更新结果")
        
        # 保存结果到文件
        result_data = {
            'test_info': {
                'course_id': course_id,
                'group_id': group_id,
                'problem_id': problem_id,
                'test_time': '2025-08-18'
            },
            'original_code': current_code,
            'sent_code': test_code,
            'put_response': put_response,
            'verification': updated_code_data if 'updated_code_data' in locals() else None
        }
        
        try:
            filename = f"put_test_result_{problem_id}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            print(f"\n测试结果已保存到文件: {filename}")
        except Exception as e:
            print(f"保存测试结果失败: {e}")

def test_put_first_programming_problem():
    """测试PUT请求发送第一个编程题的代码（跳过choice题目）"""
    print("=" * 60)
    print("Python123.io 编程题代码PUT请求工具")
    print("仅供学习使用 - 跳过选择题")
    print("=" * 60)
    
    # 加载问题ID数据
    problem_ids = load_problem_ids()
    
    if not problem_ids:
        print("没有找到问题ID数据，使用已知编程题目进行测试")
        test_put_specific_problem()
        return
    
    print("正在查找第一个编程题目...")
    print("跳过 type='choice' 的选择题")
    print("-" * 50)
    
    # 已知的课程和组ID
    course_id = 8717
    group_id = 114918  # 使用第一个组
    
    # 遍历问题找到第一个编程题
    for course_name, course_data in problem_ids.items():
        for group_key, problems in course_data.items():
            for problem in problems:
                problem_id = problem['id']
                problem_name = problem['name']
                problem_type = problem['type']
                
                print(f"检查题目: {problem_name} (ID: {problem_id}, 类型: {problem_type})")
                
                if problem_type == 'choice':
                    print("  [跳过选择题]")
                    continue
                
                print("  [找到编程题，开始PUT测试]")
                
                # 获取当前代码
                current_code_data = get_problem_code(course_id, group_id, problem_id)
                
                if not current_code_data or 'data' not in current_code_data:
                    print("  获取代码失败")
                    continue
                
                current_code = current_code_data['data'].get('code', '')
                test_code = current_code + "\n# PUT测试 - " + "2025-08-18"
                
                print(f"  原始代码: {current_code}")
                print(f"  测试代码: {test_code}")
                
                # 发送PUT请求
                put_response = put_problem_code(course_id, group_id, problem_id, test_code)
                
                if put_response:
                    print("  ✓ PUT请求成功!")
                else:
                    print("  ✗ PUT请求失败")
                
                return  # 只测试第一个编程题
    
    print("没有找到编程题目")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 4:
        # 指定题目测试模式：python put_code.py <course_id> <group_id> <problem_id>
        course_id = int(sys.argv[1])
        group_id = int(sys.argv[2])
        problem_id = int(sys.argv[3])
        
        print("=" * 60)
        print("指定题目PUT测试")
        print("=" * 60)
        
        # 获取当前代码
        current_code_data = get_problem_code(course_id, group_id, problem_id)
        if current_code_data and 'data' in current_code_data:
            current_code = current_code_data['data'].get('code', '')
            test_code = current_code + "\n# PUT测试 - " + "2025-08-18"
            put_problem_code(course_id, group_id, problem_id, test_code)
        else:
            print("获取代码失败")
            
    elif len(sys.argv) > 1 and sys.argv[1] == "--auto":
        test_put_first_programming_problem()
    else:
        test_put_specific_problem()
        
        print("\n" + "-" * 50)
        print("提示：")
        print("  python put_code.py                    # 测试指定编程题PUT请求")
        print("  python put_code.py --auto             # 自动查找第一个编程题测试")
        print("  python put_code.py 8717 114918 99764  # 指定题目测试")
