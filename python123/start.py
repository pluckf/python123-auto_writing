"""
Python123.io API 工具集启动器
一键运行所有功能的快捷脚本
"""

import os
import sys
import subprocess

def show_banner():
    """显示横幅"""
    banner = """
    ╔══════════════════════════════════════════╗
    ║      Python123.io API 工具集            ║
    ║      仅供学习使用                        ║
    ╚══════════════════════════════════════════╝
    """
    print(banner)

def show_menu():
    """显示菜单"""
    menu = """
    请选择要运行的工具:

    🚀 推荐选项:
    [1] 快速演示所有功能 (quick_run_all.py)
        
    📊 完整工作流程:
    [2] 完整数据获取和测试 (run_all.py)
    [3] 完整数据获取和测试3个题目
        
    🔧 单独功能:
    [4] 获取课程数据 (main.py)
    [5] 获取问题数据 (problems_fetcher.py)
    [6] 获取代码数据 (code_fetcher.py)
    [7] 测试PUT请求 (put_code.py)
        
    📚 其他:
    [8] 查看使用说明 (README.md)
    [9] 查看所有文件
    [0] 退出
    """
    print(menu)

def run_script(script_name, args=None):
    """运行指定脚本"""
    try:
        cmd = [sys.executable, script_name]
        if args:
            cmd.extend(args)
            
        print(f"\n🔄 正在运行: {' '.join(cmd)}")
        print("-" * 50)
        
        result = subprocess.run(cmd, cwd=os.getcwd())
        
        print("-" * 50)
        if result.returncode == 0:
            print("✅ 运行完成")
        else:
            print(f"⚠️  程序退出，返回码: {result.returncode}")
            
    except FileNotFoundError:
        print(f"❌ 找不到文件: {script_name}")
    except Exception as e:
        print(f"❌ 运行出错: {e}")

def show_files():
    """显示所有文件"""
    print("\n📁 当前目录文件:")
    print("-" * 50)
    
    files = os.listdir('.')
    python_files = [f for f in files if f.endswith('.py')]
    json_files = [f for f in files if f.endswith('.json')]
    other_files = [f for f in files if not f.endswith('.py') and not f.endswith('.json')]
    
    if python_files:
        print("🐍 Python脚本:")
        for f in sorted(python_files):
            print(f"   {f}")
    
    if json_files:
        print("\n📄 数据文件:")
        for f in sorted(json_files):
            print(f"   {f}")
    
    if other_files:
        print("\n📋 其他文件:")
        for f in sorted(other_files):
            print(f"   {f}")

def show_readme():
    """显示README内容"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
            print("\n📖 使用说明:")
            print("=" * 60)
            print(content)
    except FileNotFoundError:
        print("❌ README.md 文件不存在")
    except Exception as e:
        print(f"❌ 读取README失败: {e}")

def main():
    """主函数"""
    show_banner()
    
    while True:
        try:
            show_menu()
            choice = input("请输入选择 (0-9): ").strip()
            
            if choice == '0':
                print("👋 再见！")
                break
                
            elif choice == '1':
                run_script('quick_run_all.py')
                
            elif choice == '2':
                run_script('run_all.py', ['1'])
                
            elif choice == '3':
                run_script('run_all.py', ['3'])
                
            elif choice == '4':
                run_script('main.py')
                
            elif choice == '5':
                print("\n子选项:")
                print("a) 获取第一个课程组问题")
                print("b) 获取所有问题")
                print("c) 显示已保存问题")
                
                sub_choice = input("请选择 (a-c): ").strip().lower()
                if sub_choice == 'a':
                    run_script('problems_fetcher.py')
                elif sub_choice == 'b':
                    run_script('problems_fetcher.py', ['--all'])
                elif sub_choice == 'c':
                    run_script('problems_fetcher.py', ['--show'])
                else:
                    print("❌ 无效选择")
                    
            elif choice == '6':
                print("\n子选项:")
                print("a) 自动获取编程题代码")
                print("b) 指定题目获取 (8717 114918 99764)")
                
                sub_choice = input("请选择 (a-b): ").strip().lower()
                if sub_choice == 'a':
                    run_script('code_fetcher.py')
                elif sub_choice == 'b':
                    run_script('code_fetcher.py', ['8717', '114918', '99764'])
                else:
                    print("❌ 无效选择")
                    
            elif choice == '7':
                print("\n子选项:")
                print("a) 自动测试PUT请求")
                print("b) 指定题目测试 (8717 114918 99764)")
                
                sub_choice = input("请选择 (a-b): ").strip().lower()
                if sub_choice == 'a':
                    run_script('put_code.py', ['--auto'])
                elif sub_choice == 'b':
                    run_script('put_code.py', ['8717', '114918', '99764'])
                else:
                    print("❌ 无效选择")
                    
            elif choice == '8':
                show_readme()
                
            elif choice == '9':
                show_files()
                
            else:
                print("❌ 无效选择，请输入0-9之间的数字")
                
            if choice != '0':
                input("\n按回车键继续...")
                print("\n" + "=" * 60)
                
        except KeyboardInterrupt:
            print("\n\n👋 用户取消操作，再见！")
            break
        except Exception as e:
            print(f"\n❌ 程序出错: {e}")
            input("按回车键继续...")

if __name__ == "__main__":
    main()
