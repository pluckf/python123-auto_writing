#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Group7 专用测试脚本
获取group7的explanation_content，提取代码，并批量提交测试
"""
import requests
import json
import re
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API配置
BASE_URL = "https://python123.io/api/v1/student/courses"
HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMTY1MzA4MzQ3MUBxcS5jb20iLCJuYW1lIjoi5aec6L-c5bCaIiwiaWQiOiIxMjQzOTYxIiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTEyODY0MjcwfSwiaWF0IjoxNzU1NTE1MjU1LCJleHAiOjE3NTY4MTEyNTV9.4CFizZ4KvcRwad7ACdvSPfG0Kf3epPQYJdwiv_YUPps",
    "Content-Type": "application/json"
}

class Group7Tester:
    def __init__(self):
        self.course_ids = {}
        self.course_group_mapping = {}
        self.group7_explanations = {}
        self.group7_codes = {}
        self.submission_results = {}
        
    def load_session_data(self):
        """加载会话数据"""
        try:
            import glob
            session_files = glob.glob('python123_complete_session_*.json')
            if session_files:
                latest_file = max(session_files)
                print(f"📂 使用会话文件: {latest_file}")
                with open(latest_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                self.course_ids = session_data.get('course_ids', {})
                self.course_group_mapping = session_data.get('course_group_mapping', {})
                
                print(f"📊 加载了 {len(self.course_ids)} 个课程")
                return True
            else:
                print("❌ 未找到会话文件")
                return False
        except Exception as e:
            print(f"❌ 加载会话数据失败: {e}")
            return False
    
    def get_group7_problems(self):
        """获取group7的所有问题"""
        problems = []
        
        for course_name, course_id in self.course_ids.items():
            group_mapping = self.course_group_mapping.get(course_name, {})
            group7_id = group_mapping.get('7')  # 查找group_7的ID
            
            if group7_id:
                print(f"🔍 在课程 '{course_name}' 中找到 group7 (ID: {group7_id})")
                
                # 获取group7的问题列表
                url = f"{BASE_URL}/{course_id}/groups/{group7_id}/problems"
                try:
                    response = requests.get(url, headers=HEADERS, verify=False)
                    if response.status_code == 200:
                        response_data = response.json()
                        group_problems = response_data.get('data', [])
                        print(f"   📝 找到 {len(group_problems)} 个题目")
                        
                        for problem in group_problems:
                            # 使用 _id 字段而不是 id 字段
                            if '_id' not in problem:
                                print(f"     ⚠️  题目数据缺少_id字段: {problem}")
                                continue
                                
                            problems.append({
                                'course_name': course_name,
                                'course_id': course_id,
                                'group_id': group7_id,
                                'problem_id': problem['_id'],
                                'problem_name': problem.get('name', 'Unknown'),
                                'type': problem.get('type', 'unknown')
                            })
                    else:
                        print(f"   ❌ 获取问题失败: HTTP {response.status_code}")
                        print(f"      错误内容: {response.text[:200]}")
                        
                except Exception as e:
                    print(f"   ❌ 请求异常: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"⚠️  课程 '{course_name}' 中未找到 group7")
        
        return problems
    
    def get_explanation_content(self, course_id, group_id, problem_id):
        """获取单个问题的explanation_content"""
        url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}"
        
        try:
            response = requests.get(url, headers=HEADERS, verify=False)
            if response.status_code == 200:
                data = response.json().get('data', {})
                return data.get('explanation_content', '')
            else:
                print(f"     ❌ 获取失败: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"     ❌ 请求异常: {e}")
            return None
    
    def extract_code_from_explanation(self, explanation_content):
        """从explanation_content中提取<code>标签内的代码"""
        if not explanation_content:
            return None
        
        # 使用正则表达式匹配<code>...</code>标签
        pattern = r'<code>(.*?)</code>'
        matches = re.findall(pattern, explanation_content, re.DOTALL)
        
        if matches:
            # 如果有多个code标签，合并它们
            code = '\n'.join(matches)
            
            # 修复HTML实体编码
            code = code.replace('&lt;', '<')
            code = code.replace('&gt;', '>')
            code = code.replace('&amp;', '&')  # 也处理&符号
            code = code.replace('&quot;', '"')  # 处理引号
            code = code.replace('&#39;', "'")   # 处理单引号
            
            return code.strip()
        
        return None
    
    def fetch_all_group7_data(self, problems):
        """获取所有group7问题的数据"""
        print(f"\n🚀 开始获取 {len(problems)} 个group7题目的数据...")
        
        for i, problem in enumerate(problems, 1):
            print(f"\n[{i}/{len(problems)}] 📝 处理: {problem['problem_name']}")
            print(f"   📍 位置: {problem['course_name']}/group7")
            
            # 获取explanation_content
            explanation = self.get_explanation_content(
                problem['course_id'], 
                problem['group_id'], 
                problem['problem_id']
            )
            
            if explanation:
                print(f"   ✅ 获取到explanation_content ({len(explanation)} 字符)")
                
                # 提取代码
                code = self.extract_code_from_explanation(explanation)
                if code:
                    print(f"   🎯 提取到代码 ({len(code)} 字符)")
                    self.group7_codes[problem['problem_id']] = {
                        'name': problem['problem_name'],
                        'course_name': problem['course_name'],
                        'course_id': problem['course_id'],
                        'group_id': problem['group_id'],
                        'code': code,
                        'type': problem['type']
                    }
                else:
                    print(f"   ⚠️  未找到<code>标签")
                
                self.group7_explanations[problem['problem_id']] = {
                    'name': problem['problem_name'],
                    'explanation_content': explanation
                }
            else:
                print(f"   ❌ 获取explanation_content失败")
    
    def submit_code(self, course_id, group_id, problem_id, code):
        """提交单个代码"""
        url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/code"
        put_data = {"code": code}
        
        try:
            response = requests.put(url, headers=HEADERS, json=put_data, verify=False)
            return {
                'success': response.status_code in [200, 201, 204],
                'status_code': response.status_code,
                'response': response.json() if response.text else {}
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"请求异常: {e}"
            }
    
    def get_testcase_result(self, course_id, group_id, problem_id):
        """获取测试结果"""
        url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/testcases/result"
        
        try:
            response = requests.get(url, headers=HEADERS, verify=False)
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
    
    def batch_submit_group7(self):
        """批量提交group7代码"""
        if not self.group7_codes:
            print("❌ 没有可提交的代码")
            return
        
        print(f"\n🚀 开始批量提交 {len(self.group7_codes)} 个group7代码")
        print("=" * 80)
        
        success_count = 0
        total_count = len(self.group7_codes)
        
        for i, (problem_id, problem_info) in enumerate(self.group7_codes.items(), 1):
            print(f"\n[{i}/{total_count}] 📝 提交: {problem_info['name']}")
            
            # 提交代码
            submit_result = self.submit_code(
                problem_info['course_id'],
                problem_info['group_id'],
                problem_id,
                problem_info['code']
            )
            
            if submit_result['success']:
                print(f"   ✅ 代码提交成功 (HTTP {submit_result['status_code']})")
                
                # 立即获取测试结果
                print(f"   🧪 获取测试结果...")
                test_result = self.get_testcase_result(
                    problem_info['course_id'],
                    problem_info['group_id'],
                    problem_id
                )
                
                if test_result['success']:
                    queue_info = test_result['data'].get('data', {})
                    queue_name = queue_info.get('queue', 'unknown')
                    task_id = queue_info.get('task_id', 'unknown')
                    message_count = queue_info.get('messageCount', 0)
                    
                    print(f"      📊 队列状态: {queue_name}")
                    print(f"      🆔 任务ID: {task_id}")
                    print(f"      📬 队列消息数: {message_count}")
                    
                    submit_result['testcase_result'] = queue_info
                else:
                    print(f"      ❌ 测试结果获取失败: {test_result.get('error', '未知错误')}")
                    submit_result['testcase_result'] = {'error': test_result.get('error')}
                
                success_count += 1
            else:
                print(f"   ❌ 代码提交失败: {submit_result.get('error', '未知错误')}")
                submit_result['testcase_result'] = None
            
            # 保存结果
            self.submission_results[problem_id] = {
                **problem_info,
                **submit_result
            }
        
        print(f"\n🎉 group7批量提交完成！")
        print(f"📊 成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
        
        # 保存结果
        self.save_results()
        
        return success_count, total_count
    
    def save_results(self):
        """保存所有结果"""
        timestamp = int(time.time())
        
        # 保存explanations
        if self.group7_explanations:
            exp_file = f"group7_explanations_{timestamp}.json"
            with open(exp_file, 'w', encoding='utf-8') as f:
                json.dump(self.group7_explanations, f, ensure_ascii=False, indent=2)
            print(f"📄 Explanations已保存: {exp_file}")
        
        # 保存提取的代码
        if self.group7_codes:
            code_file = f"group7_extracted_codes_{timestamp}.json"
            with open(code_file, 'w', encoding='utf-8') as f:
                json.dump(self.group7_codes, f, ensure_ascii=False, indent=2)
            print(f"📄 提取的代码已保存: {code_file}")
        
        # 保存提交结果
        if self.submission_results:
            result_file = f"group7_submission_results_{timestamp}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(self.submission_results, f, ensure_ascii=False, indent=2)
            print(f"📄 提交结果已保存: {result_file}")

def main():
    """主函数"""
    print("[Group7] 专用测试工具")
    print("=" * 80)
    
    tester = Group7Tester()
    
    # 加载会话数据
    if not tester.load_session_data():
        return
    
    # 获取group7问题
    print("\n📋 查找group7问题...")
    problems = tester.get_group7_problems()
    
    if not problems:
        print("❌ 未找到group7问题")
        return
    
    print(f"✅ 找到 {len(problems)} 个group7问题")
    
    # 获取所有数据
    tester.fetch_all_group7_data(problems)
    
    # 显示统计
    print(f"\n📊 数据获取完成:")
    print(f"   📝 获取到explanations: {len(tester.group7_explanations)} 个")
    print(f"   💻 提取到代码: {len(tester.group7_codes)} 个")
    
    # 询问是否提交
    if tester.group7_codes:
        print(f"\n⚠️  准备提交 {len(tester.group7_codes)} 个group7代码")
        confirm = input("是否继续提交？(y/N): ").lower().strip()
        
        if confirm == 'y':
            tester.batch_submit_group7()
        else:
            print("取消提交")
            tester.save_results()
    else:
        print("没有可提交的代码")
        tester.save_results()

if __name__ == "__main__":
    main()
