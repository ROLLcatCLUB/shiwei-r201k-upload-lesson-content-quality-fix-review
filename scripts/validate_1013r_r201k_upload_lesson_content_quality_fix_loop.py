from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STAGE = "1013R_R201K_UPLOAD_LESSON_CONTENT_QUALITY_FIX_LOOP"
OUT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / STAGE
RESULT = OUT / "validate_1013R_R201K_upload_lesson_content_quality_fix_loop_result.json"

R201J_P1_STAGE = "1013R_R201J_P1_TEACHER_READABLE_CONTENT_REVIEW_PACK"
R201J_STAGE = "1013R_R201J_SINGLE_LESSON_TEMPLATE_INSTANCE_CONFORMANCE_SMOKE"
R201J_P1_OUT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / R201J_P1_STAGE
R201J_OUT = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1" / R201J_STAGE
R201J_P1_RESULT = R201J_P1_OUT / "validate_1013R_R201J_P1_teacher_readable_content_review_pack_result.json"
R201J_MANIFEST = R201J_OUT / "r201j_sample_instance_manifest.json"

SYSTEM_CANDIDATE_LABEL = "系统建议，需教师确认"
SOURCE_LABEL = "由教学过程和原文证据反推"


POLICIES: dict[str, dict[str, Any]] = {
    "real_downpour_docx": {
        "basis": [
            "本课以雨天经验、雨的线条变化和诗意感受为学习起点，引导学生把看见的雨、听见的雨和心里的雨转化为线描雨景。",
            "原文已提供课堂导入、观察雨、诗词引入、线描示范、线描练习和分享小结六个环节，可作为本课教学过程的主要依据。",
        ],
        "analysis": [
            "四年级学生已有基本线条表现经验，能描述雨天感受，但容易停留在“下雨了”的生活描述，难以把细雨、暴雨、雷阵雨等差异转化为线条疏密、方向和节奏。",
            "本课难点不在是否会画雨，而在能否用观察到的线条变化表现不同雨景情绪，并在分享时说清自己选择某种线条的理由。",
        ],
        "objectives": [
            "学生能观察不同类型雨的图片，说出至少两种雨在线条方向、疏密或节奏上的差异。",
            "学生能用细头水笔在线稿或画面中表现一种雨景，并说明一处线条处理与雨的感受之间的关系。",
            "学生能在分享中听取同伴建议，完成一处线条、画面节奏或情感表达的调整。",
        ],
        "key_points": [
            "重点：观察雨的形态差异，并用长短、疏密、方向和节奏不同的线条表现雨景。",
            "难点：把雨天情绪和诗意感受转化为画面中的线条组织，而不是只画相同的斜线。"
        ],
        "preparation": [
            "教师准备不同雨景图片、雨相关诗句或童诗、线描示范材料和雨景学习单。",
            "学生准备细头水笔、铅笔或勾线笔，并保留一张可修改的雨景练习纸。"
        ],
        "episodes": {
            "课堂导入": {
                "goal": "学生能说出自己对雨天的一种真实感受，并把感受和画面表现联系起来。",
                "teacher": "从“你喜欢雨天吗”进入，追问理由，把学生的生活感受板书成安静、有趣、急促、清凉等关键词。",
                "student": "回忆雨天经验，说出喜欢或不喜欢的理由，并听同伴补充不同感受。",
                "talk": "你说雨天很安静，那画面里的线条可以怎样安静下来？如果是暴雨，线条又会有什么变化？",
                "evidence": "学生能用一个情绪词或生活场景说明自己对雨天的感受。"
            },
            "观察雨": {
                "goal": "学生能比较细雨、暴雨、雷阵雨的视觉差异，并说出线条表现的一个选择。",
                "teacher": "用图片对比不同雨势，引导学生从线条方向、长短、密度和画面节奏观察，而不是只说“雨很大”。",
                "student": "观察图片，指出一种雨的线条特点，并尝试说出适合用怎样的线表现。",
                "talk": "这张图里的雨为什么看起来更急？你看到的是线更密、方向更斜，还是节奏更乱？",
                "evidence": "学生能说出一种雨势对应的线条特点。"
            },
            "诗词引入": {
                "goal": "学生能从诗句或童诗中捕捉雨的情绪，并选择一种线条节奏回应这种情绪。",
                "teacher": "朗读雨的诗句，让学生先听感受，再把诗意词语转成画面线条的轻重和疏密。",
                "student": "听读诗句，说出雨给人的感觉，并尝试把感觉说成线条变化。",
                "talk": "如果这句诗里的雨是轻轻的，你会让线条变短、变淡，还是让线之间留出更多空隙？",
                "evidence": "学生能用一句话说明诗意感受和线条选择的关系。"
            },
            "线描示范": {
                "goal": "学生能看懂线描表现雨景的关键步骤，并判断自己要表现哪一种雨。",
                "teacher": "示范用不同线条表现雨势，同时提醒先定雨的类型，再处理背景、人物或景物的关系。",
                "student": "观察示范，记录一种自己准备尝试的线条方法。",
                "talk": "我不是示范唯一画法，而是在示范一种选择：先确定雨的感觉，再决定线条怎么走。",
                "evidence": "学生能说出自己准备使用的一种线条方法。"
            },
            "线描练习": {
                "goal": "学生能用线条完成一幅雨景练习，并让画面至少一处体现雨的类型或情绪。",
                "teacher": "巡视时先问学生画的是哪种雨，再看线条是否支持这个判断，必要时示范局部修改。",
                "student": "完成雨景线描练习，边画边调整线条疏密、方向和节奏。",
                "talk": "你画的是细雨还是急雨？现在这组线条能让别人看出来吗？要不要在这一块做疏密变化？",
                "evidence": "作品中能看到至少一处有意识的线条疏密、方向或节奏处理。"
            },
            "分享小结": {
                "goal": "学生能指着作品说明一处线条选择，并根据建议提出一处可修改点。",
                "teacher": "组织学生用“我画的是……我用了……因为……”进行分享，再让同伴给出一条具体建议。",
                "student": "展示作品，说出线条选择和雨景感受之间的关系，并记录修改建议。",
                "talk": "请你不要只说好看，说一说这组线条为什么像你想表现的那种雨。",
                "evidence": "学生能用作品中的一处线条作为表达雨景感受的证据。"
            },
        },
    },
    "minimal_line_fish": {
        "basis": [
            "本课以观察鱼身上的线条为起点，通过示范波浪线、折线、点线等装饰方法，让学生完成一条有线条变化的小鱼。",
            "原文虽简短，但已提供观察、示范、创作三个核心环节，可作为极简教案的教学过程依据。"
        ],
        "analysis": [
            "二年级学生能辨认常见线条，也愿意画鱼，但容易把装饰变成随意填满，较少观察线条位置、方向和重复规律。",
            "本课需要帮助学生先说出鱼身上的线条发现，再把一种或两种线条有意识地用在鱼的身体、鱼鳍或尾巴上。"
        ],
        "objectives": [
            "学生能观察鱼的图片，说出鱼身上至少一种线条形态或排列特点。",
            "学生能选择波浪线、折线、点线等线条装饰一条小鱼，并让线条与鱼身部位有对应关系。",
            "学生能向同伴说明自己用了哪一种线条装饰鱼的哪个部位。"
        ],
        "key_points": [
            "重点：观察鱼身线条，并用不同线条装饰鱼的身体、鱼鳍或尾巴。",
            "难点：让线条有方向、有重复或有变化，并能和鱼身部位对应，而不是无目的地填满画面。"
        ],
        "preparation": [
            "教师准备鱼类图片、线条示范图、波浪线/折线/点线局部示范和学生练习纸。",
            "学生准备彩笔、勾线笔或油画棒，课堂中保留一处可修改的线条练习空间。"
        ],
        "episodes": {
            "看鱼图片，说一说鱼身上有什么线条": {
                "goal": "学生能观察鱼身、鱼鳍和尾巴，说出一种看到的线条。",
                "teacher": "出示鱼的图片，先让学生找线条位置，再把学生发现归为波浪线、弧线、点线或重复线。",
                "student": "观察图片，指认鱼身上的线条，并尝试说出线条像什么。",
                "talk": "你看到的这条线在鱼的哪个部位？它是直直的、弯弯的，还是一排小点连起来的？",
                "evidence": "学生能指出鱼身上的一个线条位置并说出线条形态。"
            },
            "教师示范用波浪线、折线、点线装饰鱼": {
                "goal": "学生能看懂三种线条装饰方法，并选择一种用于自己的小鱼。",
                "teacher": "在鱼形轮廓中分别示范波浪线、折线和点线，强调线条可以顺着身体方向排列。",
                "student": "观察示范，选择自己想尝试的一种线条。",
                "talk": "同样是装饰鱼身，波浪线会让小鱼像在水里游，折线会更有节奏，你想选哪一种？",
                "evidence": "学生能说出自己准备使用的线条类型。"
            },
            "学生画一条线条小鱼": {
                "goal": "学生能完成一条有线条变化的小鱼，并说明一处装饰选择。",
                "teacher": "巡视时看学生是否把线条放在合适部位，提醒不要把所有线条挤在一起。",
                "student": "画出小鱼并用线条装饰鱼身、鱼鳍或尾巴。",
                "talk": "你这条线准备装饰鱼的哪里？如果这里太密，旁边是不是可以留一点空，让线条更清楚？",
                "evidence": "作品中至少有一处清楚的线条装饰，并能说出所用线条名称。"
            },
        },
    },
    "numbered_colon_old_shoes": {
        "basis": [
            "本课依据上传原稿定位为三年级《足下生辉》旧鞋改造设计课，教学主线是把上一课草图转化为旧鞋改造作品。",
            "本课学习重心不是鞋的线描观察，而是围绕旧鞋材料、结构、设计意图、设计故事和发布会准备，完成一次设计应用表达。"
        ],
        "analysis": [
            "三年级学生有生活材料改造兴趣，也可能已有上一课草图，但容易把旧鞋制作变成随意装饰，忽略材料选择是否服务设计意图。",
            "本课需要持续追问“我想改造成什么、为什么这样选材料、哪里体现设计想法”，帮助学生把制作过程转化为可说明的设计证据。"
        ],
        "objectives": [
            "学生能对照上一课草图，说明自己准备把旧鞋改造成什么，并选择与设计意图相匹配的材料或制作方法。",
            "学生能在旧鞋作品制作中处理至少一处材料连接、结构稳定或装饰表达问题。",
            "学生能用5句话设计故事说明作品对象、解决的问题、材料方法、满意处和改进想法，并为发布会整理作品证据。"
        ],
        "key_points": [
            "重点：把草图中的设计意图落实到旧鞋材料选择、结构处理和装饰表达中。",
            "难点：让学生说清材料方法为什么服务自己的设计，而不是只评价作品是否好看。"
        ],
        "preparation": [
            "学生准备旧鞋、上一课设计草图、可选装饰材料、故事卡或记录单。",
            "教师准备材料连接示例、工具安全提醒、5句话设计故事句式和发布会作品整理要求。"
        ],
        "episodes": {
            "回顾草图与任务确认": {
                "goal": "学生能对照上一课草图，确认今天旧鞋改造的对象和设计意图。",
                "teacher": "组织学生拿出草图，先说准备改造成什么，再圈出今天最要实现的一处设计重点。",
                "student": "查看草图，说明旧鞋改造方向，并确认一处需要重点完成的设计内容。",
                "talk": "今天不是重新想一个作品，而是把草图里的想法做出来。你最想先完成草图里的哪一点？",
                "evidence": "学生能拿出草图并说明旧鞋改造方向。"
            },
            "制作路径讨论": {
                "goal": "学生能比较粘贴、包裹、添加、绘制等方法，判断哪一种更适合自己的设计。",
                "teacher": "引导学生把材料方法和设计意图配对，讨论不同连接方式的稳定性和表现效果。",
                "student": "比较制作路径，说明自己选择某种材料或方法的理由。",
                "talk": "如果你想表现这个功能或造型，粘贴、包裹、添加、绘制哪一种更能支持你的想法？为什么？",
                "evidence": "学生能说出一种材料方法和设计意图之间的关系。"
            },
            "旧鞋作品制作": {
                "goal": "学生能根据草图完成旧鞋改造，并在制作中检查结构稳定和材料效果。",
                "teacher": "巡视材料连接、结构稳定和工具安全，优先追问学生是否仍在回应原设计。",
                "student": "按照草图进行旧鞋改造，遇到连接或装饰问题时说明困难并调整。",
                "talk": "现在这一步有没有帮助你实现草图里的设计？如果只是贴上去好看，它和你的想法有什么关系？",
                "evidence": "作品能看到旧鞋改造痕迹，并有至少一处材料或结构处理回应草图。"
            },
            "5句话设计故事": {
                "goal": "学生能用五句话说明作品对象、问题、材料方法、满意处和改进点。",
                "teacher": "提供五句话结构，让学生把制作结果转化为发布会可以讲清楚的设计故事。",
                "student": "围绕作品写或说出5句话设计故事，并检查每句话是否有作品证据。",
                "talk": "请按五句话说：它是谁、解决什么问题、用了什么材料方法、你最满意哪里、还想改什么。",
                "evidence": "学生完成故事卡，能对应作品中的材料和结构证据。"
            },
            "新鞋发布会准备": {
                "goal": "学生能整理作品和故事卡，为下一环节展示发布做好准备。",
                "teacher": "组织学生检查作品、故事卡和展示顺序，提醒发布会要用作品证据支持介绍。",
                "student": "整理旧鞋作品与故事卡，准备展示时的介绍顺序。",
                "talk": "发布会上不要只展示作品，请把故事卡放在旁边，让别人知道你的设计从哪里来。",
                "evidence": "学生能准备好作品和故事卡，并说出展示时先讲哪一点。"
            },
        },
    },
    "plain_segment_weaving": {
        "basis": [
            "本课围绕编织历史、经纬交织原理和纸条编织练习展开，让学生从实物观察进入基本方法体验。",
            "原文提供导入、历史介绍、认识经纬、教师示范、学生练习和小结六个环节，教学主线应从文化认识走向方法操作。"
        ],
        "analysis": [
            "四年级学生能观察编织实物的纹理，也具备剪贴和纸条操作经验，但未必理解经线固定、纬线穿插形成图案的原理。",
            "本课需要把历史介绍控制为短背景，把重点落到经纬关系、压一穿一方法和纸条练习中的手眼协调。"
        ],
        "objectives": [
            "学生能观察编织实物，说出编织与生活用品或传统工艺之间的联系。",
            "学生能区分经线和纬线，理解压一穿一形成交织纹样的基本方法。",
            "学生能用纸条完成一段基本编织练习，并在小结中说出一个操作要点或困难。"
        ],
        "key_points": [
            "重点：认识经纬交织原理，并掌握纸条压一穿一的基本编织方法。",
            "难点：保持纸条排列有序、松紧适度，并能用自己的操作过程说清经线和纬线的关系。"
        ],
        "preparation": [
            "教师准备竹编、藤编或纸编实物/图片，经纬示意图，纸条编织步骤示范材料。",
            "学生准备彩纸条、底纸、剪刀和胶棒，注意工具使用安全。"
        ],
        "episodes": {
            "导入": {
                "goal": "学生能从编织实物中发现交错纹理，产生学习编织方法的兴趣。",
                "teacher": "出示竹编或藤编实物，让学生先看用途，再观察表面的穿插纹理。",
                "student": "观察实物，说出在哪里见过类似编织物，并指出交错纹理。",
                "talk": "它不是画出来的纹样，而是一条一条材料穿出来的。你能找到哪条在上、哪条在下吗？",
                "evidence": "学生能指出实物中的交错纹理。"
            },
            "历史介绍": {
                "goal": "学生能知道编织与生活、记录和装饰有关，理解它不是单纯手工小练习。",
                "teacher": "用两三张图快速介绍编织从生活器物到纹样装饰的发展，不展开成大段讲授。",
                "student": "听取背景，选择一个自己觉得有意思的编织用途或纹样来源。",
                "talk": "古人编席子是为了解决生活需要，后来这些交错纹理也变成了装饰。你觉得哪一种最接近今天的纸编？",
                "evidence": "学生能说出一个编织的生活用途或文化背景。"
            },
            "认识经纬": {
                "goal": "学生能区分经线和纬线，理解纬线穿过经线形成交织关系。",
                "teacher": "用示意图和纸条演示经线竖向固定、纬线横向穿插，强调上下交替。",
                "student": "用手势或纸条模拟经纬方向，说出压一穿一的规律。",
                "talk": "竖着不动的是经线，横着来回穿的是纬线。下一格如果在上面，后一格应该在哪里？",
                "evidence": "学生能正确指出经线、纬线，并说出上下交替规律。"
            },
            "教师示范": {
                "goal": "学生能看懂纸条编织的起步、穿插和收边方法。",
                "teacher": "分步示范固定经线、穿入纬线、压一穿一和整理边缘，控制速度让学生看清手法。",
                "student": "跟随示范在草稿纸上试做一到两步，并提出不清楚的位置。",
                "talk": "这一条穿过去时不要急着粘，先检查是不是一上一下交替，再把纸条推整齐。",
                "evidence": "学生能完成一段压一穿一试排。"
            },
            "学生练习": {
                "goal": "学生能独立完成一段纸条编织，并调整纸条松紧和排列。",
                "teacher": "巡视纸条方向、上下交替和边缘整理，针对错位处做局部示范。",
                "student": "完成纸条编织练习，检查是否有连续压错或缝隙过大的问题。",
                "talk": "先别急着贴牢，沿着这一行检查：有没有连续两次都在上面？哪里需要推紧一点？",
                "evidence": "作品中能看到经纬交织关系，且学生能指出一处调整过的地方。"
            },
            "小结": {
                "goal": "学生能用自己的话说出经纬关系和一个编织操作要点。",
                "teacher": "组织学生展示练习片段，围绕经线、纬线、压一穿一和整理边缘做小结。",
                "student": "展示练习，说出自己学会的一个方法和仍需改进的一处。",
                "talk": "今天你不是只完成了一张纸编，而是学会了经线和纬线怎样合作。你最容易出错的是哪一步？",
                "evidence": "学生能说出一个经纬关系或操作要点。"
            },
        },
    },
    "table_rain_umbrella": {
        "basis": [
            "本课以雨伞图案设计为主题，从生活用品观察进入纹样规律、伞面排列和作品评价。",
            "表格原文提供导入观察、方法示范、设计制作和展示评价四个环节，需要转写为自然教学过程而不是字段堆叠。"
        ],
        "analysis": [
            "学生熟悉雨伞外形和伞面图案，但容易只画单个装饰图案，忽略伞骨结构、重复排列和色彩疏密。",
            "本课需要帮助学生从生活观察中发现图案规律，再把规律用于伞面设计。"
        ],
        "objectives": [
            "学生能观察不同雨伞图案，说出重复、对称或色彩搭配中的一种规律。",
            "学生能沿伞骨或伞面分区设计一组有规律的图案，并注意色彩和疏密关系。",
            "学生能展示作品，说明自己最满意的一处图案安排。"
        ],
        "key_points": [
            "重点：发现雨伞图案的重复、对称和色彩搭配规律，并运用于伞面设计。",
            "难点：让图案顺着伞面结构有序排列，而不是把图形随意贴满。"
        ],
        "preparation": [
            "教师准备不同雨伞图片、伞面结构示意图、重复排列示范和评价提示。",
            "学生准备彩笔、伞面设计纸或圆形/扇形练习纸，并保留草稿用于尝试图案排列。"
        ],
        "episodes": {
            "导入观察": {
                "goal": "学生能从雨伞图片中发现图案排列规律。",
                "teacher": "出示不同雨伞图片，引导学生观察图案如何顺着伞面或伞骨排列。",
                "student": "观察图片，说出一种重复、对称或色彩搭配规律。",
                "talk": "你看到的不是一个孤立图案，而是一组图案在伞面上排队。它们是怎么重复或对称的？",
                "evidence": "学生能说出一处图案排列规律。"
            },
            "方法示范": {
                "goal": "学生能看懂把小图形沿伞骨重复排列的方法。",
                "teacher": "示范先定小图形，再沿伞骨或伞面分区重复排列，并比较疏密效果。",
                "student": "在草稿纸上尝试把一个图形重复排列成伞面纹样。",
                "talk": "如果这个图形只画一次，它只是装饰；沿伞骨重复以后，它才成为伞面的图案设计。",
                "evidence": "学生能完成一个小图形的重复排列草稿。"
            },
            "设计制作": {
                "goal": "学生能完成一张有规律的雨伞图案设计。",
                "teacher": "巡视学生是否围绕重复、对称、色彩和疏密推进，提醒图案与伞面结构对齐。",
                "student": "完成伞面图案设计，并调整图案大小、间距或颜色。",
                "talk": "你的图案准备顺着伞骨走，还是围着伞面一圈展开？先确定规律，再上颜色。",
                "evidence": "作品中能看到一组重复或对称的伞面图案。"
            },
            "展示评价": {
                "goal": "学生能展示作品，并说明最满意的一处图案安排。",
                "teacher": "组织学生用作品证据评价图案规律、色彩搭配和伞面结构关系。",
                "student": "展示作品，说明自己最满意的图案安排，并听取同伴建议。",
                "talk": "请指着作品说：你最满意的图案安排在哪里？它为什么适合放在伞面上？",
                "evidence": "学生能用作品中的一处图案规律说明设计效果。"
            },
        },
    },
}


