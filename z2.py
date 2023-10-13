import undetected_chromedriver as uc
options = uc.ChromeOptions()

# setting profile
options.add_argument("start-maximized")
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
# use specific (older) version
driver = uc.Chrome(
    options = options , version_main = 116
    )  # version_main allows to specify your chrome version instead of following chrome global version
driver.set_page_load_timeout(30)
driver.get( 'https://nowsecure.nl' ) 
print(driver.current_url)
breakpoint()