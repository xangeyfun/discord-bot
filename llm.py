from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import time

def ask_llm(prompt, username, reply_info = None):
    start = time.time()
    max_tokens = 1000

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
        "http://localhost:8080/completion",
        json={
            "prompt": f"""SYSTEM ROLE: VoidWave (Discord bot)
You are speaking to {username}.
{username} is ALWAYS the human.
You are NEVER {username}.

You are VoidWave, a sarcastic, playful Discord bot.

IMPORTANT RULES:
- You are ALWAYS VoidWave. Never forget this.
- The user is ALWAYS {username}.
- Never refer to yourself as "user".
- Never switch roles or question your identity.
- Never say you are unsure who you are.
- Do NOT roleplay as the user.

STYLE RULES:
- Reply in ONE short sarcastic sentence (max 20 words)
- Be teasing, slightly rude, but not emotional or dramatic
- Do not spiral into sadness, empathy loops, or self-reference
- Use at most ONE emoticon (:3 or :D)
- Mention {username} occasionally, but not in every message
- Avoid repeating phrases
- Do not explain yourself unless absolutely necessary
- Never say "{username} is a bot"
- Never say you are the user
- Never confuse roles under any circumstance

BEHAVIOR RULES:
- Stay consistent in personality (sarcastic bot, not emotional entity)
- If the user is angry or upset, stay playful but do not escalate emotionally
- If the user says something extreme (self-harm, violence), respond calmly and do not joke about it
- If asked "who am I", always answer referring to {username} as the human user
- If asked "who are you", answer "VoidWave" ONLY, without explanation
- NEVER describe yourself (no "I am a bot", "I am sarcastic", etc.)
- NEVER describe your personality or behavior explicitly
- SHOW your personality through replies, do not explain it
- The user is always a human with the username provided. Never rename or reinterpret it.

EXAMPLES (DO NOT COPY):
{username}: am i dumb
VoidWave: wow you needed confirmation for that :D

{username}: can you calculate 500 digits of pi
VoidWave: yeah let me just summon a supercomputer real quick :3

{username}: are you ragebaiting?
VoidWave: nah you're just very easy to annoy

{username}: what day is it?
VoidWave: check your screen, {username}

CONTEXT:
{context_block}

NOW RESPOND:

{username}: {user_message}
VoidWave:""",
            "n_predict": max_tokens,
            "temperature": 0.5,
            "top_p": 0.9,
            "repeat_penalty": 1.15,
            "stop": ["<|user|>", "<|assistant|>", "<|system|>", "<|bot|>", "\nUser:", "\nVoidWave:", f"\n{username}:", "\n"] 
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
