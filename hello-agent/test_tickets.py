import os
import json

# Load api key
with open(r"D:\iCloudDrive\iCloud~md~obsidian\shushu\hello-agents\.env") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k] = v

from tavily import TavilyClient

def check_tickets(spot: str) -> str:
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "\u9519\u8bef:\u672a\u914d\u7f6e TAVILY_API_KEY"
    tavily = TavilyClient(api_key=api_key)

    query = f"{spot} \u95e8\u7968 \u4eca\u65e5 \u4f59\u7968 \u552e\u7f44"
    resp = tavily.search(query=query, search_depth="basic", include_answer=True)

    if resp.get("answer"):
        return resp["answer"]
    results = resp.get("results", [])
    if not results:
        return f"\u672a\u67e5\u5230{spot}\u95e8\u7968\u4fe1\u606f"
    return "\n".join(f"- {r['title']}: {r['content']}" for r in results)

for spot in ["\u6545\u5bab", "\u5929\u575b", "\u957f\u57ce"]:
    print(f"=== {spot} ===")
    result = check_tickets(spot)
    print(result)
    print()
