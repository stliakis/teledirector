With **TelegramDirector** you can create super simple telegram bot that executes custom server side commands

**How to**

First create a telegram bot via the telegram app. Search for the "botfather" bot on telegram, and create a new bot by typing /newbot and following the instructions, remember to save to bot token.

When you have the token then install the teledirector package

`pip install git+https://github.com/stliakis/teledirector.git --upgrade`

and write some commands

```python

import os

from teledirector import TelegramDirector, RedisDirectorHub

director = TelegramDirector("your token",
                            hub=RedisDirectorHub("localhost:6379"))


@director.register(["restart nginx"], description="Restarts nginx server")
def _(message):
    message.reply_text("shell: " + str(os.system('sudo service nginx restart')))


@director.register(["update"], description="Updates the git repo")
def _(message):
    message.reply_text("shell: " + str(os.system('cd /home/stefanos/Desktop;touch test;')))


director.start()


```


By using a hub you can collect all the chat ids that are active and send messages on demand

```python
director = TelegramDirector("your token",
                            hub=RedisDirectorHub("localhost:6379"))

director.send_message("The limit has been reached")
```