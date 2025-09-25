########## DEVIL SPIδεR'S FLOWCHART PLUGIN ##########
# Adapted for "樱花色的七日奇迹" based on the standalone release.
# 组件文档与示例来自 https://devilspider.itch.io/flowchart-plug-in

init -3:
    default segment = "chapter_1"
    default segments = ["chapter_1"]
    default endings = []
    default story_flags = {}

    default flowchart_accessible = False


init python:
    # 将当前节点登记到流程图中。建议在每个标签的开头调用 new_node("label_name")。
    def new_node(n=None):
        global segment, segments
        if not n:
            return
        if segment and segment in nodes and segment not in segments:
            segments.append(segment)
        segment = n
        if segment and segment in nodes and segment not in segments:
            segments.append(segment)

    # 记录一个已经完成的结局。
    def unlock_ending(n=None):
        global endings
        if n and n not in endings:
            endings.append(n)

    # 让流程图上的某个节点在未抵达前也可见（例如未实装的分支）。
    def unlock_node(n=None):
        global segments
        if n and n not in segments:
            segments.append(n)

    # 节点定义："标签名": [(x, y), "显示名称", "简介", "解锁条件"]
    nodes = {
        "chapter_1": [(640, 80), "序章 · 图书馆邂逅", "在图书馆与风见茜相遇，首次见到会发光的《共感日记》。", "True"],
        "fc_ch1_home": [(640, 330), "序章 · 夜晚的独白", "回到家后思考神秘的两本书，为第二天做打算。", "True"],
        "chapter_2": [(640, 580), "第二天 · 早晨起步", "带着书本准备返校，心里仍挂念共感日记的异状。", "True"],
        "fc_ch2_choice": [(640, 830), "房间里的选择", "决定是先研究书籍还是用游戏放松。", "True"],
        "love_mogic": [(200, 1080), "阅读《心动魔法》", "翻阅恋爱偏方，了解“心动魔法”的流程。", "True"],
        "diary": [(640, 1080), "翻开《共感日记》", "察觉日记中浮现的神秘文字。", "True"],
        "play_pong": [(1080, 1080), "打发时间的小游戏", "在电脑前与简陋的乒乓小游戏鏖战。", "True"],
        "fc_ch2_morning": [(640, 1350), "第二天 · 校园清晨", "踏进被樱花包围的校园，准备开始社团工作。", "True"],
        "fc_ch2_student_council": [(640, 1620), "学生会的静谧午前", "与藤原樱协力整理资料，共感日记再度闪光。", "True"],
        "fc_ch2_track": [(640, 1890), "田径场的委托", "在操场与葵一同处理社团琐事。", "True"],
        "fc_ch2_storage": [(640, 2160), "器材室的异变", "共感日记对葵造成冲击，留下更多疑问。", "True"],
        "fc_ch2_classroom": [(640, 2430), "忙碌的午休", "草草吃完午饭又被天文社召唤。", "True"],
        "fc_ch2_astronomy": [(640, 2700), "天文社的阴影", "雾岛蓝现身并带走笔记，留下谜团。", "True"],
        "fc_ch2_evening": [(640, 2970), "第二天 · 夜晚笔记", "回家后发现日记追加了新的感官刻度。", "True"],
        "chapter_3": [(640, 3240), "第三天 · 清晨反思", "抱着新的觉悟，再次走进春日校园。", "True"],
        "fc_ch3_library": [(640, 3510), "图书馆的指引", "风见茜说明共感日记的危险与任务。", "True"],
        "fc_ch3_self_study": [(640, 3780), "自习室的真相", "亲眼见证樱花化作光点消散。", "True"],
        "fc_ch3_cooking": [(640, 4050), "烹饪教室的携手", "与藤原樱并肩烘焙，让彼此更靠近。", "True"],
        "fc_ch3_dessert": [(640, 4320), "甜品店集会", "四人在樱花甜品店共享新款点心。", "True"],
        "fc_ch3_dessert_choice": [(640, 4590), "如何介绍神秘女孩", "决定如何回应同伴的追问。", "True"],
        "fc_ch3_dessert_option_a": [(200, 4860), "只在图书馆见过", "坦诚自己与女孩仍是萍水相逢。", "True"],
        "fc_ch3_dessert_option_b": [(1080, 4860), "承认今早交流", "说明早上曾与女孩攀谈。", "True"],
        "fc_ch3_dessert_option_merge": [(640, 5130), "甜品时间的尾声", "众人道别，氛围仍旧温暖。", "True"],
        "fc_ch3_evening": [(640, 5400), "星空观测的裂痕", "夜间拍摄时记忆与现实产生冲突。", "True"],
        "fc_ch3_playground": [(640, 5670), "岛蓝的告白", "雾岛蓝倾诉听觉疾病与对朋友的在意。", "True"],
        "fc_ch3_afterglow": [(640, 5940), "拍摄后的余韵", "返回拍摄地点，听到蓝的提醒。", "True"],
        "fc_ch3_conclusion": [(640, 6210), "第三天的终章", "夜幕降临，故事迈向第四天。", "True"],
        "chapter_4": [(640, 6480), "第四天 · 抉择之前", "决定暂时将共感日记留在家里。", "True"],
        "fc_ch4_corridor": [(640, 6750), "走廊上的约定", "葵表达想与阳太继续同行。", "True"],
        "fc_ch4_campus": [(640, 7020), "藤原樱的邀请", "樱递上手作蛋糕并邀请再次烹饪。", "True"],
        "chapter_4_choice": [(640, 7290), "下午要去哪里？", "决定放学后要前往的地点。", "True"],
        "chapter_4_sakura_afternoon": [(200, 7560), "烹饪教室的下午", "与藤原樱继续烘焙，彼此的关系更进一步。", "True"],
        "ch4_aoi_branch": [(640, 7560), "田径场支线", "小早川葵的后续事件尚待实装。", "False"],
        "ch4_ao_branch": [(1080, 7560), "雾岛蓝支线", "雾岛蓝的剧情将在未来版本开放。", "False"],
    }

    gui.flow_hotspot_size = (320, 180)

    flow_choices = {}

    extra_lines = {}


