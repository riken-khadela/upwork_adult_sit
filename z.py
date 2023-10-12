from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("start-maximized")
options.add_argument('--headless')


for _ in range(30):
    try:
        # driver = webdriver.Chrome(executable_path='/home/dell/Desktop/upwork/brazzers/chromedriver',options=options)
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        driver.get('https://site-ma.brazzers.com/login')
        driver.current_url
        break
    except Exception as e:
        print(e)
                
print(driver.execute_script(" var network = performance.getEntries() || {}; return network;"))
breakpoint()
driver.quit()
