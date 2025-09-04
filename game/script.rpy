# 游戏的脚本可置于此文件中。
# 先加一个开场logo
image splash = "splash.png"

label splashscreen:
    scene black
    with Pause(1)

    play sound "dinglingling.MP3"

    show splash with dissolve
    with Pause(2)

    scene black with dissolve
    with Pause(1)

    return

# 确保有默认值
default quick_menu = True

# 声明此游戏使用的角色。颜色参数可使角色姓名着色。

define yt = Character("佐佐木 阳太")
define akn = Character("风见 茜")
define skr = Character("藤原 樱")
define aoi = Character("小早川 葵")
define ao = Character("雾岛 蓝")

define n = nvl_narrator

# 游戏在此开始。
# 其他设定：立绘所谓的平常标签“normal”，应该是略带微笑的表情，但不及happy
# 同样sad重在眉尖向下，serious重在眉尖向上，none则是平的；部分表情有眼泪差分
# 如果立绘一点都找不着了，就把差分全删了

label start: # 调试的时候可以直接从指定章节开玩
    jump chapter_1

label chapter_1:
    stop music
    "【序章:沙化的毕业季】"

    play music "平静.mp3"

    scene bg sky with fade
    "樱花盛开的3月份。"
    scene bg library with dissolve
    "随风飘落的樱花通过窗户进到了图书馆内。"
    "我上前想要把窗户关上。"
    show akane normal with dissolve
    akn "『开着吧，反正之后也会清理的』"
    show akane normal2 with dissolve #闭眼
    "被不知道什么时候在我身后的图书管理员阻止了。"
    hide akane with dissolve
    "风见茜是同班的图书管理员。"
    "我对她并没有什么印象，好像只有我找书的时候才会出现。"
    yt "『好的』"
    "为了避免尴尬，我顺手摆了摆靠窗桌子的位置。"
    show cherry_flower at truecenter with dissolve
    "但在我没注意到的时候，飘落在桌子上的樱花像灭霸打了响指一样消散了。"
    hide cherry_flower with Dissolve(2.0)
    yt "『是我眼花了吗？』"

    show akane question with dissolve
    akn "『阳太同学，这个点你怎么还在图书馆？』"
    yt "『啊，我是学生会成员，过来帮忙整理图书馆的』"
    "此乃谎言。"
    "其实我是想掐着点在图书馆偶遇学生会会长————藤原樱"
    "以便增进一下感情，顺便在图书馆找些情感偏方什么的。"
    "但很明显，她今天应该是不会来了。"
    akn "『快毕业了，学生会的工作不是停了吗？』"
    yt "『嗯……』"
    yt "『我还需要找书，抱歉』"
    akn "『什么类型的？』"
    "说实话，我非常不好意思说出自己想找《这样做就能永远在一起~★》之类的书。"
    "不，是超级不好意思！"
    yt "『啊啊……不用麻烦你了，我自己找就可以了』"
    show akane none with dissolve #无表情
    akn "『我需要早点下班，所以你只要告诉我就可以了。{nw}" #语句中切换
    show akane interesting #饶有趣味
    akn "『我需要早点下班，所以你只要告诉我就可以了。{fast}还是说，你是在等谁吗？』"
    yt "『！！』"
    scene black with fade
    pause 1.0
    scene bg library with fade
    show akane normal2 with dissolve
    akn "『在你后面第二排的那列架子上』"
    yt "『谢谢……』"
    # hide akane with dissolve
    "我非常不好意思地从书架上取了一本《心动魔法》。"
    "我看着她帮我登记，羞愧的心理让我完全不敢抬起头来。"
    "登记完后她把《心动魔法》递给了我，同时在包里掏什么东西。应该是钥匙吧。"
    "我跟着她离开了图书馆。"
    scene bg corridor with dissolve
    show akane normal with dissolve
    "就在她锁完门后，她突然递给了我一本樱花色的笔记本。"
    "上面赫然写着“共感日记”四个大字。"
    akn "『比起你那本《心动魔法》，还是这个更有用，最起码这个是真的』"
    "“真的”？我接过《共感日记》看了一眼。"
    yt "『不用了还是还给你吧』"
    akn "『不，你拿着。这个对你有用，我试过了，放心』"
    hide akane with dissolve
    "她说完就离开了，只剩我和书看着窗外在樱花树下正在沙化的落花。"
    stop music
    # 依照篇幅，此处应有op
    jump chapter_2

label love_mogic:
    n """
    ____________________________________________________________________________{fast}{nw}

    {space=400}{size=*2}【心动魔法】{/size}{nw}

    {space=60}分别在三个纸条上写上在意之人会出现的地方{nw}

    {space=60}摆成三角阵，中间是在意之人喜欢的饮料

    {space=60}在饮料上放上在意之人的头发{nw}

    {space=60}头发指向哪第二天就能在哪遇到在意之人{nw}

    {space=60}且能搞好关系！{nw}

    ____________________________________________________________________________{fast}
    """
    yt "『这是什么小学生的迷信游戏，不相信』"
    nvl clear
    return

label diary:
    n """
    ____________________________________________________________________________{fast}{nw}
    
    {space=400}{size=*2}【共感日记】{/size}{nw}

    {space=60}『七日为期，寻一人共感，否则一切归零』{nw}

    （手写字迹：）{nw}
    
    {space=60}必须在剩下的七天内与一人完成【共感契约】

    {space=60}且一起记录下二人间的故事{nw}

    {space=60}才能够获得永远的记忆{nw}

    {space=60}然后能永远在一起{nw}

    ____________________________________________________________________________{fast}
    """
    yt "『虽然也不是很相信，但图书管理员的话确实让人在意』"
    nvl clear
    return

