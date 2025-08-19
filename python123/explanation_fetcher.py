#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python123.io 题目说明获取工具
专门用于获取题目的 explanation_content
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

class ExplanationFetcher:
    """专门获取题目explanation_content的类"""
    
    def __init__(self):
        self.explanation_contents = {}
    
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
    
    def load_existing_data(self):
        """加载现有的课程和问题数据"""
        try:
            # 尝试从最新的完整会话文件加载数据
            import glob
            session_files = glob.glob('python123_complete_session_*.json')
            if session_files:
                latest_file = max(session_files)
                print(f"📂 从文件加载数据: {latest_file}")
                with open(latest_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                course_ids = session_data.get('course_ids', {})
                problem_ids = session_data.get('problem_ids', {})
                course_group_mapping = session_data.get('course_group_mapping', {})
                
                return course_ids, problem_ids, course_group_mapping
            else:
                print("❌ 未找到完整会话文件，请先运行 run_all.py")
                return None, None, None
                
        except Exception as e:
            print(f"❌ 加载数据失败: {e}")
            return None, None, None
    
    def get_all_explanation_contents(self):
        """获取所有题目的explanation_content"""
        print("🔍 开始获取所有题目的说明内容")
        print("="*60)
        
        # 加载现有数据
        result = self.load_existing_data()
        if not result or len(result) != 3:
            return False
        
        course_ids, problem_ids, course_group_mapping = result
        
        explanation_count = 0
        
        for course_name, course_data in problem_ids.items():
            print(f"\n📚 处理课程: {course_name}")
            self.explanation_contents[course_name] = {}
            
            for group_key, problems in course_data.items():
                print(f"  📂 处理 {group_key}...")
                self.explanation_contents[course_name][group_key] = {}
                
                for problem in problems:
                    problem_id = problem['id']
                    problem_name = problem['name']
                    problem_type = problem['type']
                    
                    print(f"    📝 获取: {problem_name} (ID: {problem_id})")
                    
                    # 获取课程ID和组ID
                    course_id = course_ids.get(course_name)
                    group_index_str = group_key.replace('group_', '')
                    group_id = course_group_mapping.get(course_name, {}).get(group_index_str)
                    
                    if not course_id or not group_id:
                        print(f"      ✗ 缺少ID信息: course_id={course_id}, group_id={group_id}, group_index={group_index_str}")
                        continue
                    
                    # 获取题目详情
                    problem_details = self.get_problem_details(course_id, group_id, problem_id)
                    
                    if problem_details and 'data' in problem_details:
                        data = problem_details['data']
                        explanation_content = data.get('explanation_content', '')
                        
                        self.explanation_contents[course_name][group_key][problem_id] = {
                            'name': problem_name,
                            'type': problem_type,
                            'explanation_content': explanation_content,
                            'additional_info': {
                                'difficulty': data.get('difficulty', ''),
                                'tags': data.get('tags', []),
                                'created_at': data.get('created_at', ''),
                                'updated_at': data.get('updated_at', '')
                            }
                        }
                        print(f"      ✓ 说明获取成功 ({len(explanation_content)} 字符)")
                        explanation_count += 1
                    else:
                        print(f"      ✗ 说明获取失败")
        
        print(f"\n✅ 总计获取了 {explanation_count} 个题目的说明")
        return explanation_count > 0
    
    def save_explanation_contents(self):
        """保存explanation_contents到文件"""
        timestamp = int(time.time())
        
        # 保存详细的explanation_contents
        filename = f"explanation_contents_{timestamp}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.explanation_contents, f, ensure_ascii=False, indent=2)
            print(f"📄 详细说明内容已保存: {filename}")
        except Exception as e:
            print(f"保存失败: {e}")
            return False
        
        # 保存简化版本（只包含explanation_content文本）
        simplified = {}
        for course_name, course_data in self.explanation_contents.items():
            simplified[course_name] = {}
            for group_key, group_data in course_data.items():
                simplified[course_name][group_key] = {}
                for problem_id, problem_data in group_data.items():
                    simplified[course_name][group_key][problem_id] = {
                        'name': problem_data['name'],
                        'explanation_content': problem_data['explanation_content']
                    }
        
        simple_filename = f"explanation_contents_simple_{timestamp}.json"
        try:
            with open(simple_filename, 'w', encoding='utf-8') as f:
                json.dump(simplified, f, ensure_ascii=False, indent=2)
            print(f"📄 简化说明内容已保存: {simple_filename}")
        except Exception as e:
            print(f"保存简化版本失败: {e}")
        
        return True

def main():
    """主函数"""
    print("🚀 Python123.io 题目说明获取工具")
    print("仅供学习使用")
    print("="*60)
    
    fetcher = ExplanationFetcher()
    
    # 获取所有explanation_content
    if fetcher.get_all_explanation_contents():
        print("\n💾 保存数据...")
        if fetcher.save_explanation_contents():
            print("\n🎉 所有操作完成！")
        else:
            print("\n❌ 保存数据失败")
    else:
        print("\n❌ 获取explanation_content失败")

if __name__ == "__main__":
    main()
