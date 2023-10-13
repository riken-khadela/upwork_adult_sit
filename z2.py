from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("start-maximized")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-data-dir=/home/dell/.config/google-chrome')
options.add_argument('--profile-directory=Default')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
driver.get( 'https://www.google.com' ) 
print(driver.current_url)
breakpoint()