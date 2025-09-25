init python:
    import math
    from collections import defaultdict
    from renpy import store
    from renpy.display import im
    from renpy.display.core import Displayable
    from renpy.display.render import Render
    from renpy.exports import call_in_new_context, hide_screen, jump

    FLOWCHART_VIEW_WIDTH = 2000
    FLOWCHART_VIEW_HEIGHT = 8200

    FLOWCHART_SPECS = {
        "chapter": {
            "image": "gui/flowchart/chapter_start.png",
            "base_size": (480, 200),
            "size": (480, 200),
        },
        "scene": {
            "image": "gui/flowchart/scene.png",
            "base_size": (460, 180),
            "size": (460, 180),
        },
        "choice": {
            "image": "gui/flowchart/choice.png",
            "base_size": (360, 360),
            "size": (360, 360),
        },
    }

    FLOWCHART_NODES = [
        dict(id="ch1_start", title="序章 · 图书馆邂逅", summary="在图书馆与风见茜相遇，首次见到会发光的《共感日记》。", type="chapter", label="chapter_1", pos=(640, 80), thumbnail="images/场景图/bg library.png"),
        dict(id="ch1_home", title="序章 · 夜晚的独白", summary="回到家后思考神秘的两本书，为第二天做打算。", type="scene", label="fc_ch1_home", pos=(640, 330), thumbnail="images/场景图/bg home.png"),
        dict(id="ch2_start", title="第二天 · 早晨起步", summary="带着书本准备返校，心里仍挂念共感日记的异状。", type="chapter", label="chapter_2", pos=(640, 580), thumbnail="images/场景图/bg home.png"),
        dict(id="ch2_choice", title="房间里的选择", summary="决定是先研究书籍还是用游戏放松。", type="choice", label="fc_ch2_choice", pos=(640, 830), thumbnail="images/场景图/bg home.png"),
        dict(id="ch2_magic", title="阅读《心动魔法》", summary="翻阅恋爱偏方，了解“心动魔法”的流程。", type="scene", label="love_mogic", pos=(200, 1080), thumbnail="images/场景图/bg home.png"),
        dict(id="ch2_diary", title="翻开《共感日记》", summary="察觉日记中浮现的神秘文字。", type="scene", label="diary", pos=(640, 1080), thumbnail="images/场景图/bg library.png"),
        dict(id="ch2_game", title="打发时间的小游戏", summary="在电脑前与简陋的乒乓小游戏鏖战。", type="scene", label="play_pong", pos=(1080, 1080), thumbnail="images/场景图/bg pong.png"),
        dict(id="ch2_morning", title="第二天 · 校园清晨", summary="踏进被樱花包围的校园，准备开始社团工作。", type="scene", label="fc_ch2_morning", pos=(640, 1350), thumbnail="images/场景图/bg school.png"),
        dict(id="ch2_student", title="学生会的静谧午前", summary="与藤原樱协力整理资料，共感日记再度闪光。", type="scene", label="fc_ch2_student_council", pos=(640, 1620), thumbnail="images/场景图/bg student_council.png"),
        dict(id="ch2_track", title="田径场的委托", summary="在操场与葵一同处理社团琐事。", type="scene", label="fc_ch2_track", pos=(640, 1890), thumbnail="images/场景图/bg field.png"),
        dict(id="ch2_storage", title="器材室的异变", summary="共感日记对葵造成冲击，留下更多疑问。", type="scene", label="fc_ch2_storage", pos=(640, 2160), thumbnail="images/场景图/bg lab2.png"),
        dict(id="ch2_classroom", title="忙碌的午休", summary="草草吃完午饭又被天文社召唤。", type="scene", label="fc_ch2_classroom", pos=(640, 2430), thumbnail="images/场景图/bg classroom.png"),
        dict(id="ch2_astronomy", title="天文社的阴影", summary="雾岛蓝现身并带走笔记，留下谜团。", type="scene", label="fc_ch2_astronomy", pos=(640, 2700), thumbnail="images/场景图/bg bad_room.png"),
        dict(id="ch2_evening", title="第二天 · 夜晚笔记", summary="回家后发现日记追加了新的感官刻度。", type="scene", label="fc_ch2_evening", pos=(640, 2970), thumbnail="images/场景图/bg home.png"),
        dict(id="ch3_start", title="第三天 · 清晨反思", summary="抱着新的觉悟，再次走进春日校园。", type="chapter", label="chapter_3", pos=(640, 3240), thumbnail="images/场景图/bg school2.png"),
        dict(id="ch3_library", title="图书馆的指引", summary="风见茜说明共感日记的危险与任务。", type="scene", label="fc_ch3_library", pos=(640, 3510), thumbnail="images/场景图/bg library.png"),
        dict(id="ch3_self_study", title="自习室的真相", summary="亲眼见证樱花化作光点消散。", type="scene", label="fc_ch3_self_study", pos=(640, 3780), thumbnail="images/场景图/bg classroom.png"),
        dict(id="ch3_cooking", title="烹饪教室的携手", summary="与藤原樱并肩烘焙，让彼此更靠近。", type="scene", label="fc_ch3_cooking", pos=(640, 4050), thumbnail="images/场景图/bg cooking_classroom.png"),
        dict(id="ch3_dessert", title="甜品店集会", summary="四人在樱花甜品店共享新款点心。", type="scene", label="fc_ch3_dessert", pos=(640, 4320), thumbnail="images/场景图/bg street.png"),
        dict(id="ch3_choice", title="如何介绍神秘女孩", summary="决定如何回应同伴的追问。", type="choice", label="fc_ch3_dessert_choice", pos=(640, 4590), thumbnail="images/场景图/bg street.png"),
        dict(id="ch3_option_a", title="只在图书馆见过", summary="坦诚自己与女孩仍是萍水相逢。", type="scene", label="fc_ch3_dessert_option_a", pos=(200, 4860), thumbnail="images/场景图/bg library.png"),
        dict(id="ch3_option_b", title="承认今早交流", summary="说明早上曾与女孩攀谈。", type="scene", label="fc_ch3_dessert_option_b", pos=(1080, 4860), thumbnail="images/场景图/bg library.png"),
        dict(id="ch3_merge", title="甜品时间的尾声", summary="众人道别，氛围仍旧温暖。", type="scene", label="fc_ch3_dessert_option_merge", pos=(640, 5130), thumbnail="images/场景图/bg street.png"),
        dict(id="ch3_evening_star", title="星空观测的裂痕", summary="夜间拍摄时记忆与现实产生冲突。", type="scene", label="fc_ch3_evening", pos=(640, 5400), thumbnail="images/场景图/bg field.png"),
        dict(id="ch3_playground", title="雾岛蓝的告白", summary="雾岛蓝倾诉听觉疾病与对朋友的在意。", type="scene", label="fc_ch3_playground", pos=(640, 5670), thumbnail="images/场景图/bg playground.png"),
        dict(id="ch3_afterglow", title="拍摄后的余韵", summary="返回拍摄地点，听到蓝的提醒。", type="scene", label="fc_ch3_afterglow", pos=(640, 5940), thumbnail="images/场景图/bg field.png"),
        dict(id="ch3_conclusion", title="第三天的终章", summary="夜幕降临，故事迈向第四天。", type="scene", label="fc_ch3_conclusion", pos=(640, 6210), thumbnail="images/场景图/bg home.png"),
        dict(id="ch4_start", title="第四天 · 抉择之前", summary="决定暂时将共感日记留在家里。", type="chapter", label="chapter_4", pos=(640, 6480), thumbnail="images/场景图/bg home.png"),
        dict(id="ch4_corridor", title="走廊上的约定", summary="葵表达想与阳太继续同行。", type="scene", label="fc_ch4_corridor", pos=(640, 6750), thumbnail="images/场景图/bg corridor.png"),
        dict(id="ch4_campus", title="藤原樱的邀请", summary="樱递上手作蛋糕并邀请再次烹饪。", type="scene", label="fc_ch4_campus", pos=(640, 7020), thumbnail="images/场景图/bg school2.png"),
        dict(id="ch4_choice", title="下午要去哪里？", summary="决定放学后要前往的地点。", type="choice", label="chapter_4_choice", pos=(640, 7290), thumbnail="images/场景图/bg corridor.png"),
        dict(id="ch4_sakura", title="烹饪教室的下午", summary="与藤原樱继续烘焙，彼此的关系更进一步。", type="scene", label="chapter_4_sakura_afternoon", pos=(200, 7560), thumbnail="images/场景图/bg cooking_classroom.png"),
        dict(id="ch4_aoi_branch", title="田径场支线", summary="小早川葵的后续事件尚待实装。", type="scene", label=None, pos=(640, 7560), thumbnail="images/场景图/bg field.png"),
        dict(id="ch4_ao_branch", title="雾岛蓝支线", summary="雾岛蓝的剧情将在未来版本开放。", type="scene", label=None, pos=(1080, 7560), thumbnail="images/场景图/bg bad_room.png"),
    ]

    FLOWCHART_EDGES = [
        ("ch1_start", "ch1_home"),
        ("ch1_home", "ch2_start"),
        ("ch2_start", "ch2_choice"),
        ("ch2_choice", "ch2_magic"),
        ("ch2_choice", "ch2_diary"),
        ("ch2_choice", "ch2_game"),
        ("ch2_magic", "ch2_morning"),
        ("ch2_diary", "ch2_morning"),
        ("ch2_game", "ch2_morning"),
        ("ch2_morning", "ch2_student"),
        ("ch2_student", "ch2_track"),
        ("ch2_track", "ch2_storage"),
        ("ch2_storage", "ch2_classroom"),
        ("ch2_classroom", "ch2_astronomy"),
        ("ch2_astronomy", "ch2_evening"),
        ("ch2_evening", "ch3_start"),
        ("ch3_start", "ch3_library"),
        ("ch3_library", "ch3_self_study"),
        ("ch3_self_study", "ch3_cooking"),
        ("ch3_cooking", "ch3_dessert"),
        ("ch3_dessert", "ch3_choice"),
        ("ch3_choice", "ch3_option_a"),
        ("ch3_choice", "ch3_option_b"),
        ("ch3_option_a", "ch3_merge"),
        ("ch3_option_b", "ch3_merge"),
        ("ch3_merge", "ch3_evening_star"),
        ("ch3_evening_star", "ch3_playground"),
        ("ch3_playground", "ch3_afterglow"),
        ("ch3_afterglow", "ch3_conclusion"),
        ("ch3_conclusion", "ch4_start"),
        ("ch4_start", "ch4_corridor"),
        ("ch4_corridor", "ch4_campus"),
        ("ch4_campus", "ch4_choice"),
        ("ch4_choice", "ch4_sakura"),
        ("ch4_choice", "ch4_aoi_branch"),
        ("ch4_choice", "ch4_ao_branch"),
    ]

    FLOWCHART_LOOKUP = {}
    FLOWCHART_NEIGHBORS = defaultdict(list)

    for node in FLOWCHART_NODES:
        spec = FLOWCHART_SPECS[node["type"]]
        node["size"] = spec["size"]
        node["image"] = spec["image"]
        FLOWCHART_LOOKUP[node["id"]] = node

    for start, end in FLOWCHART_EDGES:
        FLOWCHART_NEIGHBORS[start].append(end)
        FLOWCHART_NEIGHBORS[end].append(start)

    class FlowchartEdges(Displayable):
        def __init__(self, nodes, edges, width, height, line_color="#cfd7ff", arrow_color="#5c6ed8", line_width=6):
            super().__init__()
            self.nodes = nodes
            self.edges = edges
            self.width = width
            self.height = height
            self.line_color = line_color
            self.arrow_color = arrow_color
            self.line_width = line_width

        def render(self, width, height, st, at):
            edge_render = Render(self.width, self.height)
            canvas = edge_render.canvas()
            for start_id, end_id in self.edges:
                start_node = self.nodes[start_id]
                end_node = self.nodes[end_id]
                sx = start_node["pos"][0] + start_node["size"][0] / 2.0
                sy = start_node["pos"][1] + start_node["size"][1]
                ex = end_node["pos"][0] + end_node["size"][0] / 2.0
                ey = end_node["pos"][1]
                canvas.line(self.line_color, (sx, sy), (ex, ey), width=self.line_width)
                dx = ex - sx
                dy = ey - sy
                distance = math.hypot(dx, dy)
                if distance == 0:
                    continue
                ux = dx / distance
                uy = dy / distance
                arrow_len = 24
                arrow_width = 16
                px = ex - ux * arrow_len
                py = ey - uy * arrow_len
                left = (px - uy * arrow_width / 2.0, py + ux * arrow_width / 2.0)
                right = (px + uy * arrow_width / 2.0, py - ux * arrow_width / 2.0)
                canvas.polygon(self.arrow_color, [(ex, ey), left, right])
            return edge_render

    def flowchart_jump(node_id, from_main_menu):
        node = FLOWCHART_LOOKUP.get(node_id)
        if not node or not node.get("label"):
            return
        store._flowchart_selected = node_id
        hide_screen("flowchart")
        if from_main_menu:
            call_in_new_context(node["label"])
        else:
            jump(node["label"])

