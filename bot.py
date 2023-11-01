import os,shutil, pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,NoSuchElementException,WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver  
import requests
import json, random, time, pandas as pd, os, sys
from datetime import datetime, timedelta
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from main.models import configuration

class scrapping_bot():
    
    def __init__(self,brazzers_bot = False):
        with open('configrations.json', 'r') as json_file:    
            self.config_data = json.load(json_file)
        configs = configuration.objects.get(website_name='brazzers')
        if brazzers_bot == True:
            self.category = str(configs.category)
            old_days = str(configs.more_than_old_days_download)
            self.download_videos_count = int(configs.numbers_of_download_videos)
            self.username = str(configs.username)
            self.password = str(configs.password)
            self.delete_old_days = str(configs.delete_old_days)
            self.calculate_old_date(int(old_days))

            self.brazzers_delete_old_videos()
            self.downloaded_videos_list = os.listdir('downloads')
            self.videos_collection = []
            self.videos_collection = pd.read_csv(os.path.join(os.getcwd(),'brazzers_videos_details.csv'))
            if "Category" not in self.videos_collection.columns:
                # Create the "Category" column without adding values to rows
                self.videos_collection["Category"] = None
                self.videos_collection.to_csv(os.path.join(os.getcwd(),'brazzers_videos_details.csv'),index=False)
                self.videos_collection = pd.read_csv(os.path.join(os.getcwd(),'brazzers_videos_details.csv'))
                
            self.videos_collection = self.videos_collection.to_dict(orient='records')

            self.videos_data = []
            self.videos_data = pd.read_csv(os.path.join(os.getcwd(),'brazzers_videos.csv'))
            self.videos_data = self.videos_data.to_dict(orient='records')

            self.videos_urls = []
            self.brazzers_category_url = 'https://site-ma.brazzers.com/categories'

    def get_driver(self,add_cybeghost=False):
        """Start webdriver and return state of it."""
        from selenium.webdriver.chrome.options import Options
        options = Options()

        options = uc.ChromeOptions()
        options.add_argument('--lang=en')  # Set webdriver language to English.
        options.add_argument('log-level=3')  # No logs is printed.
        options.add_argument('--mute-audio')  # Audio is muted.
        options.add_argument("--enable-webgl-draft-extensions")
        options.add_argument('--mute-audio')
        options.add_argument("--ignore-gpu-blocklist")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        prefs = {"credentials_enable_service": True,
                 "download.default_directory" : f"{os.path.join(os.getcwd(),'downloads')}",
            'download.prompt_for_download': False,  # Optional, suppress download prompt
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True ,
            "profile.password_manager_enabled": True}
        options.add_experimental_option("prefs", prefs)
        if add_cybeghost :
            options.add_extension('./Stay-secure-with-CyberGhost-VPN-Free-Proxy.crx')#crx file path
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')    
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--enable-javascript")
        options.add_argument("--enable-popup-blocking")
        for _ in range(30):
            try:
                driver = webdriver.Chrome(options=options)
                driver.get('https://site-ma.brazzers.com/store')
                break
            except Exception as e:
                print(e)
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
        self.driver = driver
        return self.driver
    
    def connect_vpn(self,vpn_country):
        
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get('chrome-extension://ffbkglfijbcbgblgflchnbphjdllaogb/index.html')
        time.sleep(3)

        # Disconnect if already connected
        connected_btn = self.driver.find_elements(By.CLASS_NAME, 'dark outer-circle connected')
        time.sleep(1)
        connected_btn[0].click() if connected_btn else None
        time.sleep(2)

        # Select country
        countries_drop_down_btn = self.driver.find_elements(By.TAG_NAME, 'mat-select-trigger')
        time.sleep(1)
        countries_drop_down_btn[0].click() if countries_drop_down_btn else None
        time.sleep(2)
        total_option_country = self.driver.find_elements(By.TAG_NAME, 'mat-option')
        for i in total_option_country:
            i_id = i.get_attribute('id')
            time.sleep(1)
            country_text_ele = i.find_element(By.XPATH, f"//*[@id='{i_id}']/span")
            
            country_text = country_text_ele.text
            time.sleep(1)
            # checking if the country is whether same or not and click on it
            if vpn_country == country_text:
                time.sleep(1)
                print('connected country is :',vpn_country)
                country_text_ele.click()
                break
        time.sleep(3)
        # Checking is the VPN connected or not
        connect_btn = self.driver.find_element(By.XPATH, '//div[@class="dark disconnected outer-circle"]')
        connect_btn.click()
        time.sleep(4)
      
    def delete_cache_folder(self,folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print("Cache folder deleted successfully.")
        else:
            print("Cache folder not found.")

    def find_element(self, element, locator, locator_type=By.XPATH,
            page=None, timeout=10,
            condition_func=EC.presence_of_element_located,
            condition_other_args=tuple()):
        """Find an element, then return it or None.
        If timeout is less than or requal zero, then just find.
        If it is more than zero, then wait for the element present.
        """
        try:
            if timeout > 0:
                wait_obj = WebDriverWait(self.driver, timeout)
                ele = wait_obj.until(EC.presence_of_element_located((locator_type, locator)))
                # ele = wait_obj.until( condition_func((locator_type, locator),*condition_other_args))
            else:
                print(f'Timeout is less or equal zero: {timeout}')
                ele = self.driver.find_element(by=locator_type,
                        value=locator)
            if page:
                print(
                    f'Found the element "{element}" in the page "{page}"')
            else:
                print(f'Found the element: {element}')
            return ele
        except (NoSuchElementException, TimeoutException) as e:
            if page:
                print(f'Cannot find the element "{element}"'
                        f' in the page "{page}"')
            else:
                print(f'Cannot find the element: {element}')
                
    def click_element(self, element, locator, locator_type=By.XPATH,
            timeout=10):
        """Find an element, then click and return it, or return None"""
        ele = self.find_element(element, locator, locator_type, timeout=timeout)
        
        if ele:
            self.driver.execute_script('arguments[0].scrollIntoViewIfNeeded();',ele)
            ele.click()
            print(f'Clicked the element: {element}')
            return ele

    def input_text(self, text, element, locator, locator_type=By.XPATH,
            timeout=10, hide_keyboard=True):
        """Find an element, then input text and return it, or return None"""
        
        ele = self.find_element(element, locator, locator_type=locator_type,
                timeout=timeout)
        
        if ele:
            for i in range(3):
                try: 
                    ele.send_keys(text)
                    print(f'Inputed "{text}" for the element: {element}')
                    return ele    
                except ElementNotInteractableException :...
    
    def ScrollDown(self,px):
        self.driver.execute_script(f"window.scrollTo(0, {px})")
    
    def ensure_click(self, element):
        try:
            element.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", element)
    
    def new_tab(self):
        self.driver.find_element(By.XPATH,'/html/body').send_keys(Keys.CONTROL+'t')

    def random_sleep(self,a=3,b=7):
        random_time = random.randint(a,b)
        print('time sleep randomly :',random_time)
        time.sleep(random_time)

    def getvalue_byscript(self,script = '',reason=''):
        """made for return value from ele or return ele"""
        if reason :print(f'Script execute for : {reason}')
        else:
            print(f'execute_script : {script}')
        value = self.driver.execute_script(f'return {script}')  
        return value
        
    def CloseDriver(self):
        try: 
            self.driver.quit()
            print('Driver is closed !')
        except Exception as e: ...
        
    def calculate_old_date(self, days = 30) : 
        """ get old date from today's by the accepting date and return datetime object"""
        today = datetime.now()
        self.old_date = today - timedelta(days=days)
        return self.old_date

    def date_older_or_not(self,date_string=''):
        if date_string :  
            date_obj = datetime.strptime(date_string, "%b %d, %Y")
            if date_obj < self.old_date :
                return True 
        return False

    def starting_brazzers_bots(self):
        self.get_driver(add_cybeghost=True)

    def connect_cyberghost_vpn(self,vpn_country='Netherlands'):
        vpn_country_list = ['Romania','Netherlands','United States']
        vpn_country = random.choice(vpn_country_list)
        for  _ in range(3):
            self.driver.get('chrome-extension://ffbkglfijbcbgblgflchnbphjdllaogb/index.html')
            self.random_sleep()

            # Disconnect if already connected
            connected_btn = self.find_element('connected vpn circle','/html/body/app-root/main/app-home/div/div[2]/app-switch/div')
            if connected_btn :
                if not "disconnected" in connected_btn.get_attribute('class') : 
                    self.click_element('connected vpn circle','/html/body/app-root/main/app-home/div/div[2]/app-switch/div')
                    self.random_sleep()
                else: 
                    self.random_sleep(5,10)

            self.driver.execute_script('document.querySelector("body > app-root > main > app-home > div > div.servers.en > mat-form-field > div > div.mat-form-field-flex.ng-tns-c19-0 > div").click()')
            self.driver.execute_script('document.querySelector("body > div.cdk-overlay-container > div.cdk-overlay-backdrop.cdk-overlay-transparent-backdrop.cdk-overlay-backdrop-showing").click()')
            
            drop_down_ = self.click_element('country drop down','mat-select-trigger',By.TAG_NAME)       
            if not drop_down_ : 
                self.CloseDriver()
                self.get_driver()
                continue

            # selecting the country
            total_option_country = self.driver.find_elements(By.TAG_NAME, 'mat-option')
            for i in total_option_country:
                i_id = i.get_attribute('id')
                country_text_ele = i.find_element(By.XPATH, f"//*[@id='{i_id}']/span")
                country_text = country_text_ele.text

                # checking if the country is whether same or not and click on it
                if vpn_country in country_text:
                    print('connected country is :',vpn_country)
                    country_text_ele.click()
                    break
            time.sleep(1)
            # Checking is the VPN connected or not
            self.click_element('Connecting vpn circle','//div[@class="dark disconnected outer-circle"]')
            self.random_sleep()
            connected_btn = self.find_element('connected vpn circle','/html/body/app-root/main/app-home/div/div[2]/app-switch/div')
            if connected_btn :
                if not "disconnected" in connected_btn.get_attribute('class') : 
                    return

    def find_and_delete_video(self,folder_path, video_title):
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                base_name, extension = os.path.splitext(filename)
                if base_name == video_title:
                    file_path = os.path.join(foldername, filename)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
        return

    def brazzers_login(self):
        first_time = False
        path = f"{os.getcwd()}/cookietest.json"
        if os.path.isfile(path):
            with open('cookietest.json','rb') as f:cookies = json.load(f)
            for item in cookies: self.driver.add_cookie(item)
            self.random_sleep()
        self.driver.get('https://site-ma.brazzers.com/store')
        while not self.driver.execute_script("return document.readyState === 'complete'"):pass
        
        self.random_sleep(5,7)
        if self.driver.current_url != "https://site-ma.brazzers.com/store":
            for _ in range(3):
                time.sleep(1.5)
                if not self.find_element('Login form','//*[@id="root"]/div[1]/div[1]/div/div/div/div/form/button') :
                    self.driver.refresh()
                if self.find_element('Login form','//*[@id="root"]/div[1]/div[1]/div/div/div/div/form/button') :
                    self.random_sleep(1,1)
                    self.input_text(self.username,'Username','username',By.NAME)
                    self.random_sleep(1,1)
                    self.input_text(self.password,'password','password',By.NAME)
                    self.random_sleep(1,1)
                    self.click_element('Submit','//button[@type="submit"]')
                    self.random_sleep(2,3)
                    for _ in range(4):
                        if "login" not in self.driver.current_url:
                            cookies = self.driver.get_cookies()
                            with open('cookietest.json', 'w', newline='') as outputdata:
                                json.dump(cookies, outputdata)
                            return True
                        self.random_sleep(2,3)
                self.driver.delete_all_cookies()
                self.driver.refresh()
            return False
        else :
            return True

    def brazzers_get_categories(self):
        if not self.driver.current_url.lower() == self.brazzers_category_url :
            self.driver.get(self.brazzers_category_url)

        found_category = False
        for i1 in range(1,6) :
            cate1 = self.find_element('category',f'//*[@id="root"]/div[1]/div[2]/div[3]/div[2]/div[2]/div[{i1}]/div/div/a',timeout= 1)
            if cate1 : 
                if cate1.text.lower() == self.category.lower() :
                    time.sleep(1)
                    cate1.click()
                    found_category = True
                    break 
        
        if found_category == False :
            for i2 in range(4,15):
                if self.find_element('catefory grid',f'//*[@id="root"]/div[1]/div[2]/div[3]/div[2]/div[{i2}]/div',timeout=5):
                    for i3 in range(1,6):
                        cate1 = self.find_element('category',f'//*[@id="root"]/div[1]/div[2]/div[3]/div[2]/div[{i2}]/div[{i3}]/div/div/a',timeout=1)
                        if cate1:
                            if cate1.text.lower() == self.category.lower() :
                                found_category = True
                                cate1.click()
                                break
                else : break
                if found_category == True : break
        if found_category == True : 
            return True
        else: 
            return False
        
    def brazzers_get_videos_url(self):
        df1 = pd.read_csv('brazzers_videos_details.csv')
        df_url = df1['Url'].values.tolist()
        page_number = 2
        driver_url = self.driver.current_url
        tags = driver_url.split('tags=')[-1]
        found_max_videos = self.download_videos_count * 1.5
        self.random_sleep(6,10)
        while True:
            try :
                for url_idx in range(1,24):
                    print(url_idx,'------------')
                    video_date = self.find_element(f'video : {url_idx}',f'/html/body/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/section/div/div[2]/div/div[{url_idx}]/div/div[2]/div[2]',timeout=3)
                    self.driver.execute_script("arguments[0].scrollIntoView();", video_date)
                    time.sleep(0.3)
                    if video_date :
                        if self.date_older_or_not(video_date.text) :
                            video_ele = self.find_element(f'Video number : {url_idx}',f'/html/body/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/section/div/div[2]/div/div[{url_idx}]/div/div[1]/a',timeout=3)
                            post_url = self.find_element('post url',f'/html/body/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/section/div/div[2]/div/div[{url_idx}]/div/div[1]/a/div[1]/div/picture/img',timeout=0)
                            if video_ele and post_url:
                                video_url = video_ele.get_attribute('href')
                                post_url = post_url.get_attribute('src')
                                if video_url and post_url and video_url not in df_url:
                                    self.videos_urls.append({"video_url":video_url,'post_url':post_url})
            except Exception as e :
                print(e) 
            if len(self.videos_urls) < found_max_videos :
                self.driver.get(f'https://site-ma.brazzers.com/scenes?page={page_number}&tags={tags}')
                page_number +=1
            else : break

    def brazzers_download_video(self):
        for idx,videoss_urll in enumerate(self.videos_urls) : 
            # if idx == 0: continue          
            master_url = []
            for _ in range(3):
                self.driver.get(videoss_urll['video_url'])
                self.random_sleep(10,15)
                networks_list = self.driver.execute_script(" var network = performance.getEntries() || {}; return network;")
                for i in networks_list :
                    if "mp4.urlset/master.m3u8" in i['name']:
                        master_url.append(i['name'])
                video_name = f"{self.driver.current_url.split('https://site-ma.brazzers.com/')[-1].replace('/','_').replace('-','_')}"
                if len(master_url) > 0: break
                else: continue

            v_urllll = f'http://159.223.134.27:8000/downloads/{video_name}.mp4'
            p_urllll = f'http://159.223.134.27:8000/downloads/{video_name}.jpg'
            if len(master_url) > 0 :
                tmp = {
                    "Likes" : "",
                    "Disclike" :"",
                    "Url" : videoss_urll['video_url'] ,
                    "video_download_url" : v_urllll,
                    "Title" : '',
                    "Discription" : "",
                    "Release-Date" : "",
                    "Poster-Image_uri" : videoss_urll['post_url'],
                    "poster_download_uri" : p_urllll,
                    "Video-name" : f'{video_name}.mp4',
                    "Photo-name" : f'{video_name}.jpg',
                    "Pornstarts" : ''
                }
                try:
                    response = requests.get(tmp['Poster-Image_uri'])
                    with open(f'downloads/{video_name}.jpg', 'wb') as f:f.write(response.content)
                    likes_count = self.find_element('Likes count','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[1]/div/section/div[3]/div[1]/div[7]/span[1]/strong')
                    if likes_count :
                        tmp['Likes'] = likes_count.text

                    likes_count = self.find_element('Likes count','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[1]/div/section/div[3]/div[1]/div[7]/span[1]/strong')
                    if likes_count :
                        tmp['Likes'] = likes_count.text
                    
                    # self.getvalue_byscript('document.querySelector("#root > div.sc-yo7o1v-0.hlvViO > div.sc-yo7o1v-0.hlvViO > div.sc-1fep8qc-0.ekNhDD > div.sc-1deoyo3-0.iejyDN > div:nth-child(1) > div > section > div.sc-1wa37oa-0.irrdH > div.sc-bfcq3s-0.ePiyNl > div.sc-k44n71-0.gbGmcO > span:nth-child(1) > strong").textContent')
                    Disclike_count = self.find_element('Disclike count','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[1]/div/section/div[3]/div[1]/div[7]/span[2]/strong')
                    if Disclike_count :
                        tmp['Disclike'] = Disclike_count.text

                    Title = self.find_element('Title','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[5]/div/section/div/div/h2[2]')
                    if Title :
                        tmp['Title'] = Title.text

                    Release = self.find_element('Release','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[5]/div/section/div/div/h2[1]')
                    if Release :
                        tmp['Release-Date'] = Release.text

                    Discription = self.find_element('Discription','/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[6]/div/section/div/p')
                    if Discription :
                        tmp['Discription'] = Discription.text

                    port_starts = self.find_element('pornstars','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[5]/div/section/div/div/div[2]/h2')
                    if port_starts :
                        tmp['Pornstarts'] = port_starts.text

                    self.click_element('download btn','//button[@class="sc-yox8zw-1 VZGJD sc-rco9ie-0 jnUyEX"]')
                    self.click_element('download high_quality','//div[@class="sc-yox8zw-0 cQnfGv"]/ul/div/button[1]')
                    new_video_download = ''
                    self.random_sleep(2,3)
                    seconds = 0
                    while seconds < 20 :
                        time.sleep(1)
                        new_video_download = [i for i in os.listdir('downloads')if i.endswith('.crdownload')]
                        if new_video_download:
                            new_video_download = new_video_download[0]
                            print('New video file name -----------------',new_video_download)
                            break
                        else:
                            seconds+=1

                    # if len(self.driver.window_handles) == 1:
                    #     self.driver.execute_script("window.open()")
                    #     self.driver.switch_to.window(self.driver.window_handles[-1])
                    #     self.driver.get('chrome://downloads')
                    # else:
                    #     self.driver.switch_to.window(self.driver.window_handles[-1])

                    
                    while True :
                        if os.path.isfile(f'downloads/{new_video_download}'):
                            sys.stdout.write("\rDownloding ...........")
                            sys.stdout.flush()
                        else:
                            sys.stdout.write("\rDownloding Complete...")
                            sys.stdout.flush()
                            self.random_sleep(3,5)
                            break
                        # download_progress = self.driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#progress").shadowRoot.querySelector("#primaryProgress")')
                        # download_progress = self.driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#description").textContent')
                        # if download_progress == "\n      \n    ":
                        #     break
                        # else:
                        time.sleep(0.5)
                    # self.driver.switch_to.window(self.driver.window_handles[0])
                    self.random_sleep(2,3)
                    os.rename(os.path.join(os.getcwd(),f'downloads/{new_video_download.replace(".crdownload","")}'),os.path.join(os.getcwd(),f'downloads/{video_name}.mp4')) 
                    self.videos_collection.append(tmp)
                    self.videos_data.append({ "Video-title" : video_name,"video_url" : v_urllll,"downloaded_time" : datetime.now()})
                    pd.DataFrame(self.videos_collection).to_csv(os.path.join(os.getcwd(),'brazzers_videos_details.csv'),index=False)
                    pd.DataFrame(self.videos_data).to_csv(os.path.join(os.getcwd(),'brazzers_videos.csv'),index=False)
                except Exception as e :
                    print('Error :', e)

    def get_collection_name(self: str) -> str:
        if self.find_element('No results found','//*[text()="No results found"]'):
            print('No video results found')
            return False
        else:
            name_of_collection =  self.find_element('catagory name','/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div/section/div/div[1]/div/h1')
            if name_of_collection:
                collection_name = name_of_collection.text.replace(' ','_').lower()
                return collection_name
            
    def get_videos_url(self,url=None):
        video_detailes = {'collection_name':'','video_list':[]}
        self.videos_urls = []
        df1 = pd.read_csv('brazzers_videos_details.csv')
        df_url = df1['Url'].values.tolist()
        page_number = 2
        if not url:
            tags = driver_url.split('tags=')[-1]
        else:
            self.driver.get(url)
            tags = url.split('tags=')[-1]
        found_max_videos = self.download_videos_count * 1.5
        self.random_sleep(6,10)
        driver_url = self.driver.current_url
        collection_name = self.get_collection_name()
        if not collection_name:return False
        video_detailes['collection_name'] = collection_name
        while True:
            try :
                for url_idx in range(1,24):
                    print(url_idx,'------------')
                    video_date = self.find_element(f'video : {url_idx}',f'/html/body/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/section/div/div[2]/div/div[{url_idx}]/div/div[2]/div[2]',timeout=3)
                    self.driver.execute_script("arguments[0].scrollIntoView();", video_date)
                    time.sleep(0.3)
                    if video_date :
                        if self.date_older_or_not(video_date.text) :
                            video_ele = self.find_element(f'Video number : {url_idx}',f'/html/body/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/section/div/div[2]/div/div[{url_idx}]/div/div[1]/a',timeout=3)
                            post_url = self.find_element('post url',f'/html/body/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/section/div/div[2]/div/div[{url_idx}]/div/div[1]/a/div[1]/div/picture/img',timeout=0)
                            if video_ele and post_url:
                                video_url = video_ele.get_attribute('href')
                                post_url = post_url.get_attribute('src')
                                if video_url and post_url and video_url not in df_url:
                                    self.videos_urls.append({"video_url":video_url,'post_url':post_url})
            except Exception as e :
                print(e)
            if len(self.videos_urls) < found_max_videos :
                if 'tags' in driver_url:
                    self.driver.get(f'https://site-ma.brazzers.com/scenes?page={page_number}&tags={tags}')
                    page_number +=1
                else:
                    self.driver.get(f'{driver_url}&page={page_number}')
                    page_number +=1
                    
            else : break
        video_detailes['video_list'] = self.videos_urls
        return video_detailes

    def download_videos(self, videos_dict):
        videos_urls = videos_dict['video_list']
        collection_name = videos_dict['collection_name']
        collection_path = self.create_or_check_path(collection_name)

        for idx, video_url in enumerate(videos_urls):
            self.driver.get(video_url['video_url'])
            self.random_sleep(10,15)
            download_video_name = self.driver.current_url.split('/')[-1]
            video_name = f"{collection_name}_{self.driver.current_url.split('https://site-ma.brazzers.com/')[-1].replace('/','_').replace('-','_')}"
            v_url = f'http://159.223.134.27:8000/downloads/{collection_name}/{video_name}.mp4/'
            p_url = f'http://159.223.134.27:8000/downloads/{collection_name}/{video_name}.jpg/'
            tmp = {
                    "Likes" : "",
                    "Disclike" :"",
                    "Url" : video_url['video_url'],
                    "Category" : collection_name,
                    "video_download_url" : v_url,
                    "Title" : '',
                    "Discription" : "",
                    "Release-Date" : "",
                    "Poster-Image_uri" : video_url['post_url'],
                    "poster_download_uri" : p_url,
                    "Video-name" : f'{video_name}.mp4',
                    "Photo-name" : f'{video_name}.jpg',
                    "Pornstarts" : ''
                }
            try:
                likes_count = self.find_element('Likes count','//*[text()="Likes:"]/strong')
                if likes_count :
                    tmp['Likes'] = likes_count.text

                # self.getvalue_byscript('document.querySelector("#root > div.sc-yo7o1v-0.hlvViO > div.sc-yo7o1v-0.hlvViO > div.sc-1fep8qc-0.ekNhDD > div.sc-1deoyo3-0.iejyDN > div:nth-child(1) > div > section > div.sc-1wa37oa-0.irrdH > div.sc-bfcq3s-0.ePiyNl > div.sc-k44n71-0.gbGmcO > span:nth-child(1) > strong").textContent')
                Disclike_count = self.find_element('Disclike count','//*[text()="Dislikes:"]/strong')
                if Disclike_count :
                    tmp['Disclike'] = Disclike_count.text

                Title = self.find_element('Title','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[5]/div/section/div/div/h2[2]')
                if Title :
                    tmp['Title'] = Title.text

                Release = self.find_element('Release','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[5]/div/section/div/div/h2[1]')
                if Release :
                    tmp['Release-Date'] = Release.text

                Discription = self.find_element('Discription','/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[6]/div/section/div/p')
                if Discription :
                    tmp['Discription'] = Discription.text

                port_starts = self.find_element('pornstars','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[5]/div/section/div/div/div[2]/h2')
                if port_starts :
                    tmp['Pornstarts'] = port_starts.text

                response = requests.get(video_url['post_url'])
                with open(f'downloads/{collection_name}/{video_name}.jpg', 'wb') as f:f.write(response.content)
                self.click_element('download btn', '//button[@class="sc-yox8zw-1 VZGJD sc-rco9ie-0 jnUyEX"]') 
                quality = self.find_element('download high_quality','//div[@class="sc-yox8zw-0 cQnfGv"]/ul/div/button[1]')
                file_name = f'downloads/{download_video_name}_{quality.text}.mp4'
                quality.click()
                self.wait_for_file_download()
                self.random_sleep(3,5)
                
                file_name = [i for i in os.listdir('downloads')if '-' in i and i.endswith('.mp4')][0]
                name_of_file = os.path.join(os.getcwd(), f'downloads/{video_name}.mp4')
                file_name = f'downloads/{file_name}'
                os.rename(os.path.join(os.getcwd(),file_name), name_of_file)
                self.copy_files_in_catagory_folder(name_of_file,collection_path)
                self.videos_data.append({"Video-title": video_name,"video_url": v_url,"downloaded_time": datetime.now()})
                
                self.videos_collection.append(tmp)
                pd.DataFrame(self.videos_collection).to_csv(os.path.join(os.getcwd(), 'brazzers_videos_details.csv'), index=False)
                pd.DataFrame(self.videos_data).to_csv(os.path.join(os.getcwd(), 'brazzers_videos.csv'), index=False)
            except Exception as e:
                print('Error:', e)


    def wait_for_file_download(self):
        print('waiting for download')
        seconds = 0
        while seconds < 20 :
            time.sleep(1)
            new_video_download = [i for i in os.listdir('downloads')if i.endswith('.crdownload')]
            if new_video_download:
                break
            else:
                seconds+=1
                
        while True:
            new_files = [i for i in os.listdir('downloads')if i.endswith('.crdownload')]
            if not new_files:
                print('download complete')
                return  # Download completed
            time.sleep(1)

    def create_or_check_path(self,folder_name, main=False):
        base_path = os.path.join(os.getcwd(), 'downloads') if not main else os.getcwd()
        folder = os.path.join(base_path, folder_name)
        os.makedirs(folder, exist_ok=True)
        return folder
    
    def copy_files_in_catagory_folder(self,src_file,dst_folder):
        shutil.move(src_file, os.path.join(dst_folder, os.path.basename(src_file)))
        
    def brazzers_delete_old_videos(self):
        
        if not os.path.exists(os.path.join(os.getcwd(),'downloads')) : os.makedirs(os.path.join(os.getcwd(),'downloads'))
        if not os.path.exists(os.path.join(os.getcwd(),'photos')) : os.makedirs(os.path.join(os.getcwd(),'photos'))
        if not os.path.exists(os.path.join(os.getcwd(),'brazzers_videos.csv')) :
            column_names = ["Video-title","video_url","downloaded_time"]
            df = pd.DataFrame(columns=column_names)
            df.to_csv('brazzers_videos.csv', index=False)

        if not os.path.exists(os.path.join(os.getcwd(),'brazzers_videos_details.csv')) :
            column_names = ["Likes","Disclike","Url","Title","Discription","Release-Date","Poster-Image_uri",'poster_download_uri',"Video-name",'video_download_uri',"Photo-name","Pornstarts"]
            df = pd.DataFrame(columns=column_names)
            df.to_csv('brazzers_videos_details.csv', index=False)

        df = pd.read_csv(os.path.join(os.getcwd(),'brazzers_videos.csv'))
        df['downloaded_time'] = pd.to_datetime(df['downloaded_time'])
        
        breakpoint()
        temp_df = df[df['downloaded_time'] < (datetime.now() - timedelta(days=int(self.delete_old_days)))]
        for idx,row in temp_df.iterrows():
            self.find_and_delete_video('downloads',row['Video-title'])
            df = df.drop(idx)
        df.to_csv(os.path.join(os.getcwd(),'brazzers_videos.csv'))
            
        
        delete_resume_file = [i for i in os.listdir('downloads')if i.endswith('.crdownload')]
        if delete_resume_file:
            for i in delete_resume_file:
                file_path = os.path.join(f'{os.getcwd()}/downloads', i)
                os.remove(file_path)
            