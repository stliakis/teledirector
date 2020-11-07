from teledirector import TelegramDirector, RedisDirectorHub

bot_token = "token"

director = TelegramDirector("put your bot token here",
                            hub=RedisDirectorHub("localhost:6379"))

director.send_message("statistics", "statistics")
