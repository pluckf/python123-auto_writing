#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试HTML实体编码修复功能
检查是否正确替换了&lt; &gt;等HTML实体
"""

import json

def test_html_entity_fix():
    """测试HTML实体修复功能"""
    
    # 读取group7提交结果，检查其中的代码
    try:
        # 查找最新的group7结果文件
        import glob
        result_files = glob.glob('group7_submission_results_*.json')
        if result_files:
            latest_file = max(result_files)
            print(f"📂 使用文件: {latest_file}")
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        print("🔍 检查group7提交结果中的代码是否有HTML实体编码问题...")
        print("=" * 80)
        
        found_issues = []
        
        for problem_id, problem_info in data.items():
            name = problem_info.get('name', 'Unknown')
            code = problem_info.get('code', '')
            
            # 检查是否包含HTML实体
            if '&lt;' in code or '&gt;' in code or '&amp;' in code:
                found_issues.append({
                    'id': problem_id,
                    'name': name,
                    'issues': []
                })
                
                if '&lt;' in code:
                    found_issues[-1]['issues'].append('含有&lt;')
                if '&gt;' in code:
                    found_issues[-1]['issues'].append('含有&gt;')
                if '&amp;' in code:
                    found_issues[-1]['issues'].append('含有&amp;')
                
                print(f"⚠️  题目: {name}")
                print(f"   问题: {', '.join(found_issues[-1]['issues'])}")
                print(f"   代码预览: {code[:100]}...")
                print()
        
        if found_issues:
            print(f"❌ 发现 {len(found_issues)} 个题目有HTML实体编码问题")
            print("建议重新运行group7_tester.py来修复这些问题")
        else:
            print("✅ 所有代码都没有HTML实体编码问题")
            
        return found_issues
        
    except FileNotFoundError:
        print("❌ 未找到group7_submission_results_1755529402.json文件")
        return []
    except Exception as e:
        print(f"❌ 检查过程出错: {e}")
        return []

def test_sample_cases():
    """测试一些HTML实体编码样例"""
    print("\n🧪 测试HTML实体编码修复功能...")
    print("=" * 80)
    
    test_cases = [
        '<code>for i in range(10):\n    if i &lt; 5:\n        print(i)</code>',
        '<code>def func(a, b):\n    return a &gt; b and b &lt;= 10</code>',
        '<code>text = "Hello &amp; World"</code>',
        '<code>attr = &quot;value&quot;</code>'
    ]
    
    from extract_code import extract_code_from_explanation
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试用例 {i}:")
        print(f"输入: {test_case}")
        result = extract_code_from_explanation(test_case)
        print(f"输出: {result}")
        print()

if __name__ == "__main__":
    # 检查现有数据
    issues = test_html_entity_fix()
    
    # 测试修复功能
    test_sample_cases()
    
    if issues:
        print(f"\n💡 建议: 重新运行group7_tester.py来获取修复后的代码")
    else:
        print(f"\n✅ 所有检查通过！")
