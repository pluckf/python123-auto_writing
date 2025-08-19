import requests
import json
import urllib3
import os

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 全局字典存储数据
course_ids = {}  # 存储课程数据的id
group_ids = {}   # 存储group数据的id

def save_data_ids(data):
    """
    从响应数据中提取并保存id到字典中
    """
    global course_ids, group_ids
    
    if isinstance(data, dict):
        # 检查是否包含_id或id字段
        id_field = None
        if '_id' in data:
            id_field = '_id'
        elif 'id' in data:
            id_field = 'id'
        
        if id_field:
            # 判断这是课程数据还是组数据
            if 'name' in data and 'code' in data and 'owner_name' in data:
                # 这是课程数据
                key = data.get('name', str(data[id_field]))
                course_ids[key] = data[id_field]
                print(f"保存课程ID: {key} -> {data[id_field]}")
            elif 'groups' in data or 'index' in data:
                # 这可能是组相关的数据
                if 'index' in data:  # 这是单个组
                    key = f"Group_{data.get('index', data[id_field])}"
                    group_ids[key] = data[id_field]
                    print(f"保存组ID: {key} -> {data[id_field]}")
            else:
                # 其他包含id的数据，保存到课程id中
                key = data.get('name', data.get('title', str(data[id_field])))
                course_ids[key] = data[id_field]
                print(f"保存数据ID: {key} -> {data[id_field]}")
        
        # 特殊处理groups数组
        if 'groups' in data and isinstance(data['groups'], list):
            for group in data['groups']:
                if isinstance(group, dict) and '_id' in group:
                    key = f"Group_{group.get('index', group['_id'])}"
                    group_ids[key] = group['_id']
                    print(f"保存组ID: {key} -> {group['_id']}")
        
        # 递归处理其他字段
        for key, value in data.items():
            if key not in ['groups']:  # groups已经特殊处理过了
                save_data_ids(value)
    
    elif isinstance(data, list):
        for item in data:
            save_data_ids(item)

