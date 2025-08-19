#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复emoji图标工具
将所有ASCII标识符恢复为原始的emoji表情符号
"""
import os
import glob

def restore_emojis():
    """恢复emoji表情符号"""
    
    # ASCII标识符到emoji的映射（反向映射）
    ascii_to_emoji = {
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
        '🚀': '🚀',
        '📝': '📝',
        '📊': '📊'
    }
    
    print("🚀 恢复emoji表情符号工具")
    print("=" * 60)
    
    # 获取所有Python文件
    python_files = glob.glob("*.py")
    print(f"📂 找到 {len(python_files)} 个Python文件")
    print("-" * 60)
    
    total_replacements = 0
    files_modified = 0
    
    for file_path in python_files:
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            replacements_in_file = 0
            
            # 执行所有替换
            for ascii_tag, emoji in ascii_to_emoji.items():
                if ascii_tag in content:
                    count = content.count(ascii_tag)
                    content = content.replace(ascii_tag, emoji)
                    if count > 0:
                        print(f"   替换 {ascii_tag} -> {emoji} ({count}次)")
                        replacements_in_file += count
            
            # 如果有修改，写回文件
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ 已恢复: {file_path} ({replacements_in_file}个替换)")
                files_modified += 1
                total_replacements += replacements_in_file
            else:
                print(f"- 无需恢复: {file_path}")
        
        except Exception as e:
            print(f"❌ 处理文件 {file_path} 时出错: {e}")
    
    print("-" * 60)
    print(f"🎉 恢复完成!")
    print(f"📊 恢复了 {files_modified}/{len(python_files)} 个文件")
    print(f"📊 总共进行了 {total_replacements} 次替换")
    print("📝 现在所有文件都恢复了原始的emoji图标")

if __name__ == "__main__":
    restore_emojis()
