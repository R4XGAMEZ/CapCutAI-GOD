#!/usr/bin/env python3
"""
CapCut UI Map - Vivo Y22 (720x1600)
All known UI element coordinates for CapCut automation
"""

# ========================
#  SCREEN DIMENSIONS
# ========================
SCREEN_W = 720
SCREEN_H = 1600
CENTER_X = 360
CENTER_Y = 800

# ========================
#  HOME SCREEN
# ========================
HOME = {
    "new_project": (360, 780),        # Big "+" / New Project button
    "templates": (540, 780),           # Templates tab
    "draft_first": (180, 400),         # First draft in list
    "draft_second": (540, 400),
    "draft_more": (180, 600),
    "search": (360, 120),
    "profile": (680, 60),
}

# ========================
#  IMPORT SCREEN
# ========================
IMPORT = {
    "recent_tab": (90, 230),
    "videos_tab": (270, 230),
    "photos_tab": (450, 230),
    "first_video": (120, 420),
    "second_video": (360, 420),
    "third_video": (600, 420),
    "select_confirm": (360, 1520),     # "Add" button
    "album_dropdown": (360, 175),
}

# ========================
#  EDITOR - MAIN TIMELINE
# ========================
EDITOR = {
    # Top bar
    "back": (40, 60),
    "undo": (100, 60),
    "redo": (160, 60),
    "export": (660, 60),
    "auto_caption": (580, 60),
    "settings": (640, 60),
    
    # Preview area
    "preview_center": (360, 450),
    "preview_play": (360, 750),
    
    # Timeline
    "timeline_start": (80, 950),
    "timeline_center": (360, 950),
    "timeline_end": (640, 950),
    "timeline_scroll_left": (40, 950),
    "timeline_scroll_right": (680, 950),
    "playhead": (360, 870),
    
    # Add track buttons
    "add_audio": (120, 1100),
    "add_text": (240, 1100),
    "add_sticker": (360, 1100),
    "add_effect": (480, 1100),
    "add_filter": (600, 1100),
}

# ========================
#  BOTTOM TOOLBAR (Edit mode)
# ========================
TOOLBAR = {
    "trim_split": (80, 1400),          # Scissor icon
    "speed": (160, 1400),              # Speed ramp
    "animate": (240, 1400),            # Animation
    "edit": (320, 1400),               # Basic edit
    "filter": (400, 1400),             # Filters
    "adjust": (480, 1400),             # Color adjust
    "volume": (560, 1400),             # Volume
    "text": (640, 1400),               # Text overlay
    
    # Second row (swipe right)
    "auto_enhance": (80, 1480),
    "background": (160, 1480),
    "remove_bg": (240, 1480),
    "green_screen": (320, 1480),
    "reframe": (400, 1480),
    "stabilize": (480, 1480),
}

# ========================
#  TRIM / SPLIT PANEL
# ========================
TRIM = {
    "split_here": (360, 1400),         # Split at playhead
    "trim_start": (60, 950),           # Left trim handle
    "trim_end": (660, 950),            # Right trim handle
    "delete_clip": (360, 1480),
}

# ========================
#  SPEED PANEL
# ========================
SPEED = {
    "normal_0_5x": (120, 1300),
    "normal_1x": (240, 1300),
    "normal_1_5x": (360, 1300),
    "normal_2x": (480, 1300),
    "normal_3x": (600, 1300),
    "curve_mode": (360, 1200),         # Speed curve
    "montage_preset": (180, 1400),
    "hero_preset": (360, 1400),
    "bullet_preset": (540, 1400),
    "confirm": (360, 1550),
}

# ========================
#  FILTERS PANEL
# ========================
FILTERS = {
    "popular_tab": (100, 1200),
    "cinematic_tab": (220, 1200),
    "portrait_tab": (340, 1200),
    "food_tab": (460, 1200),
    "preset_1": (80, 1350),
    "preset_2": (200, 1350),
    "preset_3": (320, 1350),
    "preset_4": (440, 1350),
    "preset_5": (560, 1350),
    "intensity_slider": (360, 1450),   # Drag to adjust
    "confirm": (360, 1550),
}

# ========================
#  ADJUST (COLOR GRADE)
# ========================
ADJUST = {
    "brightness": (80, 1350),
    "contrast": (160, 1350),
    "saturation": (240, 1350),
    "sharpness": (320, 1350),
    "highlight": (400, 1350),
    "shadow": (480, 1350),
    "temperature": (560, 1350),
    "vignette": (640, 1350),
    "slider": (360, 1450),
    "confirm": (360, 1550),
}

