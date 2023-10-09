from bot import scrapping_bot

# user credentials
login_id= 'love4porn'
password_id = 'Skjcv9sdflj27'

bot = scrapping_bot(brazzers_bot=True)
bot.starting_brazzers_bots()
# bot.connect_cyberghost_vpn()
bot.brazzers_login(username=login_id,password = password_id)
bot.get_categories()
bot.get_videos_url()
bot.brazzers_download_video(video_url='https://site-ma.brazzers.com/scene/9426051/what-hubby-doesnt-know')

bot.CloseDriver()