# Hello Agents - Python 学习笔记

> 最后更新: 2026-05-29  |  当前章节: hello_agents_llm.py

---

## 已学概念


- [x] A or B 模式用于默认值
- [x] class 类定义与 __init__
- [x] if __name__ == "__main__" 入口守卫
- [x] import 导入模块
- [x] try/except 异常处理
- [x] 函数类型标注 (List[Dict[str, str]])
- [x] 变量局部作用域 (apiKey vs self.model)
- [x] 字典解包 **kwargs
- [x] 流式响应 for chunk in response

---

## 学习进度


## 第一天：Hello Agents LLM 客户端

学习了如何封装一个 LLM 客户端类，包括：
- 从 `.env` 加载配置
- 类的构造与默认值处理
- 调用 OpenAI 接口并处理流式响应
- 异常捕获与降级处理
- 项目入口格式

下步预备：继续深入 agent 项目，学习 async/await 和 Pydantic models。

---

## LLM 指令模板


当你希望 Codex 帮你学习 Python 或操作这个项目时，可以直接复制以下模板作为提示词：


### 可用工具


- 阅读和解释 `hello_agents_llm.py` 中的 Python 代码
- 对比相似概念（如 dataclass vs BaseModel）
- 生成类似的代码示例供学习
- 说明包的结构和各文件的作用
- 后期可以运行 Python 脚本测试代码
- 帮助配置 .env 和安装依赖

### 输出格式要求


1. **代码解释**：按以下结构回答：
   - 这是什么：一句话定义
   - 为什么用在这里：在 agent 项目中的具体角色
   - 精简示例：不超过 5 行的独立示例

2. **概念对比**：用表格展示差异
   - 例如：dataclass 和 Pydantic BaseModel 的区别

3. **解释语言**：以中文为主，英文术语后可括注中文翻译

4. **每次学习结束**：调用 update_study_notes.py 更新进度

### 重要提示


- 说明概念时尽量用简单直接的语言，避免学术化表述
- 如果某个概念有常见的坑（pitfall），必须指出
- 如果用户提出的问题包含多个 Python 概念，分层解释，先粗后细
- 不要一次性输出大段代码，若需展示多行，用 ```python ... ``` 格式块
- 学习进度必须实时保存到 .progress.json，不能丢失