screen flowchart():
    tag menu

    default hovered_node = None
    default confirm_target = None
    $ default_id = FLOWCHART_NODES[0]["id"] if FLOWCHART_NODES else None
    $ current_selected = _flowchart_selected if _flowchart_selected in FLOWCHART_LOOKUP else default_id
    default selected_node = current_selected

    use game_menu(_("流程图"), scroll=None):
        hbox:
            spacing 40

            viewport:
                id "flowchart_viewport"
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                child_size (FLOWCHART_VIEW_WIDTH, FLOWCHART_VIEW_HEIGHT)

                fixed:
                    xysize (FLOWCHART_VIEW_WIDTH, FLOWCHART_VIEW_HEIGHT)
                    add FlowchartEdges(FLOWCHART_LOOKUP, FLOWCHART_EDGES, FLOWCHART_VIEW_WIDTH, FLOWCHART_VIEW_HEIGHT)

                    for node in FLOWCHART_NODES:
                        $ node_id = node["id"]
                        $ node_spec = FLOWCHART_SPECS[node["type"]]
                        $ bg = Transform(node_spec["image"], xzoom=node["size"][0] / float(node_spec["base_size"][0]), yzoom=node["size"][1] / float(node_spec["base_size"][1]))
                        button:
                            style "flowchart_node_button"
                            xpos node["pos"][0]
                            ypos node["pos"][1]
                            xsize node["size"][0]
                            ysize node["size"][1]
                            background bg
                            hovered SetScreenVariable("hovered_node", node_id)
                            unhovered SetScreenVariable("hovered_node", None)
                            action SetScreenVariable("selected_node", node_id)
                            if not node.get("label"):
                                sensitive False
                            if node_id == selected_node:
                                add Solid("#ffffff22")
                            if hovered_node == node_id and node_id != selected_node:
                                add Solid("#ffffff11")
                            vbox:
                                style "flowchart_node_content"
                                text node["title"] style "flowchart_node_title"
                                text node["summary"] style "flowchart_node_summary"

            frame:
                style "flowchart_detail_frame"
                has vbox
                spacing 20

                if selected_node and selected_node in FLOWCHART_LOOKUP:
                    $ node = FLOWCHART_LOOKUP[selected_node]
                    text node["title"] style "flowchart_detail_title"
                    if node.get("thumbnail"):
                        add im.Scale(node["thumbnail"], 420, 236)
                    text node["summary"] style "flowchart_detail_summary"
                    if FLOWCHART_NEIGHBORS[selected_node]:
                        text "相关节点" style "flowchart_detail_heading"
                        for neighbor_id in FLOWCHART_NEIGHBORS[selected_node]:
                            $ neighbor = FLOWCHART_LOOKUP[neighbor_id]
                            text "{0}：{1}".format(neighbor["title"], neighbor["summary"]) style "flowchart_detail_neighbor"
                    if node.get("label"):
                        textbutton "跳转到该节点":
                            style "flowchart_jump_button"
                            action SetScreenVariable("confirm_target", selected_node)
                    else:
                        text "该节点尚未实装，敬请期待。" style "flowchart_detail_disabled"
                else:
                    text "请选择左侧的节点来查看详情。" style "flowchart_detail_placeholder"

    if confirm_target:
        use flowchart_jump_confirm(confirm_target)

