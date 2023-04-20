from .data_source import getData, buildMessage
import re
from hoshino import Service,priv
from hoshino.typing import CQEvent

sv_help='''
        动漫人物识别[图片] --搜索并返回一个动漫人物
        多可能动漫人物识别 [图片] --返回多个人物
        GAL人物识别 [图片] --搜索并返回一个游戏人物
        多可能GAL人物识别 [图片] --返回多个人物
'''.strip()


sv = Service('魔改版动漫人物搜索',enable_on_default=True,help_=sv_help,use_priv=priv.NORMAL)


@sv.on_prefix(('动漫人物识别'))
async def handle_event(bot, ev: CQEvent):
    ret = re.match(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
    pic_url = ret.group(2)
    result = await getData(pic_url, "anime", 0)
    message = buildMessage(result, 0, "anime")
    if len(result['data']) == 0:
        await bot.send(ev,"抱歉图片中未识别到动漫人物")
        return
    await bot.send(ev,"感谢使用AnimeTrace动漫查询引擎，您的图片预测结果是\n" + str(message) + "共预测到" + str(
        len(result['data'])) + "个角色\n" + "感谢使用，支持列表请到官网查看!")

@sv.on_prefix(('多可能动漫人物识别'))
async def handle_event(bot,ev:CQEvent):
    ret = re.match(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
    pic_url = ret.group(2)
    result = await getData(pic_url, "anime", 1)
    message = buildMessage(result, 1, "anime")
    if len(result['data']) == 0:
        await bot.send(ev,"抱歉图片中未识别到动漫人物")
        return
    await bot.send_group_forward_msg(group_id=ev.group_id, messages=message)

@sv.on_prefix(('GAL人物识别'))
async def handle_event_gal(bot, ev: CQEvent):
    ret = re.match(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
    pic_url = ret.group(2)
    result = await getData(pic_url, "game", 0)
    message = buildMessage(result, 0, "game")
    if len(result['data']) == 0:
        await bot.send(ev,"抱歉图片中未识别到游戏人物")
        return
    await bot.send(ev,"感谢使用AnimeTrace动漫查询引擎，您的图片预测结果是\n" + str(message) + "共预测到" + str(
        len(result['data'])) + "个角色\n" + "感谢使用，支持列表请到官网查看!")

@sv.on_prefix((('多可能GAL人物识别')))
async def handle_event_gal(bot, ev:CQEvent):
    ret = re.match(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
    pic_url = ret.group(2)
    result = await getData(pic_url, "game", 1)
    message = buildMessage(result, 1, "game")
    if len(result['data']) == 0:
        await bot.send(ev,"抱歉图片中未识别到游戏人物")
        return
    await bot.send_group_forward_msg(group_id=ev.group_id, messages=message)

