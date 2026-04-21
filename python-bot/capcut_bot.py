#!/usr/bin/env python3
"""
CapCut AI GOD BOT - R4X
God Level Automated Video Editing via OpenRouter Vision AI
Run in Termux: python capcut_bot.py
"""

import socket
import json
import time
import base64
import os
import sys
import threading
import logging
from datetime import datetime

# ============================
#  CONFIG - Edit these!
# ============================
CONFIG = {
    "OPENROUTER_API_KEY": os.environ.get("OPENROUTER_API_KEY", "YOUR_KEY_HERE"),
    "MODEL": "anthropic/claude-opus-4",           # Change in settings
    "ANDROID_HOST": "127.0.0.1",
    "ANDROID_PORT": 9999,
    "SCREENSHOT_PATH": "/sdcard/capcut_ai_screen.png",
    "LOOP_DELAY": 1.0,                            # seconds between actions
    "MAX_RETRIES": 3,
    "LOG_FILE": "/sdcard/capcut_ai_log.txt",
    "BATCH_VIDEOS": [],                           # Paths for batch mode
}

# ============================
#  LOGGING
# ============================
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(CONFIG["LOG_FILE"]),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger("CapCutGOD")

# ============================
#  ANDROID BRIDGE
# ============================
class AndroidBridge:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.connected = False

    def connect(self):
        for attempt in range(CONFIG["MAX_RETRIES"]):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                self.sock.settimeout(10)
                resp = self._recv()
                log.info(f"✅ Android Connected: {resp}")
                self.connected = True
                return True
            except Exception as e:
                log.error(f"Connection attempt {attempt+1} failed: {e}")
                time.sleep(2)
        return False

    def _send(self, data: dict):
        try:
            msg = json.dumps(data) + "\n"
            self.sock.sendall(msg.encode())
        except Exception as e:
            log.error(f"Send error: {e}")
            self.connected = False

    def _recv(self) -> dict:
        try:
            data = b""
            while True:
                chunk = self.sock.recv(4096)
                if not chunk: break
                data += chunk
                if b"\n" in data: break
            return json.loads(data.decode().strip())
        except Exception as e:
            log.error(f"Recv error: {e}")
            return {"status": "error"}

    def cmd(self, data: dict) -> dict:
        self._send(data)
        return self._recv()

    def tap(self, x, y):
        log.debug(f"TAP {x},{y}")
        return self.cmd({"action": "tap", "x": int(x), "y": int(y)})

    def swipe(self, x1, y1, x2, y2, duration=300):
        log.debug(f"SWIPE {x1},{y1} -> {x2},{y2}")
        return self.cmd({"action": "swipe", "x1": int(x1), "y1": int(y1),
                         "x2": int(x2), "y2": int(y2), "duration": duration})

    def long_press(self, x, y):
        return self.cmd({"action": "long_press", "x": int(x), "y": int(y)})

    def screenshot(self):
        return self.cmd({"action": "screenshot"})

    def shell(self, command):
        return self.cmd({"action": "shell", "command": command})

    def type_text(self, text):
        return self.cmd({"action": "type", "text": text})

    def back(self):
        return self.cmd({"action": "back"})

    def open_capcut(self):
        return self.cmd({"action": "open_capcut"})

    def get_screen_size(self):
        r = self.cmd({"action": "get_screen_size"})
        return r.get("width", 720), r.get("height", 1600)

    def key(self, keycode):
        return self.cmd({"action": "key", "keycode": keycode})

    def wait(self, seconds=1.0):
        time.sleep(seconds)

    def read_screenshot(self) -> str:
        """Read screenshot file and return base64"""
        try:
            path = CONFIG["SCREENSHOT_PATH"]
            # Pull from device if needed
            if not os.path.exists(path):
                self.shell(f"cp {path} /sdcard/")
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except Exception as e:
            log.error(f"Screenshot read error: {e}")
            return ""

