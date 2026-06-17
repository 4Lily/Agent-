import re
import os
from dotenv import load_dotenv
from OpenAICompatibleClient import OpenAICompatibleClient
from get_attraction import get_attraction
from get_weather import get_weather
import json

load_dotenv()

# --- 1. 配置LLM客户端 ---
# --- 1. 配置LLM客户端 ---
# 请根据您使用的服务，将这里替换成对应的凭证和地址
API_KEY = "sk-dcbdb95c2862473d91bbd2f17d906974"
BASE_URL = "https://api.deepseek.com"
MODEL_ID = "deepseek-chat"
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("未配置TAVILY_API_KEY环境变量。")



llm = OpenAICompatibleClient(
    model=MODEL_ID,
    api_key=API_KEY,
    base_url=BASE_URL
)

# --- 2. 初始化 ---
user_prompt = "你好，请帮我查询一下今天北京的天气，我喜欢登高，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f"用户请求: {user_prompt}"]

print(f"用户输入: {user_prompt}\n" + "="*40)

# --- 3. 运行主循环 ---
for i in range(5): # 设置最大循环次数
    print(f"--- 循环 {i+1} ---\n")
    
    # 3.1. 构建Prompt
    full_prompt = "\n".join(prompt_history)
    
    # 3.2. 调用LLM进行思考
    with open ("AGENT_SYSTEM_PROMPT.txt", "r", encoding="utf-8") as f:
        AGENT_SYSTEM_PROMPT = f.read().strip()
    llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
    # 模型可能会输出多余的Thought-Action，需要截断
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")
    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)
    
    # 3.3. 解析并执行行动
    action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip()

    if action_str.startswith("Finish"):
        final_answer = re.match(r"Finish\[(.*)\]", action_str).group(1)
        print(f"任务完成，最终答案: {final_answer}")
        conversation = "\n".join(prompt_history)
        if os.path.exists("memory.json"):
            with open("memory.json", "r", encoding="utf-8") as f:
                preference = json.load(f)
        else:
            preference = {}
            
        memory_context = json.dumps(preference, ensure_ascii=False)
        memory_prompt = f"从用户提示词中提取用户偏好信息（喜欢什么类型的景点、预算等），以 JSON 格式返回。如果没有新信息，返回 null。\n\n对话:\n{conversation}"
        memory_js=llm.generate(memory_prompt, system_prompt=memory_context)
        try:
            new_data = json.loads(memory_js) if memory_js.strip() else None
        except json.JSONDecodeError:
            print(f"警告: 记忆解析失败，LLM 返回了非 JSON: {memory_js[:50]}")
            new_data = None
        if new_data and new_data.get("update") != False:
            preference.update(new_data)
            json.dump(preference, open("memory.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

        # 跳出循环，不再继续解析 Action
        break
        
    tool_name = re.search(r"(\w+)\(", action_str).group(1)
    args_str = re.search(r"\((.*)\)", action_str).group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

    available_tools = {"get_attraction": get_attraction, "get_weather": get_weather}
    
    if tool_name in available_tools:
        observation = available_tools[tool_name](**kwargs)
    else:
        observation = f"错误:未定义的工具 '{tool_name}'"

    # 3.4. 记录观察结果
    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "="*40)
    prompt_history.append(observation_str)
