import sys
import json
import base64
import os
from notion_client import Client

# Initialize clients (Expects env vars to be set by n8n or system)
try:
    from openai import OpenAI
    client_ai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except ImportError:
    client_ai = None

try:
    notion = Client(auth=os.environ.get("NOTION_TOKEN"))
except Exception:
    notion = None

def decode_message(b64_str):
    try:
        if not b64_str:
            return ""
        return base64.b64decode(b64_str).decode('utf-8')
    except Exception as e:
        return f"[Error decoding message: {str(e)}]"

def ask_openai(user_query):
    if not client_ai:
        return {"action": "error", "reply": "OpenAI library not installed or API Key missing."}
    
    system_prompt = """
    You are a helpful 'Universal Notion Assistant' bot for Slack.
    Your goal is to help the user interact with their Notion workspace.
    
    Analyze the user's query and strictly return a JSON object with:
    1. "action": One of ["search", "create_page", "unknown", "chat"]
    2. "params": Dictionary of parameters based on action.
       - for "search": {"query": "search term"}
       - for "create_page": {"title": "page title", "content": "page content summary"}
    3. "reply": A friendly, natural language response to the user summarizing what you are about to do (in Korean).
    
    If it's just a casual chat, action="chat", and put your answer in "reply".
    """
    
    try:
        response = client_ai.chat.completions.create(
            model="gpt-4o",  # or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"action": "error", "reply": f"AI Error: {str(e)}"}

def perform_notion_action(action_data):
    if not notion:
         return "Notion integration is not configured (Token missing)."

    action = action_data.get("action")
    params = action_data.get("params", {})
    
    if action == "search":
        query = params.get("query", "")
        try:
            results = notion.search(query=query, page_size=3).get("results", [])
            if not results:
                return "검색 결과가 없습니다."
            
            output = "🔍 **Notion 검색 결과:**\n"
            for page in results:
                title = "Untitled"
                # Handle different Notion object types (page, database)
                if page["object"] == "page":
                    props = page.get("properties", {})
                    # Try to find a title property (usually 'Name' or 'title')
                    for key, val in props.items():
                        if val["type"] == "title" and val["title"]:
                            title = val["title"][0]["text"]["content"]
                            break
                elif page["object"] == "database":
                    if page.get("title"):
                        title = page["title"][0]["text"]["content"]
                
                url = page.get("url", "#")
                output += f"- <{url}|{title}>\n"
            return output
        except Exception as e:
            return f"Notion Search Error: {str(e)}"

    elif action == "create_page":
        # Simplified creation: requires a parent page ID. 
        # For universal assistant, without a parent ID, we might default to searching via search first?
        # For now, return a placeholder as we don't know WHERE to create it.
        return "Notion 페이지 생성 기능은 현재 부모 페이지 ID 설정이 필요하여 준비 중입니다. (검색 기능만 가능)"

    elif action == "chat":
        return "" # Logic handled in main response

    return "" # Default

def main():
    # Input arguments from n8n: ["script.py", "b64_message", "user", "channel"]
    if len(sys.argv) < 2:
        print(json.dumps({"response": "Error: Not enough arguments."}))
        sys.exit(1)

    b64_message = sys.argv[1]
    user_id = sys.argv[2] if len(sys.argv) > 2 else "unknown"
    # channel_id = sys.argv[3] if len(sys.argv) > 3 else "unknown"

    user_text = decode_message(b64_message)
    
    # 1. Ask AI intent
    ai_decision = ask_openai(user_text)
    
    reply_text = ai_decision.get("reply", "")
    
    # 2. Perform Notion Action if needed
    notion_result = ""
    if ai_decision.get("action") not in ["chat", "unknown", "error"]:
        notion_result = perform_notion_action(ai_decision)
    
    # 3. Combine Response
    final_response = f"{reply_text}\n\n{notion_result}".strip()

    # Output JSON for n8n
    result = {
        "response": final_response,
        "original_text": user_text,
        "action_taken": ai_decision.get("action")
    }
    print(json.dumps(result))

if __name__ == "__main__":
    main()