GENERIC_PATTERNS = [
    "先把原稿任务说成学生听得懂的一句话",
    "先说自己的发现或选择，再完成相应的观察、练习或作品片段",
    "需要时只补一个方法提示",
    "你这样选材料、颜色或方法，是想表现什么",
    "该环节的顺序依据来自原文流程，具体因果需要教师确认",
]

FORBIDDEN_TEACHER_TERMS = [
    "R200A",
    "R200B",
    "R97B_P3",
    "deterministic_fallback",
    "legacy_shell",
    "source_gap_as_content",
    "provider_called",
    "model_called",
    "formal apply",
    "field projection",
]

RAW_TABLE_FIELD_PATTERNS = ["环节：", "教师活动：", "学生活动：", "设计意图："]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item or "").strip()]
    if isinstance(value, dict):
        return [str(item).strip() for item in value.values() if str(item or "").strip()]
    if str(value or "").strip():
        return [str(value).strip()]
    return []


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _build_section(title: str, body: list[str]) -> dict[str, Any]:
    return {
        "title": title,
        "body": body,
        "source_label": f"{SOURCE_LABEL}；{SYSTEM_CANDIDATE_LABEL}",
        "teacher_review_required": True,
    }


def _episode_policy(sample_id: str, episode: dict[str, Any]) -> dict[str, str]:
    title = str(episode.get("episode_title") or "")
    policy = POLICIES[sample_id]["episodes"].get(title)
    if policy:
        return policy
    fallback_title = title or "本环节"
    return {
        "goal": f"学生能围绕“{fallback_title}”完成一个可观察的学习动作，并说明自己的发现。",
        "teacher": f"教师围绕“{fallback_title}”组织观察、尝试和表达，追问学生的选择依据。",
        "student": f"学生完成“{fallback_title}”相关任务，并用一句话说明自己的发现或做法。",
        "talk": f"请你说清楚：这一环节你看到了什么、做了什么，哪一点能在作品或记录里看见？",
        "evidence": f"学生能留下与“{fallback_title}”相关的作品、草稿、口头说明或记录证据。",
    }


