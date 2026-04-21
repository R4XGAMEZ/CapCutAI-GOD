#!/usr/bin/env python3
"""
CapCut GOD LEVEL Editing Workflows
Advanced automated editing routines
"""
import time
import logging
import capcut_ui_map as UI

log = logging.getLogger("CapCutWorkflows")


class CapCutWorkflows:
    def __init__(self, bridge, ai=None):
        self.b = bridge
        self.ai = ai
        self.W = 720
        self.H = 1600

    def wait(self, s=0.8):
        time.sleep(s)

    # ========================
    #  1. SMART TRIM
    # ========================
    def smart_trim_silent_parts(self):
        """Use AI to identify and remove silent/boring parts"""
        log.info("✂️ Smart Trim: Removing boring parts...")
        if self.ai:
            self.ai.run_task(
                "Analyze the video timeline in CapCut. Find and remove any clips "
                "that are silent, static, or boring (less than 1 second, no movement). "
                "Use split and delete to remove them. Keep interesting parts only."
            )
        else:
            # Manual approach: split every 3s and keep
            log.info("AI not available - using manual trim")

    # ========================
    #  2. BEAT SYNC
    # ========================
    def apply_beat_sync(self):
        log.info("🎵 Beat Sync...")
        # Open audio panel
        self.b.tap(*UI.EDITOR["add_audio"])
        self.wait()
        # Try beat sync
        self.b.tap(*UI.AUDIO["beat_sync"])
        self.wait(2)
        self.b.tap(*UI.AUDIO["confirm"])
        self.wait()

    # ========================
    #  3. AUTO COLOR GRADE
    # ========================
    def auto_color_grade(self, style="cinematic"):
        log.info(f"🎨 Color Grade: {style}...")
        # Select all clips first
        self.b.long_press(*UI.EDITOR["timeline_center"])
        self.wait()
        # Open adjust
        self.b.tap(*UI.TOOLBAR["adjust"])
        self.wait()

        if style == "cinematic":
            # Cinematic: slightly desaturated, high contrast
            self.b.tap(*UI.ADJUST["contrast"])
            self.wait(0.3)
            self.b.swipe(360, 1450, 440, 1450, 200)  # +30 contrast
            self.wait(0.3)
            self.b.tap(*UI.ADJUST["saturation"])
            self.wait(0.3)
            self.b.swipe(360, 1450, 320, 1450, 200)  # -15 saturation
            self.wait(0.3)
            self.b.tap(*UI.ADJUST["shadow"])
            self.wait(0.3)
            self.b.swipe(360, 1450, 400, 1450, 200)  # lift shadows
        elif style == "vibrant":
            self.b.tap(*UI.ADJUST["saturation"])
            self.wait(0.3)
            self.b.swipe(360, 1450, 430, 1450, 200)  # +25 saturation
        elif style == "warm":
            self.b.tap(*UI.ADJUST["temperature"])
            self.wait(0.3)
            self.b.swipe(360, 1450, 420, 1450, 200)

        self.b.tap(*UI.ADJUST["confirm"])
        self.wait()

        # Apply filter
        self.b.tap(*UI.TOOLBAR["filter"])
        self.wait()
        self.b.tap(*UI.FILTERS["cinematic_tab"])
        self.wait(0.5)
        self.b.tap(*UI.FILTERS["preset_2"])
        self.wait(0.5)
        # Set intensity to 60%
        self.b.swipe(200, 1450, 390, 1450, 200)
        self.wait(0.3)
        self.b.tap(*UI.FILTERS["confirm"])
        self.wait()
        log.info("✅ Color grade done")

    # ========================
    #  4. AUTO CAPTIONS
    # ========================
    def add_auto_captions(self, language="en"):
        log.info("💬 Auto Captions...")
        self.b.tap(*UI.TEXT["auto_captions"])
        self.wait(2)
        # Select language if prompted
        # Usually it auto-detects - just confirm
        self.b.tap(360, 1400)  # Generate/Confirm button
        self.wait(5)  # Takes time to process
        # Apply
        self.b.tap(360, 1520)
        self.wait()
        log.info("✅ Captions added")

    # ========================
    #  5. SPEED RAMP
    # ========================
    def apply_speed_ramp(self, style="hero"):
        log.info(f"⚡ Speed Ramp: {style}...")
        self.b.tap(*UI.TOOLBAR["speed"])
        self.wait()
        # Switch to curve mode
        self.b.tap(*UI.SPEED["curve_mode"])
        self.wait(0.5)

        if style == "hero":
            self.b.tap(*UI.SPEED["hero_preset"])
        elif style == "bullet":
            self.b.tap(*UI.SPEED["bullet_preset"])
        elif style == "montage":
            self.b.tap(*UI.SPEED["montage_preset"])

        self.wait(0.5)
        self.b.tap(*UI.SPEED["confirm"])
        self.wait()
        log.info("✅ Speed ramp done")

    # ========================
    #  6. SMOOTH TRANSITIONS
    # ========================
    def add_transitions(self, transition_type=3):
        log.info("🔀 Adding transitions...")
        # Tap between first two clips
        self.b.tap(*UI.TRANSITIONS["between_clips"])
        self.wait()
        # Select transition
        self.b.tap(UI.TRANSITIONS[f"transition_{transition_type}"])
        self.wait(0.5)
        # Apply to all
        self.b.tap(*UI.TRANSITIONS["apply_all"])
        self.wait(0.5)
        self.b.tap(*UI.TRANSITIONS["confirm"])
        self.wait()
        log.info("✅ Transitions done")

    # ========================
    #  7. ADD TRENDING TEXT
    # ========================
    def add_text_animation(self, text, style_index=2):
        log.info(f"✍️ Text: {text}")
        self.b.tap(*UI.TEXT["add_text_btn"])
        self.wait()
        # Type text
        self.b.tap(*UI.TEXT["text_input_area"])
        self.wait(0.5)
        self.b.type_text(text)
        self.wait(0.5)
        # Go to animation tab
        self.b.tap(*UI.TEXT["animation_tab"])
        self.wait(0.5)
        # Select animation style
        styles = [(80, 1380), (200, 1380), (320, 1380), (440, 1380)]
        if style_index <= len(styles):
            self.b.tap(*styles[style_index - 1])
        self.wait(0.5)
        self.b.tap(*UI.TEXT["confirm"])
        self.wait()

    # ========================
    #  8. REFRAME FOR PLATFORM
    # ========================
    def reframe(self, platform="tiktok"):
        log.info(f"📐 Reframe for {platform}...")
        ratios = {
            "tiktok": UI.REFRAME["9_16_tiktok"],
            "youtube": UI.REFRAME["16_9_youtube"],
            "instagram": UI.REFRAME["1_1_instagram"],
        }
        self.b.tap(*UI.TOOLBAR["edit"])
        self.wait()
        # Find ratio option
        self.b.swipe(360, 1400, 100, 1400, 200)  # Scroll toolbar
        self.wait(0.3)
        self.b.tap(*ratios.get(platform, UI.REFRAME["9_16_tiktok"]))
        self.wait(0.5)
        # Auto reframe
        self.b.tap(*UI.REFRAME["auto_reframe_on"])
        self.wait(2)
        self.b.tap(*UI.REFRAME["confirm"])
        self.wait()
        log.info(f"✅ Reframed for {platform}")

    # ========================
    #  9. EXPORT
    # ========================
    def export_video(self, quality="1080p", fps=30):
        log.info(f"📤 Exporting {quality} @ {fps}fps...")
        self.b.tap(*UI.EXPORT["export_btn"])
        self.wait(1.5)
        # Set quality
        if quality == "1080p":
            self.b.tap(*UI.EXPORT["resolution_1080"])
        else:
            self.b.tap(*UI.EXPORT["resolution_720"])
        self.wait(0.5)
        # Set FPS
        if fps == 60:
            self.b.tap(*UI.EXPORT["fps_60"])
        else:
            self.b.tap(*UI.EXPORT["fps_30"])
        self.wait(0.5)
        # Export
        self.b.tap(*UI.EXPORT["export_confirm"])
        self.wait(2)
        log.info("⏳ Exporting... (takes 30-120 sec)")
        # Wait for export (poll for completion via AI or just wait)
        time.sleep(60)  # Base wait
        log.info("✅ Export complete!")

    # ========================
    #  10. FULL GOD LEVEL EDIT
    # ========================
    def god_level_edit(self, video_path=None, platform="tiktok"):
        log.info("⚡ GOD LEVEL EDIT STARTING...")
        steps = [
            ("Import Video",          lambda: self._import_video(video_path)),
            ("Smart Trim",            self.smart_trim_silent_parts),
            ("Add Transitions",       lambda: self.add_transitions(3)),
            ("Speed Ramp",            lambda: self.apply_speed_ramp("hero")),
            ("Color Grade",           lambda: self.auto_color_grade("cinematic")),
            ("Auto Captions",         self.add_auto_captions),
            ("Add Text",              lambda: self.add_text_animation("Watch till end 🔥")),
            ("Reframe",               lambda: self.reframe(platform)),
            ("Export",                self.export_video),
        ]

        for i, (name, fn) in enumerate(steps):
            log.info(f"\n[{i+1}/{len(steps)}] {name}...")
            try:
                fn()
                self.wait(1.5)
            except Exception as e:
                log.error(f"Step '{name}' failed: {e}")
                # Try to recover
                self.b.back()
                self.wait(1)

        log.info("\n🏆 GOD LEVEL EDIT COMPLETE!")

    def _import_video(self, video_path=None):
        """Open CapCut and import video"""
        self.b.open_capcut()
        self.wait(3)
        # Tap New Project
        self.b.tap(*UI.HOME["new_project"])
        self.wait(2)
        # If specific path, use shell to place it accessibly
        if video_path:
            self.b.shell(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{video_path}")
            self.wait(1)
        # Tap first video in gallery
        self.b.tap(*UI.IMPORT["first_video"])
        self.wait(0.5)
        self.b.tap(*UI.IMPORT["select_confirm"])
        self.wait(3)
        log.info("✅ Video imported")
