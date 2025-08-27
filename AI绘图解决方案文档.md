
> [!Abstract] Abstract
> 本文档是对`🃏🧑‍💻数据结构王炸`小组的数据结构作业的AI绘图部分编撰的文档，旨在分享本小组作业美术部分实现的解决方案，以供交流学习。
> 作者：Tim2354
# 解决方案
本项目AI绘图基于[LibLib](https://www.liblib.art/)平台，这是国内一个相当大的生图AI模型社区，提供大量的用户微调模型和Lora。同时也提供在线云计算服务，使本项目的美术工作推进成为可能，尽管花了29元开通基础会员，但提供的云计算力已完全满足不断地试错，调优和输出项目所需美术素材。

基座模型是基于SDXL（Stable Diffusion XL）的[illustrious](https://www.illustrious-xl.ai/)的微调模型[WAI_NSFW-illustrious-SDXL](https://www.liblib.art/modelinfo/0f204323a06f40e18f8ffc5b1813df5a?from=sd&versionUuid=2940fa308c9d4eed8b01e3909a0096dc)（或者称为checkpoint）。由一位用户[WAI](https://www.liblib.art/userpage/07b938deb03043649319c0db9316f0f8/publish)上传。Illustrious原生支持ACG领域的动漫人物绘图，而该用户经过14次的迭代，模型在保证人物立绘质量上有了更强的可靠性和实用性。

LoRA（Low-Rank Adaptation）是一个更小规模的“微调模型”，在AI绘图中用作更精确地控制画风，笔触，基调。在本项目中采用了同样为用户[晨雨秋林](https://www.liblib.art/userpage/2a45e8ae96cf40e5b3c92e1d6eee461c/publish)制作的[可爱平涂风格插画_NKMCYQL_Illustrious](https://www.liblib.art/modelinfo/02274e29a3984e6b9dd9987a26e99919?from=sd&versionUuid=a75b70a30211494389225bd438c6e70a)。针对Illustrious优化，在本次项目中对控制输出绘图的画风一致性起到了至关重要的作用。

可以简单理解为基座模型是游戏本身，微调模型是由用户制作，基于游戏的“整合包”，而LoRA则是可选的Mod/插件。

接着在[LibLib](https://www.liblib.art/)提供的WebUI上进行文生图操作。对于人设构想，首先是想象一个在故事中的人的外观应该是什么样的，然后尽可能使用自然语言记录，交给Gemini来生成一套适用于SDXL的提示词（大体上仍然是自然语言描述，但更规范化）。审阅输出的英文，导入到WebUI上查看效果，接着反复让AI迭代提示词，直到有一个符合预期的效果图，下载并作为图生图原素材，用作接下来的微调和表情差分。

然后在图生图流程中，将提示词更改成Danbooru的风格，能以更精简的词汇来调整图片的各种细节。为获得更高的图片质量，往往使用了PS来进行背景去除和微调，节省算力与时间。

图生图流程的图片统一采用1048 * 2048，缩放模式视情况使用拉伸或裁剪，迭代步数在敲定人物底图前往往设置为30~40来获得更好的效果（但耗时也更长），之后设置为20来加速生成效果。采样方法设置为`Euler a`或`DPM++ 2M Karras`（前者为illustrious推荐使用，后者为业界常用。在该项目的应用场景中无明显的差距）。重绘幅度视情况而定，往往更改动作时会拉至最高`1`来获取更高自由度，更改表情时会大幅降低为`0.3`左右。ADetailer采用`hand_yolov8n`和`face_yolov8n`来修正脸部和手部，ControlNet在制作第二个及以后的人物立绘时有所使用，目的是为了控制人物立绘姿态一致性（为保证每个人物有所差异，往往把控制权重调整为`0.3`以下）

接着就是反复的生成图片，筛选图片。直到输出项目所需的所有人物立绘。

# 提示词
大量参考Danbooru百科,Gemini给出了非常实用的提示词

参考[tag group](https://danbooru.donmai.us/wiki_pages/tag_groups)，按照推荐顺序：
[groups](https://danbooru.donmai.us/wiki_pages/tag_group%3Agroups)：描述图像基本特征，主要为人物数量与性别
[image composition](https://danbooru.donmai.us/wiki_pages/tag_group%3Aimage_composition)：描述图片的视角
[posture](https://danbooru.donmai.us/wiki_pages/tag_group%3Aposture)：描述人物的姿势特征，包括动作
[eyes tags](https://danbooru.donmai.us/wiki_pages/tag_group%3Aeyes_tags)：描述人物眼睛外观
[face tags](https://danbooru.donmai.us/wiki_pages/tag_group%3Aface_tags)：描述面部特征，通常是表情
[holding](https://danbooru.donmai.us/wiki_pages/holding)：描述人物手持的事物
[attire Tags](https://danbooru.donmai.us/wiki_pages/tag_group%3Aattire)：描述人物的服饰
[body parts](https://danbooru.donmai.us/wiki_pages/tag_group%3Abody_parts)：描述人物的身体部位
[verbs and gerunds](https://danbooru.donmai.us/wiki_pages/tag_group%3Averbs_and_gerunds)：直译为动名词，描述人物此时的动作。与上面的posture不同的是，往往指代的是人物正在执行某件事，比如`cleaning`
[on tag](https://danbooru.donmai.us/wiki_pages/tag_group%3Averbs_and_gerunds)：描述人物在什么场景上，比如`on grass`
[locations](https://danbooru.donmai.us/wiki_pages/tag_group%3Alocations)：描述人物所处位置
[backgrounds](https://danbooru.donmai.us/wiki_pages/tag_group%3Abackgrounds)：描述所处人物的背景
[style parodies](https://danbooru.donmai.us/wiki_pages/list_of_style_parodies)：描述整体风格，可指定一个艺术家的
[viusal noval games](https://danbooru.donmai.us/wiki_pages/tag_group%3Avisual_novel_games)：描述为视觉小说风格

理想的提示词顺序应为： `<Quality Tags?>, <People Tags>, <Character Tags?>, <Action Tags>, <Appearance Tags>, <Background Tags>, <Composition Tags>, <Style/Artist Tags?>, <Quality Tags?>`

# 人设提示词
对于差分图，可能需要额外修改面部表情的提示词。
## 藤原樱
人设：学生会长，完美优等生，黑色长发，日本校园JK，责任心强，给人一种难以接近的高冷感。做事认真仔细
正向：
```
1girl,standing,arms at sides,black eyes,red pupils,black hair,long hair,short bangs,looking at viewer,medium breasts,pensive,holding book,office,classroom,straight-on,full body,senren banka
```
负向：
```
bad quality,worst quality,worst detail,sketch,censor
```


## 雾岛蓝
雾岛蓝的图是基于藤原樱图生图改的，
正向：
```
1girl,blazer,blue eyes,blue hair,cowboy shot,hair bobbles,hair ornament,jacket,long hair,long sleeves,looking at viewer,neck ribbon,one side up,plaid,plaid skirt,pleated skirt,red neckwear,red ribbon,ribbon,school uniform,skirt,solo,thighhighs,white background,white legwear,
```

```
bad quality,worst quality,worst detail,sketch,censor
```

### 小早川葵
小早川葵首先是提示词海量筛选，确定主体后图生图。
以下给出部分图的提示词示例：

正向：
```
1girl,hair ornament,hairclip,blush,shorts,happy,excited,open mouth,purple eyes,close eyes,smile,running,sailor collar,school uniform,shirt,short hair,solo,simple background,(wet clothes:0.5),
```

负向：
```
ng_deepnegative_v1_75t,(badhandv4:1.2),EasyNegative,(worst quality:2),
```

## 风见茜
文生图参考提示词：
AI输入：
```
我正在编写一套文生图的提示词，请严格参考danbooru网站给出的提示词，基于我给出的人设，生成一套提示词。

人设：一个成熟，稳重，身份是高中的图书管理员，佩戴眼睛。请帮我补充服装和其他饰品的设定

更改为适合Illustrious模型(基于SDXL)的提示词，请联网参考该模型的数据

最后优化为人物的立绘，也就是正面照片。

在此基础上更改，只需要一个人的照片，竖屏，照片只需要展示到小腿中部。也就是针对照片结构修改

再生成一版，人设与构图不变，但着装是夏装，而且是用作Galgame的动漫半身立绘

```
Gemini回复，给出的是最终版本：
```
masterpiece, best quality, galgame CG, visual novel style.
Anime half-body portrait (waist-up) of a mature and calm female high school librarian.
She is standing, facing the viewer with a gentle smile.
She has large, expressive brown eyes and is wearing elegant glasses. Her long brown hair is styled in a neat bun.
Her summer outfit consists of a light blue short-sleeved blouse and a white A-line skirt.
Simple abstract background with a soft gradient.
Style: clean line art, vibrant colors, soft lighting, sharp focus.
```

基于我的想象，给出的修正提示词，danbooru参考
图生图提示词：
```
1girl,mature,solo,smile,straight-on,null background,white background,standing,arms at side,belt,black legwear,Lift an arm to support the glasses on her face,another arm at side,blue ribbon,breasts,brown eyes,brown hair,dress,glasses,long hair,looking at viewer,pantyhose,ribbon,sailor collar,short sleeves,solo,
```

针对差分，给出可选的，用于补充的关键词：
```
happy,open mouth
serious,frown
```
# 场景提示词
场景风格理所应当是二次元的画风，而且要很有Gal的味道。
以下针对不同场景给出对于的正负面提示词，同样由Gemini驱动：
参数方面设置为原始分辨率1280 * 720，高清修复为1920 * 1080（96dpi）。放大算法采用`R-ESRGAN_4x+ Anime6B` 。
使用的模型为基础模型F.1，LoRA采用的是由用户 [Devilworld](galgame场景) 上传的[galgame场景](https://www.liblib.art/userpage/f1cd68423b354abba991fe16eb70fb0a/publish)

## 学校走廊

正向提示词：
```
masterpiece, best quality, highres, ultra-detailed, illustration, cinematic lighting,
scenery, no humans, empty, school corridor,
sunlight pouring through the window, bright, lens flare, light particles, dust motes in the air,
detailed background, wooden floor, lockers, classroom doors, depth of field, peaceful, serene

```
负面提示词：
```
(low quality, worst quality:1.4), (bad_prompt_version2:0.8), EasyNegative,
blurry, jpeg artifacts, signature, watermark, username, text, error,
1girl, 1boy, character, person, figure, silhouette,
ugly, deformed, disfigured,
3d, realistic, photorealistic, photo,
nsfw
```

## 男主的房间

正向：
```
masterpiece,best quality,highres,ultra-detailed,illustration,cinematic lighting,
scenery,no humans,boy's room,protagonist's room,bedroom interior,
morning sunlight streaming through the window,dust motes,cozy,lived-in feel,
desk with a computer,gaming console,bookshelf filled with manga,posters on the wall,slightly unmade bed,detailed background,depth of field,
```

负向：
```
(low quality, worst quality:1.4),(bad_prompt_version2:0.8),EasyNegative,
blurry,jpeg artifacts,signature,watermark,username,text,error,
1girl,1boy,character,person,figure,silhouette,
empty,sterile,too neat,hotel room,
girly,pink,frills,doll,makeup,
3d,realistic,photorealistic,photo,
nsfw,
```

## 学校天台
正向：
```
masterpiece,best quality,highres,ultra-detailed,illustration,cinematic lighting,anime style,
scenery,no humans,empty,school rooftop,clear blue sky,sunny day,bright,soft shadows,
metal fence,water tank,distant cityscape,vibrant greenery,
peaceful,serene,nostalgic,light particles,depth of field,
```

负向：
```
(low quality, worst quality:1.4),(bad_prompt_version2:0.8),bad-hands-5,EasyNegative,
blurry,jpeg artifacts,signature,watermark,username,text,error,
ugly,deformed,disfigured,poorly drawn hands,extra limb,missing limb,mutated hands,
3d,realistic,photorealistic,photo,
nsfw,multiple girls,multiple people,
```


## 学校图书馆

正向：
```
masterpiece, best quality, highres, ultra-detailed, illustration, cinematic lighting, anime style,
scenery, no humans, empty, library entrance, grand architecture, stone pillars, large closed glass doors, reflections on glass,
late afternoon, golden hour, warm light, long shadows, paved plaza, ginkgo trees with yellow leaves,
quiet, serene, nostalgic, depth of field
```

负向：
```
(low quality, worst quality:1.4), (bad_prompt_version2:0.8), EasyNegative,
blurry, jpeg artifacts, signature, watermark, username, text, error,
1girl, 1boy, character, person, figure, silhouette,
messy, cluttered, dirty, classroom, library,
3d, realistic, photorealistic, photo,
nsfw
```

## 学生会办公室
正向：
```
masterpiece, best quality, highres, ultra-detailed, illustration, cinematic lighting, anime style,
scenery, no humans, empty, student council room, office interior,
late afternoon sun streaming through large windows, stripes of light from window blinds, long shadows, dust motes in the air,
large mahogany meeting table, leather chairs, a president's desk at the head, school crest banner on the wall, bookshelves filled with binders and trophies, neatly stacked documents, a whiteboard with faded writing,
quiet, formal, dignified, depth of field
```

负向：
```
(low quality, worst quality:1.4), (bad_prompt_version2:0.8), EasyNegative,
blurry, jpeg artifacts, signature, watermark, username, text, error,
1girl, 1boy, character, person, figure, silhouette,
messy, cluttered, dirty, classroom, library,
3d, realistic, photorealistic, photo,
nsfw
```


## 田径场
正向：
```
masterpiece, best quality, highres, ultra-detailed, illustration, cinematic lighting, anime style,
scenery, no humans, empty, tranquil,
school athletic field, red running track, green grass infield, starting line,
vast blue sky, white fluffy clouds, brilliant sunlight, lens flare,
flags fluttering in the wind, leaves blowing gently across the track,
refreshing, youthful, energetic, sense of freedom, depth of field
```

负向：
```
(low quality, worst quality:1.4), (bad_prompt_version2:0.8), bad-hands-5, EasyNegative,
blurry, jpeg artifacts, signature, watermark, username, text, error,
ugly, deformed, disfigured, poorly drawn hands,
rainy, cloudy, night, dark, indoor,
crowd, audience, stadium,
3d, realistic, photorealistic, photo,
nsfw
```

## 器材室
正向：
```
(masterpiece, best quality, absurdres, ultra detailed), official art, key visual, anime style, sharp focus, cinematic lighting,
scenery, interior, (astronomy equipment storage room, storage closet:1.3), observatory utility room, (cramped space:1.2), no chairs,
(heavy-duty metal shelves:1.4), packed shelves, storage cabinets, cardboard boxes stacked on floor, wooden crates,
(dark room, darkness:1.2), (faint moonlight from a single small, grimy window:1.3), god rays, dust particles, deep shadows,
(many dust cloths:1.2), draped cloth, covering astronomical telescopes, (unevenly draped:1.1), deep folds,
cluttered, messy, (workbench instead of desk:1.2), tools left out, cables and wires hanging from shelves, half-unpacked equipment case,
silhouette of telescopes, faint reflection on lens, rolled-up star charts in a rack
```

负向：
```
(worst quality, low quality, normal quality:1.4), (EasyNegative, bad-hands-5, bad_prompt_version2), jpeg artifacts, blurry, watermark, signature, username, text, error,
(classroom, school desk, student chairs, blackboard, whiteboard:1.5),
(spacious, open space, wide room, high ceiling:1.2),
light on, lamp, bright, well-lit, sunny, daytime,
person, character,
neat, tidy, organized, clean, minimalist,
dirty, trash, garbage, abandoned, derelict,
(photorealistic, realistic, 3d:1.1),
nsfw
```

## 教室
正向：
```
(masterpiece, best quality, absurdres, ultra detailed), official art, key visual, anime style, sharp focus, beautiful detailed lighting,
scenery, interior, (empty school classroom:1.2), no humans,
(afternoon light, golden hour:1.3), (bright sunlight streaming through large windows:1.4), warm tones,
long shadows of desks and chairs stretching across the wooden floor,
rows of wooden student desks and chairs, neatly arranged, a teacher's desk at the front,
(blackboard with chalk writings:1.1), educational posters on the wall, a clock showing 3:30 PM,
serene, quiet, peaceful, nostalgic atmosphere, (dust particles floating in the sunbeams:1.2)

```

负向：
```
(worst quality, low quality, normal quality:1.4), (EasyNegative, bad-hands-5, bad_prompt_version2), jpeg artifacts, blurry, watermark, signature, username, text, error,
(dark, night, overcast, rainy, gloomy:1.5), artificial lighting, lamp,
messy, cluttered, dirty, abandoned, broken,
person, student, teacher, character,
(storage room, warehouse, office:1.3), metal shelves, boxes,
(photorealistic, realistic, 3d:1.1),
nsfw
```

## 阴暗的教室
正向：
```
(masterpiece, best quality, absurdres, ultra detailed), horror, creepy, unsettling atmosphere, cinematic lighting, sharp focus, anime style,
scenery, interior and exterior view, (abandoned astronomy club room:1.2), derelict, decay,
(an old, rusty metal door stands wide open, leading out onto the school rooftop:1.5),
(The only light in the room comes from a single, malfunctioning fluorescent lamp on the ceiling, casting harsh, flickering shadows:1.3), cold color palette,
(thick dust and cobwebs covering everything:1.2), peeling paint, grimy floor, overturned chairs, scattered and torn star charts,
Through the dark doorway, the rooftop is visible under a starless, deep indigo night sky, (a cold wind blows in, making old papers on the floor rustle:1.1),
A lone, forgotten telescope tripod stands on the rooftop, silhouetted against the dark sky,
ominous, silent, desolate, a sense of dread
```

负向：
```
(worst quality, low quality, normal quality:1.4), (EasyNegative, bad-hands-5, bad_prompt_version2), jpeg artifacts, blurry, watermark, signature, username, text, error,
(warm, cozy, safe, peaceful, nostalgic, serene:1.5),
(bright, well-lit, sunlight, moonlight, stars, daytime, clean:1.4),
(closed door:1.3),
person, character, student, monster, ghost,
(neat, tidy, organized:1.2),
(photorealistic, realistic, 3d:1.1),
nsfw
```

## 街道
正向：
```
(masterpiece, best quality, absurdres, 8k, ultra detailed, sharp focus on the environment),
cinematic, anime style, by Makoto Shinkai,
(a wide, establishing shot of a vibrant Japanese shopping street (shōtengai):1.4), the street itself is the main subject,
(late afternoon, golden hour, warm sunlight streaming down, casting long, soft shadows:1.3), lens flare, atmospheric light particles,
rows of richly detailed storefronts: ramen shop with noren curtains, takoyaki stall with rising steam, cafe, bookstore, vibrant banners,
(in the middle of the street, a single high school student in a summer uniform is walking away from the camera:1.5), (small in the frame, seen from a distance:1.2), their presence adds scale and a sense of story,
(deep depth of field, keeping both foreground and background sharp:1.1),
warm, lively, peaceful, nostalgic atmosphere
```


负向：
```
(worst quality, low quality, normal quality:1.4), (EasyNegative, bad-hands-5, ng_deepnegative_v1_75t),
(more than one person:1.5), (2 people, crowd, group, pedestrians, shoppers:1.5),
(close-up:1.5), (portrait:1.5), (character focus:1.4), (face focus:1.4),
(empty, deserted, abandoned:1.2),
(blurry background:1.2), (shallow depth of field),
(text, watermark, signature, error),
(photorealistic, 3d, realistic:1.2)
```

## 烹饪课教室
正向：
```
(masterpiece, best quality, absurdres, 8k, ultra detailed),
anime style, by Makoto Shinkai,
(a quiet and clean school nurse's office (hoken-shitsu):1.4),
(bright afternoon sunlight streaming through large windows:1.3), dust motes dancing in the light beams, creating a peaceful and serene atmosphere,
(a single medical bed with clean white sheets:1.2) and a privacy curtain pulled partially aside,
a nurse's simple wooden desk with a chair and a medical journal,
(a glass-fronted medical cabinet on the wall, filled with neatly arranged medicine bottles, gauze, and bandages:1.2),
(a classic height and weight scale in the corner:1.1), (an eye chart on the wall:1.1),
a potted plant on the windowsill,
clean, tidy, tranquil
```

负向：
```
(worst quality, low quality, normal quality:1.4), (EasyNegative, bad-hands-5, ng_deepnegative_v1_75t),
(hospital, emergency room, operating room, surgery:1.5), (high-tech medical equipment, IV drip, monitors:1.4),
(patient, sick person, doctor, blood, injury:1.4),
(messy, cluttered, dark, dirty, gloomy, sterile, cold atmosphere:1.2),
(classroom, office),
(text, watermark, signature, error),
(photorealistic, 3d, realistic:1.2)
```

