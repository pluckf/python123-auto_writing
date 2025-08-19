#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python123.io 测试工具图形界面
提供友好的GUI界面来配置认证信息和执行测试
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
import subprocess
import sys
import os
from datetime import datetime
import queue

class Python123TestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python123.io 测试工具")
        self.root.geometry("900x700")
        
        # 消息队列用于线程间通信
        self.message_queue = queue.Queue()
        
        # 默认配置
        self.default_auth = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMTY1MzA4MzQ3MUBxcS5jb20iLCJuYW1lIjoi5aec6L-c5bCaIiwiaWQiOiIxMjQzOTYxIiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTEyODY0MjcwfSwiaWF0IjoxNzU1NTE1MjU1LCJleHAiOjE3NTY4MTEyNTV9.4CFizZ4KvcRwad7ACdvSPfG0Kf3epPQYJdwiv_YUPps"
        self.default_cookie = "token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImVtYWlsIjoiMTY1MzA4MzQ3MUBxcS5jb20iLCJuYW1lIjoi5aec6L-c5bCaIiwiaWQiOiIxMjQzOTYxIiwicm9sZXMiOlsic3R1ZGVudCJdLCJsYXN0X2xvZ2luIjoxNzU1NTEyODY0MjcwfSwiaWF0IjoxNzU1NTE1MjU1LCJleHAiOjE3NTY4MTEyNTV9.4CFizZ4KvcRwad7ACdvSPfG0Kf3epPQYJdwiv_YUPps; Hm_lvt_6f63cfeea8c9a84040e2c4389f01bb91=1755516075,1755522844; HMACCOUNT=3EE86EE065B9114B; Hm_lpvt_6f63cfeea8c9a84040e2c4389f01bb91=1755528898; io=VqDxjqf6eE8qFv9cABv0"
        
        self.create_widgets()
        self.load_saved_config()
        
        # 定时检查消息队列
        self.root.after(100, self.check_message_queue)
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置认证信息
        auth_frame = ttk.LabelFrame(main_frame, text="认证配置", padding="10")
        auth_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Authorization输入
        ttk.Label(auth_frame, text="Authorization Token:").grid(row=0, column=0, sticky=tk.W)
        self.auth_var = tk.StringVar(value=self.default_auth)
        auth_entry = ttk.Entry(auth_frame, textvariable=self.auth_var, width=80, show="*")
        auth_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 10))
        
        # Cookie输入
        ttk.Label(auth_frame, text="Cookie:").grid(row=2, column=0, sticky=tk.W)
        self.cookie_var = tk.StringVar(value=self.default_cookie)
        cookie_entry = ttk.Entry(auth_frame, textvariable=self.cookie_var, width=80, show="*")
        cookie_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(5, 10))
        
        # 显示/隐藏密码按钮
        self.show_auth = tk.BooleanVar()
        ttk.Checkbutton(auth_frame, text="显示认证信息", variable=self.show_auth, 
                       command=self.toggle_auth_visibility).grid(row=4, column=0, sticky=tk.W)
        
        # 保存认证信息按钮
        ttk.Button(auth_frame, text="保存配置", command=self.save_config).grid(row=5, column=0, sticky=tk.W, pady=(10, 0))
        ttk.Button(auth_frame, text="加载配置", command=self.load_config).grid(row=5, column=0, sticky=tk.E, pady=(10, 0))
        
        # 测试选项
        options_frame = ttk.LabelFrame(main_frame, text="测试选项", padding="10")
        options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 测试模式选择
        self.test_mode = tk.StringVar(value="extract_only")
        ttk.Radiobutton(options_frame, text="仅提取代码", variable=self.test_mode, 
                       value="extract_only").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(options_frame, text="提取并提交代码", variable=self.test_mode, 
                       value="extract_and_submit").grid(row=0, column=1, sticky=tk.W)
        
        # 测试范围选择
        ttk.Label(options_frame, text="测试范围:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.test_range = tk.StringVar(value="all_groups")
        ttk.Radiobutton(options_frame, text="所有Groups", variable=self.test_range, 
                       value="all_groups").grid(row=2, column=0, sticky=tk.W)
        ttk.Radiobutton(options_frame, text="指定Group", variable=self.test_range, 
                       value="specific_group").grid(row=2, column=1, sticky=tk.W)
        
        # 指定Group输入
        self.specific_group = tk.StringVar(value="7")
        ttk.Label(options_frame, text="Group编号:").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(options_frame, textvariable=self.specific_group, width=10).grid(row=3, column=1, sticky=tk.W)
        
        # 控制按钮
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="🧪 测试认证", command=self.test_auth).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(control_frame, text="🚀 开始测试", command=self.start_test).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(control_frame, text="📄 查看结果", command=self.view_results).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(control_frame, text="🔄 清空日志", command=self.clear_log).grid(row=0, column=3)
        
        # 日志显示区域
        log_frame = ttk.LabelFrame(main_frame, text="执行日志", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 配置权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        auth_frame.columnconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def toggle_auth_visibility(self):
        """切换认证信息显示/隐藏"""
        show_type = "" if self.show_auth.get() else "*"
        
        # 找到Entry组件并更新show属性
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame) and "认证配置" in str(child['text']):
                        for entry in child.winfo_children():
                            if isinstance(entry, ttk.Entry):
                                entry.configure(show=show_type)
    
    def log(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        self.log("日志已清空")
    
    def save_config(self):
        """保存配置到文件"""
        config = {
            "auth_token": self.auth_var.get(),
            "cookie": self.cookie_var.get(),
            "saved_at": datetime.now().isoformat()
        }
        
        try:
            with open("python123_gui_config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            self.log("✅ 配置已保存到 python123_gui_config.json")
            messagebox.showinfo("保存成功", "认证配置已保存！")
        except Exception as e:
            self.log(f"❌ 保存配置失败: {e}")
            messagebox.showerror("保存失败", f"保存配置时出错: {e}")
    
    def load_config(self):
        """从文件加载配置"""
        try:
            file_path = filedialog.askopenfilename(
                title="选择配置文件",
                filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
            )
            
            if file_path:
                with open(file_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                
                self.auth_var.set(config.get("auth_token", ""))
                self.cookie_var.set(config.get("cookie", ""))
                
                self.log(f"✅ 配置已从 {file_path} 加载")
                messagebox.showinfo("加载成功", "认证配置已加载！")
                
        except Exception as e:
            self.log(f"❌ 加载配置失败: {e}")
            messagebox.showerror("加载失败", f"加载配置时出错: {e}")
    
    def load_saved_config(self):
        """启动时自动加载保存的配置"""
        try:
            if os.path.exists("python123_gui_config.json"):
                with open("python123_gui_config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                
                self.auth_var.set(config.get("auth_token", self.default_auth))
                self.cookie_var.set(config.get("cookie", self.default_cookie))
                
                self.log("✅ 已自动加载保存的配置")
        except Exception as e:
            self.log(f"⚠️  加载保存配置失败: {e}")
    
    def test_auth(self):
        """测试认证信息"""
        auth_token = self.auth_var.get().strip()
        cookie = self.cookie_var.get().strip()
        
        if not auth_token or not cookie:
            messagebox.showerror("错误", "请填写完整的认证信息！")
            return
        
        self.log("🧪 开始测试认证信息...")
        self.status_var.set("测试认证中...")
        self.progress.start()
        
        # 在新线程中执行测试
        threading.Thread(target=self._test_auth_worker, args=(auth_token, cookie), daemon=True).start()
    
    def _test_auth_worker(self, auth_token, cookie):
        """测试认证信息的工作线程"""
        try:
            import requests
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json",
                "Cookie": cookie
            }
            
            # 测试API访问
            response = requests.get(
                "https://python123.io/api/v1/student/courses",
                headers=headers,
                verify=False,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                course_count = len(data.get('data', []))
                self.message_queue.put(("success", f"✅ 认证测试成功！找到 {course_count} 个课程"))
            else:
                error_msg = response.json().get('data', {}).get('message', '未知错误')
                self.message_queue.put(("error", f"❌ 认证失败: {error_msg} (HTTP {response.status_code})"))
                
        except Exception as e:
            self.message_queue.put(("error", f"❌ 认证测试异常: {e}"))
    
    def start_test(self):
        """开始测试"""
        auth_token = self.auth_var.get().strip()
        cookie = self.cookie_var.get().strip()
        
        if not auth_token or not cookie:
            messagebox.showerror("错误", "请填写完整的认证信息！")
            return
        
        # 确认操作
        if self.test_mode.get() == "extract_and_submit":
            if not messagebox.askyesno("确认", "将会提取代码并提交到服务器，确认继续吗？"):
                return
        
        self.log("🚀 开始执行测试...")
        self.status_var.set("测试执行中...")
        self.progress.start()
        
        # 在新线程中执行测试
        threading.Thread(target=self._test_worker, args=(auth_token, cookie), daemon=True).start()
    
    def _test_worker(self, auth_token, cookie):
        """测试执行的工作线程"""
        try:
            if self.test_range.get() == "all_groups":
                # 执行全组测试
                script_path = "all_groups_tester.py"
                self.message_queue.put(("log", "📋 执行全组测试..."))
            else:
                # 执行指定组测试
                group_num = self.specific_group.get()
                script_path = f"group{group_num}_tester.py"
                self.message_queue.put(("log", f"📋 执行 Group{group_num} 测试..."))
            
            # 检查脚本是否存在
            if not os.path.exists(script_path):
                if self.test_range.get() == "specific_group":
                    # 为指定组创建临时脚本
                    self._create_specific_group_script(group_num, auth_token, cookie)
                    script_path = f"temp_group{group_num}_tester.py"
                else:
                    self.message_queue.put(("error", f"❌ 未找到测试脚本: {script_path}"))
                    return
            
            # 设置环境变量传递认证信息
            env = os.environ.copy()
            env['PYTHON123_AUTH'] = auth_token
            env['PYTHON123_COOKIE'] = cookie
            env['PYTHON123_MODE'] = self.test_mode.get()
            
            # 执行测试脚本
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                bufsize=1,
                universal_newlines=True
            )
            
            # 实时读取输出
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.message_queue.put(("log", output.strip()))
            
            # 获取返回码
            return_code = process.poll()
            
            if return_code == 0:
                self.message_queue.put(("success", "✅ 测试执行完成！"))
            else:
                error_output = process.stderr.read()
                self.message_queue.put(("error", f"❌ 测试执行失败: {error_output}"))
                
            # 清理临时文件
            if script_path.startswith("temp_"):
                try:
                    os.remove(script_path)
                except:
                    pass
                    
        except Exception as e:
            self.message_queue.put(("error", f"❌ 执行异常: {e}"))
    
    def _create_specific_group_script(self, group_num, auth_token, cookie):
        """为指定组创建临时测试脚本"""
        script_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from group7_tester import Group7Tester

class Group{group_num}Tester(Group7Tester):
    def get_group_problems(self):
        """获取group{group_num}的所有问题"""
        problems = []
        
        for course_name, course_id in self.course_ids.items():
            group_mapping = self.course_group_mapping.get(course_name, {{}})
            group_id = group_mapping.get('{group_num}')  
            
            if group_id:
                print(f"🔍 在课程 '{{course_name}}' 中找到 group{group_num} (ID: {{group_id}})")
                
                url = f"{{self.BASE_URL}}/{{course_id}}/groups/{{group_id}}/problems"
                try:
                    import requests
                    response = requests.get(url, headers=self.headers, verify=False)
                    if response.status_code == 200:
                        group_problems = response.json().get('data', [])
                        print(f"   📝 找到 {{len(group_problems)}} 个题目")
                        
                        for problem in group_problems:
                            if '_id' in problem:
                                problems.append({{
                                    'course_name': course_name,
                                    'course_id': course_id,
                                    'group_id': group_id,
                                    'problem_id': problem['_id'],
                                    'problem_name': problem.get('name', 'Unknown'),
                                    'type': problem.get('type', 'unknown')
                                }})
                    else:
                        print(f"   ❌ 获取问题失败: HTTP {{response.status_code}}")
                        
                except Exception as e:
                    print(f"   ❌ 请求异常: {{e}}")
            else:
                print(f"⚠️  课程 '{{course_name}}' 中未找到 group{group_num}")
        
        return problems

if __name__ == "__main__":
    print("🚀 Group{group_num} 专用测试工具")
    
    # 从环境变量获取认证信息
    auth_token = os.environ.get('PYTHON123_AUTH', '{auth_token}')
    cookie = os.environ.get('PYTHON123_COOKIE', '{cookie}')
    mode = os.environ.get('PYTHON123_MODE', 'extract_only')
    
    tester = Group{group_num}Tester()
    tester.update_credentials(auth_token, cookie)
    
    if not tester.load_session_data():
        sys.exit(1)
    
    problems = tester.get_group_problems()
    
    if not problems:
        print("❌ 未找到group{group_num}问题")
        sys.exit(1)
    
    print(f"✅ 找到 {{len(problems)}} 个group{group_num}问题")
    
    tester.fetch_all_group_data(problems)
    
    if tester.group_codes and mode == 'extract_and_submit':
        tester.batch_submit_group()
    else:
        tester.save_results()
'''
        
        with open(f"temp_group{group_num}_tester.py", "w", encoding="utf-8") as f:
            f.write(script_content)
    
    def view_results(self):
        """查看测试结果"""
        result_files = []
        
        # 查找结果文件
        import glob
        patterns = ["*_submission_results_*.json", "*_extracted_codes_*.json", "*_test_summary_*.json"]
        
        for pattern in patterns:
            result_files.extend(glob.glob(pattern))
        
        if not result_files:
            messagebox.showinfo("提示", "未找到测试结果文件")
            return
        
        # 让用户选择文件
        file_path = filedialog.askopenfilename(
            title="选择结果文件",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            initialdir="."
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # 在新窗口中显示结果
                self._show_result_window(file_path, data)
                
            except Exception as e:
                messagebox.showerror("错误", f"读取结果文件失败: {e}")
    
    def _show_result_window(self, file_path, data):
        """在新窗口中显示结果"""
        result_window = tk.Toplevel(self.root)
        result_window.title(f"测试结果 - {os.path.basename(file_path)}")
        result_window.geometry("800x600")
        
        # 结果显示区域
        result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD)
        result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 格式化显示数据
        formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
        result_text.insert(tk.END, formatted_data)
        result_text.configure(state='disabled')
        
        # 关闭按钮
        ttk.Button(result_window, text="关闭", 
                  command=result_window.destroy).pack(pady=10)
    
    def check_message_queue(self):
        """检查消息队列"""
        try:
            while True:
                msg_type, message = self.message_queue.get_nowait()
                
                if msg_type == "log":
                    self.log(message)
                elif msg_type == "success":
                    self.log(message)
                    self.status_var.set("完成")
                    self.progress.stop()
                    messagebox.showinfo("成功", message)
                elif msg_type == "error":
                    self.log(message)
                    self.status_var.set("错误")
                    self.progress.stop()
                    messagebox.showerror("错误", message)
                    
        except queue.Empty:
            pass
        
        # 继续检查队列
        self.root.after(100, self.check_message_queue)

def main():
    """主函数"""
    root = tk.Tk()
    app = Python123TestGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()

if __name__ == "__main__":
    main()
