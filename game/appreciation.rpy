# -*- coding: utf-8 -*-

init python:
    import renpy

    def _list_appreciation_files(prefix):
        """Collect image files under the given prefix while skipping helper folders."""
        valid_exts = (".png", ".jpg", ".jpeg", ".webp")
        results = []
        for filepath in renpy.list_files():
            if not filepath.startswith(prefix):
                continue
            if "/素材" in filepath or "/素材库" in filepath:
                continue
            if filepath.lower().endswith(valid_exts):
                results.append(filepath)
        results.sort()
        return results

    APPRECIATION_CG_IMAGES = _list_appreciation_files("images/场景图/")

    APPRECIATION_HEROINES = [
        {
            "id": "aoi",
            "name": _("小早川葵"),
            "images": _list_appreciation_files("images/小早川葵/"),
        },
        {
            "id": "sakura",
            "name": _("藤原樱"),
            "images": _list_appreciation_files("images/藤原樱/"),
        },
        {
            "id": "ao",
            "name": _("雾岛蓝"),
            "images": _list_appreciation_files("images/雾岛蓝/"),
        },
        {
            "id": "akane",
            "name": _("风见茜"),
            "images": _list_appreciation_files("images/风见茜/"),
        },
    ]

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
                                        add Transform(image_path, fit="contain", xalign=0.5, yalign=0.5, xsize=360, ysize=220)
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

                                fixed:
                                    xfill True
                                    yfill True

                                    drag:
                                        draggable True
                                        child Transform(heroine["images"][sprite_index], fit="contain", xalign=0.5, yalign=1.0)

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