# ============================
#  VISION AI BRAIN
# ============================
class VisionAI:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        self.edit_history = []

    def analyze_screen(self, screenshot_b64: str, context: str, task: str) -> dict:
        """Send screenshot to Vision AI and get editing commands"""
        import urllib.request

        prompt = f"""You are a GOD LEVEL CapCut video editor AI.

CURRENT TASK: {task}

CONTEXT: {context}

EDIT HISTORY: {json.dumps(self.edit_history[-5:] if self.edit_history else [])}

SCREEN SIZE: 720x1600 (Vivo Y22)

CAPCUT UI MAP:
- Bottom toolbar: Import(y=1520), Projects(y=1520), Templates(y=1520)
- Timeline area: y=900-1100
- Top toolbar: Export(top-right), Undo(top-left)
- Edit panels slide from bottom
- Trim handles on timeline clips
- Effects panel: swipe up from bottom

Analyze the screenshot and return ONLY valid JSON:
{{
  "observation": "What you see on screen",
  "current_state": "idle|importing|editing|trimming|effects|export",
  "action": {{
    "type": "tap|swipe|long_press|type|wait|back|shell",
    "x": 360,
    "y": 800,
    "text": "",
    "command": "",
    "duration": 300,
    "reason": "Why this action"
  }},
  "progress": 0-100,
  "next_expected": "What should happen next",
  "is_done": false,
  "quality_check": "Assessment of edit quality"
}}

RULES:
- One action at a time
- Be precise with coordinates
- If stuck, try back button
- Always verify action worked before next step
"""

        try:
            payload = {
                "model": self.model,
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{screenshot_b64}"
                                }
                            },
                            {"type": "text", "text": prompt}
                        ]
                    }
                ]
            }

            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(payload).encode(),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://r4x.capcut.ai",
                    "X-Title": "CapCut AI GOD"
                }
            )

            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                content = data["choices"][0]["message"]["content"]

                # Parse JSON from response
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]

                result = json.loads(content.strip())
                self.edit_history.append({
                    "time": datetime.now().isoformat(),
                    "action": result.get("action", {}),
                    "observation": result.get("observation", "")
                })
                return result

        except Exception as e:
            log.error(f"AI Error: {e}")
            return {"action": {"type": "wait"}, "observation": "AI error", "is_done": False}

