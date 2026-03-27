#!/usr/bin/env python3
import os, re, sys, subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

BUILD = os.path.dirname(os.path.abspath(__file__))
MI_TTF    = os.path.join(BUILD, "MaterialIcons-Regular.ttf")
PXA_TTF   = os.path.join(BUILD, "node_modules/pixelarticons/fonts/pixelart-icons-font.ttf")
PXA_CSS   = os.path.join(BUILD, "node_modules/pixelarticons/fonts/pixelart-icons-font.css")
OUT_TTF   = os.path.join(BUILD, "pixel-material-icons.ttf")
OUT_WOFF2 = os.path.join(BUILD, "..", "assets", "pixel-material-icons.woff2")

MAPPING = {
    "access_time":             "clock",
    "account_circle":          "avatar",
    "add":                     "plus",
    "airplay":                 "cast",
    "album":                   "music",
    "analytics":               "analytics",
    "app_settings_alt":        "sliders-2",
    "arrow_back":              "arrow-left",
    "arrow_drop_down":         "chevron-down",
    "arrow_forward":           "arrow-right",
    "arrow_forward_ios":       "chevron-right",
    "article":                 "article",
    "audiotrack":              "music",
    "autorenew":               "reload",
    "backup":                  "upload",
    "book":                    "book-open",
    "call_merge":              "git-merge",
    "call_split":              "git-branch",
    "cancel":                  "close",
    "cast":                    "cast",
    "cast_connected":          "monitor",
    "check":                   "check",
    "check_box":               "checkbox-on",
    "check_box_outline_blank": "checkbox",
    "chevron_left":            "chevron-left",
    "chevron_right":           "chevron-right",
    "clear":                   "close",
    "clear_all":               "trash",
    "close":                   "close",
    "closed_caption":          "subtitles",
    "cloud_download":          "cloud-download",
    "comment":                 "message",
    "computer":                "device-laptop",
    "content_copy":            "copy",
    "dashboard":               "dashbaord",
    "delete":                  "delete",
    "devices":                 "devices",
    "download":                "download",
    "dvr":                     "video",
    "edit":                    "edit",
    "exit_to_app":             "logout",
    "expand_less":             "chevron-up",
    "expand_more":             "chevron-down",
    "explore":                 "gps",
    "extension":               "grid",
    "fast_forward":            "speed-fast",
    "fast_rewind":             "speed-slow",
    "favorite":                "heart",
    "fiber_manual_record":     "circle",
    "fiber_smart_record":      "circle",
    "file_download":           "download",
    "filter_alt":              "sliders",
    "folder":                  "folder",
    "fullscreen":              "expand",
    "get_app":                 "download",
    "group_add":               "user-plus",
    "groups":                  "users",
    "help_outline":            "info-box",
    "home":                    "home",
    "image":                   "image",
    "info":                    "info-box",
    "info_outline":            "info-box",
    "keyboard_arrow_down":     "chevron-down",
    "keyboard_arrow_left":     "chevron-left",
    "keyboard_arrow_up":       "chevron-up",
    "lan":                     "modem",
    "library_add":             "folder-plus",
    "library_add_check":       "check",
    "list":                    "list",
    "live_tv":                 "device-tv",
    "logout":                  "logout",
    "lyrics":                  "note",
    "meeting_room":            "open",
    "memory":                  "server",
    "menu":                    "menu",
    "mode_edit":               "edit",
    "more_vert":               "more-vertical",
    "movie":                   "movie",
    "music_note":              "music",
    "music_video":             "video",
    "open_in_new":             "link",
    "palette":                 "paint-bucket",
    "pause":                   "pause",
    "pause_circle_filled":     "pause",
    "people":                  "users",
    "person":                  "user",
    "person_add":              "user-plus",
    "person_off":              "user-x",
    "person_remove":           "user-minus",
    "phonelink_lock":          "lock",
    "photo":                   "image",
    "photo_album":             "image-gallery",
    "picture_in_picture_alt":  "picture-in-picture-alt",
    "play":                    "play",
    "play_arrow":              "play",
    "play_circle":             "play",
    "play_circle_filled":      "play",
    "playlist_add":            "playlist",
    "playlist_remove":         "minus",
    "preview":                 "eye",
    "queue":                   "list",
    "quiz":                    "info-box",
    "redo":                    "redo",
    "refresh":                 "reload",
    "remove_circle":           "remove-box",
    "remove_circle_outline":   "close-box",
    "repeat":                  "repeat",
    "repeat_one":              "repeat",
    "replay":                  "reload",
    "restore":                 "reload",
    "schedule":                "clock",
    "search":                  "search",
    "select_all":              "check-double",
    "settings":                "sliders-2",
    "settings_remote":         "sliders-2",
    "share":                   "link",
    "shuffle":                 "shuffle",
    "skip_next":               "next",
    "skip_previous":           "prev",
    "slideshow":               "image-gallery",
    "smartphone":              "device-phone",
    "sort_by_alpha":           "sort-alphabetic",
    "star":                    "trophy",
    "stop":                    "power",
    "stop_circle":             "circle",
    "storage":                 "server",
    "subtitles":               "subtitles",
    "tablet":                  "device-tablet",
    "theaters":                "movie",
    "tune":                    "sliders",
    "tv":                      "device-tv",
    "undo":                    "undo",
    "usb":                     "sd",
    "vertical_align_bottom":   "arrow-bar-down",
    "vertical_align_top":      "arrow-bar-up",
    "video_library":           "video",
    "video_settings":          "sliders",
    "videocam":                "video",
    "view_comfy":              "grid",
    "visibility":              "eye",
    "visibility_off":          "eye-closed",
    "volume_up":               "volume-3",
    "vpn_key":                 "lock",
    "warning":                 "warning-box",
}