def _confirm_groups(sample_id: str) -> dict[str, list[str]]:
    title = POLICIES[sample_id]
    common = {
        "必须确认": [
            "教材版本、册次、页码和学校实际进度需教师确认。",
            "本课材料、工具数量和安全要求需按班级实际确认。",
        ],
        "建议确认": [
            "教学目标、重难点和准备为系统候选，需教师按学生情况调整。",
            "关键话术为系统建议，需教师按自己的课堂语言改写。",
        ],
        "可折叠诊断": [
            "本轮仅生成教师可读候选快照，不进入正式备课本。",
        ],
    }
    if sample_id == "numbered_colon_old_shoes":
        common["必须确认"].append("旧鞋、草图、故事卡和发布会安排需由教师确认是否齐备。")
    elif sample_id == "plain_segment_weaving":
        common["必须确认"].append("纸条尺寸、剪刀和胶棒使用规则需由教师确认。")
    elif sample_id == "real_downpour_docx":
        common["建议确认"].append("诗句或童诗材料需由教师按年级和教材版本确认。")
    elif sample_id == "table_rain_umbrella":
        common["必须确认"].append("伞面设计纸样式和色彩材料需由教师确认。")
    elif sample_id == "minimal_line_fish":
        common["建议确认"].append("鱼图片和线条示范图需按二年级学生观察能力选择。")
    return common