screen flowchart():
    tag menu

    default select_node = None

    $ current_segment = segment if segment in nodes else next(iter(nodes.keys()))

    use game_menu(_("流程图"), scroll="viewport"):
        vbox:
            align (0.5, 0.0)
            spacing 30

            viewport:
                xalign 0.5
                xysize (1625, 7925)
                child_size (1600, 7900)
                mousewheel True
                scrollbars "vertical"
                edgescroll (150, 2000)
                draggable True
                xinitial 0.5

                for img, cnd in extra_lines.items():
                    if eval(cnd):
                        add "flowchart/image/" + img + ".png"

                imagemap:
                    auto "flowchart/image/%s.png"
                    for i in segments:
                        if i in nodes:
                            hotspot nodes[i][0] + gui.flow_hotspot_size:
                                action SetScreenVariable("select_node", i)
                                sensitive eval(nodes[i][3])

                if current_segment in nodes:
                    add "flowchart/image/crosshair.png" xpos nodes[current_segment][0][0] ypos nodes[current_segment][0][1]

            frame:
                style_prefix "flowchart_panel"
                xalign 0.5

                vbox:
                    spacing 12
                    if select_node and select_node in nodes:
                        text nodes[select_node][1] style "flowchart_panel_title"
                        text nodes[select_node][2]
                        if eval(nodes[select_node][3]):
                            textbutton _("跳转至此节点") action [SetVariable("segment", select_node), Start(select_node)]
                        else:
                            text _("该节点尚未实装。") style "flowchart_panel_note"
                    else:
                        text _("请选择上方的节点来查看详情。") style "flowchart_panel_note"


style flowchart_panel_frame is frame:
    padding (30, 30)

style flowchart_panel_title is gui_text:
    size 36
    color "#2d3a6d"

style flowchart_panel_note is gui_text:
    color "#5f6680"