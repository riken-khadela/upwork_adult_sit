from bot import scrapping_bot

bot = scrapping_bot(brazzers_bot=True)
bot.brazzers_delete_old_videos()
bot.starting_brazzers_bots()
bot.connect_cyberghost_vpn()
if bot.brazzers_login() :
    bot.brazzers_get_categories()
    bot.brazzers_get_videos_url()
    bot.brazzers_download_video()

bot.CloseDriver()