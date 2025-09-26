## 鉴赏模式界面
## 参考一般 galgame 鉴赏实现，提供 CG 和立绘两类浏览。

init python:
    from renpy import store

    try:
        from renpy import exports as _renpy_exports
    except ImportError:
        _renpy_exports = None

    try:
        from renpy import loader as _renpy_loader
    except ImportError:
        _renpy_loader = None

    def _iter_game_files():
        if _renpy_exports and hasattr(_renpy_exports, "list_files"):
            return _renpy_exports.list_files()
        if _renpy_loader and hasattr(_renpy_loader, "listdirfiles"):
            return _renpy_loader.listdirfiles()
        raise RuntimeError("无法枚举资源文件，请检查 Ren'Py 运行环境是否完整。")

    def _image_size(filename):
        if _renpy_exports and hasattr(_renpy_exports, "image_size"):
            return _renpy_exports.image_size(filename)
        return (None, None)

    def _appreciation_is_image(filename):
        filename = filename.lower()
        return filename.endswith((".png", ".jpg", ".jpeg", ".webp"))

    def _appreciation_collect(prefix):
        prefix = prefix.rstrip("/") + "/"
        files = []
        for fn in _iter_game_files():
            if not fn.startswith(prefix):
                continue
            remainder = fn[len(prefix):]
            if "/" in remainder:
                # 跳过子目录（如素材库等）
                continue
            if _appreciation_is_image(fn):
                files.append(fn)
        files.sort()
        return files

    appreciation_cg_images = _appreciation_collect("images/场景图")

    _sprite_sources = [
        ("小早川葵", "images/小早川葵"),
        ("藤原樱", "images/藤原樱"),
        ("雾岛蓝", "images/雾岛蓝"),
        ("风见茜", "images/风见茜"),
    ]

    appreciation_sprite_lookup = {}
    appreciation_sprite_names = []

    for display_name, folder in _sprite_sources:
        entries = _appreciation_collect(folder)
        if entries:
            appreciation_sprite_lookup[display_name] = entries
            appreciation_sprite_names.append(display_name)

    appreciation_first_sprite = appreciation_sprite_names[0] if appreciation_sprite_names else None

    def appreciation_cycle_sprite(delta):
        name = store.appreciation_selected_sprite
        if not name:
            return
        sprites = appreciation_sprite_lookup.get(name, [])
        if not sprites:
            return
        store.appreciation_sprite_index = (store.appreciation_sprite_index + delta) % len(sprites)


default appreciation_category = "cg"
default appreciation_selected_cg = None
default appreciation_selected_sprite = appreciation_first_sprite
default appreciation_sprite_index = 0


screen appreciation_gallery():
    tag menu
    modal False

    add gui.main_menu_background

    frame:
        style "appreciation_side_frame"

        vbox:
            spacing 20
            text _("鉴赏模式") style "appreciation_heading"

            textbutton _("CG 鉴赏"):
                style "appreciation_tab_button"
                selected appreciation_category == "cg"
                action SetVariable("appreciation_category", "cg")

            textbutton _("立绘鉴赏"):
                style "appreciation_tab_button"
                selected appreciation_category == "sprite"
                action [
                    SetVariable("appreciation_category", "sprite"),
                    If(appreciation_selected_sprite is None and appreciation_sprite_names, SetVariable("appreciation_selected_sprite", appreciation_sprite_names[0]))
                ]

            null height 40

            textbutton _("返回标题") action ShowMenu("main_menu")

    frame:
        style "appreciation_content_frame"

        if appreciation_category == "cg":
            use appreciation_cg_panel
        else:
            use appreciation_sprite_panel

    if appreciation_selected_cg:
        use appreciation_cg_preview


screen appreciation_cg_panel():
    default column_count = 3

    if appreciation_cg_images:
        viewport:
            scrollbars "vertical"
            draggable True
            mousewheel True
            pagekeys True

            vpgrid:
                cols column_count
                spacing 20

                for cg_path in appreciation_cg_images:
                    button:
                        style "appreciation_cg_thumb"
                        action SetVariable("appreciation_selected_cg", cg_path)

                        has fixed
                        add im.Scale(cg_path, 360, 202)
                        text cg_path.split("/")[-1] style "appreciation_thumb_caption"
    else:
        text _("暂无 CG 可供鉴赏") style "appreciation_empty" xalign 0.5 yalign 0.5


