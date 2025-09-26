# -*- coding: utf-8 -*-

init python:
    """
    Utility helpers for the appreciation mode screen.

    The functions below are designed to work with the Ren'Py 8 series API.
    They avoid importing the legacy "renpy" module directly and instead rely
    on the modern exports helpers that remain stable between versions.
    """

    try:
        from renpy import exports as _renpy_exports
    except Exception:
        _renpy_exports = None

    def _iter_appreciation_files():
        """Yield project file names using the safest available API."""
        if _renpy_exports and hasattr(_renpy_exports, "list_files"):
            try:
                return _renpy_exports.list_files()
            except Exception:
                pass
        return []

    def _normalise_filename(entry):
        """Extract the real filename from different iterator return types."""
        if isinstance(entry, str):
            return entry
        if isinstance(entry, (list, tuple)) and entry:
            head = entry[0]
            if isinstance(head, str):
                return head
        return None

    def _list_appreciation_files(prefix):
        """Collect image files under the given prefix while skipping helpers."""
        valid_exts = (".png", ".jpg", ".jpeg", ".webp")
        prefix = prefix or ""
        blacklist = [
            "images/场景图/bg pong.png",   # 把你不想显示的 CG 路径写在这里
            "images/场景图/black.png",
        ]
        results = []
        for entry in _iter_appreciation_files():
            filename = _normalise_filename(entry)
            if not filename:
                continue
            if prefix and not filename.startswith(prefix):
                continue
            if "/素材" in filename or "/素材库" in filename:
                continue
            if filename.lower().endswith(valid_exts):
                if filename in blacklist:   # 跳过黑名单里的文件
                    continue
                results.append(filename)
        results.sort()
        return results

    def _build_heroine_catalog():
        """Assemble heroine metadata with optional user overrides."""
        # Developers can provide a custom list named appreciation_heroines in
        # store to override the defaults below. Each entry is expected to be a
        # mapping with id, name, and optional "prefix" or explicit "images".
        try:
            from store import appreciation_heroines as custom_heroines
        except Exception:
            custom_heroines = None

        catalog = []
        source = custom_heroines
        if not source:
            source = [
                {"id": "aoi", "name": _("小早川葵"), "prefix": "images/小早川葵/"},
                {"id": "sakura", "name": _("藤原樱"), "prefix": "images/藤原樱/"},
                {"id": "ao", "name": _("雾岛蓝"), "prefix": "images/雾岛蓝/"},
                {"id": "akane", "name": _("风见茜"), "prefix": "images/风见茜/"},
            ]

        for heroine in source:
            entry = dict(heroine)
            if "images" not in entry:
                prefix = entry.get("prefix", "")
                entry["images"] = _list_appreciation_files(prefix)
            entry.setdefault("images", [])
            catalog.append(entry)
        return catalog

    APPRECIATION_CG_IMAGES = _list_appreciation_files("images/场景图/")
    APPRECIATION_HEROINES = _build_heroine_catalog()
    APPRECIATION_HEROINES_MAP = {heroine["id"]: heroine for heroine in APPRECIATION_HEROINES}


screen appreciation_mode():
    tag menu
    style_prefix "appreciation"

    default category = "cg"
    default selected_heroine = APPRECIATION_HEROINES[0]["id"] if APPRECIATION_HEROINES else None
    default sprite_index = 0

    use game_menu(_("鉴赏模式")):
        hbox:
            spacing 30
            xfill True

            frame:
                style "appreciation_sidebar"

                vbox:
                    spacing 20
                    text _("分类") style "appreciation_heading"

                    textbutton _("CG鉴赏"):
                        action [SetScreenVariable("category", "cg"), SetScreenVariable("sprite_index", 0)]
                        selected category == "cg"

                    textbutton _("立绘鉴赏"):
                        action SetScreenVariable("category", "sprites")
                        selected category == "sprites"

                    if category == "sprites" and APPRECIATION_HEROINES:
                        null height 15
                        text _("角色") style "appreciation_heading"

                        viewport:
                            mousewheel True
                            scrollbars "vertical"
                            ymaximum 480

                            vbox:
                                spacing 8
                                for heroine in APPRECIATION_HEROINES:
                                    textbutton heroine["name"]:
                                        action [
                                            SetScreenVariable("selected_heroine", heroine["id"]),
                                            SetScreenVariable("sprite_index", 0),
                                        ]
                                        selected selected_heroine == heroine["id"]

            frame:
                style "appreciation_content"
                xfill True
                yfill True

                if category == "cg":
                    if APPRECIATION_CG_IMAGES:
                        python:
                            total = len(APPRECIATION_CG_IMAGES)
                            columns = 3
                            rows = (total + columns - 1) // columns if total else 1

                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            pagekeys True

                            grid rows columns spacing 20:
                                for image_path in APPRECIATION_CG_IMAGES:
                                    frame:
                                        style "appreciation_thumbnail"
                                        add Transform(
                                            image_path,
                                            fit="contain",
                                            xalign=0.5,
                                            yalign=0.5,
                                            xsize=360,
                                            ysize=220
                                        )
                    else:
                        text _("目前没有可用的CG素材。") style "appreciation_body"
                else:
                    $ heroine = APPRECIATION_HEROINES_MAP.get(selected_heroine)

                    if heroine and heroine["images"]:
                        vbox:
                            spacing 20
                            xfill True
                            yfill True

                            text heroine["name"] style "appreciation_heading"

                            frame:
                                style "appreciation_sprite_stage"
                                xfill True
                                yfill True

                                viewport:
                                    scrollbars "vertical"
                                    mousewheel True
                                    draggable True
                                    pagekeys True

                                    add Transform(
                                        heroine["images"][sprite_index],
                                        fit="contain",   # 按比例缩放
                                        xalign=0.5,
                                        yalign=0.0,
                                        xsize=int(config.screen_width * 0.5)
                                    )

                            if len(heroine["images"]) > 1:
                                hbox:
                                    style "appreciation_switcher"

                                    textbutton _("上一张"):
                                        action SetScreenVariable(
                                            "sprite_index",
                                            (sprite_index - 1) % len(heroine["images"]),
                                        )

                                    textbutton _("下一张"):
                                        action SetScreenVariable(
                                            "sprite_index",
                                            (sprite_index + 1) % len(heroine["images"]),
                                        )
                    else:
                        text _("当前角色暂无可鉴赏的立绘。") style "appreciation_body"




style appreciation_sidebar is frame
style appreciation_content is frame
style appreciation_thumbnail is frame
style appreciation_heading is gui_label
style appreciation_body is gui_text
style appreciation_sprite_stage is frame
style appreciation_switcher is hbox

style appreciation_sidebar:
    xsize 320
    yfill True
    padding (20, 20)

style appreciation_content:
    padding (30, 30)

style appreciation_thumbnail:
    xsize 360
    ysize 220
    padding (10, 10)

style appreciation_heading:
    properties gui.text_properties("label", accent=True)

style appreciation_body:
    properties gui.text_properties("interface")

style appreciation_sprite_stage:
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)
    padding (30, 30)

style appreciation_switcher:
    spacing 40
    xalign 0.5
