#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取 explanation_content 中的纯代码内容
提取 <code> 和 </code> 之间的内容，不包含标签本身
"""

import json
import re

def extract_code_from_explanation(explanation_content):
    """提取 explanation_content 中 <code> 和 </code> 之间的内容"""
    if not explanation_content:
        return ""
    
    # 使用正则表达式提取 <code> 和 </code> 之间的内容
    # re.DOTALL 标志让 . 匹配包括换行符在内的任何字符
    code_pattern = r'<code>(.*?)</code>'
    matches = re.findall(code_pattern, explanation_content, re.DOTALL)
    
    if matches:
        # 如果有多个 <code> 块，用换行符连接
        code_content = '\n\n'.join(matches)
        
        # 修复HTML实体编码
        code_content = code_content.replace('&lt;', '<')
        code_content = code_content.replace('&gt;', '>')
        code_content = code_content.replace('&amp;', '&')
        code_content = code_content.replace('&quot;', '"')
        code_content = code_content.replace('&#39;', "'")
        
        # 去除多余的空白
        code_content = code_content.strip()
        return code_content
    
    return ""

def process_explanation_dict(input_filename):
    """处理explanation字典，提取其中的代码内容"""
    try:
        # 读取原始文件
        with open(input_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📂 读取文件: {input_filename}")
        print(f"📊 找到 {len(data)} 个题目")
        
        # 创建新的字典存储提取的代码
        code_dict = {}
        explanation_with_code = {}
        
        for problem_id, problem_info in data.items():
            name = problem_info.get('name', '')
            explanation_content = problem_info.get('explanation_content', '')
            
            print(f"\n🔍 处理题目: {name} (ID: {problem_id})")
            
            # 提取代码
            extracted_code = extract_code_from_explanation(explanation_content)
            
            if extracted_code:
                code_dict[problem_id] = {
                    'name': name,
                    'code': extracted_code
                }
                explanation_with_code[problem_id] = {
                    'name': name,
                    'original_explanation': explanation_content,
                    'extracted_code': extracted_code
                }
                print(f"  ✓ 成功提取代码 ({len(extracted_code)} 字符)")
                # 显示代码预览
                preview = extracted_code[:100] + "..." if len(extracted_code) > 100 else extracted_code
                print(f"  📝 代码预览: {preview}")
            else:
                print(f"  ⚠️ 未找到代码块")
        
        return code_dict, explanation_with_code
        
    except Exception as e:
        print(f"❌ 处理文件失败: {e}")
        return None, None

def save_extracted_results(code_dict, explanation_with_code, base_filename):
    """保存提取结果"""
    import time
    timestamp = int(time.time())
    
    # 保存纯代码字典
    code_filename = f"extracted_code_{timestamp}.json"
    try:
        with open(code_filename, 'w', encoding='utf-8') as f:
            json.dump(code_dict, f, ensure_ascii=False, indent=2)
        print(f"📄 纯代码字典已保存: {code_filename}")
    except Exception as e:
        print(f"❌ 保存纯代码字典失败: {e}")
    
    # 保存完整对比版本
    full_filename = f"explanation_with_extracted_code_{timestamp}.json"
    try:
        with open(full_filename, 'w', encoding='utf-8') as f:
            json.dump(explanation_with_code, f, ensure_ascii=False, indent=2)
        print(f"📄 完整对比版本已保存: {full_filename}")
    except Exception as e:
        print(f"❌ 保存完整版本失败: {e}")
    
    return code_filename, full_filename

def print_extraction_summary(code_dict):
    """打印提取结果摘要"""
    print("\n" + "="*60)
    print("📊 代码提取结果摘要")
    print("="*60)
    
    for problem_id, problem_info in code_dict.items():
        name = problem_info['name']
        code = problem_info['code']
        
        print(f"\n📝 题目: {name} (ID: {problem_id})")
        print(f"📏 代码长度: {len(code)} 字符")
        print("🔍 提取的代码:")
        print("-" * 40)
        print(code)
        print("-" * 40)

def main():
    """主函数"""
    print("🚀 explanation_content 代码提取工具")
    print("提取 <code> 和 </code> 之间的纯代码内容")
    print("="*60)
    
    # 处理最新的 group_4 字典文件
    import glob
    dict_files = glob.glob('group_4_explanation_dict_*.json')
    if not dict_files:
        print("❌ 未找到 group_4_explanation_dict_*.json 文件")
        return
    
    latest_file = max(dict_files)
    print(f"📂 处理文件: {latest_file}")
    
    # 提取代码
    code_dict, explanation_with_code = process_explanation_dict(latest_file)
    
    if code_dict:
        print(f"\n✅ 成功提取了 {len(code_dict)} 个题目的代码")
        
        # 保存结果
        code_file, full_file = save_extracted_results(code_dict, explanation_with_code, latest_file)
        
        # 打印摘要
        print_extraction_summary(code_dict)
        
        print("\n🎉 代码提取完成！")
        print(f"📄 纯代码字典: {code_file}")
        print(f"📄 完整对比版本: {full_file}")
    else:
        print("❌ 代码提取失败")

if __name__ == "__main__":
    main()
