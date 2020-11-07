import re

from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext


class TelegramDirector(object):
    commands = []

    def __init__(self, bot_token, allowed_users=None, hub=None):
        self.bot_token = bot_token
        self.allowed_users = allowed_users
        self.bot = Bot(bot_token)
        self.hub = hub

        self.commands = [
            DirectorCommand(
                ["help", "help me"],
                lambda message: self.command_help(message, self.commands),
                description="Prints the commands list"
            ),
            DirectorCommand(
                ["hi", "hello"],
                lambda message: self.command_hi(message),
                description="Registers this chat to the main hub"
            ),
            DirectorCommand(
                ["good by", "shut up", "close"],
                lambda message: self.command_good_by(message),
                description="Removes this chat from all the hubs"
            ),
            DirectorCommand(
                ["subscribe (.*)", "join (.*)"],
                lambda message, command_variables: self.command_subscribe(message, command_variables),
                description="Subscribes this chat to a hub",
                regex_commands=True
            ),
            DirectorCommand(
                ["unsubscribe (.*)", "leave (.*)"],
                lambda message, command_variables: self.command_unsubscribe(message, command_variables),
                description="Unsubscribes this chat from a hub",
                regex_commands=True
            )
        ]

    def get_chat_ids(self):
        print(self.bot.getChat())

    def send_message(self, message, hub_name="main"):
        if not self.hub:
            raise Exception("You need to setup a hub in order to send messages")

        chat_ids = self.hub.get_chat_ids(hub_name)
        print("sending message to chats(hub=%s): %s" % (hub_name, chat_ids))
        for chat_id in map(int, chat_ids):
            self.bot.send_message(chat_id, message)

    def message_process(self, update: Update, context: CallbackContext) -> None:
        user_id = update.message.from_user.id
        chat_id = update.message.chat_id

        print("got message, user=%s, chat=%s" % (user_id, chat_id))
        if self.allowed_users:
            if user_id not in self.allowed_users:
                print("non allowed user tried to send a message %s" % update.message.text)
                return

        for command in self.commands:
            matches = command.matches(update.message.text)
            if matches:
                if matches is True:
                    command.func(update.message)
                else:
                    command.func(update.message, matches)
                return

        update.message.reply_text("unknown command")

    def register(self, commands, description=None, regex_commands=False):
        def wrapper(func):
            self.commands.append(
                DirectorCommand(commands, func, description=description, regex_commands=regex_commands)
            )

        return wrapper

    def command_help(self, message, commands):
        help_text = ""
        for command in commands:
            help_text += "*{command}* \-\> {description}\n".format(command=command.commands,
                                                                   description=command.description or "?")

        message.reply_markdown_v2(help_text)

    def command_hi(self, message):
        hub_name = "main"

        if self.hub:
            self.hub.add_chat_id(message.chat_id)

            return message.reply_text("hello there, your chat(%s) has been registered to the %s hub" % (
                message.chat_id, hub_name
            ))
        else:
            return message.reply_text("hello there, this Telegram Director does not have any hubs" % (
                message.chat_id
            ))

    def command_good_by(self, message):
        if self.hub:
            self.hub.remove_chat_id_from_all_hubs(message.chat_id)

        return message.reply_text("good by %s" % (
            message.from_user.first_name
        ))

    def command_subscribe(self, message, matched_groups):
        if self.hub:
            self.hub.add_chat_id(message.chat_id, matched_groups[0])
            message.reply_text("subscribed to %s hub" % (
                matched_groups[0]
            ))
        else:
            message.reply_text("this Telegram Director does not have any hubs")

    def command_unsubscribe(self, message, matched_groups):
        if self.hub:
            self.hub.remove_chat_id(message.chat_id, matched_groups[0])
            message.reply_text("unsubscribed from %s hub" % (matched_groups[0]))
        else:
            message.reply_text("this Telegram Director does not have any hubs")

    def start(self):
        updater = Updater(bot=self.bot, use_context=True)

        dispatcher = updater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.text, self.message_process))

        updater.start_polling()

        updater.idle()


class DirectorCommand(object):

    def __init__(self, commands, func, description=None, regex_commands=False):
        self.commands = commands
        self.func = func
        self.description = description
        self.regex_commands = regex_commands

    def matches(self, input):
        for command in self.commands:
            match = re.match(command, input)
            if match:
                if self.regex_commands:
                    return list(match.groups())
                else:
                    return True
        return False
