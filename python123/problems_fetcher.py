import requests
import json
import time
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 全局变量用于保存问题ID
problem_ids = {}  # 用于保存问题ID的字典

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

def save_problem_ids(course_name, group_index, problems):
    """保存问题ID到全局字典中"""
    if course_name not in problem_ids:
        problem_ids[course_name] = {}
    
    group_key = f"group_{group_index}"
    problem_ids[course_name][group_key] = []
    
    for problem in problems:
        problem_id = problem.get('_id')
        problem_name = problem.get('name', '未命名')
        problem_type = problem.get('type', '未知类型')
        
        if problem_id:
            problem_ids[course_name][group_key].append({
                'id': problem_id,
                'name': problem_name,
                'type': problem_type
            })

def get_problem_ids_by_course(course_name):
    """获取指定课程的所有问题ID"""
    return problem_ids.get(course_name, {})

def get_problem_ids_by_group(course_name, group_index):
    """获取指定课程组的问题ID"""
    course_data = problem_ids.get(course_name, {})
    group_key = f"group_{group_index}"
    return course_data.get(group_key, [])

def save_problem_ids_to_file(filename="problem_ids.json"):
    """将问题ID字典保存到文件"""
    try:
        data = {
            "problem_ids": problem_ids,
            "timestamp": "2025-08-18",
            "api_base": BASE_URL
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"问题ID数据已保存到文件: {filename}")
        return True
    except Exception as e:
        print(f"保存问题ID文件时发生错误: {e}")
        return False

def load_problem_ids_from_file(filename="problem_ids.json"):
    """从文件加载问题ID数据"""
    global problem_ids
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        problem_ids.update(data.get('problem_ids', {}))
        
        print(f"问题ID数据已从文件加载: {filename}")
        return True
    except Exception as e:
        print(f"加载问题ID文件时发生错误: {e}")
        return False

def get_courses():
    """获取所有课程列表"""
    try:
        response = requests.get(BASE_URL, headers=HEADERS, verify=False)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"获取课程列表失败: {e}")
    return None

def get_course_problems(course_id, group_id):
    """获取指定课程组的问题列表"""
    url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems"
    try:
        response = requests.get(url, headers=HEADERS, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"获取问题列表失败: {e}")
    return None

def fetch_first_course_first_group():
    """测试功能：只获取第一个课程的第一个组的问题"""
    print("=" * 60)
    print("Python123.io 问题获取工具（测试版本）")
    print("仅供学习使用")
    print("=" * 60)
    
    # 获取课程列表
    courses_data = get_courses()
    if not courses_data or 'data' not in courses_data:
        print("获取课程列表失败")
        return
    
    courses = courses_data['data']
    if not courses:
        print("没有可用的课程")
        return
    
    # 获取第一个课程
    first_course = courses[0]
    course_id = first_course['_id']
    course_name = first_course['name']
    
    print(f"\n测试课程: {course_name} (ID: {course_id})")
    
    # 获取第一个组
    groups = first_course.get('groups', [])
    if not groups:
        print("该课程没有组")
        return
    
    first_group = groups[0]
    group_id = first_group['_id']
    group_index = first_group['index']
    
    print(f"测试组: Group_{group_index} (ID: {group_id})")
    print("-" * 50)
    
    # 获取问题列表
    problems_data = get_course_problems(course_id, group_id)
    
    if problems_data and 'data' in problems_data:
        problems = problems_data['data']
        print(f"\n成功获取 {len(problems)} 个问题:")
        print("-" * 50)
        
        # 保存问题ID到字典中
        save_problem_ids(course_name, group_index, problems)
        
        for i, problem in enumerate(problems, 1):
            problem_id = problem['_id']
            problem_name = problem.get('name', '未命名')
            problem_type = problem.get('type', '未知类型')
            problem_score = problem.get('score', 0)
            
            print(f"{i:2d}. {problem_name}")
            print(f"    ID: {problem_id} | 类型: {problem_type} | 分数: {problem_score}")
        
        # 保存到文件
        filename = f"problems_course_{course_id}_group_{group_id}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(problems_data, f, ensure_ascii=False, indent=2)
            print(f"\n数据已保存到文件: {filename}")
        except Exception as e:
            print(f"保存文件失败: {e}")
            
        # 保存问题ID字典到文件
        save_problem_ids_to_file()
        
        # 显示保存的问题ID
        print(f"\n保存的问题ID (课程: {course_name}, 组: {group_index}):")
        print("-" * 50)
        saved_problems = get_problem_ids_by_group(course_name, group_index)
        for i, prob in enumerate(saved_problems, 1):
            print(f"{i:2d}. ID: {prob['id']} | {prob['name']} ({prob['type']})")
            
    else:
        print("获取问题数据失败")

