from teledirector import TelegramDirector, RedisDirectorHub

director = TelegramDirector("put your bot token here",
                            hub=RedisDirectorHub("localhost:6379"))

director.send_message("statistics", "statistics")