label chapter_2:
    $ f1=0
    play music "休息.mp3"
    scene bg home with fade
    menu:
        "看看《心动魔法》":
            $ f1=1
            call love_mogic
        "看看《共感日记》":
            call diary
        "玩游戏":
            "回到家还是打游戏要紧！"
            call play_pong
            jump chapter_2
    
    if f1:
        menu:
            "再看看《共感日记》":
                call diary

    else:
        menu:
            "再看看《心动魔法》":
                call love_mogic

    "先塞书包里面明天还给图书管理员吧。"
    stop music
    scene black with Dissolve(2.5)
    "day 2"

    scene bg school with fade
    play music "阳光.mp3"
    # 环境描写，樱花的景象与自己对校园的不舍
    "三月的阳光无比温和。"
    "校园里到处都是樱花，风一吹就漫天飞舞。"
    "一想到马上就要毕业了，我的心里也有些许对校园和同学的不舍。"
    "顺带一提，由于马上就要毕业了，这周并不上课。"
    "但还是有一部分同学留在学校里忙着社团的事，以及听老师讲过无数遍的的安全教育。"
    scene bg school2 with dissolve # 既然这样，背景学校2的就默认是在图书馆前拍摄的广角相片
    "我来到图书馆门口，发现门还没有开。"
    "男の声" "『你书包不放在教室吗？』"
    "学生会的同僚吗。他看起来也是来还书的。"
    yt "『这个嘛，我着急还书就先过来了，没想到门还没开』"
    "同僚" "『书不重吧，等会到学生会肯定又是给其他社团打杂去了』"
    yt "『是啊……其实还好吧……』"
    "如果不是为了和会长相处，谁又乐意待在学生会里打杂呢。"

    scene bg student_council with fade
    stop music
    "我们来到了学生会办公室门口。"
    play music "平静.mp3"
    "我推开门，与平时拥挤的场景不同，办公室里一片寂静。"
    show sakura serious at top with dissolve
    "只有会长一个人坐在办公桌前，埋头在资料上写写画画，听得见笔尖划过纸张的细微声响。"
    "同僚" "『我们这么早的？』"
    skr "『嗯？你们来晚了』"
    "同僚" "『没有吧，我就刚刚去图书馆还书，发现还没开门就回来了』"
    skr "『所以才晚了啊』"
    "会长对着桌前的一沓资料抬了抬眼睛。"
    skr "『这是你要干的活，园艺社的，最上面那张是我打印出来的工作细则』"
    "同僚" "『好~知道了~~会长大人~~~』"

    scene bg student_council with fade
    show sakura normal at top with dissolve
    "同僚走了之后，办公室内就只剩下我和会长两个人。"
    "或许是樱花的原因，窗外的风景让会长显得比平常更加神圣。"
    skr "『你怎么还背着包？』"
    yt "『！！哦！哦哦！！好，我我刚刚也是去图书馆忘了！』"
    skr "『你把包拿过来』"
    skr "『你负责田径部的，资料还挺多，拿包来装刚刚好』"
    "我听话地上前把包放在桌上，一只手帮忙扶着书包。"
    skr "『？里面还有书，先拿出来再塞资料吧。诶我刚打印的清单呢』"
    yt "『哦哦好的！！』"
    "等等好个鬼啊！我慌忙地把包拉开，想要赶紧把书拿出来。"
    "可能是方便吧，她先我一步伸手将里面的两本书拿……不对？怎么就一本？还忘了一本在家？"
    "在我慌忙回忆是哪一本时，书在会长的手中微微发光。封面似乎浮现出一行字：“味觉：未同步”。"
    "？？？"
    "是《共感日记》？？？来真的？？"
    "那一缕光也被会长察觉到了，她看了看书封面上的内容。"
    show sakura serious with dissolve
    skr "『味觉？』"
    "她皱了皱眉头。"
    skr "『什么东西？』"
    yt "『哦抱歉是我要还的书我先拿着吧不麻烦您了——』"
    "会长的神色有些奇怪，但手上的工作还没有停。"
    "让我把资料装好后，递给了我一张打印好的工作清单就让我离开了。"

    menu:
        "看一眼工作清单":
                n """
                ____________________________________________________________________________{fast}{nw}

                {space=400}{size=*2}【工作清单】{/size}{nw}

                {space=60}1.将更改学籍的学生资料档案交接给体育部老师{nw}

                {space=60}2.找体育部老师签名确定运动员保送名单{nw}

                {space=60}3.将田径场假期建设资料给到体育老师，保证假期田径部的正常练习

                {space=60}4.清点田径部器材，上报损坏明细{nw}

                {space=60}5.随便清理一下田径部办公室谢谢{nw}

                ____________________________________________________________________________{fast}
                """
                yt "『……』"
                nvl clear
            
        "工作什么的，还是敬谢不敏了……":
            pass

    "关上门，隐隐约约听见会长在自言自语。"
    show sakura none with dissolve
    skr "『味觉吗，我的……』"

    scene bg field with fade
    play music "风.mp3" fadeout 1.0 fadein 1.0 #要是没有这个BGM，用阳光.mp3也行，但情绪并非那么高昂
    "我来到了田径场，将书包里的资料给到了体育部办公室的老师。"
    "那本《共感日记》就先拿在了手上。"
    "跟老师确定明细时我听见了田径场的跑步声。"

    show aoi happy with dissolve
    "是那个在体育和文化间摇摆不定的小早川葵同学！"
    "之前每次到田径场干活的时候，她都会莫名其妙上来对我冷嘲热讽。"
    "虽然会过来帮忙，但还是很不爽啊怒怒怒（"
    "话说这还是第一次看见她训练诶？"
    hide aoi with dissolve
    "……"
    "在我走神的同时，体育部老师探出头来朝葵喊道。"
    "体育部老师A" "『小早川！过来！』"
    aoi "『好！』"

    transform move_in_left:
        xalign 0.0    # 起点在最左边
        alpha 0.0     # 从透明开始
        linear 1.0 xalign 0.5 alpha 1.0  # 一秒钟内移到中间并渐显

    # 展示角色并播放移动动画
    scene bg field with fade
    show aoi none at move_in_left
    "看到还有我在体育部办公室，葵这家伙先是不解，随后便装着没看见我走到了老师旁边。"
    stop music
    "体育部老师A" "『呐，你的资料，现在该确定了吧』"
    aoi "『……』"
    "体育部老师A" "『你已经拖了很久了。现在你两方面都考完试了总该确定下来了吧』"
    "嗯？什么事？她要改学籍？"
    aoi "『老师……我还需要想一想……』"
    "体育部老师A" "『你还有多久时间？剩六七天了，现在人家都过来了，你为难我也别为难他啊』"
    show aoi serious with Dissolve(0.2)
    aoi "『……！』"
    "小早川葵突然朝我瞪了一眼，但她的事好像依旧没有确定。"
    show aoi none with dissolve
    yt "『啊，老师，这。这个也还不是很急，因为我后面几天也会来。老师先签名一下这个吧』"
    "我帮忙着打圆场，老师也把态度放了放，顺着拿了我手上的名单。"
    "体育部老师A" "『……』"
    "体育部老师A" "『再给你两天，后天我就确定了，就不管你了，你自己看着办』"
    show aoi none2 with dissolve #最理想的：2都代表闭眼差分
    aoi "『……嗯』"
    show aoi none with dissolve
    "看样子暂时是没问题了，我将剩下的资料堆好在老师桌上。"
    yt "『那老师我就先去清点一下器材室的器材咯』"
    "体育部老师A" "『小早川去搭把手』"
    show aoi none with dissolve
    aoi "『。好』"

    scene bg lab2 with fade
    show aoi serious at top with dissolve
    "刚进器材室，葵就伸手把我手上的笔记本连同清单一起抽走。"
    show aoi angry with Dissolve(0.2)
    aoi "『你就是过来找我麻烦的吗？』"
    show aoi surprise with dissolve
    "还没等我回答，笔记本不出意外也发出了光，并且在封闭的器材室更加明显。{nw}"
    play music "神秘.mp3" #用作压抑、微恐、神迹的音乐
    "还没等我回答，笔记本不出意外也发出了光，并且在封闭的器材室更加明显。{fast}"
    show aoi serious with dissolve
    aoi "『这是什么啊？』"
    "她刚翻看着几页，手却突然像被电击般抽走，书掉落在地上。"
    yt "『嗨！干嘛？』"
    show aoi suffering with dissolve
    "她用手捂着肩胛骨的位置，延续了在老师那时的沉默。"
    aoi "『嘶。随便你，你自己干吧软脚虾』"

    # 向右退场
    transform move_out_right:
        xalign 0.5 #从中间
        linear 1.0 xalign 1.2 alpha 0.0  #移动到右侧

    show aoi serious with dissolve
    show aoi serious at move_out_right
    with AlphaDissolve(move_out_right, delay=1.0, reverse=True) #向右渐隐移动
    
    "说着就跑出去了，剩下我捡起地上的书。"
    "离谱的是清单也不知道去哪了，我却要一个人负责清点项目。"
    
    scene bg classroom with fade
    play music "风.mp3" fadeout 1.0 fadein 1.0
    "上午一个人清点了器材室的所有器材，期间还帮老师顺手建了个表格。"
    "工作量之大让我不得不牺牲掉午餐时间，虽然还是没清点完。"
    "体育部老师A让我明天继续。"
    "我打开饭盒，准备在教室里享受午餐。"
    "这时却有人叫我。"
    "classmate" "『阳太，你今天上午没去天文社啊』"
    yt "『额……嗯，我没去，我去学生会了』"
    "classmate" "『上午天文社的同学让我叫你一回来就去天文社，说事挺急的』"
    yt "『啊——别吧——』"
    "我关上还没吃几口的饭盒，书包还没放下来就又走了。"
    yt "（本来还想着去图书馆呢……）"

    scene bg bad_room with fade
    play music "平静.mp3" fadeout 1.0 fadein 1.0
    yt "『你好，有人吗？』"
    "我敲了敲一如既往阴森的社团活动室。"
    "由于天文社主要是室外观测，再加上天台有人失足掉下去后就被封住了。"
    "学校只能安排天文社在最高楼层的教室，之前还是杂物室来着。"
    "室外观测也只是去学校现在楼花漫天的小树林里面的小土包上面。"
    "反正就是天文社活动室阴森森的。每次我来都是要人打扫卫生打杂之类。"
    yt "（那看样子是没人了）"
    "？？？" "『喀哒，喀哒……』"
    yt "『我靠什么鬼！！』"
    "我吼道，每次都有这种奇奇怪怪的声音出现。"
    "？？？" "『……喀哒，喀哒……』"
    "貌似是按动笔的声音？从那群纸箱子里传来的……"
    yt "『说话，喂！』"
    "？？？" "『……』"
    "我将书包脱下，往纸箱子那里砸过去。"
    show ao normal #可以立绘下移
    "稀稀拉拉掉下来的纸箱下，露出来的是竟然是雾岛蓝同学的头。"
    yt "『……你是笨蛋吗』"
    yt "『雾岛蓝同学』"
    show ao normal with dissolve #移动到原位
    ao "『怎么了，不尖叫了？还吓的你要扔书包』"
    "雾岛蓝是天文部的幽灵社员，说话声音很小。我虽然很无语，但也还是压低了声音。"
    yt "『算了。社长有什么事？』"
    "雾岛蓝拿起了从我书包里掉出来的《共感日记》。我来的很急，所以书包拉链还没关。"
    ao "『果然……』"
    yt "『什么？』"
    "本子又在雾岛蓝的接触下发光了，上面又浮现出其他的字样。"
    "我下意识地想上去把本子拿回来却扑了个空。"
    ao "『社长叫你打扫教室，然后拿块干净干燥的布把天文望远镜盖上』"
    yt "『那你现在能把本子还给我了吗？』"
    ao "『你还要把这些箱子给整理回来，等你干完了我再还你』"
    "雾岛蓝用按动笔指着我，要不是环境很安静我都不一定听得见她很小的声音。"
    
    scene bg bad_room with fade
    play music "平静.mp3" fadeout 1.0 fadein 1.0
    show ao none with dissolve
    "可能是我干活的同时一直在盯着雾岛蓝同学，又或许是那本子里除了第一页其他都是空白页没什么可看的。"
    "雾岛蓝在我干活中途就把本子塞给我让我出去了。"
    ao "『社长说这些是你这几天的工作。我要记录星空的声音。你先走吧』"
    "很莫名其妙的一个人，但看样子，她应该知道一些关于本子的事。"
    hide ao with dissolve
    "正想着，我已经被赶出天文教室了，还有书包。"
    "然后就是她按动笔的声音『喀哒，喀哒……』"
    "那是录音笔还是在接收电波啊，声音还比一开始大声了些。"
    
    scene bg school2 with fade
    "在天文数室待的也快放学了。"
    "我跑去图书馆，发现图书馆也关门了。"
    "我找不到图书管理员，只得先回家。"
    scene bg street with dissolve
    "路上经过了校门附近开的甜品店，看见里面开开心心的jk。"
    yt "（下次，可以的话，试着约会长出来吧。）"
    
    scene bg home with fade
    stop music
    n """
    ____________________________________________________________________________{fast}{nw}
    
    {space=400}{size=*2}【共感日记】{/size}{nw}

    {space=60}“味觉 未同步”：故事A1{nw}
    
    {space=60}“触觉 未同步”：故事B1{nw}

    {space=60}“听觉 微弱同步”：故事C1{nw}

    ____________________________________________________________________________{fast}
    """
    yt "『不仅封面更新了，内页也更新了啊……』"
    nvl clear
    scene black with Dissolve(2.5)

    jump chapter_3

