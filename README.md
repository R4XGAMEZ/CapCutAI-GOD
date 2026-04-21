# ⚡ CapCut AI GOD - R4X
> God Level Automated Video Editing • No Root • Vivo Y22

---

## 🗂️ Project Structure
```
CapCutAI/
├── android-app/          → Java Android App (APK)
│   ├── app/src/main/
│   │   ├── java/com/r4x/capcutai/
│   │   │   ├── MainActivity.java
│   │   │   ├── ShizukuBridge.java      ← ADB commands
│   │   │   ├── FloatingOverlayService  ← Always-on button
│   │   │   ├── SocketServerService     ← Python bridge (port 9999)
│   │   │   ├── CapCutAccessibilityService
│   │   │   └── SettingsActivity.java
│   │   └── res/layout/
├── python-bot/           → AI Vision Bot (Termux)
│   ├── capcut_bot.py     ← Main bot (run this)
│   ├── capcut_ui_map.py  ← All CapCut coordinates
│   ├── capcut_workflows.py ← Editing routines
│   └── setup_termux.sh
└── .github/workflows/
    └── build.yml         ← One-click APK build
```

---

## 🚀 QUICK START

### Step 1 — GitHub Setup (One-time)
```bash
# Fork/upload this project to GitHub
# Go to Actions tab → Enable workflows
# Push any commit → APK auto builds
# Download from Releases tab
```

### Step 2 — Install APK on Vivo Y22
```
1. Download APK from GitHub Releases
2. Install (allow unknown sources)
3. Grant permissions:
   - Overlay (draw over other apps)
   - Accessibility Service → CapCut AI Controller
   - Storage
```

### Step 3 — Setup Shizuku
```
Shizuku app → Start via Wireless ADB or Developer Options
```

### Step 4 — Configure API Key
```
Open app → Settings → Enter OpenRouter API Key
Get key free: https://openrouter.ai
Recommended model: anthropic/claude-opus-4
```

### Step 5 — Termux Bot
```bash
# Install setup
bash setup_termux.sh

# Set API key
export OPENROUTER_API_KEY=sk-or-v1-yourkey

# Run bot
python capcut_bot.py
```

### Step 6 — Start Editing
```
1. Open CapCut AI GOD app
2. Tap "START AI BOT SERVER"
3. Run capcut_bot.py in Termux
4. Select mode (single/batch/custom)
5. Watch the magic 🔥
```

---

## 🤖 AI Vision Loop
```
Screenshot → OpenRouter Vision AI → Action Decision → Execute → Repeat
```
The AI sees CapCut's screen and makes editing decisions like:
- Where to tap
- Which effects to apply
- When a step is done
- How to fix errors

---

## ⚙️ Supported Models (OpenRouter)
| Model | Speed | Quality | Cost |
|-------|-------|---------|------|
| claude-opus-4 | Slow | Best | $$$ |
| claude-sonnet-4-5 | Medium | Great | $$ |
| gpt-4o | Medium | Great | $$ |
| gemini-2.0-flash | Fast | Good | $ |
| llama-3.2-90b-vision | Fast | Good | Free |

---

## 🎬 GOD LEVEL Features
- ✂️ Smart auto-trim (silent part removal)
- 🎵 Beat sync transitions
- 🎨 Auto color grading (cinematic/vibrant/warm)
- 💬 Auto captions (speech-to-text)
- ⚡ Speed ramp (slow-mo + fast montage)
- 📐 Auto reframe (9:16 / 16:9 / 1:1)
- ✍️ Text animations
- 🔀 Smooth transitions
- 📦 Batch processing (100+ videos)
- 🔄 Auto error recovery
- 📊 Progress tracking

---

## 🔌 Socket Protocol (port 9999)
```json
// Commands (Python → Android)
{"action": "tap", "x": 360, "y": 800}
{"action": "swipe", "x1": 360, "y1": 800, "x2": 360, "y2": 400, "duration": 300}
{"action": "screenshot"}
{"action": "shell", "command": "dumpsys window"}
{"action": "open_capcut"}
{"action": "back"}

// Response
{"status": "ok"}
{"status": "ok", "path": "/sdcard/screen.png"}
{"status": "error", "message": "..."}
```

---

## 📱 Device Info
- Phone: Vivo Y22 (Android 12, arm64-v8a)
- Screen: 720x1600
- No root required
- Shizuku for ADB-level access

---

**Made by R4X** • CapCut package: `com.lemon.lvoverseas`
