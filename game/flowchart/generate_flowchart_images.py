"""Utility for generating flowchart imagemap assets.

This module recreates the ground/idle/hover/selected/insensitive imagery that
Ren'Py's imagemap loader expects.  The coordinates and labels are sourced from
``game/flowchart/flowchart.rpy`` so that the generated artwork always matches
the interactive flowchart.  Only drawing logic is provided here – run the
module as a script to render the PNG files locally when needed.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont


# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------
CANVAS_SIZE: Tuple[int, int] = (1600, 7900)
"""Overall resolution used by the flowchart imagemap."""

NODE_SIZE: Tuple[int, int] = (320, 180)
"""Dimensions of a single flowchart hotspot as defined in ``flowchart.rpy``."""

BACKGROUND_COLOR = (247, 245, 252)
GRID_COLOR = (225, 220, 240)
CONNECTOR_COLOR = (180, 175, 210)
CONNECTOR_HIGHLIGHT = (210, 205, 235)

# Location of the bundled font that already ships with the project so that the
# generated images match the in-game typography.
FONT_PATH = (Path(__file__).resolve().parent.parent / "fonts" / "NotoSerifSC-VF.ttf")
TITLE_FONT_SIZE = 36

# Output directory for the generated assets.
OUTPUT_DIR = Path(__file__).resolve().parent / "image"


@dataclass(frozen=True)
class Node:
    """Represents an interactive node on the flowchart."""

    key: str
    xy: Tuple[int, int]
    title: str

    @property
    def rect(self) -> Tuple[int, int, int, int]:
        x, y = self.xy
        w, h = NODE_SIZE
        return (x, y, x + w, y + h)

    @property
    def center(self) -> Tuple[float, float]:
        x, y = self.xy
        w, h = NODE_SIZE
        return (x + w / 2.0, y + h / 2.0)


# Node definitions copied from ``game/flowchart/flowchart.rpy``.  Only the label
# titles are rendered on the imagemap – descriptions remain in the interactive
# panel handled by Ren'Py.
NODE_DATA: Sequence[Node] = (
    Node("chapter_1", (640, 80), "序章 · 图书馆邂逅"),
    Node("fc_ch1_home", (640, 330), "序章 · 夜晚的独白"),
    Node("chapter_2", (640, 580), "第二天 · 早晨起步"),
    Node("fc_ch2_choice", (640, 830), "房间里的选择"),
    Node("love_mogic", (200, 1080), "阅读《心动魔法》"),
    Node("diary", (640, 1080), "翻开《共感日记》"),
    Node("play_pong", (1080, 1080), "打发时间的小游戏"),
    Node("fc_ch2_morning", (640, 1350), "第二天 · 校园清晨"),
    Node("fc_ch2_student_council", (640, 1620), "学生会的静谧午前"),
    Node("fc_ch2_track", (640, 1890), "田径场的委托"),
    Node("fc_ch2_storage", (640, 2160), "器材室的异变"),
    Node("fc_ch2_classroom", (640, 2430), "忙碌的午休"),
    Node("fc_ch2_astronomy", (640, 2700), "天文社的阴影"),
    Node("fc_ch2_evening", (640, 2970), "第二天 · 夜晚笔记"),
    Node("chapter_3", (640, 3240), "第三天 · 清晨反思"),
    Node("fc_ch3_library", (640, 3510), "图书馆的指引"),
    Node("fc_ch3_self_study", (640, 3780), "自习室的真相"),
    Node("fc_ch3_cooking", (640, 4050), "烹饪教室的携手"),
    Node("fc_ch3_dessert", (640, 4320), "甜品店集会"),
    Node("fc_ch3_dessert_choice", (640, 4590), "如何介绍神秘女孩"),
    Node("fc_ch3_dessert_option_a", (200, 4860), "只在图书馆见过"),
    Node("fc_ch3_dessert_option_b", (1080, 4860), "承认今早交流"),
    Node("fc_ch3_dessert_option_merge", (640, 5130), "甜品时间的尾声"),
    Node("fc_ch3_evening", (640, 5400), "星空观测的裂痕"),
    Node("fc_ch3_playground", (640, 5670), "岛蓝的告白"),
    Node("fc_ch3_afterglow", (640, 5940), "拍摄后的余韵"),
    Node("fc_ch3_conclusion", (640, 6210), "第三天的终章"),
    Node("chapter_4", (640, 6480), "第四天 · 抉择之前"),
    Node("fc_ch4_corridor", (640, 6750), "走廊上的约定"),
    Node("fc_ch4_campus", (640, 7020), "藤原樱的邀请"),
    Node("chapter_4_choice", (640, 7290), "下午要去哪里？"),
    Node("chapter_4_sakura_afternoon", (200, 7560), "烹饪教室的下午"),
    Node("ch4_aoi_branch", (640, 7560), "田径场支线"),
    Node("ch4_ao_branch", (1080, 7560), "雾岛蓝支线"),
)


# Manual connector definitions describing how the nodes relate to each other.
EDGE_LIST: Sequence[Tuple[str, str]] = (
    ("chapter_1", "fc_ch1_home"),
    ("fc_ch1_home", "chapter_2"),
    ("chapter_2", "fc_ch2_choice"),
    ("fc_ch2_choice", "love_mogic"),
    ("fc_ch2_choice", "diary"),
    ("fc_ch2_choice", "play_pong"),
    ("love_mogic", "fc_ch2_morning"),
    ("diary", "fc_ch2_morning"),
    ("play_pong", "fc_ch2_morning"),
    ("fc_ch2_morning", "fc_ch2_student_council"),
    ("fc_ch2_student_council", "fc_ch2_track"),
    ("fc_ch2_track", "fc_ch2_storage"),
    ("fc_ch2_storage", "fc_ch2_classroom"),
    ("fc_ch2_classroom", "fc_ch2_astronomy"),
    ("fc_ch2_astronomy", "fc_ch2_evening"),
    ("fc_ch2_evening", "chapter_3"),
    ("chapter_3", "fc_ch3_library"),
    ("fc_ch3_library", "fc_ch3_self_study"),
    ("fc_ch3_self_study", "fc_ch3_cooking"),
    ("fc_ch3_cooking", "fc_ch3_dessert"),
    ("fc_ch3_dessert", "fc_ch3_dessert_choice"),
    ("fc_ch3_dessert_choice", "fc_ch3_dessert_option_a"),
    ("fc_ch3_dessert_choice", "fc_ch3_dessert_option_b"),
    ("fc_ch3_dessert_option_a", "fc_ch3_dessert_option_merge"),
    ("fc_ch3_dessert_option_b", "fc_ch3_dessert_option_merge"),
    ("fc_ch3_dessert_option_merge", "fc_ch3_evening"),
    ("fc_ch3_evening", "fc_ch3_playground"),
    ("fc_ch3_playground", "fc_ch3_afterglow"),
    ("fc_ch3_afterglow", "fc_ch3_conclusion"),
    ("fc_ch3_conclusion", "chapter_4"),
    ("chapter_4", "fc_ch4_corridor"),
    ("fc_ch4_corridor", "fc_ch4_campus"),
    ("fc_ch4_campus", "chapter_4_choice"),
    ("chapter_4_choice", "chapter_4_sakura_afternoon"),
    ("chapter_4_choice", "ch4_aoi_branch"),
    ("chapter_4_choice", "ch4_ao_branch"),
)

# Styles for each imagemap state.
STATE_STYLES: Dict[str, Dict[str, Tuple[int, int, int, int]]] = {
    "ground": {
        "fill": (0, 0, 0, 0),
        "outline": (205, 198, 225, 255),
        "text": (0, 0, 0, 0),
    },
    "idle": {
        "fill": (255, 255, 255, 230),
        "outline": (120, 110, 170, 255),
        "text": (70, 60, 110, 255),
    },
    "hover": {
        "fill": (239, 231, 255, 255),
        "outline": (130, 90, 180, 255),
        "text": (50, 30, 100, 255),
    },
    "selected_idle": {
        "fill": (228, 246, 255, 255),
        "outline": (42, 102, 160, 255),
        "text": (15, 56, 105, 255),
    },
    "selected_hover": {
        "fill": (215, 236, 255, 255),
        "outline": (30, 92, 150, 255),
        "text": (5, 46, 95, 255),
    },
    "insensitive": {
        "fill": (230, 230, 235, 255),
        "outline": (170, 170, 180, 255),
        "text": (130, 130, 140, 255),
    },
}

CROSSHAIR_STYLE = {
    "size": NODE_SIZE,
    "stroke": (88, 132, 204, 255),
    "thickness": 8,
    "padding": 16,
}


def _node_lookup() -> Dict[str, Node]:
    return {n.key: n for n in NODE_DATA}


def _load_font(size: int = TITLE_FONT_SIZE) -> ImageFont.FreeTypeFont:
    if not FONT_PATH.exists():
        raise FileNotFoundError(
            f"Expected font at {FONT_PATH!s}. Please adjust FONT_PATH before generating images."
        )
    return ImageFont.truetype(str(FONT_PATH), size=size)


def _draw_grid(draw: ImageDraw.ImageDraw) -> None:
    """Render a subtle square grid to help with navigation."""
    step = 160
    for x in range(0, CANVAS_SIZE[0], step):
        draw.line([(x, 0), (x, CANVAS_SIZE[1])], fill=GRID_COLOR, width=1)
    for y in range(0, CANVAS_SIZE[1], step):
        draw.line([(0, y), (CANVAS_SIZE[0], y)], fill=GRID_COLOR, width=1)


def _draw_connectors(draw: ImageDraw.ImageDraw, nodes: Dict[str, Node]) -> None:
    """Draw polyline connectors between nodes."""
    for start_key, end_key in EDGE_LIST:
        start = nodes[start_key].center
        end = nodes[end_key].center
        _draw_manhattan_path(draw, start, end)


def _draw_manhattan_path(draw: ImageDraw.ImageDraw, start: Tuple[float, float], end: Tuple[float, float]) -> None:
    sx, sy = start
    ex, ey = end
    if abs(sx - ex) < 1 or abs(sy - ey) < 1:
        points = [(sx, sy), (ex, ey)]
    else:
        mid_y = (sy + ey) / 2
        points = [(sx, sy), (sx, mid_y), (ex, mid_y), (ex, ey)]
    draw.line(points, fill=CONNECTOR_COLOR, width=10, joint="curve")
    # Highlight the line slightly for added depth.
    draw.line(points, fill=CONNECTOR_HIGHLIGHT, width=4, joint="curve")


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, width: int) -> List[str]:
    """Very small helper to wrap Chinese text without spaces."""
    lines: List[str] = []
    buffer = ""
    for char in text:
        if char == "\n":
            lines.append(buffer)
            buffer = ""
            continue
        candidate = buffer + char
        if font.getlength(candidate) <= width:
            buffer = candidate
            continue
        if buffer:
            lines.append(buffer)
        buffer = char
    if buffer:
        lines.append(buffer)
    return lines


def _draw_nodes(
    draw: ImageDraw.ImageDraw,
    nodes: Iterable[Node],
    font: ImageFont.FreeTypeFont,
    *,
    fill: Tuple[int, int, int, int],
    outline: Tuple[int, int, int, int],
    text: Tuple[int, int, int, int],
) -> None:
    corner_radius = 36
    for node in nodes:
        x0, y0, x1, y1 = node.rect
        draw.rounded_rectangle(node.rect, radius=corner_radius, fill=fill, outline=outline, width=6)
        lines = _wrap_text(node.title, font, width=NODE_SIZE[0] - 40)
        total_height = len(lines) * font.size + (len(lines) - 1) * 6
        text_y = y0 + (NODE_SIZE[1] - total_height) / 2
        for line in lines:
            text_width = font.getlength(line)
            text_x = x0 + (NODE_SIZE[0] - text_width) / 2
            draw.text((text_x, text_y), line, fill=text, font=font)
            text_y += font.size + 6


def _render_state_image(state: str, nodes: Dict[str, Node], font: ImageFont.FreeTypeFont) -> Image.Image:
    canvas = Image.new("RGBA", CANVAS_SIZE, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(canvas)
    _draw_grid(draw)
    _draw_connectors(draw, nodes)

    style = STATE_STYLES[state]
    _draw_nodes(draw, nodes.values(), font, fill=style["fill"], outline=style["outline"], text=style["text"])
    return canvas


def render_all_states(output_dir: Path = OUTPUT_DIR) -> None:
    """Generate all imagemap state assets into ``output_dir``."""
    output_dir.mkdir(parents=True, exist_ok=True)
    nodes = _node_lookup()
    font = _load_font()

    for state in ("ground", "idle", "hover", "selected_idle", "selected_hover", "insensitive"):
        image = _render_state_image(state, nodes, font)
        image.save(output_dir / f"{state}.png")

    crosshair = _render_crosshair()
    crosshair.save(output_dir / "crosshair.png")


def _render_crosshair() -> Image.Image:
    width, height = CROSSHAIR_STYLE["size"]
    padding = CROSSHAIR_STYLE["padding"]
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    stroke = CROSSHAIR_STYLE["stroke"]
    thickness = CROSSHAIR_STYLE["thickness"]

    inner_rect = (
        padding,
        padding,
        width - padding,
        height - padding,
    )
    draw.rounded_rectangle(inner_rect, radius=28, outline=stroke, width=thickness)

    # Draw crosshair ticks.
    cx = width / 2
    cy = height / 2
    tick_len = 30
    draw.line([(cx - tick_len, cy), (cx + tick_len, cy)], fill=stroke, width=thickness)
    draw.line([(cx, cy - tick_len), (cx, cy + tick_len)], fill=stroke, width=thickness)

    return canvas


if __name__ == "__main__":
    # Run this module directly to generate the PNG assets.
    render_all_states()