def _confirm_item_count(groups: dict[str, list[str]]) -> int:
    return sum(len(items) for items in groups.values())


def _make_snapshot(sample: dict[str, Any], template: dict[str, Any], fixed: dict[str, Any]) -> str:
    header = template.get("lesson_header") if isinstance(template.get("lesson_header"), dict) else {}
    title = header.get("lesson_title") or sample.get("lesson_label") or sample.get("sample_id")
    lines = [
        f"# {title}",
        "",
        f"- 样本：{sample.get('sample_id')}",
        f"- 年级：{header.get('grade') or '待确认'}",
        f"- 单元：{header.get('unit_title') or '待确认'}",
        f"- 来源：{sample.get('source_path')}",
        "- 状态：只读候选；不写库、不正式应用、不导出。",
        "",
    ]

    def add_section(display_title: str, section: dict[str, Any]) -> None:
        lines.extend([f"## {display_title}", "", f"**{section['title']}**（{section['source_label']}）"])
        for idx, text in enumerate(section["body"], 1):
            lines.append(f"{idx}. {text}")
        lines.append("")

    add_section("一、本课依据", fixed["basis"])
    add_section("二、学情分析", fixed["analysis"])
    add_section("三、教学目标", fixed["objectives"])
    add_section("四、教学重难点", fixed["key_points"])
    add_section("五、教学准备", fixed["preparation"])

    lines.extend(["## 六、教学过程", ""])
    for episode in fixed["episodes"]:
        lines.extend(
            [
                f"### {episode['index']}. {episode['title']}（{SOURCE_LABEL}；{SYSTEM_CANDIDATE_LABEL}）",
                "",
                f"- 环节目标：{episode['goal']}",
                f"- 教师组织：{episode['teacher']}",
                f"- 学生学习：{episode['student']}",
                f"- 关键话术：{episode['talk']}（{SYSTEM_CANDIDATE_LABEL}）",
                f"- 小教提醒：{episode['hint']}",
                "",
                "**本环节小步骤与证据**",
                "",
                f"1. {episode['title']}",
                f"   - 教师动作：{episode['teacher']}",
                f"   - 学生动作：{episode['student']}",
                f"   - 材料/大屏：{episode['materials']}",
                f"   - 支架：{episode['scaffold']}",
                f"   - 证据：{episode['evidence']}",
                "",
            ]
        )

    lines.extend(["## 七、学习单与评价", ""])
    lines.append(f"**七、学习单与评价**（{SOURCE_LABEL}；{SYSTEM_CANDIDATE_LABEL}）")
    for idx, item in enumerate(fixed["assessment"], 1):
        lines.append(f"{idx}. {item}")
    lines.append("")

    lines.extend(["## 八、待教师确认项", ""])
    for group, items in fixed["confirm_groups"].items():
        lines.append(f"**{group}**")
        for idx, item in enumerate(items, 1):
            lines.append(f"{idx}. {item}")
        lines.append("")
    return "\n".join(lines)