label chapter_3:
    stop music
    "day 3"
    scene bg sky with fade
    play music "阳光.mp3"
    "终于记得带上那本《心动魔法》，我走在去教室的路上。"
    scene bg school2 with dissolve
    "顺路也去了趟图书馆，不过图书馆还是没开门，又吃了一次闭门羹。"
    yt "『又来早了？』"
    akn "『没有啊』"
    yt "『！？』"
    show akane normal with dissolve
    "熟悉的声音又从我身后传出来。"
    "转过头那个图书管理员已经自顾自地从我书包里拿出了一本书。"
    yt "『不要突然出现在别人身后啊』"
    akn "『怎么样你试过了吗，这本？』"
    yt "『啊，试过啦，除了会突然像个手电筒一样发光也没什么』"
    akn "『啊不是，我说的是这个“翻开了的”心动魔法』"
    yt "『………………』"

    play music "平静.mp3"
    scene bg library with fade
    "大概讲了一下共感日记旁发生的种种奇怪的事情。"
    show akane happy2 with dissolve
    akn "『哈哈，看来你就是那个命定之人啊哈哈』"
    yt "『所以到底是怎么回事？』"
    show akane happy with dissolve
    akn "『反正是对你有用的，你就先拿着那本书呗』"
    yt "『你倒是听人说话啊……』"
    "说着我从包里掏出了共感日记。"
    "封面上有着三行让人格外醒目的标识。"
    akn "『三个啊……这样，我们先交换line，之后你跟她们聊完再找我怎么样？』"
    yt "『你先回答我问题……』"
    show akane normal with dissolve
    akn "『行』"
    "她一反刚刚不靠谱的样子，变作严肃地把我拉到隔壁自习室。"

    play music "神秘.mp3" fadeout 1.0 fadein 1.0
    scene bg classroom with dissolve
    show akane serious with dissolve
    akn "『你有注意到在你身边落下的花瓣吗？』"
    yt "『花瓣？』"
    show cherry_flower at truecenter with dissolve
    yt "『这个怎么了吗？』"
    akn "『你看』"
    hide cherry_flower with Dissolve(2.0)
    "说着，花瓣就像灭霸打了响指一样散去了。"
    yt "『！』"
    akn "『一开始，也只是这些不起眼的小物件』"
    yt "『！昨天在地上消失的清单』"
    akn "『其他的我也不是很了解，不过我觉得是这本本子在发挥作用』"
    
    "陆陆续续有人来到自习室里嘟嘟囔囔了几声。"
    "风见茜看到后，便把我赶了出去。"
    akn "『总之，你只需要完成上面的任务就可以了，我会帮助你的』"

    scene bg student_council with fade
    play music "平静.mp3"
    "本想叫昨天的同僚一起去来学生会办公室。发现人不在了，就直接来了。"
    "而到了学生会办公室，则比昨天更加地寂静，甚至会长都不在。"
    yt "『……』"
    stop music
    yt "（难道人也会像花瓣一样消失……！）"
    "想到这里我不由得紧张起来。"
    "我疯狂地在办公室内查看，试图找寻一些蛛丝马迹。"
    yt "『不会吧……不会吧……』"

    "女の声" "『你东西忘在哪里了？』『不知道啊我去办公室找找』"
    "办公室外传来女生的声音。"
    show sakura dressed normal with dissolve
    "『砰』的一声门开了，是穿着烹饪围裙的会长藤原樱。"
    play music "阳光.mp3"
    skr "『啊，阳太你在办公室啊，你有没有看见我的挂包』"
    yt "『啊！……哦哦，是这个吗』"
    "我心里大舒一口气，提起了窗边的一个白色包包，上面已经有几片樱花花瓣了。"
    skr "『对没错』"
    "她接过包包。"
    skr "『里面装着我的药』"
    yt "『你身体不舒服吗会长？』"
    skr "『没事……谢谢你，那我先走了』"
    yt "『你要去哪？』"
    show sakura dressed none with dissolve
    "莫名担心使我急忙上去抓住了樱。"
    "刹那间的理性思考又让我只拉住她的围裙边。"
    skr "『……』"
    yt "『抱歉拉住了你！对不起……』"
    "我松开了手，为我不礼貌的行为道歉。"
    "藤原樱看着我的表情低头思考了一会。"
    "再抬起头时，便是和我对上了眼睛。"
    show sakura dressed normal with dissolve
    skr "『那你也一起来吧』"

    scene bg cooking_classroom with fade #资产建议：把bg classroom传给AI让它在桌子上添加一些厨具得到。
    play music "平静.mp3" fadeout 1.0 fadein 1.0
    "藤原樱和我一起来到了烹饪课的教室。"
    "我放好书包，接过烹饪围裙，戴上了一次性手套和口罩在藤原樱旁边帮忙打下手。"
    show sakura dressed normal with dissolve
    skr "『你昨天的工作搞完了吗』"
    yt "『哦，还、还差一点，当时太多了整理到饭点也没整理完，老师就让我这几天继续』"
    skr "『工作量这么多啊，需不需要我来帮忙』"
    yt "『不用了不用了，我可以的！相信我』"
    "说实话我有一点想，但是器材室我还没打扫，灰尘比较多还是不要让会长来了。"
    "而听到了我的回答，会长眼睛好像亮了一点，转过头继续切面团，像笑了一下说道。"
    skr "『这样啊，这么厉害』"

    scene bg cooking_classroom with fade
    "我在帮忙打发奶油。"
    "到了如今这么自动化的社会还手动打奶油吗……感觉很快就会累了。"
    show sakura dressed normal with dissolve
    "藤原樱在分面团，好像是要做小蛋糕。"
    yt "『好香的味道。已经有人烤好面包了吗？』"
    skr "『是吗？』"
    "樱环顾了一下四周。"
    skr "『看样子是的』"
    yt "『会长你喜欢烹饪啊，我都不知道学校里还有烹饪教室来着哈哈』"
    skr "『嗯，确实比较偏来着』"
    yt "『那个，如果你喜欢的话……』{nw=0.5}" #打断说话效果
    skr "『不过我鼻子可能闻不清什么味道，所以我更习惯和别人一起烹饪』"
    "她抬头看向我。"
    show sakura dressed happy2 with dissolve
    skr "『而且我也喜欢和别人一起聊天』"
    yt "『！啊，哦！！好的！！！』"
    show sakura dressed happy with dissolve
    "我开心到飞起。"
    yt "『我我去装点水，你渴了吧！』"
    "我慌忙地转过头去找饮水机的位置。"
    skr "『嗯谢谢你』"
    "她轻笑着说。"
    "水拿回来了，但我太过激动，以至于不小心碰到了她的手——"
    "我猛地收回来，差点把水打翻。"
    "但同时一阵疲惫的感觉清晰地传入脑内。"
    "看着藤原樱的笑容，我的注意力却放在了她眼睛下的一点淤青上。"
    yt "『藤原樱同学。』"
    show sakura dressed question with dissolve
    skr "『嗯？』"
    yt "『你最近很累吗？』"
    skr "『为什么突然这么说？』"
    "果然刚刚那个就是“共感”吗。"
    "我这么笃定，是因为我这几天完全没有熬夜。"
    yt "『这里，有些淤青了』"
    show sakura dressed none with dissolve
    "我指了指她眼睛底下。"
    "现在看，她还是拿化妆品铺了一层粉来盖住的。"
    yt "『熬夜了吗？那对皮肤会很不好的』"
    show sakura dressed none2 with dissolve
    skr "『哦哦，是最近有些事……』"
    show sakura dressed none with dissolve
    "一段时间的沉默————"
    yt "『那个……校门口有家甜品店，还挺香的。放学后有空的话不如我们一起去吧』"
    yt "『吃点甜的也对心情好，怎么样？』"
    "可能是太突然了，她一时没反应过来。"
    "但她却很快给了一个令我惊讶的答复。"
    show sakura dressed happy2 with dissolve
    skr "『为什么不呢，我们今天下午放学后一起去吧！』"
    show sakura dressed happy with dissolve
    yt "『！！』"
    "这让本来已经想好反悔的话的我惊喜万分。"
    "仿佛这一天比过去的每一天都明亮。"
    "犯花痴的我刚开始不知所措就被会长提醒该去田径部了。"
    skr "『下午我带小蛋糕去找你』"
    scene bg sky with fade
    "我在一路上走路都轻飘飘的。"
    scene bg field with dissolve
    "到了体育部办公室的时候发现其他老师都在，但昨天帮忙的体育老师不见了。"
    yt "（应该是去器材室了吧，会不会来得有点晚了）"
    play sound "knocking.mp3"
    "『砰砰砰……』"
    "器材室的门被锁上了。"
    yt "（……？回去找一下老师吧）"
    "刚一转身，另一个体育老师B就来到了我身后。"
    "体育老师B" "『哦，你是学生会的吧』"
    yt "『是的老师，器材室的门怎么锁了？』"
    "体育老师B" "『你是要登记器材的是吧，昨天跟老师A的？』"
    "体育老师B" "『他昨天下午说清点了大半的名单不见了，以为是弄丢了就和我们又去清点了一遍』"
    "体育老师B" "『名单刚刚在电脑上打印出来了，你来办公室拿就行了』"
    yt "『好的，谢谢老师』"
    "透过器材室的门，我隐隐约约听见了什么声音。"
    stop music
    "『……？』"
    "不过看见老师还想说什么，我又跟上了老师的步伐。"
    "体育老师B" "『呐，还有这些是签名了的也拿去吧。还好昨天他把文档传了一份到我电脑上，不然他今天没来我都打不开他电脑，哈哈……』"
    "体育老师B" "『我记得这里还有一份档案是他还没改的，你下午再过来看看他来没来吧』"
    yt "『……好的，谢谢老师』"
    "比起昨天那一书包的资料，这薄薄的几张可要简单多了。"
    "经过田径场，我又看到了那一群集训的体育生们在跑道上挥洒汗水，大约有20来个。"
    yt "（小早川葵那家伙也是体育生吧，也没看见过她跑几次步啊）"
    "思考间，手机响了一声。是风见茜发来的。"
    "没有任何前缀或多余的话语——"
    "『去器材室』"
    "『快』{nw}"
    play music "神秘.mp3"
    "『快』{fast}"
    yt "（她怎么知道我在田径部？我刚刚去到过器材室，器材室是锁着的啊？）"
    yt "（什么情况？）"
    "不知为何，我开始有些紧张，身上的汗毛都立起来了，像是要有不好的事情发生。"
    "我卷起被汗水打湿的资料就往回跑。"
    "到了门口，我用力地摇着器材室的铁门，发出的巨大声响把老师都引了过来。"
    "体育老师B" "『怎么啦怎么啦？你忘东西了吗？』"
    yt "『老师你有钥匙吗！能开下门吗！』"    
    "体育老师B" "『到底怎么了？』"
    "疑惑的老师开始找钥匙。"
    "也许是我制造的声响太大声，不等我解释，一阵细微的女声就从器材室里传出来。"    
    "微弱の声" "『有人吗……救命……』"
    "佐佐木 阳太&体育老师B" "『有人在里面！！』"
    scene black with Dissolve(0.5)
    scene bg lab with Dissolve(2.0)
    "终于打开了门，室外的光亮与室内形成鲜明的对比。"
    show aoi sad2 with dissolve
    "进来的光线照在了趴在地上的小早川葵，旁边是堆起来的纸箱子，上面是窗户。"
    yt "『快！医务室！』"
    "我顾不上老师，上前要去把葵抱起来。"
    "霎时，传递过来的疼痛让我脱力也跪倒在了地上。"
    "肩膀，膝盖，小腿……一阵阵的疼痛让我切实感受到了共感的强烈。"
    "我和小早川葵互相支撑着对方，她看上去很虚弱，一只手还一直摁着肩膀。"
    yt "（我要不行了……）"
    stop music fadeout 1.0
    play sound "扑通倒地音效.mp3"
    scene black with fade
    pause 2.0
    "……"
    "…………"
    "………………"
    scene bg health_room with Dissolve(2.5)
    pause 2.0
    "在老师的帮助下，我们两个都到了保健室。"
    "体育老师B把办公室里面的其他老师叫来了，把我们两个直接公主抱了过去。"
    "抱小早川葵是因为她很虚弱，而我是因为受了共感的影响平地摔了一下。"    
    "我浑身脱力，在被老师带去保健室时就晕了过去。"
    scene black with fade
    "迷糊间隐隐约约听见了葵的声音。"
    "…………"
    "………………"
    scene bg health_room with Dissolve(2.5)
    "再次醒来是因为又一阵的痛觉传递，小早川葵在擦风油精。"
    "看到我醒了，旁边床的葵出声把保健室老师叫了过来。"
    play music "休息.mp3"
    "保健室老师" "『你是因为没吃饭加上运动的低血糖晕倒了是吗』"
    "保健室老师" "『来一杯葡萄糖休息一下应该就能走了，等会记得去吃饭，知道了吗？』"
    yt "『知道了，谢谢老师』"
    "随着保健室老师出门吃饭的关门声响起，我还没开口小早川葵就把糖水递到了我手边。"
    show aoi sad with dissolve
    aoi "『……喝点水吧』"
    "我接过水喝了一口。"
    yt "『谢谢，不过你是怎么困在里面的？』"
    "我故意学着她平时的语气，尝试让气氛变得不要那么严肃。"
    aoi "『……』"
    aoi "『……呜呜』"
    show aoi crying with dissolve
    aoi "『那你是为什么找到我的啊……你不是已经走了吗……』"
    "卧槽她哭了！她不好意思地把头扭了过去，细微的抽泣声在保健室里格外清晰。"
    yt "『！你怎么了？啊那个，，你肩膀膝盖还疼是吗？』"
    "听到肩膀二字，她身体抖了一下，抽了张纸巾擦了擦又转过来和我说话。"
    aoi "『……我不是困在里面，我是说我带了钥匙，但是钥匙就在我手里不见了』"
    "……"
    show aoi serious tears with dissolve
    aoi "『我是说真的！器材室门给风吹上了，我要打开门刚拿出钥匙它就不见了……』{nw=0.5}"
    show aoi suffering
    aoi "『嘶——』"
    yt "『扯到伤口了吗？！』"
    "我一个鲤鱼打挺起来，但小早川葵倒是抓住了我的手。"
    show aoi serious with dissolve
    aoi "『你是怎么知道我肩膀上有伤的』"
    yt "『这里有药需要我帮你上药吗……因为你之前一直捂着你的肩膀』"
    show aoi sad with dissolve
    aoi "『嗯…………不了谢谢……』"
    "她低下头，平常梳起的头发顺着头的低下而散下来，遮住了她的半张脸让我看不见她的表情。"
    "她开始慢慢诉说，一滴滴的眼泪掺杂着她的话语落下。"
    aoi "『肩膀上是考试前一个月跑步时摔的，倒地时肩胛骨肌肉拉伤了』"
    aoi "『还有半月板磨损，虽然所幸现在恢复得差不多』"
    aoi "『当时感觉这辈子完了，我都不敢想家里人会对我有多失望……』"
    aoi "『甚至我都有些自暴自弃开始学起了文化课，哈哈……』"
    aoi "『体育考试那天身体还在恢复阶段，当然也跑了个还好的成绩但当时我不知道。就想着给自己一个退路把文化考试也考了，结果成绩还比体育的更加好，搞的我都动摇了哈哈……』"
    show aoi crying with dissolve
    "说着她又哭了起来。"
    yt "『纸巾纸巾。呐擦擦……』"
    show aoi sad tears with dissolve
    aoi "『……按体育成绩去高中的话还要更努力才能到父母要求的学校，但我已经无法恢复到原来的水平了』"
    aoi "『按文化考试的话能去那所学校，但我就不能继续体育集训了……这也不是我想要的……所以一直到现在我都不知道要怎么弄资料……』"
    yt "『噢…………』"
    aoi "『然后昨天还往你身上撒脾气了我真是神经病，对不起……果然我这种人就不配有什么好未来，什么事在我身上都会被搞砸。』"
    aoi "『连钥匙在我手上都能被搞丢……还觉得是钥匙像被沙化了一样真是笑死人了…………』"
    yt "『不，别这样……需要我帮忙吗？可以的话』"
    yt "（……我要告诉她关于物品消失的事吗？但我也不清楚啊。她现在看上去情况很不好）"
    yt "（而且风见茜是怎么知道她在器材室的？）"
    yt "（现在告诉她的话她可能还不能消化接受，可能还会让她的情况更糟，我要怎么办？）"
    yt "（告诉她让她注意吗？但这个消失是不可预防且不可逆的）"
    "我头脑风暴了一阵最后也只能叹了口气，安慰她道。"
    show aoi sad
    yt "『不要这么说自己，你能同时兼顾两边考试已经很不错了，你不需要自责，因为做一个选择而去否定掉自己的一切。』"
    yt "『如果可以的话你可以试着说说找找自己真正想要的是什么。』"
    yt "『刚刚你释放了情绪也是很正常的现象，不用着急给自己上价值没事的。我可以暂时听你说话。』"
    yt "（还是话疗管用点……）"
    "我这么想着，手上也没停地给小早川葵递纸巾。"
    "小早川葵看上去也不再哭泣了，静静地坐在那里思考我所说的话。"
    "她把手放在了她的受伤的肩颈部位，就像是习惯性的防御性肢体动作。"
    "按压时的阵痛也通过“共感”传递到我的身上。"
    show aoi none with dissolve
    aoi "『我想吃甜品了。』"
    yt "『什么？』"
    aoi "『快放学了我们一起去吃甜品好吗，就在校门口。』"
    "她的眼圈泛着刚哭完的红晕，声音装着无事发生但也比平时要更加颤抖。"
    yt "（可是我约了藤原樱啊！）"
    "这样的话语出现在我的脑海里。"
    "但她看上去就好像她只有我一个人一样，让我很难拒绝。"
    show aoi sad with dissolve
    yt "『……抱歉我已经约了同学了。』"
    "我不好意思地回复她，在她失落之际补充到又补充道。"
    show aoi none with dissolve
    yt "『……那要一起去吗？』"
    show aoi surprise with Dissolve(0.2)
    aoi "『！』"
    show aoi happy2 with dissolve
    aoi "『好！』"
    # 今日改写工作至此，明天有脑子再继续。25.8.9-4:09
    "青春期jk喜极而泣的笑容和话语交错着回应我。"
    scene black with Dissolve(2.5)
    "———"
    "后续剧情暂未进行修缮并制作演出，敬请期待~"


    "下午的下课铃响起。"
    "走廊是熙熙攘攘的人群嘈杂(培养学生情的班级活动)。"
    "聊天间，我们也差不多休息好了。"
    aoi "『你下午还要去干学生会的活吗?』"
    yt "『哦我还有资料在书包里，都给我捏皱了还。』"
    aoi "『。嗯。。。好，那就先再见啦，我就在B班!』"
    yt "『我去找你吧，放学见。』"
    aoi "『放学见!』"
    yt "(emmmm要跟藤原 楼讲一下临时加人的事情啊。。。)"
    yt "(小葵那个可怜的样子会长应该会比我更加心疼吧。。唉--我和会长的约会啊。)"
    yt "(不过!一开始就只有两个人去的话会给会长造成困扰吧!那还是三个人一起去吧!)"
    "想着，我上楼走向了天文社活动室，完全忘记了上课铃的响起。"
    "开门声————"
    yt "(没人吗?)"
    "空荡的教室里，天文望远镜和观测仪整齐摆放在一起。"
    "最近的桌子上放了张纸条，用录音条带压住了。"
    "纸条内容：我看你下午没来就写张纸条放桌上了，今天的天文社活动改到今天晚上八点，在学校的旧校舍里面的土堆上面。已经跟老师申请通过了。活动内容是记录天文现象，顺便和摄影社的各位一起录制视频，佐佐木阳太你负责搬运需要的器材雾岛蓝 留"
    yt "『晚上?!为什么!那不是明天又要找时间打扫一遍?唉————』"
    "一个熟悉的女声又从我身后传来，是零岛蓝。"
    ao "『大叫什么啊?』"
    "我被吓到了。"
    ao "『喂喂，不要每次都被吓得这么狼狈啊。。。』"
    yt "『无路赛， 你们就不能不要一声不吭地出现在别人的身后吗?』"
    ao "『你们?』"
    "雾岛蓝疑惑地看着我。"
    "此时窗外的活动声打断了我们的对视。"
    ao "『你怎么也没去底下参加班级活动啊?』"
    yt "『有班级活动吗?我不知道，我经过图书馆就直接上来了。』"
    yt "『?什么叫'也’?』"
    ao "『这个班级活动完了就直接放学了，比平时要早半个小时。我们班刚好有个女生身体不好，我借着照顾她的名义就跑出来了。』"
    yt "(那意思就是说我要先去找 藤原 樱，看她什么时候能结束活动?)"
    ao "『你最近经常去图书馆吗?又怕鬼了?』"
    yt "『还不是你吓的。。』"
    yt "(没错我直到加入天文社之前都是坚强的唯物主义者。)"
    yt "(初一时听到学校地下室也只觉得是老鼠的声音。)"
    yt "(到初二才加入天文社，他们欢迎新人的仪式是鬼怪主题的吓人。)"
    yt "(这使得我直到初三都对着鬼怪故事深信不疑，经常出入于图书馆寻找偏方。)"
    yt "(之前认识 雾岛蓝同学的时候还专门问了关于鬼怪的故事。)"
    yt "(果然是那时太坦白了 搞得她现在都能随意抓住我这点来嘲弄了是吗？)"
    yt "『所以说为什么又要晚上去啊，晚上回家也很危险的，连末班车都不一定赶得到。』"
    ao "『你怎么又和之前一样啊，你没来的时候还是我们几个跟学生会会长沟通的呢。』"
    yt "『会长过来说的?』"
    ao "『是啊，她比我们还急呢。』"
    yt "(会长有因为而着急吗?!好开心好开心好开心!!!)"
    "雾岛蓝看着我窃喜时花痴股的神态转身时透过了一丝的鄙夷。"
    ao "『你不会是yong。。。算了。』"
    yt "『什么？』"
    ao "『没什么，这个桌子，和这个，这些。』"
    "她指着这些稀稀拉拉的设备对着我说。"
    ao "『你先把这些搬去一楼的空教室，钥匙我一把他们俩一把。走吧。』"
    yt "『这么多？』"
    ao "『我和他们俩下午已经把该搬的搬完了，快点。。。』"
    yt "『嘿！』"
    yt "(累死了，终于搬完了。)"
    "本该是清爽的三月份现如今我却因为搬东西跑上跑下跑的大汗淋漓的。"
    yt "(对了!还要和她说一声!)"
    "不耐烦的声音油然而生。"
    yt "『可以了吧就这些了，今天晚上八点钟我会来的。』"
    yt "(我是不是该换身衣服?)"
    ao "『不要说的我好像是故意虐待你一样，我也有搬好吗。』"
    "没想着和雾岛蓝继续拌嘴，藤原 楼就从楼梯口下来了。"
    yt "(手中的包比上午要鼓了一倍，是装了资料回去吗?真是辛苦呢?)"
    yt "『藤原 樱同学，你怎么在这?』"
    skr "『啊，刚刚下楼的时候看到你们在搬东西了，想着和你们打个招呼。』"
    yt "『哦哦!!抱歉我身上有些臭，能不能麻烦你等我一下我去换身衣服?』"
    yt "(尴尬的笑容，啊啊啊，还想着给出自己较好的一面呢ww。。。)"
    skr "『可以呀!』"
    yt "『哦哦，对了!抱歉能临时加一个人吗?』"
    "藤原 樱愣住了。。。"
    skr "『可以呀！』"
    skr "『是雾岛蓝同学吗?我下午也见过她的。』"
    ao "『o!有我的份吗!我去我去!』"
    "我此时语气强硬地有些没有礼貌"
    yt "『不是！』"
    yt "『等会我不是这个意思!语无伦次*。。是B班的小早川葵同学。』"
    ao "『o我们班的!』"
    skr "『她班的?』"
    ao "『那我还能去吗?』"
    skr "『那还要邀请她去吗?』"
    ao "『一起吧！』"
    skr "『一起吧！』"
    "两个人爱逗人的部分都展现的淋漓尽致，像是已经聊好了的。"
    "看他们俩个人一唱一和的样子我也只能放弃解释，无力的垂下头同意。"
    yt "(上楼换衣服，顺路给小早川葵同学说一声吧。)"
    yt "(现在还没放学吧!)"
    "换完衣服后我才去到B班找小早川葵同学。"
    "然后两个人下去找另外两个人会合一起去门口的甜品店了。"
    "路上，三个女生互相聊天。"
    "先是谈论今天下午的班级活动。"
    "再是聊到自己怎么想到要来甜品店。"
    ao "『你邀请哒。』"
    skr "『诶呀，还不是上午和阳太一起在烹饪教室时他先说的。』"
    yt "『昨天放学时路过看到了嘛。』"
    yt "『上面还出了樱花味的新品，好像只在学生毕业季才有。』"
    yt "『想着一个人去会显得有些可怜当时一时头热就邀请了藤原 樱过来。。。』"
    yt "『果然还是太唐突了啊果咩捏。』"
    yt "『没有啦，偶尔尝试一下也不是什么坏事，是吧，小早川葵同学。』"
    "看着小早川葵同学迟迟没能加入，藤原 樱好心地把她拉入了话题。"
    yt "(她现在还好吗?)"
    "我这么担心着，不过显然是我多虑了。"
    "小早川葵 发挥自己 属于体育生刻板印象的 豪爽的一面。"
    aoi "『是啊，难得能和班级以外的同学一起去吃甜品，还是大美女，这是何等的喜事呀！』"
    ao "『也是，不用担心吃坏肚子影响什么考试，真是舒服呢。』"
    aoi "『真是期待呢樱花的味道。』"
    skr "『。。是呢，真是期待呢。。』"
    "进到店内，符合季节的樱花装饰将店面搞得粉不拉机。"
    "我们找了最近的靠窗位置坐下"
    aoi "『哇，这里新品好多欸，甚至专门搞了一面菜单。』"
    ao "『是欸，粉粉的呢。』"
    skr "『都有什么啊。』"
    aoi "『很多呢，樱花奶昔，樱花慕斯，樱花果冻花麻糬什么的。』"
    yt "『麻糬?像年糕一样的吗?』"
    skr "『差不多呢，也是拿糯米闹成黏糊状，要有樱花味的话就需要在内陷和糯米上下手了。』"
    ao "『藤原 樱同学好了解啊，不愧是烹饪教室的!』"
    skr "『什么?抱歉我刚刚没听清。』"
    aoi "『她说你很厉害呢，我也觉得。』"
    skr "『也没有啦。。』"
    "藤原 樱不好意思地低下了头，她们俩个已经想好了自己想点的东西。"
    ao "『藤原 樱同学会想试试这家店的樱花麻糬吗？』"
    skr "『嗯？』"
    "藤原 樱同学好像是又没听见，摆出了’没听见的表情‘。"
    ao "『啊，抱歉，藤原 樱同学还是点自己想吃的吧，我只是说说』"
    skr "『啊，不用。我本来就比较想吃一下这家店的樱花麻糬.』"
    "藤原 樱的表情有些僵硬，但还是微笑着回复零岛蓝："
    skr "『如果很好吃的话我还要向店长要配方呢。』"
    yt "『那我点一个奶昔，樱花味的。』"
    "甜品到了，对面那两人看上去是真的挺喜欢这些甜品。"
    "藤原 樱同学则像平时办公一样沉稳。"
    aoi "『怎么样怎么样、好吃吗？』"
    skr "『还可以，味道淡淡的。』"
    yt "『手让一下我再拿个勺子。』"
    "我伸手跨过藤原 樱的位置，朝桌子边的餐具盒伸去。"
    "结果不小心碰到了藤原 樱的手肘，‘共感’又一次触发了"
    "本来还在嘴里的甜腻奶昔味道瞬间消失了。"
    yt "(我尝不到味道了?)"
    "看着藤原 樱再一次吃那个破麻糬。"
    "我嘴里奶昔味存在的感觉越来越淡。"
    yt "(是’共感“啊，这就是她一直以来的感觉吗?)"
    yt "(如果我喝了她也会感觉到吗?)"
    "然后我喝了奶昔，还看着藤原 樱，注意着她的反应。"
    "藤原 楼的反应cg。"
    yt "(果然是可以的啊，真是不容易。)"
    "大家在甜品店里都有说有笑的，其乐融融。"
    "这时候一个熟悉的声音进了甜品店。"
    yt "『你好，我要这个樱花麻糬。』"
    "我转过头看了看她，她没理我，打包了麻糬就走了。"
    "此时雾岛 蓝变了一种神色看着我。"
    skr "『你认识她吗?』"
    menu:
        "A.我之前去图书馆有见过她":
            jump choice_a
        "B.认识，今天上午还和她聊了几句":
            jump choice_b
    "『』"
    "『』"
    "『』"
    "『』"
    "『』"
    "『』"
    "『』"
    ""
    return