def fetch_all_problems():
    """获取所有课程所有组的问题（完整版本）"""
    print("=" * 60)
    print("Python123.io 问题获取工具（完整版本）")
    print("仅供学习使用 - 将获取所有课程的所有问题")
    print("=" * 60)
    
    # 获取课程列表
    courses_data = get_courses()
    if not courses_data or 'data' not in courses_data:
        print("获取课程列表失败")
        return
    
    courses = courses_data['data']
    all_problems = {}
    
    for course in courses:
        course_id = course['_id']
        course_name = course['name']
        groups = course.get('groups', [])
        
        print(f"\n正在处理课程: {course_name} (ID: {course_id})")
        print(f"该课程有 {len(groups)} 个组")
        
        course_problems = {}
        
        for group in groups:
            group_id = group['_id']
            group_index = group['index']
            
            print(f"  正在获取 Group_{group_index} (ID: {group_id}) 的问题...")
            
            # 获取该组的问题
            problems_data = get_course_problems(course_id, group_id)
            
            if problems_data and 'data' in problems_data:
                problems = problems_data['data']
                course_problems[f"group_{group_index}"] = {
                    'group_id': group_id,
                    'problems_count': len(problems),
                    'problems': problems
                }
                
                # 保存问题ID到字典中
                save_problem_ids(course_name, group_index, problems)
                
                print(f"    ✓ 获取到 {len(problems)} 个问题")
            else:
                print(f"    ✗ 获取问题失败")
        
        all_problems[course_name] = {
            'course_id': course_id,
            'groups': course_problems
        }
    
    # 保存所有数据
    filename = "all_problems_data.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_problems, f, ensure_ascii=False, indent=2)
        print(f"\n所有问题数据已保存到文件: {filename}")
        
        # 统计信息
        total_problems = 0
        for course_name, course_data in all_problems.items():
            course_total = sum(group_data['problems_count'] for group_data in course_data['groups'].values())
            total_problems += course_total
            print(f"课程 '{course_name}': {course_total} 个问题")
        
        print(f"\n总计获取了 {total_problems} 个问题")
        
        # 保存问题ID字典到文件
        save_problem_ids_to_file()
        
        # 显示保存的问题ID统计
        print(f"\n问题ID保存统计:")
        print("-" * 30)
        for course_name in problem_ids:
            course_problem_count = sum(len(group_data) for group_data in problem_ids[course_name].values())
            print(f"课程 '{course_name}': {course_problem_count} 个问题ID")
        
    except Exception as e:
        print(f"保存文件失败: {e}")

def show_saved_problem_ids():
    """显示已保存的所有问题ID"""
    if not problem_ids:
        print("没有保存的问题ID数据")
        return
    
    print("=" * 60)
    print("保存的问题ID汇总")
    print("=" * 60)
    
    for course_name, course_data in problem_ids.items():
        print(f"\n课程: {course_name}")
        print("-" * 50)
        
        for group_key, problems in course_data.items():
            print(f"\n  {group_key.upper()}:")
            for i, problem in enumerate(problems, 1):
                print(f"    {i:2d}. ID: {problem['id']} | {problem['name']} ({problem['type']})")

if __name__ == "__main__":
    # 可以选择运行测试版本或完整版本
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            fetch_all_problems()
        elif sys.argv[1] == "--show":
            # 先尝试从文件加载数据
            load_problem_ids_from_file()
            show_saved_problem_ids()
        else:
            print("使用方法:")
            print("  python problems_fetcher.py          # 获取第一个课程第一个组的问题")
            print("  python problems_fetcher.py --all    # 获取所有课程所有组的问题")
            print("  python problems_fetcher.py --show   # 显示已保存的问题ID")
    else:
        fetch_first_course_first_group()
        
        print("\n" + "-" * 50)
        print("提示：更多使用选项：")
        print("  python problems_fetcher.py --all    # 获取所有课程的所有问题")
        print("  python problems_fetcher.py --show   # 显示已保存的问题ID")
        print("注意：完整获取可能需要较长时间")