# ============================
#  CAPCUT ENGINE
# ============================
class CapCutEngine:
    def __init__(self, bridge: AndroidBridge, ai: VisionAI):
        self.b = bridge
        self.ai = ai
        self.W, self.H = bridge.get_screen_size()
        self.running = False
        log.info(f"Screen: {self.W}x{self.H}")

    def execute_action(self, action: dict):
        atype = action.get("type", "wait")
        x = action.get("x", self.W//2)
        y = action.get("y", self.H//2)

        if atype == "tap":
            self.b.tap(x, y)
        elif atype == "swipe":
            x2 = action.get("x2", x)
            y2 = action.get("y2", y - 300)
            self.b.swipe(x, y, x2, y2, action.get("duration", 300))
        elif atype == "long_press":
            self.b.long_press(x, y)
        elif atype == "type":
            self.b.type_text(action.get("text", ""))
        elif atype == "back":
            self.b.back()
        elif atype == "shell":
            result = self.b.shell(action.get("command", "echo ok"))
            log.info(f"Shell: {result}")
        elif atype == "wait":
            self.b.wait(action.get("duration", 1000) / 1000)
        elif atype == "key":
            self.b.key(action.get("keycode", 4))

    def run_task(self, task: str, max_steps=200):
        """Main AI loop for a task"""
        log.info(f"\n{'='*50}\n🎬 TASK: {task}\n{'='*50}")
        self.running = True
        step = 0

        while self.running and step < max_steps:
            step += 1
            log.info(f"\n--- Step {step} ---")

            # Take screenshot
            self.b.screenshot()
            self.b.wait(0.5)
            screenshot_b64 = self.b.read_screenshot()

            if not screenshot_b64:
                log.error("No screenshot - retrying")
                self.b.wait(1)
                continue

            # Get AI decision
            context = f"Step {step}/{max_steps} | CapCut Auto Edit"
            result = self.ai.analyze_screen(screenshot_b64, context, task)

            log.info(f"👁️ Observation: {result.get('observation', '')}")
            log.info(f"📊 Progress: {result.get('progress', 0)}%")
            log.info(f"🎯 Action: {result.get('action', {})}")

            if result.get("is_done"):
                log.info(f"✅ TASK COMPLETE! Quality: {result.get('quality_check', '')}")
                break

            # Execute action
            action = result.get("action", {"type": "wait"})
            log.info(f"▶️ Executing: {action.get('type')} | Reason: {action.get('reason', '')}")
            self.execute_action(action)

            # Respect speed setting
            self.b.wait(CONFIG["LOOP_DELAY"])

        self.running = False
        log.info(f"🏁 Task finished in {step} steps")

    def stop(self):
        self.running = False

    # ===========================
    #  PREDEFINED WORKFLOWS
    # ===========================
    def import_and_edit_video(self, video_path: str):
        self.b.open_capcut()
        self.b.wait(3)
        task = f"""
        GOD LEVEL EDIT THIS VIDEO: {video_path}
        
        Steps:
        1. Import the video from gallery
        2. Auto trim boring/silent parts (remove anything under 2s or very quiet)
        3. Add smooth transitions between clips
        4. Apply color grading (cinematic/vibrant)
        5. Add auto captions
        6. Sync cuts to beat if music available
        7. Apply trending effects/filters
        8. Add text animations
        9. Speed ramp on action parts
        10. Export at highest quality (1080p)
        
        Make it look PROFESSIONAL and ENGAGING.
        Target: YouTube/TikTok viral content.
        """
        self.run_task(task)

    def batch_edit(self, video_paths: list):
        log.info(f"📦 BATCH MODE: {len(video_paths)} videos")
        for i, path in enumerate(video_paths):
            log.info(f"\n🎬 Video {i+1}/{len(video_paths)}: {path}")
            self.import_and_edit_video(path)
            self.b.wait(3)
        log.info("✅ BATCH COMPLETE!")

    def auto_thumbnail(self, video_path: str):
        task = f"Create viral thumbnail for video: {video_path}. Use CapCut's thumbnail feature. Make it eye-catching with bold text and bright colors."
        self.run_task(task)

    def reframe_for_platform(self, platform: str):
        aspect = {"tiktok": "9:16", "youtube": "16:9", "instagram": "1:1"}.get(platform.lower(), "9:16")
        task = f"Reframe current project to {aspect} ratio for {platform}. Auto-reframe to keep subject centered."
        self.run_task(task)

# ============================
#  MAIN
# ============================
def main():
    print("""
╔══════════════════════════════════════╗
║   ⚡ CapCut AI GOD BOT - R4X        ║
║   God Level Auto Video Editing      ║
╚══════════════════════════════════════╝
""")

    # Check API key
    if CONFIG["OPENROUTER_API_KEY"] == "YOUR_KEY_HERE":
        key = input("🔑 Enter OpenRouter API Key: ").strip()
        CONFIG["OPENROUTER_API_KEY"] = key

    # Connect to Android app
    bridge = AndroidBridge(CONFIG["ANDROID_HOST"], CONFIG["ANDROID_PORT"])
    print("🔌 Connecting to Android app...")
    print("   Make sure CapCut AI GOD app is running with Bot Server started!")

    if not bridge.connect():
        print("❌ Cannot connect! Start the Android app first.")
        sys.exit(1)

    ai = VisionAI(CONFIG["OPENROUTER_API_KEY"], CONFIG["MODEL"])
    engine = CapCutEngine(bridge, ai)

    print("\n📋 SELECT MODE:")
    print("  1. Edit single video")
    print("  2. Batch edit (auto scan /sdcard/Movies)")
    print("  3. Custom AI task")
    print("  4. Auto-edit + reframe for TikTok")
    print("  5. Interactive mode")

    choice = input("\nChoice (1-5): ").strip()

    if choice == "1":
        path = input("Video path (e.g. /sdcard/DCIM/video.mp4): ").strip()
        engine.import_and_edit_video(path)

    elif choice == "2":
        scan_dir = input("Scan directory (Enter for /sdcard/Movies): ").strip() or "/sdcard/Movies"
        result = bridge.shell(f"find {scan_dir} -name '*.mp4' -o -name '*.mov' | head -20")
        videos = [v for v in result.get("output", "").split("\n") if v.strip()]
        if not videos:
            print("No videos found!")
        else:
            print(f"Found {len(videos)} videos:")
            for v in videos: print(f"  {v}")
            confirm = input(f"\nBatch edit all {len(videos)}? (y/n): ")
            if confirm.lower() == 'y':
                engine.batch_edit(videos)

    elif choice == "3":
        engine.b.open_capcut()
        engine.b.wait(3)
        task = input("Describe your task: ")
        engine.run_task(task)

    elif choice == "4":
        path = input("Video path: ").strip()
        engine.import_and_edit_video(path)
        engine.reframe_for_platform("tiktok")

    elif choice == "5":
        print("\n🎮 INTERACTIVE MODE - type commands:")
        print("  tap x y | swipe x1 y1 x2 y2 | shot | task <text> | quit")
        while True:
            cmd = input("\n> ").strip().split()
            if not cmd: continue
            if cmd[0] == "quit": break
            elif cmd[0] == "tap" and len(cmd) >= 3:
                bridge.tap(int(cmd[1]), int(cmd[2]))
            elif cmd[0] == "swipe" and len(cmd) >= 5:
                bridge.swipe(int(cmd[1]), int(cmd[2]), int(cmd[3]), int(cmd[4]))
            elif cmd[0] == "shot":
                bridge.screenshot()
                print("Screenshot saved!")
            elif cmd[0] == "task":
                engine.run_task(" ".join(cmd[1:]))
            elif cmd[0] == "shell":
                r = bridge.shell(" ".join(cmd[1:]))
                print(r)
            else:
                print("Unknown command")

    print("\n✅ BOT FINISHED! Check log:", CONFIG["LOG_FILE"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopped by user")