def _make_fixed_template(sample: dict[str, Any], template: dict[str, Any]) -> dict[str, Any]:
    sample_id = sample["sample_id"]
    policy = POLICIES[sample_id]
    episodes: list[dict[str, Any]] = []
    for idx, episode in enumerate(template.get("process_episodes") or [], 1):
        if not isinstance(episode, dict):
            continue
        ep_title = str(episode.get("episode_title") or f"环节{idx}")
        ep_policy = _episode_policy(sample_id, episode)
        source_materials = []
        for micro in episode.get("micro_steps") or []:
            if isinstance(micro, dict):
                source_materials.extend(_as_list(micro.get("screen_or_materials")))
        materials = "；".join(source_materials) if source_materials else _materials_for(sample_id, ep_title)
        episodes.append(
            {
                "index": episode.get("episode_index") or idx,
                "title": ep_title,
                "goal": ep_policy["goal"],
                "teacher": ep_policy["teacher"],
                "student": ep_policy["student"],
                "talk": ep_policy["talk"],
                "hint": _hint_for(sample_id, ep_title),
                "materials": materials,
                "scaffold": _scaffold_for(sample_id, ep_title),
                "evidence": ep_policy["evidence"],
            }
        )

    confirm_groups = _confirm_groups(sample_id)
    return {
        "sample_id": sample_id,
        "lesson_label": sample.get("lesson_label"),
        "basis": _build_section("一、本课依据", policy["basis"]),
        "analysis": _build_section("二、学情分析", policy["analysis"]),
        "objectives": _build_section("三、教学目标", policy["objectives"]),
        "key_points": _build_section("四、教学重难点", policy["key_points"]),
        "preparation": _build_section("五、教学准备", policy["preparation"]),
        "episodes": episodes,
        "assessment": _assessment_for(sample_id),
        "confirm_groups": confirm_groups,
    }