screen flowchart_jump_confirm(target_id):
    modal True
    zorder 200
    $ node = FLOWCHART_LOOKUP[target_id]
    frame:
        style "flowchart_confirm_frame"
        vbox:
            spacing 20
            text "是否从当前位置跳转至『{0}』？".format(node["title"]) style "flowchart_detail_title"
            text node["summary"] style "flowchart_detail_summary"
            hbox:
                spacing 40
                textbutton "取消" action SetScreenVariable("confirm_target", None)
                textbutton "确认跳转":
                    action [SetScreenVariable("confirm_target", None), Function(flowchart_jump, target_id, main_menu)]

style flowchart_node_button is button
style flowchart_node_button_text is button_text
style flowchart_node_content is vbox
style flowchart_node_title is text
style flowchart_node_summary is text
style flowchart_detail_frame is frame
style flowchart_detail_title is text
style flowchart_detail_summary is text
style flowchart_detail_heading is text
style flowchart_detail_neighbor is text
style flowchart_detail_disabled is text
style flowchart_detail_placeholder is text
style flowchart_jump_button is button
style flowchart_jump_button_text is button_text
style flowchart_confirm_frame is frame

style flowchart_node_button:
    padding (24, 24)
    background None
    foreground None

style flowchart_node_content:
    spacing 10

