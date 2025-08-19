#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全Group测试工具
自动测试所有可用的group，获取explanation_content，提取代码，批量提交并获取测试结果
"""
import requests
import json
import re
import time
import urllib3
import os
from datetime import datetime
import glob
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AllGroupTester:
    def __init__(self, auth_token=None, cookie=None):
        """初始化测试工具"""
        # 默认配置
        self.BASE_URL = "https://python123.io/api/v1/student/courses"
        
        # 优先使用环境变量，如果没有则使用传入参数或默认值
        self.auth_token = (os.environ.get("PYTHON123_AUTHORIZATION") or 
                          auth_token or 
                          "***OiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMTY1MzA4MzQ3MUBxcS5jb20iLCJuYW1lIjoi5aec6L-c5bCaIiwiaWQiOiIxMjQzOTYxIiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTEyODY0MjcwfSwiaWF0IjoxNzU1NTE1MjU1LCJleHAiOjE3NTY4MTEyNTV9.4CFizZ4KvcRwad7ACdvSPfG0Kf3epPQYJdwiv_YUPps")
        
        self.cookie = (os.environ.get("PYTHON123_COOKIE") or 
                      cookie or 
                      "token=eyJhbGciOiJIU**1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMTY1MzA4MzQ3MUBxcS5jb20iLCJuYW1lIjoi5aec6L-c5bCaIiwiaWQiOiIxMjQzOTYxIiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTEyODY0MjcwfSwiaWF0IjoxNzU1NTE1MjU1LCJleHAiOjE3NTY4MTEyNTV9.4CFizZ4KvcRwad7ACdvSPfG0Kf3epPQYJdwiv_YUPps; Hm_lvt_6f63cfeea8c9a84040e2c4389f01bb91=1755516075,1755522844; HMACCOUNT=3EE86EE065B9114B; Hm_lpvt_6f63cfeea8c9a84040e2c4389f01bb91=1755528898; io=VqDxjqf6eE8qFv9cABv0")
        
        # 如果使用了环境变量，打印提示信息
        if os.environ.get("PYTHON123_AUTHORIZATION"):
            print(f"使用环境变量中的Authorization: {self.auth_token[:50]}...")
        if os.environ.get("PYTHON123_COOKIE"):
            print(f"使用环境变量中的Cookie: {self.cookie[:50]}...")
        
        # 去除 Bearer 前缀（如果存在），因为后面会重新添加
        if self.auth_token.startswith("Bearer "):
            self.auth_token = self.auth_token[7:]
        
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Cookie": self.cookie
        }
        
        # 数据存储
        self.course_ids = {}
        self.course_group_mapping = {}
        self.all_problems = {}
        self.extracted_codes = {}
        self.submission_results = {}
        self.test_summary = {
            'total_groups': 0,
            'total_problems': 0,
            'total_programming_problems': 0,
            'successful_extractions': 0,
            'successful_submissions': 0,
            'groups_tested': [],
            'errors': []
        }
    
    def update_credentials(self, auth_token, cookie):
        """更新认证凭据"""
        self.auth_token = auth_token
        self.cookie = cookie
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json", 
            "Connection": "keep-alive",
            "Cookie": cookie
        }
        print(f"✅ 已更新认证凭据")
    
    def load_session_data(self):
        """加载会话数据"""
        try:
            # 首先尝试查找完整会话文件
            session_files = glob.glob('python123_complete_session_*.json')
            if session_files:
                latest_file = max(session_files)
                print(f"📂 使用完整会话文件: {latest_file}")
                with open(latest_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                self.course_ids = session_data.get('course_ids', {})
                self.course_group_mapping = session_data.get('course_group_mapping', {})
                
                print(f"📊 加载了 {len(self.course_ids)} 个课程")
                return True
            
            # 如果没有完整会话文件，尝试读取main.py生成的基础数据文件
            elif os.path.exists('python123_ids.json'):
                print(f"📂 使用基础数据文件: python123_ids.json")
                with open('python123_ids.json', 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                self.course_ids = session_data.get('course_ids', {})
                group_ids = session_data.get('group_ids', {})
                
                # 从group_ids构建course_group_mapping
                if self.course_ids and group_ids:
                    print("📊 正在构建课程-组映射关系...")
                    
                    # 首先尝试从API获取详细映射
                    api_success = False
                    for course_name, course_id in self.course_ids.items():
                        try:
                            course_data = self._get_course_detail(course_id)
                            if course_data and 'groups' in course_data:
                                group_list = [group['_id'] for group in course_data['groups']]
                                self.course_group_mapping[course_id] = group_list
                                print(f"   ✓ {course_name}: {len(group_list)} 个组")
                                api_success = True
                        except Exception as e:
                            print(f"   ⚠️ 获取课程 {course_name} 的组信息失败: {e}")
                    
                    # 如果API请求失败，使用简单的映射策略
                    if not api_success:
                        print("   ⚠️ API请求失败，使用简化映射策略...")
                        # 将所有group_ids分配给第一个课程
                        if self.course_ids:
                            first_course_id = list(self.course_ids.values())[0]
                            all_group_ids = list(group_ids.values())
                            self.course_group_mapping[first_course_id] = all_group_ids
                            first_course_name = list(self.course_ids.keys())[0]
                            print(f"   ✓ {first_course_name}: {len(all_group_ids)} 个组 (简化映射)")
                
                print(f"📊 加载了 {len(self.course_ids)} 个课程，{sum(len(groups) for groups in self.course_group_mapping.values())} 个组")
                return True
            else:
                print("❌ 未找到会话文件，请先运行main.py获取课程数据")
                print("   需要文件: python123_complete_session_*.json 或 python123_ids.json")
                return False
        except Exception as e:
            print(f"❌ 加载会话数据失败: {e}")
            return False
    
    def _get_course_detail(self, course_id):
        """获取课程详细信息，包括组数据"""
        url = f"{self.BASE_URL}/{course_id}"
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Cookie": self.cookie
        }
        
        try:
            response = requests.get(url, headers=headers, verify=False, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    return data.get('data')
            return None
        except Exception as e:
            print(f"   ❌ 获取课程详情失败: {e}")
            return None

    def get_all_group_problems(self):
        """获取所有group的问题"""
        print(f"\n🔍 开始扫描所有group...")
        print("=" * 80)
        
        for course_name, course_id in self.course_ids.items():
            print(f"\n📚 课程: {course_name} (ID: {course_id})")
            
            group_mapping = self.course_group_mapping.get(course_id, [])
            if not group_mapping:
                print(f"   ⚠️  未找到group映射信息")
                continue
            
            # 如果group_mapping是列表（简化映射），创建索引映射
            if isinstance(group_mapping, list):
                group_items = [(i+1, group_id) for i, group_id in enumerate(group_mapping)]
            else:
                # 按group编号排序（原有逻辑）
                group_items = sorted(group_mapping.items(), key=lambda x: int(x[0]))
            
            for group_index, group_id in group_items:
                group_name = f"group_{group_index}"
                group_key = f"{course_name}_{group_name}"  # 定义group_key
                print(f"\n   📁 {group_name} (ID: {group_id})")
                
                try:
                    # 获取group的问题列表
                    url = f"{self.BASE_URL}/{course_id}/groups/{group_id}/problems"
                    response = requests.get(url, headers=self.headers, verify=False)
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        group_problems = response_data.get('data', [])
                        print(f"      📝 找到 {len(group_problems)} 个题目")
                        
                        # 统计题目类型
                        programming_count = len([p for p in group_problems if p.get('type') == 'programming'])
                        choice_count = len([p for p in group_problems if p.get('type') == 'choice'])
                        
                        print(f"         🔥 编程题: {programming_count} 个")
                        print(f"         📋 选择题: {choice_count} 个")
                        
                        # 存储问题信息
                        group_key = f"{course_name}_{group_name}"
                        self.all_problems[group_key] = {
                            'course_name': course_name,
                            'course_id': course_id,
                            'group_name': group_name,
                            'group_id': group_id,
                            'problems': []
                        }
                        
                        for problem in group_problems:
                            if '_id' in problem:
                                self.all_problems[group_key]['problems'].append({
                                    'problem_id': problem['_id'],
                                    'problem_name': problem.get('name', 'Unknown'),
                                    'type': problem.get('type', 'unknown'),
                                    'score': problem.get('score', 0)
                                })
                        
                        # 更新统计
                        self.test_summary['total_groups'] += 1
                        self.test_summary['total_problems'] += len(group_problems)
                        self.test_summary['total_programming_problems'] += programming_count
                        self.test_summary['groups_tested'].append(group_key)
                        
                    elif response.status_code == 403:
                        print(f"      ❌ 访问被拒绝: {response.json().get('data', {}).get('message', '权限不足')}")
                        self.test_summary['errors'].append(f"{group_key}: 403权限错误")
                    else:
                        print(f"      ❌ 获取失败: HTTP {response.status_code}")
                        self.test_summary['errors'].append(f"{group_key}: HTTP {response.status_code}")
                        
                except Exception as e:
                    print(f"      ❌ 请求异常: {e}")
                    self.test_summary['errors'].append(f"{group_key}: 异常 {e}")
        
        print(f"\n📊 扫描完成！总计:")
        print(f"   🗂️  Groups: {self.test_summary['total_groups']} 个")
        print(f"   📝 题目总数: {self.test_summary['total_problems']} 个")
        print(f"   🔥 编程题: {self.test_summary['total_programming_problems']} 个")
        if self.test_summary['errors']:
            print(f"   ❌ 错误: {len(self.test_summary['errors'])} 个")
    
    def extract_code_from_explanation(self, explanation_content):
        """从explanation_content中提取代码"""
        if not explanation_content:
            return None
        
        pattern = r'<code>(.*?)</code>'
        matches = re.findall(pattern, explanation_content, re.DOTALL)
        
        if matches:
            code = '\n'.join(matches)
            
            # 修复HTML实体编码
            code = code.replace('&lt;', '<')
            code = code.replace('&gt;', '>')
            code = code.replace('&amp;', '&')
            code = code.replace('&quot;', '"')
            code = code.replace('&#39;', "'")
            
            return code.strip()
        
        return None
    
    def get_explanation_and_extract_code(self, group_key, problem):
        """获取explanation_content并提取代码"""
        if problem['type'] != 'programming':
            return None
        
        group_info = self.all_problems[group_key]
        course_id = group_info['course_id']
        group_id = group_info['group_id']
        problem_id = problem['problem_id']
        
        try:
            url = f"{self.BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}"
            response = requests.get(url, headers=self.headers, verify=False)
            
            if response.status_code == 200:
                data = response.json().get('data', {})
                explanation_content = data.get('explanation_content', '')
                
                if explanation_content:
                    code = self.extract_code_from_explanation(explanation_content)
                    if code:
                        self.test_summary['successful_extractions'] += 1
                        return code
            
            return None
            
        except Exception as e:
            print(f"         ❌ 获取异常: {e}")
            return None
    
    def submit_code(self, course_id, group_id, problem_id, code):
        """提交代码"""
        url = f"{self.BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/code"
        put_data = {"code": code}
        
        try:
            response = requests.put(url, headers=self.headers, json=put_data, verify=False)
            return {
                'success': response.status_code in [200, 201, 204],
                'status_code': response.status_code,
                'response': response.json() if response.text else {}
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"提交异常: {e}"
            }
    
    def get_testcase_result(self, course_id, group_id, problem_id):
        """获取测试结果"""
        url = f"{self.BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/testcases/result"
        
        try:
            response = requests.get(url, headers=self.headers, verify=False)
            if response.status_code == 200:
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                'success': False,
                'error': f"请求异常: {e}"
            }
    
    def process_all_groups(self, submit_codes=False):
        """处理所有group"""
        print(f"\n🚀 开始处理所有group的编程题...")
        print("=" * 80)
        
        for group_key, group_info in self.all_problems.items():
            print(f"\n📁 处理: {group_key}")
            print(f"   📚 课程: {group_info['course_name']}")
            print(f"   📂 Group: {group_info['group_name']}")
            
            programming_problems = [p for p in group_info['problems'] if p['type'] == 'programming']
            if not programming_problems:
                print(f"   ⚠️  没有编程题，跳过")
                continue
            
            print(f"   🔥 编程题数量: {len(programming_problems)}")
            
            group_codes = {}
            group_results = {}
            
            # 提取代码
            for i, problem in enumerate(programming_problems, 1):
                print(f"      [{i}/{len(programming_problems)}] 📝 {problem['problem_name']}")
                
                code = self.get_explanation_and_extract_code(group_key, problem)
                if code:
                    print(f"         ✅ 代码提取成功 ({len(code)} 字符)")
                    group_codes[problem['problem_id']] = {
                        'name': problem['problem_name'],
                        'code': code,
                        'type': problem['type'],
                        'score': problem['score']
                    }
                    
                    # 如果需要提交代码
                    if submit_codes:
                        submit_result = self.submit_code(
                            group_info['course_id'],
                            group_info['group_id'],
                            problem['problem_id'],
                            code
                        )
                        
                        if submit_result['success']:
                            print(f"         🎯 提交成功 (HTTP {submit_result['status_code']})")
                            
                            # 获取测试结果
                            test_result = self.get_testcase_result(
                                group_info['course_id'],
                                group_info['group_id'],
                                problem['problem_id']
                            )
                            
                            if test_result['success']:
                                queue_info = test_result['data'].get('data', {})
                                queue_name = queue_info.get('queue', 'unknown')
                                task_id = queue_info.get('task_id', 'unknown')
                                print(f"         📊 测试队列: {queue_name} (任务ID: {task_id})")
                                
                                submit_result['testcase_result'] = queue_info
                            else:
                                submit_result['testcase_result'] = {'error': test_result.get('error')}
                            
                            self.test_summary['successful_submissions'] += 1
                        else:
                            print(f"         ❌ 提交失败: {submit_result.get('error', '未知错误')}")
                            submit_result['testcase_result'] = None
                        
                        group_results[problem['problem_id']] = {
                            **group_codes[problem['problem_id']],
                            **submit_result
                        }
                else:
                    print(f"         ❌ 代码提取失败")
            
            # 保存结果
            if group_codes:
                self.extracted_codes[group_key] = group_codes
            if group_results:
                self.submission_results[group_key] = group_results
            
            print(f"   📊 本组处理完成: 提取 {len(group_codes)} 个代码")
            if submit_codes:
                success_count = len([r for r in group_results.values() if r.get('success', False)])
                print(f"   📊 提交结果: {success_count}/{len(group_results)} 成功")
    
    def save_results(self):
        """保存所有结果"""
        timestamp = int(time.time())
        
        # 保存提取的代码
        if self.extracted_codes:
            code_file = f"all_groups_extracted_codes_{timestamp}.json"
            with open(code_file, 'w', encoding='utf-8') as f:
                json.dump(self.extracted_codes, f, ensure_ascii=False, indent=2)
            print(f"📄 提取的代码已保存: {code_file}")
        
        # 保存提交结果
        if self.submission_results:
            result_file = f"all_groups_submission_results_{timestamp}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(self.submission_results, f, ensure_ascii=False, indent=2)
            print(f"📄 提交结果已保存: {result_file}")
        
        # 保存测试摘要
        summary_file = f"all_groups_test_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_summary, f, ensure_ascii=False, indent=2)
        print(f"📄 测试摘要已保存: {summary_file}")
        
        return code_file, result_file if self.submission_results else None, summary_file
    
    def print_summary(self):
        """打印测试摘要"""
        print(f"\n" + "="*80)
        print(f"📊 全Group测试摘要")
        print(f"="*80)
        print(f"🗂️  测试的Groups: {self.test_summary['total_groups']} 个")
        print(f"📝 题目总数: {self.test_summary['total_problems']} 个")
        print(f"🔥 编程题总数: {self.test_summary['total_programming_problems']} 个")
        print(f"✅ 成功提取代码: {self.test_summary['successful_extractions']} 个")
        print(f"🎯 成功提交代码: {self.test_summary['successful_submissions']} 个")
        
        if self.test_summary['errors']:
            print(f"\n❌ 错误列表:")
            for error in self.test_summary['errors']:
                print(f"   • {error}")
        
        print(f"\n✅ 测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """主函数"""
    print("🚀 全Group测试工具")
    print("=" * 80)
    
    # 初始化测试器
    tester = AllGroupTester("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMzEyNzkzMDAyOEBxcS5jb20iLCJuYW1lIjoicGx1Y2tmIiwiaWQiOiIxNzY4MDg5Iiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTE1MTQwMjQ2fSwiaWF0IjoxNzU1NTY2NTg5LCJleHAiOjE3NTY4NjI1ODl9.MA-CzqIELG0wgfWsbOZZDpdyjVCX6hPc9ks8KWUKMg4","Hm_lvt_6f63cfeea8c9a84040e2c4389f01bb91=1755516075,1755522844,1755532756; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMzEyNzkzMDAyOEBxcS5jb20iLCJuYW1lIjoicGx1Y2tmIiwiaWQiOiIxNzY4MDg5Iiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTE1MTQwMjQ2fSwiaWF0IjoxNzU1NTY2NTg5LCJleHAiOjE3NTY4NjI1ODl9.MA-CzqIELG0wgfWsbOZZDpdyjVCX6hPc9ks8KWUKMg4; io=dtZJyHJ1K2vslbCLACMP")
    
    # 加载会话数据
    if not tester.load_session_data():
        return
    
    # 获取所有group问题
    tester.get_all_group_problems()
    
    if tester.test_summary['total_programming_problems'] == 0:
        print("❌ 没有找到可处理的编程题")
        return
    
    # 询问是否提交代码
    print(f"\n⚠️  发现 {tester.test_summary['total_programming_problems']} 个编程题")
    print(f"是否要提取代码并提交测试？")
    print("1. 仅提取代码 (不提交)")
    print("2. 提取代码并提交测试")
    print("3. 取消")
    
    choice = input("请选择 (1/2/3): ").strip()
    
    if choice == '1':
        tester.process_all_groups(submit_codes=False)
    elif choice == '2':
        confirm = input(f"⚠️  将提交 {tester.test_summary['total_programming_problems']} 个编程题的代码，确认吗？(y/N): ")
        if confirm.lower() == 'y':
            tester.process_all_groups(submit_codes=True)
        else:
            print("已取消")
            return
    else:
        print("已取消")
        return
    
    # 保存结果
    tester.save_results()
    
    # 打印摘要
    tester.print_summary()

if __name__ == "__main__":
    main()
