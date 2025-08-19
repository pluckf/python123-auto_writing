import requests
import json
import time
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
    "Content-Type": "application/json"
}

# 全局数据存储
course_ids = {}
course_group_mapping = {}  # 存储课程与组的正确映射关系：{course_name: {group_index: group_id}}
problem_ids = {}
programming_codes = {}
explanation_contents = {}  # 存储题目的explanation_content
all_results = {}

class Python123Manager:
    """Python123.io API管理器 - 一站式解决方案"""
    
    def __init__(self):
        self.session_data = {
            'courses': {},
            'problems': {},
            'codes': {},
            'put_results': {}
        }
    
    def log_step(self, step_num, description):
        """打印步骤信息"""
        print(f"\n{'='*60}")
        print(f"第{step_num}步: {description}")
        print('='*60)
    
    def log_substep(self, description):
        """打印子步骤信息"""
        print(f"\n{'-'*50}")
        print(f">>> {description}")
        print('-'*50)
    
    def get_courses(self):
        """步骤1：获取所有课程列表"""
        try:
            response = requests.get(BASE_URL, headers=HEADERS, verify=False)
            if response.status_code == 200:
                data = response.json()
                self.session_data['courses'] = data
                return data
        except Exception as e:
            print(f"获取课程列表失败: {e}")
        return None
    
    def extract_course_and_group_ids(self, courses_data):
        """步骤2：提取并保存课程和组ID"""
        global course_ids, course_group_mapping
        
        if not courses_data or 'data' not in courses_data:
            return False
        
        courses = courses_data['data']
        total_groups = 0
        
        for course in courses:
            course_id = course['_id']
            course_name = course['name']
            groups = course.get('groups', [])
            
            # 保存课程ID
            course_ids[course_name] = course_id
            print(f"保存课程ID: {course_name} -> {course_id}")
            
            # 为每个课程建立组映射
            course_group_mapping[course_name] = {}
            
            # 保存组ID（按课程分组）
            for group in groups:
                group_id = group['_id']
                group_index = group['index']
                
                course_group_mapping[course_name][group_index] = group_id
                print(f"保存组ID: {course_name} - Group_{group_index} -> {group_id}")
                total_groups += 1
        
        print(f"✅ 保存了 {len(course_ids)} 个课程ID 和 {total_groups} 个组ID")
        return True
    
    def get_all_problems(self, courses_data):
        """步骤3：获取所有问题数据"""
        global problem_ids
        
        if not courses_data or 'data' not in courses_data:
            return False
        
        courses = courses_data['data']
        
        for course in courses:
            course_id = course['_id']
            course_name = course['name']
            groups = course.get('groups', [])
            
            print(f"\n处理课程: {course_name} (ID: {course_id})")
            
            if course_name not in problem_ids:
                problem_ids[course_name] = {}
            
            for group in groups:
                group_id = group['_id']
                group_index = group['index']
                
                print(f"  获取 Group_{group_index} (ID: {group_id}) 的问题...")
                
                # 获取该组的问题
                problems_data = self.get_course_problems(course_id, group_id)
                
                if problems_data and 'data' in problems_data:
                    problems = problems_data['data']
                    problem_ids[course_name][f"group_{group_index}"] = []
                    
                    for problem in problems:
                        problem_id = problem.get('_id')
                        problem_name = problem.get('name', '未命名')
                        problem_type = problem.get('type', '未知类型')
                        
                        if problem_id:
                            problem_ids[course_name][f"group_{group_index}"].append({
                                'id': problem_id,
                                'name': problem_name,
                                'type': problem_type
                            })
                    
                    print(f"    ✓ 获取到 {len(problems)} 个问题")
                else:
                    print(f"    ✗ 获取问题失败")
                
                # 添加延时避免请求过快
                
        
        return True
    
    def get_course_problems(self, course_id, group_id):
        """获取指定课程组的问题列表"""
        url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems"
        try:
            response = requests.get(url, headers=HEADERS, verify=False)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"获取问题列表失败: {e}")
        return None
    
    def get_problem_code(self, course_id, group_id, problem_id):
        """获取指定题目的代码"""
        url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/code"
        try:
            response = requests.get(url, headers=HEADERS, verify=False)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"获取代码失败: {e}")
        return None
    
    def get_problem_details(self, course_id, group_id, problem_id):
        """获取指定题目的详细信息（包括explanation_content）"""
        url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}"
        try:
            response = requests.get(url, headers=HEADERS, verify=False)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"获取题目详情失败: {e}")
        return None
    
    def put_problem_code(self, course_id, group_id, problem_id, code_content):
        """通过PUT请求发送代码"""
        url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/code"
        put_data = {"code": code_content}
        
        try:
            response = requests.put(url, headers=HEADERS, json=put_data, verify=False)
            if response.status_code in [200, 201, 204]:
                try:
                    return response.json()
                except:
                    return {"success": True, "text": response.text}
        except Exception as e:
            print(f"PUT请求失败: {e}")
        return None
    
    def get_all_programming_codes(self):
        """步骤4：获取所有编程题的代码（跳过选择题）"""
        global programming_codes
        
        if not problem_ids:
            print("没有问题数据，无法获取代码")
            return False
        
        programming_count = 0
        
        for course_name, course_data in problem_ids.items():
            print(f"\n处理课程: {course_name}")
            programming_codes[course_name] = {}
            
            for group_key, problems in course_data.items():
                print(f"  处理 {group_key}...")
                programming_codes[course_name][group_key] = {}
                
                for problem in problems:
                    problem_id = problem['id']
                    problem_name = problem['name']
                    problem_type = problem['type']
                    
                    # 跳过选择题
                    if problem_type == 'choice':
                        print(f"    跳过选择题: {problem_name}")
                        continue
                    
                    print(f"    获取编程题代码: {problem_name} (ID: {problem_id})")
                    
                    # 获取课程ID和组ID
                    course_id = course_ids.get(course_name)
                    group_index = int(group_key.replace('group_', ''))
                    group_id = course_group_mapping.get(course_name, {}).get(group_index)
                    
                    if not course_id or not group_id:
                        print(f"      ✗ 缺少课程或组ID信息: course_id={course_id}, group_id={group_id}")
                        continue
                    
                    # 获取代码
                    code_data = self.get_problem_code(course_id, group_id, problem_id)
                    
                    if code_data and 'data' in code_data:
                        actual_code = code_data['data'].get('code', '')
                        programming_codes[course_name][group_key][problem_id] = {
                            'name': problem_name,
                            'code': actual_code,
                            'full_data': code_data
                        }
                        print(f"      ✓ 代码获取成功")
                        programming_count += 1
                    else:
                        print(f"      ✗ 代码获取失败")
        
        print(f"\n总计获取了 {programming_count} 个编程题的代码")
        return programming_count > 0
    
    def get_all_explanation_contents(self):
        """获取所有题目的explanation_content"""
        global explanation_contents
        
        if not problem_ids:
            print("没有问题数据，无法获取explanation_content")
            return False
        
        explanation_count = 0
        
        for course_name, course_data in problem_ids.items():
            print(f"\n获取课程 {course_name} 的题目说明...")
            explanation_contents[course_name] = {}
            
            for group_key, problems in course_data.items():
                print(f"  处理 {group_key}...")
                explanation_contents[course_name][group_key] = {}
                
                for problem in problems:
                    problem_id = problem['id']
                    problem_name = problem['name']
                    problem_type = problem['type']
                    
                    print(f"    获取题目说明: {problem_name} (ID: {problem_id})")
                    
                    # 获取课程ID和组ID
                    course_id = course_ids.get(course_name)
                    group_index = int(group_key.replace('group_', ''))
                    group_id = course_group_mapping.get(course_name, {}).get(group_index)
                    
                    if not course_id or not group_id:
                        print(f"      ✗ 缺少课程或组ID信息: course_id={course_id}, group_id={group_id}")
                        continue
                    
                    # 获取题目详情
                    problem_details = self.get_problem_details(course_id, group_id, problem_id)
                    
                    if problem_details and 'data' in problem_details:
                        explanation_content = problem_details['data'].get('explanation_content', '')
                        explanation_contents[course_name][group_key][problem_id] = {
                            'name': problem_name,
                            'type': problem_type,
                            'explanation_content': explanation_content,
                            'full_data': problem_details
                        }
                        print(f"      ✓ 题目说明获取成功")
                        explanation_count += 1
                    else:
                        print(f"      ✗ 题目说明获取失败")
        
        print(f"\n总计获取了 {explanation_count} 个题目的说明")
        return explanation_count > 0
    
    def test_put_requests(self, test_count=1):
        """步骤5：测试PUT请求（只测试指定数量的题目）"""
        put_results = {}
        tested_count = 0
        
        for course_name, course_data in programming_codes.items():
            if tested_count >= test_count:
                break
                
            print(f"\n测试课程: {course_name}")
            
            for group_key, group_data in course_data.items():
                if tested_count >= test_count:
                    break
                    
                print(f"  测试 {group_key}...")
                
                for problem_id, problem_data in group_data.items():
                    if tested_count >= test_count:
                        break
                    
                    problem_name = problem_data['name']
                    original_code = problem_data['code']
                    
                    print(f"    测试PUT: {problem_name} (ID: {problem_id})")
                    
                    # 准备测试代码（添加注释）
                    test_code = original_code + f"\n# PUT测试 - {time.strftime('%Y-%m-%d %H:%M:%S')}"
                    
                    # 获取课程ID和组ID
                    course_id = course_ids.get(course_name)
                    group_index = int(group_key.replace('group_', ''))
                    group_id = course_group_mapping.get(course_name, {}).get(group_index)
                    
                    if not course_id or not group_id:
                        print(f"      ✗ 缺少ID信息: course_id={course_id}, group_id={group_id}")
                        continue
                    
                    # 发送PUT请求
                    put_result = self.put_problem_code(course_id, group_id, problem_id, test_code)
                    
                    if put_result:
                        print(f"      ✓ PUT请求成功")
                        put_results[problem_id] = {
                            'name': problem_name,
                            'course_name': course_name,
                            'group_key': group_key,
                            'original_code': original_code,
                            'sent_code': test_code,
                            'result': put_result,
                            'success': True
                        }
                    else:
                        print(f"      ✗ PUT请求失败")
                        put_results[problem_id] = {
                            'name': problem_name,
                            'success': False
                        }
                    
                    tested_count += 1
        
        self.session_data['put_results'] = put_results
        return put_results
    
    def save_all_data(self):
        """步骤6：保存所有数据到文件"""
        # 计算总组数
        total_groups = sum(len(groups) for groups in course_group_mapping.values())
        
        all_data = {
            'session_info': {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_courses': len(course_ids),
                'total_groups': total_groups,
                'total_programming_problems': sum(len(group_data) for course_data in programming_codes.values() for group_data in course_data.values()),
                'total_explanation_contents': sum(len(group_data) for course_data in explanation_contents.values() for group_data in course_data.values())
            },
            'course_ids': course_ids,
            'course_group_mapping': course_group_mapping,
            'problem_ids': problem_ids,
            'programming_codes': programming_codes,
            'explanation_contents': explanation_contents,
            'session_data': self.session_data
        }
        
        # 保存完整数据
        filename = f"python123_complete_session_{int(time.time())}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            print(f"完整会话数据已保存: {filename}")
        except Exception as e:
            print(f"保存数据失败: {e}")
        
        # 保存简化的统计报告
        report = {
            'summary': all_data['session_info'],
            'courses': list(course_ids.keys()),
            'programming_problems_count': all_data['session_info']['total_programming_problems'],
            'put_test_results': self.session_data.get('put_results', {}),
            'successful_puts': len([r for r in self.session_data.get('put_results', {}).values() if r.get('success', False)])
        }
        
        report_filename = f"session_report_{int(time.time())}.json"
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"会话报告已保存: {report_filename}")
        except Exception as e:
            print(f"保存报告失败: {e}")
    
    def run_complete_workflow(self, put_test_count=1):
        """运行完整的工作流程"""
        print("🚀 开始执行 Python123.io 完整工作流程")
        print("仅供学习使用")
        print("="*80)
        
        # 步骤1：获取课程列表
        self.log_step(1, "获取课程列表")
        courses_data = self.get_courses()
        
        if not courses_data:
            print("❌ 获取课程列表失败，程序终止")
            return False
        
        courses = courses_data.get('data', [])
        print(f"✅ 成功获取 {len(courses)} 个课程")
        
        # 步骤2：提取ID数据
        self.log_step(2, "提取并保存课程和组ID")
        if not self.extract_course_and_group_ids(courses_data):
            print("❌ 提取ID数据失败，程序终止")
            return False
        
        # 已在 extract_course_and_group_ids 中打印了完整信息
        
        # 步骤3：获取所有问题
        self.log_step(3, "获取所有问题数据")
        if not self.get_all_problems(courses_data):
            print("❌ 获取问题数据失败，程序终止")
            return False
        
        total_problems = sum(len(group_data) for course_data in problem_ids.values() for group_data in course_data.values())
        print(f"✅ 成功获取 {total_problems} 个问题")
        
        # 步骤4：获取编程题代码
        self.log_step(4, "获取编程题代码（跳过选择题）")
        if not self.get_all_programming_codes():
            print("❌ 获取编程题代码失败")
        else:
            print("✅ 编程题代码获取完成")
        
        # 步骤4.5：获取所有题目的explanation_content
        self.log_step("4.5", "获取所有题目的说明内容（explanation_content）")
        if not self.get_all_explanation_contents():
            print("❌ 获取题目说明失败")
        else:
            print("✅ 题目说明获取完成")
        
        # 步骤5：测试PUT请求
        self.log_step(5, f"测试PUT请求（测试 {put_test_count} 个题目）")
        put_results = self.test_put_requests(put_test_count)
        successful_puts = len([r for r in put_results.values() if r.get('success', False)])
        print(f"✅ PUT测试完成，成功 {successful_puts}/{len(put_results)} 个请求")
        
        # 步骤6：保存数据
        self.log_step(6, "保存所有数据到文件")
        self.save_all_data()
        print("✅ 数据保存完成")
        
        # 最终总结
        print("\n" + "="*80)
        print("🎉 完整工作流程执行完毕！")
        print("="*80)
        print(f"📊 统计信息:")
        print(f"   - 课程数量: {len(course_ids)}")
        total_groups = sum(len(groups) for groups in course_group_mapping.values())
        print(f"   - 组数量: {total_groups}")
        print(f"   - 总问题数: {total_problems}")
        print(f"   - 编程题数: {sum(len(group_data) for course_data in programming_codes.values() for group_data in course_data.values())}")
        print(f"   - PUT成功数: {successful_puts}")
        print("="*80)
        
        return True

def main():
    """主函数"""
    import sys
    
    # 创建管理器实例
    manager = Python123Manager()
    
    if len(sys.argv) > 1:
        try:
            put_test_count = int(sys.argv[1])
        except ValueError:
            put_test_count = 1
            print("参数无效，使用默认值测试1个题目")
    else:
        put_test_count = 1
    
    print(f"将测试 {put_test_count} 个编程题的PUT请求")
    
    # 运行完整工作流程
    success = manager.run_complete_workflow(put_test_count)
    
    if success:
        print("\n🎯 所有操作成功完成！")
        print("💾 检查生成的文件:")
        print("   - python123_complete_session_*.json (完整数据)")
        print("   - session_report_*.json (简化报告)")
    else:
        print("\n❌ 工作流程执行失败")
    
    print("\n" + "-"*60)
    print("使用方法:")
    print("  python run_all.py     # 测试1个题目的PUT请求")
    print("  python run_all.py 3   # 测试3个题目的PUT请求")
    print("  python run_all.py 0   # 不测试PUT请求，只获取数据")

if __name__ == "__main__":
    main()
