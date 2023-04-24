from .data_source import getData, buildMessage
import re
from hoshino import Service,priv
from hoshino.typing import CQEvent

sv_help='''
        动漫人物识别[图片] --搜索并返回一个动漫人物
        动漫人物多样识别 [图片] --返回多个人物
        GAL人物识别 [图片] --搜索并返回一个游戏人物
        GAL人物多样识别 [图片] --返回多个人物
        可对他人图片回复相关指令直接查询
'''.strip()


sv = Service('魔改版动漫人物搜索',enable_on_default=True,help_=sv_help,use_priv=priv.NORMAL)

async def get_search(bot,ev,model):
    ret = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
    pic_url = ret.group(2)
    result = await getData(pic_url, model, 0)
    message = buildMessage(result, 0, model)
    if len(result['data']) == 0:
        if model=="anime":
            await bot.send(ev, "抱歉图片中未识别到动漫人物")
        else:
            await bot.send(ev, "抱歉图片中未识别到游戏人物")
        return
    await bot.send(ev, "感谢使用AnimeTrace动漫查询引擎，您的图片预测结果是\n" + str(message) + "共预测到" + str(
        len(result['data'])) + "个角色\n" + "感谢使用，支持列表请到官网查看!")

async def get_searchall(bot,ev,model):
    ret = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
    pic_url = ret.group(2)
    result = await getData(pic_url, model, 1)
    message = buildMessage(result, 1, model)
    if len(result['data']) == 0:
        if model == "anime":
            await bot.send(ev, "抱歉图片中未识别到动漫人物")
        else:
            await bot.send(ev, "抱歉图片中未识别到游戏人物")
        return
    await bot.send_group_forward_msg(group_id=ev.group_id, messages=message)


@sv.on_keyword(('动漫人物识别'))
async def handle_event(bot, ev: CQEvent):
    if ev.message[0].type == "reply":
        msg = await bot.get_msg(message_id=int(ev.message[0].data['id']))
        ev.message = msg["message"]
        await get_search(bot, ev, "anime")
    else:
        await get_search(bot, ev, "anime")


@sv.on_keyword(('动漫人物多样识别'))
async def handle_event(bot,ev:CQEvent):
    if ev.message[0].type == "reply":
        msg = await bot.get_msg(message_id=int(ev.message[0].data['id']))
        ev.message = msg["message"]
        await get_searchall(bot,ev,"anime")
    else:
        await get_searchall(bot,ev,"anime")

@sv.on_keyword(('GAL人物识别'))
async def handle_event_gal(bot, ev: CQEvent):
    if ev.message[0].type == "reply":
        msg = await bot.get_msg(message_id=int(ev.message[0].data['id']))
        ev.message = msg["message"]
        await get_search(bot, ev, "game")
    else:
        await get_search(bot, ev, "game")

@sv.on_keyword((('GAL人物多样识别')))
async def handle_event_gal(bot, ev:CQEvent):
    if ev.message[0].type == "reply":
        msg = await bot.get_msg(message_id=int(ev.message[0].data['id']))
        ev.message = msg["message"]
        await get_searchall(bot, ev, "game")
    else:
        await get_searchall(bot, ev, "game")