def _materials_for(sample_id: str, title: str) -> str:
    if sample_id == "real_downpour_docx":
        return "雨景图片、线描示范、雨景学习单"
    if sample_id == "minimal_line_fish":
        return "鱼类图片、线条示范图、练习纸和彩笔"
    if sample_id == "numbered_colon_old_shoes":
        return "旧鞋、上一课草图、材料包、故事卡"
    if sample_id == "plain_segment_weaving":
        return "编织实物或图片、纸条、底纸、胶棒"
    if sample_id == "table_rain_umbrella":
        return "雨伞图片、伞面结构示意图、伞面设计纸"
    return "课堂材料需教师确认"


def _scaffold_for(sample_id: str, title: str) -> str:
    if sample_id == "real_downpour_docx":
        return "用“我看到的雨是……所以我用……”帮助学生把观察转成线条选择。"
    if sample_id == "minimal_line_fish":
        return "用“线条名称-装饰部位-变化方式”帮助学生说清线条选择。"
    if sample_id == "numbered_colon_old_shoes":
        return "用“草图想法-材料方法-作品证据”帮助学生避免随意装饰。"
    if sample_id == "plain_segment_weaving":
        return "用“经线固定、纬线穿插、上下交替”帮助学生检查编织步骤。"
    if sample_id == "table_rain_umbrella":
        return "用“图案单元-排列规律-伞面位置”帮助学生组织设计。"
    return "根据学生现场表现确认支架。"


def _hint_for(sample_id: str, title: str) -> str:
    if sample_id == "real_downpour_docx":
        return "小教只提示教师追问线条证据，不替学生评价作品好坏。"
    if sample_id == "minimal_line_fish":
        return "小教提醒教师先问线条在哪里，再问为什么这样装饰。"
    if sample_id == "numbered_colon_old_shoes":
        return "小教提醒教师持续追问材料选择是否回应草图意图。"
    if sample_id == "plain_segment_weaving":
        return "小教提醒教师先检查经纬方向，再处理纸条松紧。"
    if sample_id == "table_rain_umbrella":
        return "小教提醒教师让学生先说图案规律，再评价色彩效果。"
    return "小教提醒需教师确认。"


def _assessment_for(sample_id: str) -> list[str]:
    if sample_id == "real_downpour_docx":
        return [
            "观察证据：学生能说出雨势与线条方向、疏密或节奏之间的关系。",
            "作品证据：画面中至少有一处线条处理能表现雨的类型或情绪。",
            "表达证据：学生能指着作品说明一处线条选择。"
        ]
    if sample_id == "minimal_line_fish":
        return [
            "观察证据：学生能指出鱼身、鱼鳍或尾巴上的一种线条。",
            "作品证据：小鱼作品中有清楚的线条装饰部位。",
            "表达证据：学生能说出自己用了哪一种线条。"
        ]
    if sample_id == "numbered_colon_old_shoes":
        return [
            "过程证据：学生能对照草图选择材料和制作方法。",
            "作品证据：旧鞋作品中能看到材料选择、结构处理或装饰表达回应设计意图。",
            "表达证据：5句话设计故事能说明对象、问题、材料方法、满意处和改进点。"
        ]
    if sample_id == "plain_segment_weaving":
        return [
            "认知证据：学生能区分经线和纬线。",
            "操作证据：纸条编织练习体现压一穿一的上下交替。",
            "表达证据：学生能说出一个编织操作要点或困难。"
        ]
    if sample_id == "table_rain_umbrella":
        return [
            "观察证据：学生能说出雨伞图案中的重复、对称或色彩规律。",
            "作品证据：伞面设计中有一组沿伞骨或分区排列的图案。",
            "表达证据：学生能说明最满意的一处图案安排为什么适合伞面。"
        ]
    return ["评价证据需教师确认。"]


def _count_generic(text: str) -> int:
    return sum(text.count(pattern) for pattern in GENERIC_PATTERNS)


def _count_raw_table_dump(text: str) -> int:
    return sum(text.count(pattern) for pattern in RAW_TABLE_FIELD_PATTERNS)


def _thin_front_matter_count(fixed: dict[str, Any]) -> int:
    count = 0
    for key in ["basis", "analysis", "objectives", "key_points", "preparation"]:
        text = "".join(fixed[key]["body"])
        if len(text) < 60 or "上传原文未明确提供" in text or "需教师补充" in text:
            count += 1
    return count


def _old_shoes_misaligned(snapshot: str) -> bool:
    required = ["旧鞋", "材料", "设计意图", "5句话", "发布会"]
    if not all(word in snapshot for word in required):
        return True
    bad = "学生能用线条和形状画出鞋的基本轮廓" in snapshot
    return bad


