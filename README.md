# 🌑 ShadowScribe

A real-time background AI assistant that detects highlighted questions on webpages and automatically generates and types context-aware answers or code using a locally hosted Qwen model via Ollama.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Ollama](https://img.shields.io/badge/Ollama-local-black?style=flat-square)
![Qwen](https://img.shields.io/badge/Qwen-2.5--Coder--7B-orange?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## ⚡ How It Works

```
Highlight question → Press F9 → Click answer box → Answer types itself
```

- **Code questions** → Types with correct indentation (Monaco/LeetCode safe)
- **Theory questions** → Types naturally like a human
- **Fully local** → Uses Ollama on your machine, no internet needed for AI

---

## 🛠️ Requirements

| Tool | Purpose |
|---|---|
| Python 3.10+ | Runs the script |
| Ollama | Runs Qwen AI locally |
| Qwen 2.5 Coder 7B | The AI model that answers |

### Python Libraries
```bash
pip install keyboard pyperclip pyautogui requests
```

---

## 🚀 Setup

### 1. Install Python
- Download from [python.org/downloads](https://python.org/downloads)
- ⚠️ During install, **check "Add Python to PATH"**

### 2. Install Ollama + Qwen Model
```bash
# Download Ollama from https://ollama.com
# Then pull the model:
ollama pull qwen2.5-coder:7b
```

### 3. Install Python Libraries
```bash
pip install keyboard pyperclip pyautogui requests
```

### 4. Save the Script
Save `qwen_helper.py` to any folder on your PC (e.g. `Desktop/SRM QWEN/`)

---

## ▶️ Running the Script

> Make sure Ollama is running in the background first.
> If you get a port error when running `ollama serve`, it's already running — that's fine.

Open CMD and run:
```bash
cd "C:\Users\YourName\Desktop\SRM QWEN"
python qwen_helper.py
```

The CMD window will **minimize itself automatically** — it runs silently in the background.

---

## 🎮 How To Use

| Step | Action |
|---|---|
| 1 | Open your assignment website |
| 2 | **Highlight** the question text with your mouse |
| 3 | Press **F9** |
| 4 | **Click** inside the answer/code box within 3 seconds |
| 5 | Watch the answer type itself ✅ |

---

## 🧠 Smart Detection

The script automatically detects what kind of question it is:

### Code Questions (LeetCode / NeetCode / College Coding)
Detected when question contains keywords like:
`code`, `function`, `implement`, `array`, `class`, `python`, `algorithm`, `nums`, `return`, etc.

**Behaviour:**
- Clears the existing code editor
- Types line by line with correct indentation
- Fixes Monaco editor auto-indent issue automatically

### Theory Questions (MCQ / Short Answer / Essay)
Everything else is treated as a theory question.

**Behaviour:**
- Types character by character
- Random speed variation (looks human)
- Occasional natural pauses

---

## 🔧 Monaco Editor Fix (LeetCode / NeetCode)

Monaco editor auto-adds indentation after every `Enter` key.
Without a fix, this causes `IndentationError`.

**How we fix it — after every new line:**
```
Press Enter
→ Monaco adds its own spaces    (unwanted)
→ Home key (go to line start)
→ Shift + End (select Monaco's spaces)
→ Delete (wipe them)
→ Type our exact spaces         (correct ✅)
```

---

## ⚙️ Configuration

Inside `ShadowScribe.py` you can change:

```python
MODEL = "qwen2.5-coder:7b"   # Change AI model here
```

```python
time.sleep(3)   # Change seconds to click answer box (default: 3)
```

---

## ❗ Troubleshooting

| Problem | Fix |
|---|---|
| `pip not recognized` | Reinstall Python and check "Add to PATH" |
| `python not recognized` | Same as above, close and reopen CMD after install |
| Ollama port error on `ollama serve` | Already running in background — ignore it |
| Nothing happens on F9 | Make sure text is highlighted before pressing F9 |
| Wrong answer typed | Highlight only the question text, not examples |
| Code has wrong indentation | Use this latest version of the script with Monaco fix |

---

## 📁 File Structure

```
SRM QWEN/
│
├── qwen_helper.py      ← Main script
└── README.md           ← This file
```

---

## 🔒 Privacy

- Everything runs **100% locally** on your machine
- No data is sent to the internet
- Qwen model runs through Ollama on `localhost:11434`

---

## 🛑 How To Stop

Click the minimized CMD window in taskbar → Press `Ctrl + C`

---

## 🏷️ GitHub Topics

```
ollama  qwen  python  automation  pyautogui  leetcode
neetcode  ai-assistant  local-ai  keyboard-automation
```