label choice_a:
    yt "『我之前去图书馆有见过她。』"
    skr "『哦，这样子啊。』"
    ao "『』"  # 这里雾岛蓝的台词，你可后续补充完整
    return

label choice_b:
    yt "『认识，今天上午还和她聊了几句。』"
    skr "『哦，这样子啊。』"
    ao "『』"  # 同样雾岛蓝台词后续补充
    return

#内嵌小游戏

init python:
    class PongDisplayable(renpy.Displayable):
        def __init__(self):
            renpy.Displayable.__init__(self)
            
            #游戏参数
            self.PADDLE_WIDTH = 22
            self.PADDLE_HEIGHT = 142
            self.PADDLE_X = 360
            self.BALL_WIDTH = 22
            self.BALL_HEIGHT = 22
            self.COURT_TOP = 193
            self.COURT_BOTTOM = 975
            
            #元素
            self.paddle = Solid("#ffffff", xsize=self.PADDLE_WIDTH, ysize=self.PADDLE_HEIGHT)
            self.ball = Solid("#ffffff", xsize=self.BALL_WIDTH, ysize=self.BALL_HEIGHT)
            
            #状态
            self.stuck = True
            # 初始化球拍位置于球场中心
            self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2 + self.COURT_TOP
            self.computery = self.playery
            self.computerspeed = 570.0
            self.bx = self.PADDLE_X + self.PADDLE_WIDTH + 15
            self.by = self.playery
            self.bdx = .5
            self.bdy = .5
            self.bspeed = 525.0
            self.oldst = None
            self.winner = None

        def visit(self):
            return [self.paddle, self.ball]

        def render(self, width, height, st, at):
            r = renpy.Render(width, height)
            
            if self.oldst is None:
                self.oldst = st
            dtime = st - self.oldst
            self.oldst = st
            
            #球移动逻辑
            speed = dtime * self.bspeed
            oldbx = self.bx
            
            if self.stuck:
                self.by = self.playery
            else:
                self.bx += self.bdx * speed
                self.by += self.bdy * speed
            
            #电脑移动
            cspeed = self.computerspeed * dtime
            if abs(self.by - self.computery) <= cspeed:
                self.computery = self.by
            else:
                self.computery += cspeed * (self.by - self.computery) / abs(self.by - self.computery)
            
            #碰撞检测
            ball_top = self.COURT_TOP + self.BALL_HEIGHT / 2
            if self.by < ball_top:
                self.by = ball_top + (ball_top - self.by)
                self.bdy = -self.bdy
                if not self.stuck:
                    renpy.sound.play("pong_beep.opus", channel=0)
            
            ball_bot = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
            if self.by > ball_bot:
                self.by = ball_bot - (self.by - ball_bot)
                self.bdy = -self.bdy
                if not self.stuck:
                    renpy.sound.play("pong_beep.opus", channel=0)
            
            #球拍渲染和碰撞
            def paddle(px, py, hotside):
                pi = renpy.render(self.paddle, width, height, st, at)
                r.blit(pi, (int(px), int(py - self.PADDLE_HEIGHT / 2)))
                
                if py - self.PADDLE_HEIGHT / 2 <= self.by <= py + self.PADDLE_HEIGHT / 2:
                    hit = False
                    if oldbx >= hotside >= self.bx:
                        self.bx = hotside + (hotside - self.bx)
                        self.bdx = -self.bdx
                        hit = True
                    elif oldbx <= hotside <= self.bx:
                        self.bx = hotside - (self.bx - hotside)
                        self.bdx = -self.bdx
                        hit = True
                    if hit:
                        renpy.sound.play("pong_boop.opus", channel=1)
                        self.bspeed *= 1.10
            
            paddle(self.PADDLE_X, self.playery, self.PADDLE_X + self.PADDLE_WIDTH)
            paddle(width - self.PADDLE_X - self.PADDLE_WIDTH, self.computery, width - self.PADDLE_X - self.PADDLE_WIDTH)
            
            #?
            ball = renpy.render(self.ball, width, height, st, at)
            r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2), int(self.by - self.BALL_HEIGHT / 2)))
            
            #结束
            if self.bx < -75:
                self.winner = "computer"
                renpy.timeout(0)
            elif self.bx > width + 75:
                self.winner = "player"
                renpy.timeout(0)
            
            renpy.redraw(self, 0)
            return r

        def event(self, ev, x, y, st):
            import pygame
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.stuck = False
                renpy.restart_interaction()
            
            y = max(y, self.COURT_TOP)
            y = min(y, self.COURT_BOTTOM)
            self.playery = y
            
            if self.winner:
                return self.winner
            raise renpy.IgnoreEvent()

screen pong():
    default pong = PongDisplayable()
    add "bg pong" #背景
    add pong #游戏

    #例字
    text "Youtai":
        xpos 360
        xanchor 0.5
        ypos 37
        size 60

    text "电脑":
        xpos 1560
        xanchor 0.5
        ypos 37
        size 60
    
    #开始提示
    if pong.stuck:
        text "点击开始游戏":
            xalign 0.5
            ypos 75
            size 60

# 游戏入口标签
label play_pong:
    window hide
    $ quick_menu = False
    
    call screen pong
    
    $ quick_menu = True
    window show
    
    if _return == "computer":
        yt "『……』"
        yt "『哈——哈，其实我放水了啦』"
        yt "『我认真起来区区电脑又能怎样』"
        "电脑突然嗡嗡地叫了两声。"
        "看起来机魂大不悦。"

    else:
        yt "『哈哈』"
        yt "『喂，你就是逊啦』"
        "电脑突然嗡嗡地叫了两声。"
        "看起来机魂大不悦。"
    
    return
