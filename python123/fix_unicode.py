#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Windows控制台Unicode表情符号编码问题
将表情符号替换为兼容的ASCII字符
"""

import os
import re
import glob

def fix_unicode_in_file(filepath):
    """修复单个文件中的Unicode表情符号"""
    
    # 表情符号到ASCII字符的映射
    emoji_replacements = {
        '🚀': '🚀',
        '📂': '📂', 
        '📊': '📊',
        '🔍': '🔍',
        '📚': '📚',
        '📁': '📁',
        '📝': '📝',
        '🔥': '🔥',
        '📋': '📋',
        '✅': '✅',
        '❌': '❌',
        '⚠️': '⚠️',
        '🎯': '🎯',
        '🧪': '🧪',
        '📍': '📍',
        '🔗': '🔗',
        '💻': '💻',
        '🎉': '🎉',
        '📄': '📄',
        '⚡': '⚡',
        '🔧': '🔧',
        '💬': '💬',
        '🆔': '🆔',
        '📬': '📬',
        '🖥️': '🖥️',
        '🗂️': '🗂️',
    }
    
    try:
        # 读取文件
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # 替换所有表情符号
        for emoji, replacement in emoji_replacements.items():
            if emoji in content:
                content = content.replace(emoji, replacement)
                modified = True
                print(f"   替换 {emoji} -> {replacement}")
        
        # 如果有修改，保存文件
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 已修复: {filepath}")
            return True
        else:
            print(f"- 无需修复: {filepath}")
            return False
            
    except Exception as e:
        print(f"✗ 修复失败: {filepath} - {e}")
        return False

def main():
    """主函数 - 扫描并修复所有Python文件"""
    print("🚀 Windows控制台Unicode表情符号修复工具")
    print("=" * 60)
    
    # 查找所有Python文件
    python_files = []
    patterns = ['*.py', 'group*_tester.py', 'all_groups_tester.py', 'python123_gui.py']
    
    for pattern in patterns:
        python_files.extend(glob.glob(pattern))
    
    # 去重
    python_files = list(set(python_files))
    
    if not python_files:
        print("⚠️ 未找到Python文件")
        return
    
    print(f"🔍 找到 {len(python_files)} 个Python文件")
    print("-" * 60)
    
    fixed_count = 0
    
    for filepath in python_files:
        print(f"📝 {filepath}")
        if fix_unicode_in_file(filepath):
            fixed_count += 1
        print()
    
    print("-" * 60)
    print(f"🎉 修复完成!")
    print(f"📊 修复了 {fixed_count}/{len(python_files)} 个文件")
    
    if fixed_count > 0:
        print("📊 现在可以在Windows控制台正常运行这些脚本了")

if __name__ == "__main__":
    main()
