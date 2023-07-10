# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *


@plugins.register(
    name="Hello",
    desire_priority=-1,
    hidden=True,
    desc="A simple plugin that says hello",
    version="0.1",
    author="lanvent",
)
class Hello(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[Hello] inited")

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT,
            ContextType.JOIN_GROUP,
            ContextType.PATPAT,
            ContextType.ADD_FRIEND,
        ]:
            return

        if e_context["context"].type == ContextType.JOIN_GROUP:
            e_context["context"].type = ContextType.TEXT
            msg: ChatMessage = e_context["context"]["msg"]
            e_context["context"].content = f'请你随机使用一种风格说一句问候语来欢迎新用户"{msg.actual_user_nickname}"加入群聊。'
            e_context.action = EventAction.BREAK  # 事件结束，进入默认处理逻辑
            return

        # if e_context["context"].type == ContextType.PATPAT:
        #     e_context["context"].type = ContextType.TEXT
        #     msg: ChatMessage = e_context["context"]["msg"]
        #     e_context["context"].content = f"请你随机使用一种风格介绍你自己，并告诉用户输入#help可以查看帮助信息。"
        #     e_context.action = EventAction.BREAK  # 事件结束，进入默认处理逻辑
        #     return
                    
        # if e_context["context"].type == ContextType.ADD_FRIEND:
        #     e_context["context"].type = ContextType.TEXT
        #     msg: ChatMessage = e_context["context"]["msg"]
        #     e_context["context"].content = f"请你随机使用一种风格说一句问候语来欢迎新用户添加你为好友。再请你随机使用一种风格介绍你自己。"
        #     e_context.action = EventAction.BREAK  # 事件结束，进入默认处理逻辑
        #     return

        if e_context["context"].type == ContextType.ADD_FRIEND:
            reply = Reply()
            reply.type = ReplyType.TEXT
            msg: ChatMessage = e_context["context"]["msg"]
            reply.content = f"你好, {msg.from_user_nickname}！\n" \
               "我是ALLinAI班主任的数字分身，任何关于数字分身和ChatGPT账号相关业务都可以与我交流。\n" \
               "1、链接页有多种联系我们的方式，包括班主任本人企业微信： \n" \
               "https://mp.weixin.qq.com/s/1v5CfgsUiUhdWKipUmJY5g\n" \
               "2、数字分身详细介绍：\n" \
               "https://mp.weixin.qq.com/s/618i8cX--qYKvLbaHgZipA\n" \
               "3、ChatGPT账号服务和AI新人速成班培训介绍：\n" \
               "https://mp.weixin.qq.com/s/7IyZF0j_nl9urszadOB_PA\n" \
               "4、体验数字分身和ChatGPT中文站：\n" \
               "https://gpt.chayinzi.biz\n" \
               "体验方法：\n" \
               "注册登录>应用>应用市场>选择相关数字分身或ChatGPT中文\n" \
               "更多，请从“ALLinAI商业先机”公众号了解。\n" \
               "任何问题，开始与我交流吧"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

        content = e_context["context"].content
        logger.debug("[Hello] on_handle_context. content: %s" % content)
        if content == "Hello":
            reply = Reply()
            reply.type = ReplyType.TEXT
            msg: ChatMessage = e_context["context"]["msg"]
            if e_context["context"]["isgroup"]:
                reply.content = f"Hello, {msg.actual_user_nickname} from {msg.from_user_nickname}"
            else:
                reply.content = f"Hello, {msg.from_user_nickname}"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

        if content == "Hi":
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = "Hi"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK  # 事件结束，进入默认处理逻辑，一般会覆写reply

        if content == "End":
            # 如果是文本消息"End"，将请求转换成"IMAGE_CREATE"，并将content设置为"The World"
            e_context["context"].type = ContextType.IMAGE_CREATE
            content = "The World"
            e_context.action = EventAction.CONTINUE  # 事件继续，交付给下个插件或默认逻辑

    def get_help_text(self, **kwargs):
        help_text = "输入Hello，我会回复你的名字\n输入End，我会回复你世界的图片\n"
        return help_text
