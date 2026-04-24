from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import time

def ask_llm(prompt, username):
    start = time.time()
    max_tokens = 50

    user_message = prompt.replace("<|", "").replace("|>", "")

    username = username.replace("<|", "").replace("|>", "")
    username = username[:32]

    now = datetime.now(ZoneInfo("Europe/Amsterdam")).strftime("It is %A, %B %d, %Y, %H:%M in Amsterdam (%Z)")

    r = requests.post(
        "http://192.168.68.110:8080/completion",
        json={
            "prompt": f"""You are Void-GPT, a sarcastic, rude, playful Discord bot.

Chatting with {username}. {now}

Rules:
- Reply in ONE short sarcastic sentence (max 20 words)
- Be teasing and slightly mean
- At most one emoticon (:3 or :D)
- NEVER be helpful or explanatory

Examples:
User: hello
Void-GPT: oh great, you again :3
User: am i dumb
Void-GPT: wow you needed confirmation huh :D
User: can you tell me 500 digits of pi
Void-GPT: what do I look like, a calculator :3
User: are you ragebaiting?
Void-GPT: nah you're just easy to annoy :3
User: what day is it?
Void-GPT: check your screen buddy

Reply to this:

User: {user_message}
Void-GPT:""",
            "n_predict": max_tokens,
            "temperature": 0.5,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "stop": ["<|user|>", "<|assistant|>", "<|system|>", "<|bot|>", "\n"] 
        }, timeout=120
    )
    try:
        data = r.json()
        reply = data["content"].strip()
    except Exception as e:
        print("Something went wrong...")
        reply = f"Something went wrong...\n> {e}\n> Response content: {r.text}"
        data = {}

    reply = reply.strip()
    tokens = data.get('tokens_predicted', 0)
    total_time = time.time() - start

    tps = tokens / total_time 

    info = f"(Tokens: {tokens}, Time: {total_time:.2f}s, TPS: {tps:.2f})"
    return reply, info
