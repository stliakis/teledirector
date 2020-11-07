import os

from teledirector import TelegramDirector, RedisDirectorHub

director = TelegramDirector("put your bot token here",
                            hub=RedisDirectorHub("localhost:6379"))


@director.register(["restart nginx"], description="Restarts nginx server")
def _(message):
    message.reply_text("shell: " + str(os.system('sudo service nginx restart')))


@director.register(["update"], description="Updates the git repo")
def _(message):
    message.reply_text("shell: " + str(os.system('cd /home/stefanos/Desktop;touch test;')))


director.start()
