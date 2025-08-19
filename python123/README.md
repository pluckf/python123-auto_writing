# Python123.io API 工具集使用指南

## 📁 项目文件概览

```
python123/
├── main.py                     # 主课程数据获取工具
├── problems_fetcher.py         # 问题数据获取工具
├── code_fetcher.py            # 代码获取工具
├── programming_code_fetcher.py # 编程题专用代码获取工具
├── put_code.py               # PUT请求代码提交工具
├── run_all.py               # 完整工作流程工具（复杂版）
├── quick_run_all.py         # 快速演示工具（推荐）
└── README.md               # 本说明文档
```

## 🚀 如何一次运行所有功能

### 方法1：快速演示（推荐）
```bash
python quick_run_all.py
```

这是最简单的方式，会依次执行：
1. ✅ 获取课程列表
2. ✅ 获取问题数据
3. ✅ 获取编程题代码（跳过选择题）
4. ✅ 测试PUT请求
5. ✅ 验证更新结果
6. ✅ 保存演示数据

### 方法2：完整工作流程
```bash
python run_all.py        # 测试1个编程题的PUT请求
python run_all.py 3      # 测试3个编程题的PUT请求
python run_all.py 0      # 只获取数据，不测试PUT
```

## 🛠️ 单独功能工具

### 1. 获取课程和组数据
```bash
python main.py
```

### 2. 获取问题列表
```bash
python problems_fetcher.py           # 获取第一个课程第一个组的问题
python problems_fetcher.py --all     # 获取所有课程所有组的问题
python problems_fetcher.py --show    # 显示已保存的问题ID
```

### 3. 获取题目代码
```bash
python code_fetcher.py                    # 自动查找编程题并获取代码
python code_fetcher.py 8717 114918 99764  # 获取指定题目代码
```

### 4. 编程题代码专用工具
```bash
python programming_code_fetcher.py        # 获取第一个编程题代码
python programming_code_fetcher.py --all  # 获取所有编程题代码
```

### 5. PUT请求测试
```bash
python put_code.py                    # 测试指定编程题PUT请求
python put_code.py --auto             # 自动查找第一个编程题测试
python put_code.py 8717 114918 99764  # 指定题目测试
```

## 📊 输出文件说明

运行后会生成以下文件：

### 数据文件
- `python123_ids.json` - 课程和组ID数据
- `problem_ids.json` - 问题ID数据
- `problems_course_*.json` - 具体课程组的问题数据
- `problem_code_*.json` - 题目代码数据

### 测试结果文件
- `put_test_result_*.json` - PUT请求测试结果
- `quick_demo_result_*.json` - 快速演示结果
- `python123_complete_session_*.json` - 完整会话数据
- `session_report_*.json` - 会话报告

## 🎯 功能特性

### ✅ 已实现功能
1. **数据获取**
   - 课程列表获取
   - 问题列表获取
   - 题目代码获取

2. **智能过滤**
   - 自动跳过选择题（type='choice'）
   - 专注处理编程题（type='programming'）

3. **代码提交**
   - PUT请求发送代码
   - 自动验证更新结果

4. **数据管理**
   - 自动保存所有数据
   - JSON格式存储
   - 完整的会话记录

### 🔧 API端点
- `GET /api/v1/student/courses` - 获取课程列表
- `GET /api/v1/student/courses/{course_id}/groups/{group_id}/problems` - 获取问题列表
- `GET /api/v1/student/courses/{course_id}/groups/{group_id}/problems/{problem_id}/code` - 获取代码
- `PUT /api/v1/student/courses/{course_id}/groups/{group_id}/problems/{problem_id}/code` - 提交代码

## 🎨 使用示例

### 基本使用流程
```bash
# 1. 快速查看所有功能
python quick_run_all.py

# 2. 如果需要处理更多数据
python run_all.py 5  # 测试5个编程题

# 3. 查看已保存的数据
python problems_fetcher.py --show
```

### 高级使用
```bash
# 获取指定课程组的所有问题
python problems_fetcher.py --all

# 获取所有编程题的代码
python programming_code_fetcher.py --all

# 测试特定题目的PUT请求
python put_code.py 8717 114918 99764
```

## 📝 注意事项

1. **学习目的**：所有工具仅供学习研究使用
2. **权限限制**：某些课程组可能有访问限制
3. **请求频率**：工具内置了适当的延时避免请求过快
4. **数据安全**：所有数据都保存在本地文件中

## 🔍 故障排除

如果遇到问题：
1. 检查网络连接
2. 确认Token是否有效
3. 使用`quick_run_all.py`进行快速测试
4. 查看生成的日志文件

## 📞 技术支持

所有工具都包含详细的错误信息和状态反馈，如果遇到问题可以查看控制台输出获取具体信息。

---
**最后更新**: 2025-08-18
**版本**: 1.0.0
