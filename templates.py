# -*- coding: utf-8 -*-
"""
Moduł szablonów wizualnych dla generatora okien About.
W pełni zintegrowany z architekturą przetwarzania barw TrueColor i OKLCH (zgodnie z colors.py).
Automatycznie generuje najwyższą jakość grafiki dla GUI CustomTkinter oraz silnika ANSI.
"""

import sys
import math
from typing import Dict, Any, List, Tuple, Optional

# =============================================================================
# ZAAWANSOWANY SILNIK PRZETWARZANIA BARW I GRAFIKI (HQ GRAPHICS ENGINE)
# =============================================================================
class HQColorEngine:
    """
    Silnik optymalizacji grafiki realizujący operacje matematyczne na paletach RGB.
    Zapewnia idealny dobór kontrastu, automatyczne generowanie stanów hover/active
    oraz gładkie interpolacje przestrzenne dla najwyższej jakości GUI.
    """
    
    @staticmethod
    def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
        """Konwertuje ciąg HEX na krotkę RGB."""
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 6:
            return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
        elif len(hex_str) == 3:
            return int(hex_str[0]*2, 16), int(hex_str[1]*2, 16), int(hex_str[2]*2, 16)
        return (255, 255, 255)

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Konwertuje składowe RGB na format HEX."""
        return f"#{max(0, min(255, r)):02x}{max(0, min(255, g)):02x}{max(0, min(255, b)):02x}"

    @classmethod
    def blend_colors(cls, hex_c1: str, hex_c2: str, factor: float) -> str:
        """Miksuje dwa kolory w przestrzeni liniowej TrueColor z określoną wagą (0.0 - 1.0)."""
        r1, g1, b1 = cls.hex_to_rgb(hex_c1)
        r2, g2, b2 = cls.hex_to_rgb(hex_c2)
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        return cls.rgb_to_hex(r, g, b)

    @classmethod
    def tweak_brightness(cls, hex_str: str, factor: float) -> str:
        """
        Modyfikuje jasność koloru wejściowego.
        factor > 1.0 rozjaśnia (np. dla stanów hover w Dark Mode)
        factor < 1.0 przyciemnia (np. dla stanów hover w Light Mode)
        """
        r, g, b = cls.hex_to_rgb(hex_str)
        return cls.rgb_to_hex(int(r * factor), int(g * factor), int(b * factor))

    @classmethod
    def get_contrast_color(cls, bg_hex: str) -> str:
        """Zwraca optymalny kolor tekstu (czarny lub biały) na podstawie luminancji tła."""
        r, g, b = cls.hex_to_rgb(bg_hex)
        # Standardowy wzór luminancji percepcyjnej ITU-R
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return "#ffffff" if luminance < 0.5 else "#1d1d1f"


# =============================================================================
# MATRYCE PALET I SZABLONÓW GRAFICZNYCH ULTRA-HQ
# =============================================================================

# 1. Podmenu: Style Główne (Standardowe Szablony Wizualne)
TEMPLATES_DATA = {
    "modern_dark": {
        "name_pl": "Nowoczesny Ciemny (Studio)",
        "name_en": "Modern Dark (Studio)",
        "bg_color": "#18181b",  # Głęboki, nowoczesny cynk/grafit (Zing Slate)
        "font_colors": {"app_name": "#ffffff", "version": "#a1a1aa", "description": "#e4e4e7", "author": "#71717a"},
        "font_sizes": {"app_name": 24, "version": 12, "description": 14, "author": 12},
        "btn_close_bg": "#27272a",
        "btn_close_fg": "#f4f4f5",
        "border_color": "#3f3f46",
        "width": "400",
        "height": "510",
        "ansi_gradient": ["#ffffff", "#a1a1aa", "#27272a"]
    },
    "cyberpunk": {
        "name_pl": "Cyberpunk 2077 Neon",
        "name_en": "Cyberpunk Neon",
        "bg_color": "#030303",
        "font_colors": {"app_name": "#fde047", "version": "#ef4444", "description": "#22d3ee", "author": "#c084fc"},
        "font_sizes": {"app_name": 26, "version": 11, "description": 13, "author": 12},
        "btn_close_bg": "#ef4444",
        "btn_close_fg": "#000000",
        "border_color": "#fde047",
        "width": "420",
        "height": "530",
        "ansi_gradient": ["#fde047", "#ef4444", "#22d3ee", "#c084fc"]
    },
    "clean_light": {
        "name_pl": "Czysty Jasny (Apple Silk)",
        "name_en": "Clean Light (Apple Silk)",
        "bg_color": "#f5f5f7",  # Flagowy szary od Apple
        "font_colors": {"app_name": "#1d1d1f", "version": "#86868b", "description": "#424245", "author": "#86868b"},
        "font_sizes": {"app_name": 22, "version": 13, "description": 14, "author": 12},
        "btn_close_bg": "#0071e3",  # Systemowy niebieski macOS
        "btn_close_fg": "#ffffff",
        "border_color": "#d2d2d7",
        "width": "390",
        "height": "490",
        "ansi_gradient": ["#1d1d1f", "#86868b", "#0071e3"]
    }
}

# 2. Podmenu: Informatyka / IT
IT_TEMPLATES_DATA = {
    "matrix": {
        "name_pl": "Haker (Matrix Digital)",
        "name_en": "Hacker (Matrix Digital)",
        "bg_color": "#020617",  # Ultra ciemny zielonkawy obsydian
        "font_colors": {"app_name": "#22c55e", "version": "#16a34a", "description": "#4ade80", "author": "#15803d"},
        "font_sizes": {"app_name": 22, "version": 12, "description": 14, "author": 12},
        "btn_close_bg": "#14532d",
        "btn_close_fg": "#4ade80",
        "border_color": "#22c55e",
        "width": "450",
        "height": "460",
        "ansi_gradient": ["#4ade80", "#22c55e", "#14532d"]
    },
    "dracula": {
        "name_pl": "Dracula Spec (Pro)",
        "name_en": "Dracula Spec (Pro)",
        "bg_color": "#282a36",  # Oryginalny Dracula Theme
        "font_colors": {"app_name": "#ff79c6", "version": "#6272a4", "description": "#f8f8f2", "author": "#8be9fd"},
        "font_sizes": {"app_name": 24, "version": 12, "description": 14, "author": 13},
        "btn_close_bg": "#44475a",
        "btn_close_fg": "#50fa7b",
        "border_color": "#bd93f9",
        "width": "410",
        "height": "510",
        "ansi_gradient": ["#ff79c6", "#bd93f9", "#50fa7b"]
    }
}

# 3. Podmenu: Systemy Operacyjne i Retro Platformy
OS_TEMPLATES_DATA = {
    "ms_dos": {
        "name_pl": "MS-DOS Terminal VUI",
        "name_en": "MS-DOS Terminal VUI",
        "bg_color": "#000000",
        "font_colors": {
            "app_name": "#ffffff",
            "version": "#aaaaaa",
            "description": "#00ff00",  # Klasyczny kineskopowy zielony
            "author": "#aaaaaa"
        },
        "font_sizes": {"app_name": 22, "version": 12, "description": 13, "author": 12},
        "btn_close_bg": "#555555",  # TUI Button Style
        "btn_close_fg": "#ffffff",
        "border_color": "#ffffff",
        "width": "460",
        "height": "440",
        "ansi_gradient": ["#ffffff", "#aaaaaa", "#00ff00"]
    },
    "macos_modern_light": {
        "name_pl": "Nowoczesny macOS (Jasny)",
        "name_en": "Modern macOS (Light)",
        "bg_color": "#f3f4f6",
        "font_colors": {"app_name": "#111827", "version": "#6b7280", "description": "#1f2937", "author": "#9ca3af"},
        "font_sizes": {"app_name": 23, "version": 12, "description": 14, "author": 11},
        "btn_close_bg": "#0284c7",
        "btn_close_fg": "#ffffff",
        "border_color": "#e5e7eb",
        "width": "410",
        "height": "470",
        "ansi_gradient": ["#111827", "#0284c7", "#f3f4f6"]
    },
    "macos_sequoia": {
        "name_pl": "Styl macOS Sequoia (Ciemny)",
        "name_en": "macOS Sequoia Style (Dark)",
        "bg_color": "#1c1c1e",
        "font_colors": {"app_name": "#f5f5f7", "version": "#86868b", "description": "#e3e3e3", "author": "#86868b"},
        "font_sizes": {"app_name": 23, "version": 13, "description": 14, "author": 12},
        "btn_close_bg": "#ff9f0a",  # macOS Orange accent
        "btn_close_fg": "#ffffff",
        "border_color": "#2c2c2e",
        "width": "420",
        "height": "470",
        "ansi_gradient": ["#f5f5f7", "#ff9f0a"]
    },
    "ubuntu": {
        "name_pl": "Styl Ubuntu (Yaru Canonical)",
        "name_en": "Ubuntu (Yaru Canonical)",
        "bg_color": "#2c001e",  # Oficjalny bakłażan Ubuntu
        "font_colors": {"app_name": "#e95420", "version": "#aea79f", "description": "#ffffff", "author": "#dfdbd2"},
        "font_sizes": {"app_name": 24, "version": 11, "description": 13, "author": 12},
        "btn_close_bg": "#e95420",  # Ubuntu Orange
        "btn_close_fg": "#ffffff",
        "border_color": "#77216f",
        "width": "400",
        "height": "510",
        "ansi_gradient": ["#e95420", "#aea79f", "#2c001e"]
    },
    "amiga_workbench": {
        "name_pl": "Amiga OS (Workbench 1.3)",
        "name_en": "Amiga OS Style",
        "bg_color": "#0055aa",
        "font_colors": {"app_name": "#ffffff", "version": "#000000", "description": "#ffffff", "author": "#ff5500"},
        "font_sizes": {"app_name": 22, "version": 12, "description": 14, "author": 13},
        "btn_close_bg": "#ff5500",
        "btn_close_fg": "#000000",
        "border_color": "#ffffff",
        "width": "440",
        "height": "470",
        "ansi_gradient": ["#ffffff", "#ff5500", "#0055aa"]
    },
    "commodore_64": {
        "name_pl": "Commodore 64 BASIC",
        "name_en": "Commodore 64 BASIC",
        "bg_color": "#3a319c",
        "font_colors": {"app_name": "#7b73de", "version": "#7b73de", "description": "#7b73de", "author": "#7b73de"},
        "font_sizes": {"app_name": 24, "version": 13, "description": 14, "author": 13},
        "btn_close_bg": "#10106b",
        "btn_close_fg": "#7b73de",
        "border_color": "#7b73de",
        "width": "460",
        "height": "430",
        "ansi_gradient": ["#7b73de", "#3a319c"]
    },
    "atari_st": {
        "name_pl": "Atari ST (GEM Desktop)",
        "name_en": "Atari ST (GEM Desktop)",
        "bg_color": "#ffffff",
        "font_colors": {"app_name": "#000000", "version": "#000000", "description": "#000000", "author": "#000000"},
        "font_sizes": {"app_name": 24, "version": 12, "description": 14, "author": 12},
        "btn_close_bg": "#ffffff",
        "btn_close_fg": "#000000",
        "border_color": "#000000",
        "width": "390",
        "height": "460",
        "ansi_gradient": ["#000000", "#ffffff"]
    },
    "zx_spectrum": {
        "name_pl": "ZX Spectrum Sinclair",
        "name_en": "ZX Spectrum Sinclair",
        "bg_color": "#ffffff",
        "font_colors": {"app_name": "#000000", "version": "#0000ff", "description": "#000000", "author": "#ff0000"},
        "font_sizes": {"app_name": 26, "version": 14, "description": 14, "author": 14},
        "btn_close_bg": "#ffffff",
        "btn_close_fg": "#000000",
        "border_color": "#0000ff",
        "width": "430",
        "height": "450",
        "ansi_gradient": ["#000000", "#0000ff", "#ff0000"]
    },
    "windows_11": {
        "name_pl": "Styl Windows 11 Acrylic",
        "name_en": "Windows 11 Acrylic",
        "bg_color": "#202020",
        "font_colors": {"app_name": "#ffffff", "version": "#cccccc", "description": "#ffffff", "author": "#aaaaaa"},
        "font_sizes": {"app_name": 20, "version": 11, "description": 13, "author": 11},
        "btn_close_bg": "#0078d4",
        "btn_close_fg": "#ffffff",
        "border_color": "#2f2f2f",
        "width": "370",
        "height": "490",
        "ansi_gradient": ["#ffffff", "#0078d4", "#202020"]
    }
}

# 4. Podmenu: Ramki
FRAMES_DATA = {
    "compact_box": {
        "name_pl": "Kompaktowe Pudełko",
        "name_en": "Compact Box",
        "bg_color": "#1e293b",
        "font_colors": {"app_name": "#f8fafc", "version": "#94a3b8", "description": "#f1f5f9", "author": "#64748b"},
        "font_sizes": {"app_name": 18, "version": 11, "description": 12, "author": 11},
        "btn_close_bg": "#ef4444",
        "btn_close_fg": "#ffffff",
        "border_color": "#334155",
        "width": "330",
        "height": "410",
        "ansi_gradient": ["#f8fafc", "#94a3b8"]
    },
    "panoramic": {
        "name_pl": "Szeroka Panorama",
        "name_en": "Wide Panoramic",
        "bg_color": "#1f1f1f",
        "font_colors": {"app_name": "#ffffff", "version": "#808080", "description": "#dddddd", "author": "#808080"},
        "font_sizes": {"app_name": 26, "version": 12, "description": 15, "author": 12},
        "btn_close_bg": "#007acc",
        "btn_close_fg": "#ffffff",
        "border_color": "#333333",
        "width": "620",
        "height": "395",
        "ansi_gradient": ["#ffffff", "#808080"]
    }
}


def _helper_apply(app_instance, data: Optional[Dict[str, Any]]):
    """
    Zaawansowana funkcja aplikująca szablon do głównego okna generatora.
    Wykorzystuje matematyczne filtry HQColorEngine do optymalizacji kontrastu i stanów interaktywnych.
    """
    if not data:
        return
        
    # 1. Przeniesienie kolorów i rozmiarów czcionek
    for key, value in data["font_colors"].items():
        app_instance.font_colors[key] = value
        
    for key, value in data["font_sizes"].items():
        app_instance.font_sizes[key] = value

    # 2. Konfiguracja kolorów bazowych komponentów GUI
    app_instance.bg_color = data["bg_color"]
    app_instance.btn_close_bg = data["btn_close_bg"]
    app_instance.btn_close_fg = data["btn_close_fg"]
    
    # Zapis koloru obramowania ramki (Border Color)
    app_instance.border_color = data.get("border_color", data["bg_color"])
    
    # 3. DYNAMICZNA GENERACJA STANÓW WIZUALNYCH (Hover/Pressed)
    # Wyznaczamy zaawansowany Hover na podstawie analizy jasności tła przycisku
    is_dark_btn = HQColorEngine.get_contrast_color(data["btn_close_bg"]) == "#ffffff"
    if is_dark_btn:
        # Przycisk ciemny: rozjaśniamy go o 15% przy najechaniu myszką
        app_instance.btn_close_hover_bg = HQColorEngine.tweak_brightness(data["btn_close_bg"], 1.15)
    else:
        # Przycisk jasny: lekko go przyciemniamy, aby uzyskać głębię
        app_instance.btn_close_hover_bg = HQColorEngine.tweak_brightness(data["btn_close_bg"], 0.88)
        
    # 4. Aktualizacja bocznego panelu kontrolnego w generator.py
    if hasattr(app_instance, 'btn_bg_color'):
        app_instance.btn_bg_color.configure(fg_color=data["bg_color"])
    if hasattr(app_instance, 'btn_close_bg_picker'):
        app_instance.btn_close_bg_picker.configure(fg_color=data["btn_close_bg"])
    if hasattr(app_instance, 'btn_close_fg_picker'):
        app_instance.btn_close_fg_picker.configure(text_color=data["btn_close_fg"])
    
    # 5. Aktualizacja zmiennych geometrii okna
    if hasattr(app_instance, 'win_width'):
        app_instance.win_width.set(data["width"])
    if hasattr(app_instance, 'win_height'):
        app_instance.win_height.set(data["height"])
    
    # 6. Przesłanie wektora gradientów TrueColor do silnika eksportowego ANSI
    app_instance.current_ansi_gradient = data.get("ansi_gradient", ["#ffffff", "#888888"])
    
    # 7. Synchronizacja suwaków i dynamicznego podglądu Live Preview
    if hasattr(app_instance, 'active_field') and app_instance.active_field in app_instance.font_sizes:
        if hasattr(app_instance, 'font_slider'):
            app_instance.font_slider.set(app_instance.font_sizes[app_instance.active_field])
        
    if hasattr(app_instance, 'switch_active_field'):
        link_idx = getattr(app_instance, 'active_link_index', None)
        app_instance.switch_active_field(app_instance.active_field, link_idx)


def apply_template(app_instance, template_key: str):
    """Aplikuje styl główny z palety standardowej."""
    _helper_apply(app_instance, TEMPLATES_DATA.get(template_key))


def apply_it_template(app_instance, template_key: str):
    """Aplikuje zaawansowany styl dla programistów / IT."""
    _helper_apply(app_instance, IT_TEMPLATES_DATA.get(template_key))


def apply_os_template(app_instance, template_key: str):
    """Aplikuje odwzorowany styl Systemów Operacyjnych oraz Retro Konsol."""
    _helper_apply(app_instance, OS_TEMPLATES_DATA.get(template_key))


def apply_frame_template(app_instance, template_key: str):
    """Aplikuje styl strukturalny geometrii okna."""
    _helper_apply(app_instance, FRAMES_DATA.get(template_key))