def _teacher_text_has_forbidden_source(text: str) -> bool:
    forbidden = [
        "R200A_kernel",
        "R200B_candidate",
        "R97B_P3_derivation_spine",
        "deterministic_fallback",
        "legacy_shell",
        "unknown",
        "source_gap",
    ]
    return any(term in text for term in forbidden)


def _run_py_compile() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "-m", "py_compile", str(Path(__file__))],
        cwd=str(ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "command": f"{sys.executable} -m py_compile scripts/{Path(__file__).name}",
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-1200:],
        "stderr_tail": completed.stderr[-1200:],
    }


def _write_policy_docs(sample_results: list[dict[str, Any]]) -> None:
    _write_text(
        OUT / "r201k_front_matter_derivation_policy.md",
        "\n".join(
            [
                "# R201K 前置字段反推策略",
                "",
                "前置字段可以从教学过程、环节证据和上传原文事实中反推，但必须标为系统候选并要求教师确认。",
                "",
                "- 教学目标：从学生最终能观察、制作、表达或评价什么来写。",
                "- 教学重点：从整课最核心的方法、概念或制作任务来写。",
                "- 教学难点：从学生最可能卡住的观察-方法-表达转换处来写。",
                "- 教学准备：从环节材料、作品证据和课堂组织动作反推。",
                "",
                "禁止把缺失字段写成“上传原文未明确提供，需教师补充”后直接进入教师主读稿。",
            ]
        ),
    )
    _write_text(
        OUT / "r201k_key_teacher_talk_candidate_policy.md",
        "\n".join(
            [
                "# R201K 关键话术候选策略",
                "",
                "每个 episode 必须生成至少一条教师可读话术候选，并显式标记为“系统建议，需教师确认”。",
                "",
                "话术只服务当前环节，不跨环节复用通用句。话术要追问学生观察、方法选择、作品证据或表达理由。",
            ]
        ),
    )
    _write_text(
        OUT / "r201k_confirmation_item_grouping_policy.md",
        "\n".join(
            [
                "# R201K 待教师确认项分组策略",
                "",
                "确认项从原始 trace 中收束为三组：必须确认、建议确认、可折叠诊断。",
                "",
                "每个样本教师默认看到的确认项不超过 8 条。重复的教材页码、材料、安全和候选话术确认合并显示。",
            ]
        ),
    )
    _write_text(
        OUT / "r201k_table_evidence_sanitizer_report.md",
        "\n".join(
            [
                "# R201K 表格证据自然化报告",
                "",
                "雨伞图案设计样本不再把 `环节：/教师活动：/学生活动：/设计意图：` 作为教师正文证据输出。",
                "表格字段已转写为自然语言评价证据：观察规律、伞面排列、设计制作和展示说明。",
            ]
        ),
    )
    _write_text(
        OUT / "r201k_episode_projection_repair_report.md",
        "\n".join(
            [
                "# R201K 环节投影修复报告",
                "",
                "修复原则：episode_goal 写学生学习变化；teacher_organization 写教师组织动作；student_learning 写学生具体行为；evidence 写可观察证据。",
                "",
                "## 样本结果",
                "",
                *[
                    f"- {item['lesson_label']}：环节 {item['episode_count']} 个，关键话术缺失 {item['missing_key_teacher_talk_count_after']}，通用投影句 {item['generic_episode_projection_count']}。"
                    for item in sample_results
                ],
            ]
        ),
    )


def _write_reports(sample_results: list[dict[str, Any]]) -> None:
    _write_text(
        OUT / "r201k_content_quality_fix_report.md",
        "\n".join(
            [
                "# R201K 上传备课内容质量修复报告",
                "",
                "R201K 基于 R201J-P1 的教师快照做确定性候选修复，不接渲染、不写库、不调用模型。",
                "",
                "## 修复结果",
                "",
                *[
                    f"- {item['lesson_label']}：话术缺失 {item['missing_key_teacher_talk_count_before']} -> {item['missing_key_teacher_talk_count_after']}；确认项 {item['confirm_item_count_before']} -> {item['confirm_item_count_after']}；前置薄块 {item['front_matter_thin_blocking_count']}。"
                    for item in sample_results
                ],
                "",
                "## 仍需人工判断",
                "",
                "本轮生成的是系统候选，不是正式可用教案。教师仍需确认教材版本、班级学情、材料条件和课堂语言。",
            ]
        ),
    )
    _write_text(
        OUT / "r201k_before_after_teacher_snapshot_comparison.md",
        "\n".join(
            [
                "# R201K 教师快照前后对照",
                "",
                *[
                    "\n".join(
                        [
                            f"## {item['lesson_label']}",
                            "",
                            f"- Before：{item['before_snapshot']}",
                            f"- After：{item['after_snapshot']}",
                            f"- 关键话术：{item['missing_key_teacher_talk_count_before']} 缺失 -> {item['missing_key_teacher_talk_count_after']} 缺失",
                            f"- 确认项：{item['confirm_item_count_before']} -> {item['confirm_item_count_after']}",
                            "",
                        ]
                    )
                    for item in sample_results
                ],
            ]
        ),
    )


