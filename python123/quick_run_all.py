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

def quick_demo():
    """快速演示所有功能"""
    print("🚀 Python123.io 快速演示工具")
    print("仅供学习使用")
    print("="*60)
    
    results = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'steps': {}
    }
    
    # 步骤1：获取课程列表
    print("\n📚 步骤1：获取课程列表")
    print("-" * 40)
    try:
        response = requests.get(BASE_URL, headers=HEADERS, verify=False)
        if response.status_code == 200:
            courses_data = response.json()
            courses = courses_data.get('data', [])
            print(f"✅ 成功获取 {len(courses)} 个课程")
            
            # 显示课程信息
            for i, course in enumerate(courses, 1):
                course_name = course.get('name', '未命名')
                course_id = course.get('_id')
                groups_count = len(course.get('groups', []))
                print(f"  {i}. {course_name} (ID: {course_id}, {groups_count}个组)")
            
            results['steps']['1_courses'] = {
                'success': True,
                'count': len(courses),
                'data': courses_data
            }
        else:
            print(f"❌ 获取课程失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取课程失败: {e}")
        return False
    
    # 步骤2：获取第一个课程第一个组的问题
    print("\n❓ 步骤2：获取问题列表")
    print("-" * 40)
    
    first_course = courses[0]
    course_id = first_course['_id']
    course_name = first_course['name']
    groups = first_course.get('groups', [])
    
    if not groups:
        print("❌ 该课程没有组")
        return False
    
    first_group = groups[0]
    group_id = first_group['_id']
    group_index = first_group['index']
    
    print(f"测试课程: {course_name} (ID: {course_id})")
    print(f"测试组: Group_{group_index} (ID: {group_id})")
    
    try:
        problems_url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems"
        response = requests.get(problems_url, headers=HEADERS, verify=False)
        
        if response.status_code == 200:
            problems_data = response.json()
            problems = problems_data.get('data', [])
            print(f"✅ 成功获取 {len(problems)} 个问题")
            
            # 分类显示问题
            choice_problems = [p for p in problems if p.get('type') == 'choice']
            programming_problems = [p for p in problems if p.get('type') == 'programming']
            
            print(f"  - 选择题: {len(choice_problems)} 个")
            print(f"  - 编程题: {len(programming_problems)} 个")
            
            # 显示编程题信息
            if programming_problems:
                print("  📝 编程题列表:")
                for i, problem in enumerate(programming_problems, 1):
                    problem_name = problem.get('name', '未命名')
                    problem_id = problem.get('_id')
                    print(f"    {i}. {problem_name} (ID: {problem_id})")
            
            results['steps']['2_problems'] = {
                'success': True,
                'total_count': len(problems),
                'choice_count': len(choice_problems),
                'programming_count': len(programming_problems),
                'programming_problems': programming_problems
            }
        else:
            print(f"❌ 获取问题失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取问题失败: {e}")
        return False
    
    # 步骤3：获取第一个编程题的代码
    if programming_problems:
        print("\n💻 步骤3：获取编程题代码")
        print("-" * 40)
        
        first_programming = programming_problems[0]
        problem_id = first_programming['_id']
        problem_name = first_programming['name']
        
        print(f"获取题目: {problem_name} (ID: {problem_id})")
        
        try:
            code_url = f"{BASE_URL}/{course_id}/groups/{group_id}/problems/{problem_id}/code"
            response = requests.get(code_url, headers=HEADERS, verify=False)
            
            if response.status_code == 200:
                code_data = response.json()
                actual_code = code_data.get('data', {}).get('code', '')
                print(f"✅ 成功获取代码:")
                print("```python")
                print(actual_code)
                print("```")
                
                results['steps']['3_get_code'] = {
                    'success': True,
                    'problem_name': problem_name,
                    'problem_id': problem_id,
                    'code': actual_code,
                    'full_data': code_data
                }
                
                # 步骤4：测试PUT请求
                print("\n🔄 步骤4：测试PUT请求")
                print("-" * 40)
                
                # 在代码末尾添加测试注释
                test_code = actual_code + f"\n# 快速演示PUT测试 - {time.strftime('%H:%M:%S')}"
                
                print(f"发送测试代码:")
                print("```python")
                print(test_code)
                print("```")
                
                try:
                    put_data = {"code": test_code}
                    response = requests.put(code_url, headers=HEADERS, json=put_data, verify=False)
                    
                    if response.status_code == 200:
                        print("✅ PUT请求成功!")
                        try:
                            put_result = response.json()
                            print(f"服务器响应: {json.dumps(put_result, ensure_ascii=False)}")
                        except:
                            print(f"服务器响应: {response.text}")
                        
                        # 验证代码是否更新
                        print("\n🔍 步骤5：验证代码更新")
                        print("-" * 40)
                        
                        verify_response = requests.get(code_url, headers=HEADERS, verify=False)
                        if verify_response.status_code == 200:
                            verify_data = verify_response.json()
                            updated_code = verify_data.get('data', {}).get('code', '')
                            
                            if test_code.strip() == updated_code.strip():
                                print("✅ 代码更新验证成功！")
                                print("💡 所有功能正常工作")
                            else:
                                print("⚠️  代码内容有差异，但PUT请求已执行")
                        
                        results['steps']['4_put_test'] = {
                            'success': True,
                            'sent_code': test_code,
                            'response': put_result if 'put_result' in locals() else response.text
                        }
                        
                    else:
                        print(f"❌ PUT请求失败，状态码: {response.status_code}")
                        print(f"响应内容: {response.text}")
                        results['steps']['4_put_test'] = {
                            'success': False,
                            'error': f"Status: {response.status_code}, Response: {response.text}"
                        }
                        
                except Exception as e:
                    print(f"❌ PUT请求发生错误: {e}")
                    results['steps']['4_put_test'] = {
                        'success': False,
                        'error': str(e)
                    }
                    
            else:
                print(f"❌ 获取代码失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 获取代码失败: {e}")
            return False
    else:
        print("\n❌ 没有找到编程题，无法继续演示")
        return False
    
    # 步骤6：保存演示结果
    print("\n💾 步骤6：保存演示结果")
    print("-" * 40)
    
    try:
        filename = f"quick_demo_result_{int(time.time())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"✅ 演示结果已保存: {filename}")
    except Exception as e:
        print(f"❌ 保存结果失败: {e}")
    
    # 最终总结
    print("\n" + "="*60)
    print("🎉 快速演示完成！")
    print("="*60)
    
    successful_steps = len([step for step in results['steps'].values() if step.get('success', False)])
    total_steps = len(results['steps'])
    
    print(f"📊 总结:")
    print(f"  - 成功步骤: {successful_steps}/{total_steps}")
    print(f"  - 获取课程: {results['steps'].get('1_courses', {}).get('count', 0)} 个")
    print(f"  - 获取问题: {results['steps'].get('2_problems', {}).get('total_count', 0)} 个")
    print(f"  - 编程题数: {results['steps'].get('2_problems', {}).get('programming_count', 0)} 个")
    print(f"  - PUT测试: {'✅ 成功' if results['steps'].get('4_put_test', {}).get('success') else '❌ 失败'}")
    print("="*60)
    
    return successful_steps == total_steps

def main():
    """主函数"""
    print("选择运行模式:")
    print("1. 快速演示 (推荐)")
    print("2. 退出")
    
    try:
        choice = input("\n请输入选择 (1-2): ").strip()
        
        if choice == '1':
            success = quick_demo()
            if success:
                print("\n✨ 所有功能演示成功！")
            else:
                print("\n⚠️  部分功能可能存在问题")
        elif choice == '2':
            print("👋 再见！")
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")

if __name__ == "__main__":
    main()
