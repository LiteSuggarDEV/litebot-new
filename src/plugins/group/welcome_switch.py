from nonebot import get_driver, on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
)
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

from litebot_utils.models import GroupConfig
from litebot_utils.rule import is_group_admin
from src.plugins.menu.manager import MatcherData

command_start = get_driver().config.command_start

welcome_switch = on_command(
    "welcome",
    state=MatcherData(
        rm_name="切换LiteBot成员变动监听状态",
        rm_desc="切换LiteBot成员变动监听状态",
        rm_usage="welcome on/off",
    ).model_dump(),
)

@welcome_switch.handle()
async def _(
    event: GroupMessageEvent, matcher: Matcher, bot: Bot, arg: Message = CommandArg()
):
    if not await is_group_admin(event, bot):
        return
    """开关"""
    # 获取当前群组的开关状态
    gid = event.group_id
    str_arg = arg.extract_plain_text().strip()
    group_config, _ = await GroupConfig.get_or_create(group_id=gid)
    # 切换开关状态
    if not str_arg:
        await matcher.send(
            f"成员变动提醒已 {'开启' if group_config.welcome else '关闭'} ！"
        )
    elif str_arg in ("on", "enable", "开启"):
        group_config.welcome = True
        await group_config.save()
        await matcher.send("成员变动提醒已开启！")
    elif str_arg in ("off", "disable", "关闭"):
        group_config.welcome = False
        await group_config.save()
        await matcher.send("成员变动提醒已关闭！")
    else:
        await matcher.finish("请输入 on/off 来开启或关闭！")
