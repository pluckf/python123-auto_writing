#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将提取的代码PUT到对应的API端点
批量提交代码到 python123.io
仅供学习使用
"""

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

class CodeSubmitter:
    """代码提交器，负责将提取的代码PUT到对应的API端点"""
    
    def __init__(self):
        self.submission_results = {}
        self.course_group_mapping = {}
        self.course_ids = {}
    
    def load_mapping_data(self):
        """加载课程和组的映射关系"""
        try:
            import glob
            session_files = glob.glob('python123_complete_session_*.json')
            if session_files:
                latest_file = max(session_files)
                print(f"📂 从文件加载映射数据: {latest_file}")
                with open(latest_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                self.course_ids = session_data.get('course_ids', {})
                self.course_group_mapping = session_data.get('course_group_mapping', {})
                
                return True
            else:
                print("❌ 未找到完整会话文件")
                return False
                
        except Exception as e:
            print(f"❌ 加载映射数据失败: {e}")
            return False
    
    def load_extracted_code(self, code_filename):
        """加载提取的代码数据"""
        try:
            with open(code_filename, 'r', encoding='utf-8') as f:
                code_data = json.load(f)
            print(f"📂 加载代码数据: {code_filename}")
            print(f"📊 找到 {len(code_data)} 个题目的代码")
            return code_data
        except Exception as e:
            print(f"❌ 加载代码数据失败: {e}")
            return None
    
    def put_problem_code(self, course_id, group_id, problem_id, code_content):
        """发送PUT请求提交代码"""
        url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/code"
        put_data = {"code": code_content}
        
        try:
            response = requests.put(url, headers=HEADERS, json=put_data, verify=False)
            if response.status_code in [200, 201, 204]:
                try:
                    return {
                        'success': True,
                        'status_code': response.status_code,
                        'response': response.json()
                    }
                except:
                    return {
                        'success': True,
                        'status_code': response.status_code,
                        'response': {'text': response.text}
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
    
    def get_testcase_result(self, course_id, group_id, problem_id):
        """获取题目测试用例结果"""
        url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/testcases/result"
        
        try:
            response = requests.get(url, headers=HEADERS, verify=False)
            if response.status_code == 200:
                try:
                    result_data = response.json()
                    return {
                        'success': True,
                        'status_code': response.status_code,
                        'data': result_data
                    }
                except:
                    return {
                        'success': True,
                        'status_code': response.status_code,
                        'data': {'text': response.text}
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
    
    def extract_key_testcase_info(self, testcase_result):
        """提取测试用例结果的关键信息"""
        if not testcase_result.get('success', False):
            return {
                'status': 'ERROR',
                'message': testcase_result.get('error', '获取测试结果失败'),
                'details': {}
            }
        
        data = testcase_result.get('data', {})
        
        # 如果data有特定结构，提取关键信息
        if isinstance(data, dict):
            # 检查是否是队列信息格式
            if 'queue' in data and 'task_id' in data:
                key_info = {
                    'status': 'QUEUED',
                    'queue': data.get('queue', ''),
                    'task_id': data.get('task_id', 0),
                    'message_count': data.get('messageCount', 0),
                    'consumer_count': data.get('consumerCount', 0),
                    'srcurl': data.get('srcurl', ''),
                    'message': f"任务已提交到队列 {data.get('queue', '')}，任务ID: {data.get('task_id', '')}"
                }
                return key_info
            
            # 常见的测试结果字段 (如果有其他格式的响应)
            key_info = {
                'status': data.get('status', 'PROCESSING'),
                'score': data.get('score', None),
                'total_score': data.get('total_score', None),
                'passed_tests': data.get('passed_tests', None),
                'total_tests': data.get('total_tests', None),
                'execution_time': data.get('execution_time', ''),
                'memory_usage': data.get('memory_usage', ''),
                'compile_error': data.get('compile_error', ''),
                'runtime_error': data.get('runtime_error', ''),
                'test_cases': data.get('test_cases', []),
                'message': data.get('message', ''),
                'details': data.get('details', {})
            }
            
            # 移除空值
            key_info = {k: v for k, v in key_info.items() if v not in [None, '', 0, []]}
            
            # 如果没有提取到有用信息，返回原始数据
            if not key_info or key_info == {'status': 'PROCESSING'}:
                key_info = {
                    'status': 'RAW_DATA',
                    'raw_response': data
                }
            
            return key_info
        else:
            return {
                'status': 'RAW_DATA',
                'raw_response': data
            }
    
    def get_problem_location(self, problem_id):
        """根据问题ID找到对应的课程和组"""
        # 确保problem_id是字符串类型进行比较
        problem_id_str = str(problem_id)
        
        # 从会话数据中查找问题所属的课程和组
        try:
            import glob
            session_files = glob.glob('python123_complete_session_*.json')
            if session_files:
                latest_file = max(session_files)
                with open(latest_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                problem_ids_data = session_data.get('problem_ids', {})
                
                for course_name, course_data in problem_ids_data.items():
                    for group_key, problems in course_data.items():
                        for problem in problems:
                            # 比较时都转换为字符串
                            if str(problem['id']) == problem_id_str:
                                course_id = self.course_ids.get(course_name)
                                group_index_str = group_key.replace('group_', '')
                                group_id = self.course_group_mapping.get(course_name, {}).get(group_index_str)
                                
                                print(f"  🔍 找到匹配: {problem['name']} 在 {course_name}/{group_key}")
                                return course_id, group_id, course_name, group_key
                
                print(f"  ⚠️ 未找到问题ID {problem_id_str} 的位置信息")
                
        except Exception as e:
            print(f"⚠️ 查找问题位置时出错: {e}")
        
        return None, None, None, None
    
    def submit_all_codes(self, code_data):
        """提交所有代码"""
        print("\n🚀 开始批量提交代码")
        print("="*60)
        
        total_codes = len(code_data)
        successful_submissions = 0
        
        for i, (problem_id, problem_info) in enumerate(code_data.items(), 1):
            name = problem_info.get('name', '')
            code = problem_info.get('code', '')
            
            print(f"\n[{i}/{total_codes}] 📝 提交: {name} (ID: {problem_id})")
            
            # 查找问题的位置信息
            course_id, group_id, course_name, group_key = self.get_problem_location(problem_id)
            
            if not course_id or not group_id:
                print(f"  ❌ 无法找到题目位置信息")
                self.submission_results[problem_id] = {
                    'name': name,
                    'success': False,
                    'error': '无法找到题目位置信息'
                }
                continue
            
            print(f"  📍 位置: {course_name} -> {group_key}")
            print(f"  🔗 API: /courses/{course_id}/groups/{group_id}/problems/{problem_id}/code")
            
            # 显示要提交的代码预览
            code_preview = code[:100] + "..." if len(code) > 100 else code
            print(f"  📄 代码预览: {code_preview}")
            
            # 发送PUT请求
            result = self.put_problem_code(course_id, group_id, problem_id, code)
            
            if result['success']:
                print(f"  ✅ 提交成功 (HTTP {result['status_code']})")
                
                # 立即获取测试结果
                print(f"  🧪 获取测试结果...")
                testcase_result = self.get_testcase_result(course_id, group_id, problem_id)
                
                if testcase_result.get('success', False):
                    key_info = self.extract_key_testcase_info(testcase_result)
                    print(f"     📊 测试结果状态: {key_info.get('status', 'UNKNOWN')}")
                    
                    # 显示关键信息
                    if key_info.get('status') == 'QUEUED':
                        print(f"     📝 {key_info.get('message', '')}")
                        print(f"     🏷️  任务ID: {key_info.get('task_id', 'N/A')}")
                        print(f"     📨 队列消息数: {key_info.get('message_count', 0)}")
                        print(f"     👥 消费者数: {key_info.get('consumer_count', 0)}")
                    else:
                        # 其他状态的显示逻辑
                        if 'score' in key_info:
                            print(f"     得分: {key_info['score']}/{key_info.get('total_score', '?')}")
                        if 'passed_tests' in key_info:
                            print(f"     通过测试: {key_info['passed_tests']}/{key_info.get('total_tests', '?')}")
                        if 'execution_time' in key_info:
                            print(f"     执行时间: {key_info['execution_time']}")
                        if 'memory_usage' in key_info:
                            print(f"     内存使用: {key_info['memory_usage']}")
                        if key_info.get('compile_error'):
                            print(f"     ⚠️  编译错误: {key_info['compile_error']}")
                        if key_info.get('runtime_error'):
                            print(f"     ⚠️  运行错误: {key_info['runtime_error']}")
                        if key_info.get('message'):
                            print(f"     💬 消息: {key_info['message']}")
                    
                    # 将测试结果添加到保存的结果中
                    result['testcase_result'] = key_info
                else:
                    error_msg = testcase_result.get('error', '未知错误')
                    print(f"     ❌ 测试结果获取失败: {error_msg}")
                    result['testcase_result'] = {'status': 'GET_FAILED', 'error': error_msg}
                    
                successful_submissions += 1
            else:
                print(f"  ❌ 提交失败: {result.get('error', '未知错误')}")
                result['testcase_result'] = None
            
            # 保存结果
            self.submission_results[problem_id] = {
                'name': name,
                'course_name': course_name,
                'group_key': group_key,
                'course_id': course_id,
                'group_id': group_id,
                'code_length': len(code),
                **result
            }
            
            # 延时已移除 - 加快处理速度
        
        print(f"\n✅ 提交完成！成功 {successful_submissions}/{total_codes} 个题目")
        return successful_submissions, total_codes
    
    def save_submission_results(self):
        """保存提交结果"""
        timestamp = int(time.time())
        filename = f"code_submission_results_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.submission_results, f, ensure_ascii=False, indent=2)
            print(f"📄 提交结果已保存: {filename}")
            return filename
        except Exception as e:
            print(f"❌ 保存结果失败: {e}")
            return None
    
    def print_submission_summary(self):
        """打印提交结果摘要"""
        print("\n" + "="*60)
        print("📊 提交结果摘要")
        print("="*60)
        
        successful = [r for r in self.submission_results.values() if r.get('success', False)]
        failed = [r for r in self.submission_results.values() if not r.get('success', False)]
        
        print(f"✅ 成功提交: {len(successful)} 个")
        print(f"❌ 提交失败: {len(failed)} 个")
        
        if successful:
            print("\n✅ 成功提交的题目:")
            for result in successful:
                print(f"  • {result['name']} (ID: {list(self.submission_results.keys())[list(self.submission_results.values()).index(result)]})")
        
        if failed:
            print("\n❌ 提交失败的题目:")
            for result in failed:
                print(f"  • {result['name']}: {result.get('error', '未知错误')}")

def main():
    """主函数"""
    print("🚀 Python123.io 代码批量提交工具")
    print("将提取的代码PUT到对应的API端点")
    print("仅供学习使用")
    print("="*60)
    
    # 查找最新的提取代码文件
    import glob
    code_files = glob.glob('extracted_code_*.json')
    if not code_files:
        print("❌ 未找到提取的代码文件 (extracted_code_*.json)")
        return
    
    latest_code_file = max(code_files)
    print(f"📂 使用代码文件: {latest_code_file}")
    
    # 创建提交器
    submitter = CodeSubmitter()
    
    # 加载映射数据
    if not submitter.load_mapping_data():
        print("❌ 无法加载映射数据，程序终止")
        return
    
    # 加载代码数据
    code_data = submitter.load_extracted_code(latest_code_file)
    if not code_data:
        print("❌ 无法加载代码数据，程序终止")
        return
    
    # 确认提交
    print(f"\n⚠️ 准备提交 {len(code_data)} 个题目的代码到 python123.io")
    print("这将覆盖服务器上的现有代码！")
    
    confirm = input("是否继续？(y/N): ").lower().strip()
    if confirm != 'y':
        print("❌ 用户取消操作")
        return
    
    # 提交所有代码
    successful, total = submitter.submit_all_codes(code_data)
    
    # 保存结果
    result_file = submitter.save_submission_results()
    
    # 打印摘要
    submitter.print_submission_summary()
    
    print(f"\n🎉 批量提交完成！")
    print(f"📊 成功率: {successful}/{total} ({successful/total*100:.1f}%)")
    if result_file:
        print(f"📄 详细结果: {result_file}")

if __name__ == "__main__":
    main()