style flowchart_node_title:
    font gui.interface_text_font
    size 30
    color "#ffffff"
    outlines [(2, "#2c3e8f", 0, 0)]
    xalign 0.5
    text_align 0.5
    yalign 0.5

style flowchart_node_summary:
    font gui.interface_text_font
    size 24
    color "#ecf2ff"
    outlines [(1, "#2c3e8f", 0, 0)]
    text_align 0.5
    xalign 0.5
    yalign 0.5
    layout "subtitle"

style flowchart_detail_frame:
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)
    padding (30, 30)
    xsize 520
    yfill True

style flowchart_detail_title:
    font gui.interface_text_font
    size 36
    color gui.accent_color

style flowchart_detail_summary:
    font gui.interface_text_font
    size 24
    color gui.interface_text_color
    text_align 0.0
    layout "subtitle"

style flowchart_detail_heading:
    font gui.interface_text_font
    size 28
    color gui.accent_color

style flowchart_detail_neighbor:
    font gui.interface_text_font
    size 22
    color gui.interface_text_color
    text_align 0.0
    layout "subtitle"

style flowchart_detail_disabled:
    font gui.interface_text_font
    size 22
    color "#9aa4c6"

style flowchart_detail_placeholder:
    font gui.interface_text_font
    size 26
    color gui.interface_text_color

style flowchart_jump_button:
    background Frame("gui/button/idle_background.png", gui.button_borders, tile=gui.button_tile)
    hover_background Frame("gui/button/hover_background.png", gui.button_borders, tile=gui.button_tile)
    padding (14, 24)

style flowchart_jump_button_text:
    font gui.interface_text_font
    size 26
    color gui.button_text_idle_color
    hover_color gui.button_text_hover_color

style flowchart_confirm_frame:
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)
    padding (40, 40)
    xalign 0.5
    yalign 0.5
