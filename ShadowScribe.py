import keyboard
import pyperclip
import pyautogui
import requests
import time
import threading
import random
import ctypes

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"

# ── Minimize CMD so it never steals focus ────────────────
def minimize_cmd():
    ctypes.windll.user32.ShowWindow(
        ctypes.windll.kernel32.GetConsoleWindow(), 6)

# ── Detect if question is coding or theory ───────────────
def is_coding_question(question):
    keywords = [
        'code', 'program', 'function', 'write a', 'implement',
        'class', 'algorithm', 'output', 'python', 'java', 'c++',
        'array', 'queue', 'stack', 'linked list', 'sort', 'search',
        'def ', 'return', 'loop', 'input', 'print', 'given',
        'leetcode', 'neetcode', 'integer', 'string', 'binary',
        'tree', 'graph', 'duplicate', 'element', 'nums', 'target',
        'index', 'matrix', 'node', 'pointer', 'recursive', 'iterate'
    ]
    return any(k in question.lower() for k in keywords)

# ── Ask Qwen ─────────────────────────────────────────────
def ask_qwen(question, is_code):
    try:
        if is_code:
            prompt = f"""You are solving a LeetCode/NeetCode/college coding problem.

STRICT OUTPUT RULES:
- Write ONLY the lines inside the function body
- Do NOT write class Solution
- Do NOT write the def function signature line
- Do NOT write any explanation or comments
- Do NOT add blank lines at start or end
- Use exactly 4 spaces per indentation level
- First line starts with 4 spaces (inside function)
- Output only raw Python code

Problem:
{question}"""
        else:
            prompt = f"""Answer this assignment question in 2-4 sentences.
- Direct answer only
- No 'The answer is' or similar preamble
- Clear and concise

Question:
{question}"""

        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=90)

        answer = response.json()["response"].strip()

        # Remove markdown code fences if Qwen adds them
        if "```" in answer:
            lines = answer.split('\n')
            lines = [l for l in lines if not l.strip().startswith('```')]
            answer = '\n'.join(lines).strip()

        return answer

    except Exception as e:
        print(f"Qwen error: {e}")
        return None

# ── Type one character safely ─────────────────────────────
def type_char(char):
    if char.isascii() and char.isprintable():
        pyautogui.write(char)
        time.sleep(random.uniform(0.03, 0.08))
    else:
        # Non-ASCII: use clipboard for just this one char
        pyperclip.copy(char)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.05)
    # Random human pause
    if random.random() < 0.04:
        time.sleep(random.uniform(0.1, 0.3))

# ── Type code (handles Monaco auto-indent) ────────────────
def type_code(answer):
    """
    Types code line by line.
    After each Enter, Monaco adds its own indent.
    We kill Monaco's indent with: Home → Shift+End → Delete
    Then we type our exact indentation manually.
    """
    # Clear editor first
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('delete')
    time.sleep(0.3)

    lines = answer.split('\n')

    for line_num, line in enumerate(lines):

        if line_num > 0:
            # Press Enter (Monaco will auto-add its indent here)
            pyautogui.press('enter')
            time.sleep(0.15)

            # ── KEY FIX ──────────────────────────────────
            # Kill whatever Monaco auto-typed on this new line
            pyautogui.press('home')       # Go to very start of line
            time.sleep(0.08)
            pyautogui.hotkey('shift', 'end')  # Select entire line content
            time.sleep(0.08)
            pyautogui.press('delete')     # Delete Monaco's auto-indent
            time.sleep(0.08)
            # ─────────────────────────────────────────────

        # Now type our exact line (spaces + code)
        for char in line:
            if char == ' ':
                pyautogui.press('space')
                time.sleep(0.02)
            elif char == '\t':
                # Convert tab to 4 spaces
                for _ in range(4):
                    pyautogui.press('space')
                    time.sleep(0.02)
            else:
                type_char(char)

        time.sleep(random.uniform(0.05, 0.12))

# ── Type theory answer (normal human typing) ─────────────
def type_text(answer):
    for char in answer:
        if char == '\n':
            pyautogui.press('enter')
            time.sleep(random.uniform(0.08, 0.15))
        elif char == ' ':
            pyautogui.press('space')
            time.sleep(0.03)
        else:
            type_char(char)

# ── Main hotkey handler ───────────────────────────────────
def handle_hotkey():
    def run():
        # Small delay so F9 doesn't interrupt selection
        time.sleep(0.3)

        old = pyperclip.paste()

        # Copy highlighted text
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        question = pyperclip.paste().strip()

        # Retry once if failed
        if not question or question == old:
            time.sleep(0.4)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.5)
            question = pyperclip.paste().strip()
            if not question or question == old:
                return  # silently do nothing

        is_code = is_coding_question(question)
        print(f"Type: {'CODE' if is_code else 'THEORY'}")
        print(f"Question: {question[:60]}...")
        print("Asking Qwen...")

        answer = ask_qwen(question, is_code)
        if not answer:
            return

        print(f"Answer ready! Click the answer box — starting in 3 sec...")
        time.sleep(3)

        print("Writing...")
        if is_code:
            type_code(answer)   # Monaco-safe typing
        else:
            type_text(answer)   # Normal human typing

        print("Done!")

    threading.Thread(target=run, daemon=True).start()

# ── Start ─────────────────────────────────────────────────
minimize_cmd()
print("Qwen Helper READY | Highlight → F9 → Click box")
keyboard.add_hotkey('F9', handle_hotkey)
keyboard.wait()
