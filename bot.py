import os,shutil, pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,NoSuchElementException,WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver  
import json, random, time, pandas as pd, os
from datetime import datetime, timedelta
from selenium_stealth import stealth
import m3u8_To_MP4
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

class scrapping_bot():
    
    def __init__(self,brazzers_bot = False):
        with open('configrations.json', 'r') as json_file:    
            self.config_data = json.load(json_file)

        if brazzers_bot == True:
            self.category = str(self.config_data['brazzers']['category'])
            old_days = str(self.config_data['brazzers']['old_days'])
            self.download_videos_count = int(self.config_data['brazzers']['download_videos'])
            self.username = str(self.config_data['brazzers']['username'])
            self.password = str(self.config_data['brazzers']['password'])
            self.password = str(self.config_data['brazzers']['password'])
            self.delete_old_days = str(self.config_data['brazzers']['delete_old_days'])
            self.calculate_old_date(int(old_days))
            
            self.brazzers_delete_old_videos()
            self.videos_collection = []
            self.videos_collection = pd.read_csv(os.path.join(os.getcwd(),'brazzers_videos_details.csv'))
            self.videos_collection = self.videos_collection.to_dict(orient='records')

            self.videos_data = []
            self.videos_data = pd.read_csv(os.path.join(os.getcwd(),'brazzers_videos.csv'))
            self.videos_data = self.videos_data.to_dict(orient='records')

            self.videos_urls = []
            self.brazzers_category_url = 'https://site-ma.brazzers.com/categories'
        
    def get_driver(self,add_cybeghost=False):
        
        downloads_directory = '/home/dell/Desktop/upwork/brazzers/downloads'
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
        options.add_argument("--user-data-dir=/home/sajal/.config/google-chrome")
        options.add_argument('--profile-directory=Default')
        prefs = {"credentials_enable_service": True,
                 "download.default_directory" : "./downloads",
                 'download.default_directory': downloads_directory,
            'download.prompt_for_download': False,  # Optional, suppress download prompt
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True , # Optional, enable safe browsing,
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
                # driver = webdriver.Chrome(executable_path='/home/dell/Desktop/upwork/brazzers/chromedriver',options=options)
                # driver = uc.Chrome(
                #     options = options , version_main = 116
                #     )  # version_main allows to specify your chrome version instead of following chrome global version
                # driver.set_page_load_timeout(30)
                # driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
                driver = webdriver.Chrome(options=options)
                driver.get('https://site-ma.brazzers.com/store')
                break
            except Exception as e:
                print(e)
        # driver = webdriver.Chrome(executable_path='/home/dell/Desktop/upwork/brazzers/chromedriver1',options=options)
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

        # # driver = uc.Chrome(options=option)
        # # driver = uc.Chrome()
        # driver = webdriver.Chrome(options=option)
        # self.driver = driver
        # self.driver.maximize_window()
        
        # return self.driver
    
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
        ...

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
                    # return
                else: self.random_sleep(5,10)

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
        files = os.listdir(folder_path)

        for file in files:
            if file.lower().endswith((".mp4", ".avi", ".mkv")):
                if video_title.lower() in file.lower():
                    file_path = os.path.join(folder_path, file)

                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    return

    def brazzers_login(self):
        first_time = False
        self.driver.refresh()
        path = f"{os.getcwd()}/cookietest.json"
        if os.path.isfile(path):
            with open('cookietest.json','rb') as f:cookies = json.load(f)
            for item in cookies: self.driver.add_cookie(item)
            self.random_sleep()
        self.driver.get('https://site-ma.brazzers.com/store')
        

        if self.driver.current_url != "https://site-ma.brazzers.com/store":
            for _ in range(3):
                time.sleep(1.5)
                if not self.find_element('Login form','//*[@id="root"]/div[1]/div[1]/div/div/div/div/form/button') :
                    self.driver.refresh()
                if self.find_element('Login form','//*[@id="root"]/div[1]/div[1]/div/div/div/div/form/button') :
                    self.input_text(self.username,'Username','username',By.NAME)
                    self.input_text(self.password,'password','password',By.NAME)
                    self.click_element('Submit','//button[@type="submit"]')
                    for _ in range(4):
                        if "login" not in self.driver.current_url:
                            cookies = self.driver.get_cookies()
                            with open('cookietest.json', 'w', newline='') as outputdata:
                                json.dump(cookies, outputdata)
                            return True
                        self.random_sleep()
                self.driver.delete_all_cookies()
                self.driver.refresh()
            return False
        else :
            return True
        # self.driver.get(self.brazzers_category_url)
        # if 'store' in self.driver.current_url.lower() : return True

        # for _ in range(5):
        #     self.driver.get('https://site-ma.brazzers.com/login')
        #     if self.find_element('Login form','//*[@id="root"]/div[1]/div[1]/div/div/div/div/form/button') :
        #         time.sleep(1.5)
        #         self.input_text(self.username,'Username','username',By.NAME)
        #         self.input_text(self.password,'password','password',By.NAME)
        #         self.click_element('Submit','/html/body/div[1]/div[1]/div[1]/div[1]/div/div/div/form/button')
                                
        #         for _ in range(4):
        #             if 'store' in self.driver.current_url.lower() : 
        #                 return True
        #             else: self.random_sleep()
        # else : return False

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
        page_number = 2
        driver_url = self.driver.current_url
        tags = driver_url.split('tags=')[-1]
        found_max_videos = self.download_videos_count * 1.5
        self.random_sleep(6,10)
        for _ in range(10) :
            try :
                for url_idx in range(1,24):
                    print(url_idx,'------------')
                    video_date = self.find_element(f'video : {url_idx}',f'/html/body/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/section/div/div[2]/div/div[{url_idx}]/div/div[2]/div[2]',timeout=3)
                    if video_date :
                        if self.date_older_or_not(video_date.text) :
                            video_ele = self.find_element(f'Video number : {url_idx}',f'/html/body/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/section/div/div[2]/div/div[{url_idx}]/div/div[1]/a',timeout=3)
                            post_url = self.find_element('post url',f'/html/body/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/section/div/div[2]/div/div[{url_idx}]/div/div[1]/a/div[1]/div/picture/img',timeout=0)
                            if video_ele and post_url:
                                video_url = video_ele.get_attribute('href')
                                post_url = post_url.get_attribute('src')
                                if video_url and post_url:
                                    self.videos_urls.append({"video_url":video_url,'post_url':post_url})

            except Exception as e :
                print(e) 
            if len(self.videos_urls) < found_max_videos :
                self.driver.get(f'https://site-ma.brazzers.com/scenes?page={page_number}&tags={tags}')
                page_number +=1
            else : break
        # 


    def brazzers_download_video(self):
        for idx,videoss_urll in enumerate(self.videos_urls) :
            master_url = []
            for _ in range(3):
                self.driver.get(videoss_urll['video_url'])
                # self.click_element('video play button','/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div/section/div[2]/div/section/div/div/button[1]',timeout=30)
                self.random_sleep(10,15)
                networks_list = self.driver.execute_script(" var network = performance.getEntries() || {}; return network;")
                for i in networks_list : 
                    if "mp4.urlset/master.m3u8" in i['name']:
                        master_url.append(i['name'])
                video_name = f"{self.driver.current_url.split('https://site-ma.brazzers.com/')[-1].replace('/','_').replace('-','_')}"
                # self.click_element('video play button','/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div/section/div[2]/div/section/div/div/button[1]',timeout=30)
                if len(master_url) > 0: break
                else: continue
            if len(master_url) > 0 :
                tmp = {
                    "Likes" : "",
                    "Disclike" :"",
                    "Url" : videoss_urll['video_url'],
                    "Title" : '',
                    "Discription" : "",
                    "Release-Date" : "",
                    "Poster-Image_uri" : videoss_urll['video_url'],
                    "Video-name" : f'{video_name}.mp4',
                    "Pornstarts" : ''
                }
                try:
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

                    Discription = self.find_element('Discription','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[5]/div/section/div/div/h2[1]')
                    if Discription :
                        tmp['Discription'] = Release.text

                    Release = self.find_element('Release','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[5]/div/section/div/div/h2[1]')
                    if Release :
                        tmp['Release-Date'] = Release.text

                    Release = self.find_element('Release','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[5]/div/section/div/div/h2[1]')
                    if Release :
                        tmp['Release-Date'] = Release.text

                    port_starts = self.find_element('pornstars','/html/body/div/div[1]/div[2]/div[3]/div[2]/div[5]/div/section/div/div/div[2]/h2')
                    if port_starts :
                        tmp['Pornstarts'] = port_starts.text
                    
                    import os
                    if not os.path.exists(os.path.join(os.getcwd(),'videos')) : os.makedirs(os.path.join(os.getcwd(),'videos'))
                    # with open(os.path.join(os.getcwd(),f'videos/{video_name}.mp4'), 'w') as fp:  pass
                    breakpoint()
                    m3u8_To_MP4.multithread_download(master_url[0],mp4_file_name='video.mp4',mp4_file_dir= os.path.join(os.getcwd(),'videos'))
                    self.videos_collection.append(tmp)
                    self.videos_data.append({ "Video-title" : video_name,"video_url" : videoss_urll['video_url'],"downloaded_time" : datetime.now()})

                    pd.DataFrame(self.videos_collection).to_csv(os.path.join(os.getcwd(),'brazzers_videos_details.csv'),index=False)
                    pd.DataFrame(self.videos_data).to_csv(os.path.join(os.getcwd(),'brazzers_videos.csv'),index=False)
                except Exception as e :
                    print('Error :', e)
            
    def brazzers_delete_old_videos(self):
        
        if not os.path.exists(os.path.join(os.getcwd(),'brazzers_videos.csv')) :
            column_names = ["Video-title","video_url","downloaded_time"]
            df = pd.DataFrame(columns=column_names)
            df.to_csv('brazzers_videos.csv', index=False)

        if not os.path.exists(os.path.join(os.getcwd(),'brazzers_videos_details.csv')) :
            column_names = ["Likes","Disclike","Url","Title","Discription","Release-Date","Poster-Image_uri","Video-name","Pornstarts"]
            df = pd.DataFrame(columns=column_names)
            df.to_csv('brazzers_videos_details.csv', index=False)

        df = pd.read_csv(os.path.join(os.getcwd(),'brazzers_videos.csv'))
        df['downloaded_time'] = pd.to_datetime(df['downloaded_time'])
        
        temp_df = df[df['downloaded_time'] < (datetime.now() - timedelta(days=int(self.delete_old_days)))]
        for idx,row in temp_df.iterrows() : 
            print(row['Video-title'])
            self.find_and_delete_video('videos',row['Video-title'])