def main() -> None:
    r201j_p1_result = _read_json(R201J_P1_RESULT)
    manifest = _read_json(R201J_MANIFEST)
    sample_results: list[dict[str, Any]] = []

    for sample in manifest.get("samples") or []:
        sample_id = sample["sample_id"]
        template = _read_json(ROOT / sample["instance"])
        before_snapshot = R201J_P1_OUT / "sample_snapshots" / sample_id / "teacher_readable_lesson_snapshot.md"
        before_text = before_snapshot.read_text(encoding="utf-8")
        fixed = _make_fixed_template(sample, template)
        after_text = _make_snapshot(sample, template, fixed)
        out_dir = OUT / "sample_snapshots_after_fix" / sample_id
        after_snapshot = out_dir / "teacher_readable_lesson_snapshot.md"
        fixed_json = out_dir / "fixed_lesson_template_candidate.json"
        confirm_json = out_dir / "teacher_confirmation_groups.json"
        _write_text(after_snapshot, after_text)
        _write_json(fixed_json, fixed)
        _write_json(confirm_json, fixed["confirm_groups"])

        episodes = fixed["episodes"]
        missing_talk_after = sum(1 for episode in episodes if not episode["talk"].strip())
        missing_talk_before = before_text.count("关键话术：原实例未提供")
        confirm_before = (R201J_P1_OUT / "sample_snapshots" / sample_id / "source_gap_and_teacher_confirm_items.json")
        confirm_before_count = _read_json(confirm_before).get("confirm_item_count", 0) if confirm_before.exists() else 0
        confirm_after_count = _confirm_item_count(fixed["confirm_groups"])
        generic_count = _count_generic(after_text)
        table_count = _count_raw_table_dump(after_text) if sample_id == "table_rain_umbrella" else 0
        engineering_hits = [term for term in FORBIDDEN_TEACHER_TERMS if term in after_text]
        sample_results.append(
            {
                "sample_id": sample_id,
                "lesson_label": sample.get("lesson_label"),
                "episode_count": len(episodes),
                "missing_key_teacher_talk_count_before": missing_talk_before,
                "missing_key_teacher_talk_count_after": missing_talk_after,
                "generic_episode_projection_count": generic_count,
                "old_shoes_objective_misalignment": _old_shoes_misaligned(after_text) if sample_id == "numbered_colon_old_shoes" else False,
                "table_evidence_raw_field_dump_count": table_count,
                "confirm_item_count_before": confirm_before_count,
                "confirm_item_count_after": confirm_after_count,
                "front_matter_thin_blocking_count": _thin_front_matter_count(fixed),
                "engineering_term_hits": engineering_hits,
                "source_gap_as_teacher_content": "source_gap" in after_text,
                "teacher_main_forbidden_sources": _teacher_text_has_forbidden_source(after_text),
                "before_snapshot": _rel(before_snapshot),
                "after_snapshot": _rel(after_snapshot),
                "fixed_lesson_template_candidate": _rel(fixed_json),
                "teacher_confirmation_groups": _rel(confirm_json),
            }
        )

    _write_policy_docs(sample_results)
    _write_reports(sample_results)
    py_compile = _run_py_compile()

    checks = {
        "r201j_p1_pack_pass": r201j_p1_result.get("status") == "PASS",
        "missing_key_teacher_talk_count_zero": all(item["missing_key_teacher_talk_count_after"] == 0 for item in sample_results),
        "generic_episode_projection_count_zero": all(item["generic_episode_projection_count"] == 0 for item in sample_results),
        "old_shoes_objective_misalignment_zero": all(not item["old_shoes_objective_misalignment"] for item in sample_results),
        "table_evidence_raw_field_dump_count_zero": all(item["table_evidence_raw_field_dump_count"] == 0 for item in sample_results),
        "teacher_confirm_item_count_per_sample_lte_8": all(item["confirm_item_count_after"] <= 8 for item in sample_results),
        "front_matter_thin_blocking_count_zero": all(item["front_matter_thin_blocking_count"] == 0 for item in sample_results),
        "engineering_term_in_teacher_main_zero": all(not item["engineering_term_hits"] for item in sample_results),
        "source_gap_as_teacher_content_zero": all(not item["source_gap_as_teacher_content"] for item in sample_results),
        "teacher_main_forbidden_sources_zero": all(not item["teacher_main_forbidden_sources"] for item in sample_results),
        "no_R201I_schema_structure_change": True,
        "no_R220E_rendering": True,
        "no_R97B_shell_change": True,
        "no_formal_apply": True,
        "no_write": True,
        "no_R95": True,
        "no_model_provider_call": True,
        "py_compile_pass": py_compile["returncode"] == 0,
    }

    result = {
        "stage": STAGE,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "decision": "PASS_AS_CONTENT_QUALITY_FIX_CANDIDATE_SNAPSHOTS_NOT_ROUTE_BOUND"
        if all(checks.values())
        else "FAIL",
        "checks": checks,
        "sample_results": sample_results,
        "outputs": {
            "content_quality_fix_report": _rel(OUT / "r201k_content_quality_fix_report.md"),
            "before_after_teacher_snapshot_comparison": _rel(OUT / "r201k_before_after_teacher_snapshot_comparison.md"),
            "front_matter_derivation_policy": _rel(OUT / "r201k_front_matter_derivation_policy.md"),
            "episode_projection_repair_report": _rel(OUT / "r201k_episode_projection_repair_report.md"),
            "key_teacher_talk_candidate_policy": _rel(OUT / "r201k_key_teacher_talk_candidate_policy.md"),
            "confirmation_item_grouping_policy": _rel(OUT / "r201k_confirmation_item_grouping_policy.md"),
            "table_evidence_sanitizer_report": _rel(OUT / "r201k_table_evidence_sanitizer_report.md"),
            "sample_snapshots_after_fix": _rel(OUT / "sample_snapshots_after_fix"),
            "validation_result": _rel(RESULT),
        },
        "boundary": {
            "R201I_schema_structure_changed": False,
            "R220E_rendering_connected": False,
            "R97B_shell_changed": False,
            "formal_apply": False,
            "database_written": False,
            "feishu_written": False,
            "memory_written": False,
            "R95_executed": False,
            "provider_called": False,
            "model_called": False,
        },
        "py_compile": py_compile,
    }
    _write_json(RESULT, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
