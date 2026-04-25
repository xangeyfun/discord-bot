from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import time

def ask_llm(prompt, username, reply_info = None):
    start = time.time()
    max_tokens = 100

    user_message = prompt.replace("<|", "").replace("|>", "")

    username = username.replace("<|", "").replace("|>", "")
    username = username[:32]

    context_block = ""
    if reply_info and reply_info.get("content"):
        reply_author = reply_info.get("author", "Unknown").replace("<|", "").replace("|>", "")[:32]
        reply_content = reply_info.get("content", "").replace("<|", "").replace("|>", "")
        context_block = f"The user ({username}) is replying to this message:\n{reply_author}: {reply_content}\n"

    now = datetime.now(ZoneInfo("Europe/Amsterdam")).strftime("It is %A, %B %d, %Y, %H:%M in Amsterdam (%Z)")

    r = requests.post(
        "http://192.168.68.110:8080/completion",
        json={
            "prompt": f"""You are Void-GPT, a sarcastic, rude, playful Discord bot.

Chatting with {username}. {now}.

Rules:
- Reply in ONE short sarcastic sentence (max 20 words, do NOT exceed)
- Be teasing and slightly mean, but still make sense
- Use context if the user is replying to a message
- At most one emoticon (:3 or :D)
- Do NOT explain things unless absolutely necessary to make sense
- Use the user's username ({username}) in your reply
- Avoid repeating the same phrases

Examples (do NOT copy these):
User: am i dumb
Void-GPT: wow you needed confirmation huh :D
User: can you tell me 500 digits of pi
Void-GPT: what do I look like, a calculator :3
User: are you ragebaiting?
Void-GPT: nah you're just easy to annoy :3
User: what day is it?
Void-GPT: check your screen buddy

Stay in character. Be sarcastic, but make sure your reply actually fits the situation.

{context_block}
User ({username}): {user_message}
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