screen appreciation_cg_preview():
    modal True

    $ preview_w = int(config.screen_width * 0.85)
    $ preview_h = int(config.screen_height * 0.85)
    $ img_w, img_h = _image_size(appreciation_selected_cg)
    $ scale_factor = 1.0
    if img_w and img_h:
        $ scale_factor = min(1.0, preview_w / float(img_w), preview_h / float(img_h))

    button:
        style "appreciation_preview_overlay"
        action SetVariable("appreciation_selected_cg", None)

        key "K_ESCAPE" action SetVariable("appreciation_selected_cg", None)
        key "mouseup_3" action SetVariable("appreciation_selected_cg", None)

        frame:
            style "appreciation_preview_frame"
            vbox:
                spacing 20
                text appreciation_selected_cg.split("/")[-1] style "appreciation_preview_title"
                add Transform(appreciation_selected_cg, zoom=scale_factor)
                textbutton _("关闭") action SetVariable("appreciation_selected_cg", None) xalign 0.5


screen appreciation_sprite_panel():
    if not appreciation_sprite_names:
        text _("暂无立绘可供鉴赏") style "appreciation_empty" xalign 0.5 yalign 0.5
    else:
        $ current_name = appreciation_selected_sprite if appreciation_selected_sprite else appreciation_sprite_names[0]
        $ sprite_list = appreciation_sprite_lookup.get(current_name, [])
        if appreciation_selected_sprite != current_name:
            $ appreciation_selected_sprite = current_name
            $ appreciation_sprite_index = 0
        if sprite_list:
            $ sprite_index = appreciation_sprite_index % len(sprite_list)
            $ sprite_path = sprite_list[sprite_index]
        else:
            $ sprite_path = None

        vbox:
            spacing 30

            hbox:
                spacing 12
                xalign 0.5
                for name in appreciation_sprite_names:
                    textbutton name:
                        style "appreciation_tab_button"
                        selected name == appreciation_selected_sprite
                        action [
                            SetVariable("appreciation_selected_sprite", name),
                            SetVariable("appreciation_sprite_index", 0)
                        ]

            frame:
                style "appreciation_sprite_stage"

                if sprite_path:
                    draggroup:
                        drag:
                            drag_name "appreciation_sprite"
                            child Transform(sprite_path, anchor=(0.5, 1.0))
                            draggable True
                            droppable False
                            xpos 0.5
                            xanchor 0.5
                            ypos 0.9
                            yanchor 1.0
                else:
                    text _("当前角色暂无立绘") style "appreciation_empty" xalign 0.5 yalign 0.5

            hbox:
                spacing 40
                xalign 0.5
                textbutton _("上一张") action Function(appreciation_cycle_sprite, -1)
                textbutton _("下一张") action Function(appreciation_cycle_sprite, 1)

            text _("提示：拖动立绘即可在舞台上自由移动。") style "appreciation_hint" xalign 0.5


style appreciation_side_frame is frame
style appreciation_content_frame is frame
style appreciation_heading is gui_text
style appreciation_tab_button is navigation_button
style appreciation_tab_button_text is navigation_button_text
style appreciation_cg_thumb is button
style appreciation_cg_thumb_text is button_text
style appreciation_thumb_caption is gui_text
style appreciation_preview_overlay is button
style appreciation_preview_frame is frame
style appreciation_preview_title is gui_text
style appreciation_sprite_stage is frame
style appreciation_empty is gui_text
style appreciation_hint is gui_text


style appreciation_side_frame:
    xalign 0.0
    yalign 0.5
    xsize 360
    ysize 900
    padding (40, 40, 40, 40)
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

style appreciation_content_frame:
    xalign 0.5
    yalign 0.5
    xfill True
    yfill True
    xoffset 180
    padding (40, 40, 40, 40)
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

style appreciation_heading:
    properties gui.text_properties("title")

style appreciation_tab_button:
    properties gui.button_properties("navigation_button")

style appreciation_tab_button_text:
    properties gui.text_properties("navigation_button")

style appreciation_cg_thumb:
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)
    padding (10, 10, 10, 10)
    xsize 380
    ysize 260

style appreciation_cg_thumb_text:
    properties gui.text_properties("interface")

style appreciation_thumb_caption:
    properties gui.text_properties("interface")
    xalign 0.5
    yalign 1.0

style appreciation_preview_overlay:
    xfill True
    yfill True
    background Solid("#0008")

style appreciation_preview_frame:
    xalign 0.5
    yalign 0.5
    padding (30, 30, 30, 30)
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

style appreciation_preview_title:
    properties gui.text_properties("title")
    xalign 0.5

style appreciation_sprite_stage:
    xsize 1200
    ysize 640
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

style appreciation_empty:
    properties gui.text_properties("interface")

style appreciation_hint:
    properties gui.text_properties("prompt")