# ========================
#  TEXT PANEL
# ========================
TEXT = {
    "add_text_btn": (180, 1350),
    "auto_captions": (360, 1350),
    "text_templates": (540, 1350),
    "text_input_area": (360, 450),
    "font_tab": (120, 1200),
    "style_tab": (240, 1200),
    "effects_tab": (360, 1200),
    "animation_tab": (480, 1200),
    "confirm": (360, 1550),
}

# ========================
#  TRANSITIONS
# ========================
TRANSITIONS = {
    # Tap between clips on timeline
    "between_clips": (280, 950),       # The + icon between clips
    "basic_tab": (120, 1250),
    "trendy_tab": (240, 1250),
    "effects_tab": (360, 1250),
    "transition_1": (80, 1380),
    "transition_2": (200, 1380),
    "transition_3": (320, 1380),
    "transition_4": (440, 1380),
    "duration_slider": (360, 1470),
    "apply_all": (200, 1540),
    "confirm": (540, 1540),
}

# ========================
#  AUDIO / MUSIC
# ========================
AUDIO = {
    "add_music": (120, 1100),
    "sounds_tab": (180, 1250),
    "my_music": (360, 1250),
    "extracted": (540, 1250),
    "first_track": (360, 1380),
    "beat_sync": (360, 1480),
    "volume_main": (200, 1400),
    "volume_slider": (360, 1460),
    "fade_in": (160, 1520),
    "fade_out": (540, 1520),
    "confirm": (360, 1560),
}

# ========================
#  EFFECTS
# ========================
EFFECTS = {
    "video_effects": (180, 1350),
    "body_effects": (360, 1350),
    "filter_effects": (540, 1350),
    "trending_tab": (120, 1250),
    "basic_tab": (240, 1250),
    "dynamic_tab": (360, 1250),
    "effect_1": (80, 1380),
    "effect_2": (200, 1380),
    "effect_3": (320, 1380),
    "confirm": (360, 1560),
}

# ========================
#  EXPORT
# ========================
EXPORT = {
    "export_btn": (640, 60),
    "resolution_1080": (360, 650),
    "resolution_720": (360, 730),
    "fps_30": (200, 810),
    "fps_60": (400, 810),
    "hdr_toggle": (600, 890),
    "export_confirm": (360, 1520),
    "share_more": (360, 1400),
    "save_to_album": (180, 1480),
}

# ========================
#  REFRAME / ASPECT RATIO
# ========================
REFRAME = {
    "9_16_tiktok": (180, 1300),
    "16_9_youtube": (360, 1300),
    "1_1_instagram": (540, 1300),
    "4_3": (180, 1400),
    "auto_reframe_on": (360, 1450),
    "confirm": (360, 1560),
}

# ========================
#  HELPER: Get coords by name
# ========================
ALL_ELEMENTS = {
    **{f"home.{k}": v for k, v in HOME.items()},
    **{f"import.{k}": v for k, v in IMPORT.items()},
    **{f"editor.{k}": v for k, v in EDITOR.items()},
    **{f"toolbar.{k}": v for k, v in TOOLBAR.items()},
    **{f"trim.{k}": v for k, v in TRIM.items()},
    **{f"speed.{k}": v for k, v in SPEED.items()},
    **{f"filters.{k}": v for k, v in FILTERS.items()},
    **{f"adjust.{k}": v for k, v in ADJUST.items()},
    **{f"text.{k}": v for k, v in TEXT.items()},
    **{f"transitions.{k}": v for k, v in TRANSITIONS.items()},
    **{f"audio.{k}": v for k, v in AUDIO.items()},
    **{f"effects.{k}": v for k, v in EFFECTS.items()},
    **{f"export.{k}": v for k, v in EXPORT.items()},
    **{f"reframe.{k}": v for k, v in REFRAME.items()},
}

def get(element_path: str):
    """Get coordinates by path e.g. 'export.export_btn'"""
    return ALL_ELEMENTS.get(element_path)

if __name__ == "__main__":
    print(f"Total mapped elements: {len(ALL_ELEMENTS)}")
    print("\nSample elements:")
    for k, v in list(ALL_ELEMENTS.items())[:10]:
        print(f"  {k}: {v}")