def get_course_problems(course_id, group_id):
    """
    请求指定课程组的问题列表
    仅供学习使用
    """
    url = f"https://python123.io/api/v1/student/courses/{course_id}/groups/{group_id}/problems"
    
    # 根据提供的请求头信息构建headers
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMTY1MzA4MzQ3MUBxcS5jb20iLCJuYW1lIjoi5aec6L-c5bCaIiwiaWQiOiIxMjQzOTYxIiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTEyODY0MjcwfSwiaWF0IjoxNzU1NTE1MjU1LCJleHAiOjE3NTY4MTEyNTV9.4CFizZ4KvcRwad7ACdvSPfG0Kf3epPQYJdwiv_YUPps",
        "Connection": "keep-alive",
        "Cookie": "Hm_lvt_6f63cfeea8c9a84040e2c4389f01bb91=1755516075; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMTY1MzA4MzQ3MUBxcS5jb20iLCJuYW1lIjoi5aec6L-c5bCaIiwiaWQiOiIxMjQzOTYxIiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTEyODY0MjcwfSwiaWF0IjoxNzU1NTE1MjU1LCJleHAiOjE3NTY4MTEyNTV9.4CFizZ4KvcRwad7ACdvSPfG0Kf3epPQYJdwiv_YUPps; io=yt1DxQoARfnmCYByABjJ",
        "Host": "python123.io",
        "Referer": "https://python123.io/student/home",
    }
    
    # 从环境变量覆盖授权信息（如果存在）
    auth_token = os.environ.get("PYTHON123_AUTHORIZATION")
    cookie_string = os.environ.get("PYTHON123_COOKIE")
    if auth_token:
        headers["Authorization"] = auth_token
        print(f"使用环境变量中的Authorization: {auth_token[:50]}...")
    if cookie_string:
        headers["Cookie"] = cookie_string
        print(f"使用环境变量中的Cookie: {cookie_string[:50]}...")
    
    # 继续添加其他headers
    headers.update({
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    })
    
    try:
        print(f"正在发送请求到: {url}")
        print("请求方法: GET")
        print("-" * 50)
        
        # 发送GET请求，忽略SSL验证
        response = requests.get(url, headers=headers, verify=False)
        
        # 打印响应状态
        print(f"响应状态码: {response.status_code}")
        print(f"响应头Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print("-" * 50)
        
        # 打印响应内容
        if response.status_code == 200:
            print("请求成功!")
            try:
                # 尝试解析JSON响应
                json_data = response.json()
                print("响应内容 (JSON格式):")
                print(json.dumps(json_data, ensure_ascii=False, indent=2))
                return json_data
            except json.JSONDecodeError:
                print("响应内容 (文本格式):")
                print(response.text)
                return response.text
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print("响应内容:")
            print(response.text)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None
    except Exception as e:
        print(f"发生未预期的错误: {e}")
        return None

def get_student_courses():
    """
    请求python123.io的学生课程API
    仅供学习使用
    """
    url = "https://python123.io/api/v1/student/courses"
    
    # 根据提供的请求头信息构建headers
    headers = {
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
    
    # 从环境变量覆盖授权信息（如果存在）
    auth_token = os.environ.get("PYTHON123_AUTHORIZATION")
    cookie_string = os.environ.get("PYTHON123_COOKIE")
    if auth_token:
        headers["Authorization"] = auth_token
        print(f"使用环境变量中的Authorization: {auth_token[:50]}...")
    if cookie_string:
        headers["Cookie"] = cookie_string
        print(f"使用环境变量中的Cookie: {cookie_string[:50]}...")
    
    try:
        print("正在发送请求到:", url)
        print("请求方法: GET")
        print("-" * 50)
        
        # 创建session并配置
        session = requests.Session()
        session.verify = False  # 忽略SSL证书验证
        
        # 发送GET请求
        response = session.get(url, headers=headers, timeout=30)
        
        # 打印响应状态
        print(f"响应状态码: {response.status_code}")
        print(f"响应头Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print("-" * 50)
        
        # 打印响应内容
        if response.status_code == 200:
            print("请求成功!")
            try:
                # 尝试解析JSON响应
                json_data = response.json()
                print("响应内容 (JSON格式):")
                print(json.dumps(json_data, ensure_ascii=False, indent=2))
                
                # 提取并保存id数据
                print("\n" + "="*50)
                print("开始提取并保存ID数据...")
                print("="*50)
                
                # 检查响应结构并提取data
                if 'data' in json_data:
                    save_data_ids(json_data['data'])
                else:
                    # 如果没有data字段，直接处理整个响应
                    save_data_ids(json_data)
                
                # 显示保存的数据
                print("\n" + "-"*30)
                print("保存的课程ID字典:")
                print(json.dumps(course_ids, ensure_ascii=False, indent=2))
                
                print("\n" + "-"*30)
                print("保存的组ID字典:")
                print(json.dumps(group_ids, ensure_ascii=False, indent=2))
                
                return json_data
                
            except json.JSONDecodeError:
                print("响应内容 (文本格式):")
                print(response.text)
                return response.text
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print("响应内容:")
            print(response.text)
            return None
            
    except requests.exceptions.SSLError as e:
        print(f"SSL错误: {e}")
        print("尝试使用不验证SSL证书的方式...")
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None
    except Exception as e:
        print(f"发生未预期的错误: {e}")
        return None

def get_saved_data():
    """
    获取保存的ID数据
    """
    return {
        "course_ids": course_ids,
        "group_ids": group_ids
    }

def get_course_id_by_name(course_name):
    """
    根据课程名称获取课程ID
    """
    return course_ids.get(course_name, None)

def get_group_id_by_index(group_index):
    """
    根据组索引获取组ID
    """
    group_key = f"Group_{group_index}"
    return group_ids.get(group_key, None)

def save_data_to_file(filename="python123_ids.json"):
    """
    将保存的ID数据写入JSON文件
    """
    try:
        data = {
            "course_ids": course_ids,
            "group_ids": group_ids,
            "timestamp": "2025-08-18",  # 数据获取时间
            "api_url": "https://python123.io/api/v1/student/courses"
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到文件: {filename}")
        return True
    except Exception as e:
        print(f"保存文件时发生错误: {e}")
        return False

def load_data_from_file(filename="python123_ids.json"):
    """
    从JSON文件加载ID数据
    """
    global course_ids, group_ids
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        course_ids.update(data.get('course_ids', {}))
        group_ids.update(data.get('group_ids', {}))
        
        print(f"数据已从文件加载: {filename}")
        print(f"加载了 {len(course_ids)} 个课程ID 和 {len(group_ids)} 个组ID")
        return True
    except Exception as e:
        print(f"加载文件时发生错误: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Python123.io API 请求工具")
    print("仅供学习使用")
    print("=" * 60)
    
    # 发送请求并获取数据
    result = get_student_courses()
    
    if result:
        print("\n" + "="*60)
        print("数据提取完成!")
        print("="*60)
        
        # 获取保存的数据
        saved_data = get_saved_data()
        
        print(f"共保存了 {len(saved_data['course_ids'])} 个课程ID")
        print(f"共保存了 {len(saved_data['group_ids'])} 个组ID")
        
        # 保存数据到文件
        print("\n正在保存数据到JSON文件...")
        save_data_to_file()
        
        print("\n你可以通过以下方式访问保存的数据:")
        print("- course_ids: 包含所有课程相关的ID")
        print("- group_ids: 包含所有组相关的ID")
        
        # 演示如何使用保存的数据
        print("\n" + "-"*40)
        print("使用示例:")
        if course_ids:
            first_course_name = list(course_ids.keys())[0]
            first_course_id = course_ids[first_course_name]
            print(f"通过名称获取课程ID: get_course_id_by_name('{first_course_name}') = {first_course_id}")
        
        if group_ids:
            print(f"通过索引获取组ID: get_group_id_by_index(1) = {get_group_id_by_index(1)}")
        
        print(f"\n总共有 {len(course_ids)} 个课程:")
        for name, id_val in course_ids.items():
            print(f"  - {name}: {id_val}")
        
        print(f"\n总共有 {len(group_ids)} 个组 (仅显示前10个):")
        for i, (name, id_val) in enumerate(list(group_ids.items())[:10]):
            print(f"  - {name}: {id_val}")
        if len(group_ids) > 10:
            print(f"  ... 还有 {len(group_ids) - 10} 个组")
            
        # 测试访问课程组问题
        if result and 'data' in result and len(result['data']) > 0:
            print("\n" + "=" * 60)
            print("开始测试访问课程组问题...")
            print("=" * 60)
            
            # 获取第一个课程的信息
            first_course = result['data'][0]
            course_id = first_course['_id']
            course_name = first_course['name']
            
            print(f"测试课程: {course_name} (ID: {course_id})")
            
            # 获取第一个组的信息
            if 'groups' in first_course and len(first_course['groups']) > 0:
                first_group = first_course['groups'][0]
                group_id = first_group['_id']
                group_index = first_group['index']
                
                print(f"测试组: Group_{group_index} (ID: {group_id})")
                print("-" * 50)
                
                # 访问这个组的问题列表
                problems_data = get_course_problems(course_id, group_id)
                
                if problems_data:
                    print("\n" + "=" * 60)
                    print("问题数据获取成功!")
                    print("=" * 60)
                else:
                    print("\n问题数据获取失败")
            else:
                print("该课程没有组信息")
                
    else:
        print("\n请求失败，没有获取到数据")