# Custom outlines for glyphs where pixelarticons uses smooth vectors instead of pixel art.
# Coordinates in PXA space (0–1000 UPM), snapped to 83-unit grid (1000/12 steps).
CUSTOM_OUTLINES = {
    # Two vertical bars, 3px wide × 8px tall, centered.
    "pause": [
        [("moveTo", ((167, 167),)), ("lineTo", ((416, 167),)), ("lineTo", ((416, 833),)), ("lineTo", ((167, 833),)), ("closePath", ())],
        [("moveTo", ((583, 167),)), ("lineTo", ((832, 167),)), ("lineTo", ((832, 833),)), ("lineTo", ((583, 833),)), ("closePath", ())],
    ],
}

pxa_codepoints = {}
with open(PXA_CSS) as f:
    for m in re.finditer(
        r'\.pixelart-icons-font-([\w-]+):before\s*\{\s*content:\s*"\\([0-9a-fA-F]+)"', f.read()
    ):
        pxa_codepoints[m.group(1)] = int(m.group(2), 16)

print("Loading fonts...")
mi  = TTFont(MI_TTF)
pxa = TTFont(PXA_TTF)

mi_upm  = mi["head"].unitsPerEm
pxa_upm = pxa["head"].unitsPerEm
scale   = mi_upm / pxa_upm

print(f"  MI UPM: {mi_upm}, PXA UPM: {pxa_upm}, scale: {scale:.4f}")

def get_mi_ligatures(font):
    cmap = font.getBestCmap()
    glyph_to_cp = {v: k for k, v in cmap.items()}
    result = {}
    gsub = font["GSUB"].table
    for lookup in gsub.LookupList.Lookup:
        if lookup.LookupType == 4:
            for sub in lookup.SubTable:
                for first_g, lig_set in sub.ligatures.items():
                    first_cp = glyph_to_cp.get(first_g)
                    if not first_cp:
                        continue
                    for lig in lig_set:
                        rest = "".join(
                            chr(glyph_to_cp[g]) for g in lig.Component if glyph_to_cp.get(g)
                        )
                        result[chr(first_cp) + rest] = lig.LigGlyph
    return result

print("Building ligature map...")
mi_ligatures = get_mi_ligatures(mi)
print(f"  {len(mi_ligatures)} ligatures found")

pxa_cmap      = pxa.getBestCmap()
pxa_glyph_set = pxa.getGlyphSet()
mi_glyph_set  = mi.getGlyphSet()
mi_advance    = mi["hmtx"].metrics[".notdef"][0]

print("Replacing glyphs...")
replaced = 0
skipped  = []

for mi_name, pxa_name in MAPPING.items():
    mi_glyph = mi_ligatures.get(mi_name)
    if not mi_glyph:
        skipped.append(f"no ligature: {mi_name}")
        continue

    pxa_cp = pxa_codepoints.get(pxa_name)
    if not pxa_cp:
        skipped.append(f"no pxa cp: {pxa_name}")
        continue
    pxa_glyph = pxa_cmap.get(pxa_cp)
    if not pxa_glyph or pxa_glyph not in pxa_glyph_set:
        skipped.append(f"no pxa glyph: {pxa_name}")
        continue

    rec = RecordingPen()
    if pxa_name in CUSTOM_OUTLINES:
        for contour in CUSTOM_OUTLINES[pxa_name]:
            for op, args in contour:
                getattr(rec, op)(*args)
    else:
        try:
            pxa_glyph_set[pxa_glyph].draw(rec)
        except Exception as e:
            skipped.append(f"draw error {mi_name}: {e}")
            continue

    xs, ys = [], []
    for op, args in rec.value:
        for pt in args:
            if isinstance(pt, tuple) and len(pt) == 2:
                xs.append(pt[0])
                ys.append(pt[1])
    if not xs:
        skipped.append(f"empty glyph: {mi_name}")
        continue
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    em_center = mi_upm / 2
    dx = em_center - (x_min + x_max) / 2 * scale
    dy = em_center - (y_min + y_max) / 2 * scale

    if pxa_name == "play":
        dx += (x_max - x_min) * scale * 0.15

    pen = TTGlyphPen(mi)
    tp  = TransformPen(pen, (scale, 0, 0, scale, dx, dy))
    rec.replay(tp)

    mi["glyf"][mi_glyph]          = pen.glyph()
    mi["hmtx"].metrics[mi_glyph]  = (mi_advance, int(x_min * scale + dx))

    replaced += 1

print(f"  Replaced: {replaced}")
if skipped:
    print(f"  Skipped ({len(skipped)}):")
    for s in skipped:
        print(f"    {s}")

print(f"Saving TTF → {OUT_TTF}")
mi.save(OUT_TTF)

print(f"Converting to woff2 → {OUT_WOFF2}")
try:
    from fontTools.ttLib import woff2
    woff2.compress(OUT_TTF, OUT_WOFF2)
except Exception:
    result = subprocess.run(
        [sys.executable, "-m", "fonttools", "ttLib.woff2", "compress", OUT_TTF, "-o", OUT_WOFF2],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("woff2 error:", result.stderr)
        sys.exit(1)

size_kb = os.path.getsize(OUT_WOFF2) // 1024
print(f"Done! {OUT_WOFF2} ({size_kb} KB)")
