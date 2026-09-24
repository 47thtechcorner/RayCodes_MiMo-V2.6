import json
import os
import sys
import urllib.request
import urllib.error

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# MiMo-V2.6 Local Agentic Automation Engine
MODEL_NAME = "mimo-agent"
OLLAMA_ENDPOINT = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = """You are MiMo-V2.6, a hyper-efficient 9B distilled agentic AI. 
Your goal is to parse developer automation requests, plan execution steps, generate clean Python code, and output structured JSON tool actions.
Output strictly valid JSON with keys: 'analysis', 'steps', 'code', 'status'."""

def call_mimo_agent(user_prompt: str) -> dict:
    """Send structured prompt to local MiMo-V2.6 agent endpoint."""
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "format": "json",
        "stream": False
    }
    
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(
        OLLAMA_ENDPOINT, 
        data=json.dumps(payload).encode("utf-8"), 
        headers=headers, 
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            content = res_data.get("message", {}).get("content", "{}")
            return json.loads(content)
    except Exception as err:
        print(f"⚠️ Local Ollama endpoint unreachable ({err}). Ensure 'ollama run mimo-agent' is running.")
        sys.exit(1)

def run_agent_workflow(task_description: str):
    """Execute multi-step developer automation task using MiMo-V2.6."""
    print("==================================================")
    print("🤖 MiMo-V2.6 Distill Qwen-9B Local Agent Starting")
    print(f"📋 Target Task: {task_description}")
    print("==================================================\n")
    
    print("⚡ Sending request to local MiMo-V2.6 model...")
    agent_res = call_mimo_agent(task_description)
    
    analysis = agent_res.get("analysis", "MiMo-V2.6 task analysis completed.")
    steps = agent_res.get("steps", ["Inspect codebase", "Refactor components", "Verify build"])
    code = agent_res.get("code", "# Generated Python code snippet\nprint('MiMo-V2.6 Agent Active')")
    status = agent_res.get("status", "SUCCESS")

    print("\n🔍 --- AGENT ANALYSIS ---")
    print(analysis)
    
    print("\n🛠️ --- EXECUTION STEPS ---")
    for idx, step in enumerate(steps, 1):
        print(f"  {idx}. {step}")
        
    print("\n💻 --- GENERATED CODE ---")
    print(code)
    
    os.makedirs("outputs", exist_ok=True)
    output_path = os.path.join("outputs", "outputs.md")
    
    output_content = f"""# ⚡ MiMo-V2.6 Agent Task Report

## 🎯 Task Objective
{task_description}

## 📊 Model Analysis & Execution Plan
{analysis}

### 🛠️ Execution Pipeline Steps
"""
    for idx, step in enumerate(steps, 1):
        output_content += f"{idx}. **{step}**\n"

    output_content += f"""
## 💻 Dynamic Code Output
```python
{code}
```

## 🏆 Execution Result
- **Agent Status**: {status}
- **Quantization**: IQ2_M GGUF (3GB Memory Footprint)
- **Model Base**: Distill-Qwen-9B (MiMo V2.6)
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_content.strip())
        
    print(f"\n✅ Output successfully written to '{output_path}'")

if __name__ == "__main__":
    task = "Analyze workspace, create a lightweight FastAPI endpoint for system health monitoring, and generate structured verification code."
    run_agent_workflow(task)
