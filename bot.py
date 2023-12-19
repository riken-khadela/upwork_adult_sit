import os,shutil, pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,NoSuchElementException,WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver  
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
from dateutil import parser
import json, random, time, pandas as pd, os
from datetime import datetime, timedelta
import undetected_chromedriver as uc
from main.models import configuration

class scrapping_bot():
    
    def __init__(self,brazzers_bot = False):
        self.base_path = os.getcwd()
        self.download_path = self.create_or_check_path('downloads',main=True)
        self.csv_path = self.create_or_check_path('csv',main=True)
        self.cookies_path = self.create_or_check_path('cookies',main=True)
        self.brazzers_category_path = self.create_or_check_path('brazzers_category_videos')
        self.vip4k_category_path = self.create_or_check_path('vip4k_category_videos')
        self.handjob_category_path = self.create_or_check_path('handjob_category_videos')
        self.brazzers = configuration.objects.get(website_name='brazzers')
        self.vip4k = configuration.objects.get(website_name='vip4k')
        self.handjob = configuration.objects.get(website_name='handjob')
        self.make_csv()
        self.delete_old_videos()
        if brazzers_bot == True:
            self.downloaded_videos_list = os.listdir('downloads')
            self.videos_urls = []
            self.brazzers_category_url = 'https://site-ma.brazzers.com/categories'

    def get_driver(self):
        for _ in range(30):
            """Start webdriver and return state of it."""
            from undetected_chromedriver import Chrome, ChromeOptions
            options = ChromeOptions()
            options.add_argument('--lang=en')  # Set webdriver language to English.
            options.add_argument('log-level=3')  # No logs is printed.
            options.add_argument('--mute-audio')  # Audio is muted.
            options.add_argument("--enable-webgl-draft-extensions")
            options.add_argument('--mute-audio')
            options.add_argument("--ignore-gpu-blocklist")
            options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--headless')
            prefs = {"credentials_enable_service": True,
                    'profile.default_content_setting_values.automatic_downloads': 1,
                    "download.default_directory" : f"{self.download_path}",
                'download.prompt_for_download': False,  # Optional, suppress download prompt
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True ,
                "profile.password_manager_enabled": True}
            options.add_experimental_option("prefs", prefs)
            options.add_argument('--no-sandbox')
            options.add_argument('--start-maximized')    
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--enable-javascript")
            options.add_argument("--enable-popup-blocking")
            try:
                driver = Chrome(options=options,version_main=119)
                driver.get('https://site-ma.brazzers.com/store')
                break
            except Exception as e:
                print(e)
        
        self.driver = driver
        return self.driver

    def get_local_driver(self):
        """Start webdriver and return state of it."""
        from selenium import webdriver

        for _ in range(30):
            options = webdriver.ChromeOptions()
            options.add_argument('--lang=en')  # Set webdriver language to English.
            options.add_argument('log-level=3')  # No logs is printed.
            options.add_argument('--mute-audio')  # Audio is muted.
            options.add_argument("--enable-webgl-draft-extensions")
            options.add_argument('--mute-audio')
            options.add_argument("--ignore-gpu-blocklist")
            options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--headless')
            prefs = {"credentials_enable_service": True,
                    'profile.default_content_setting_values.automatic_downloads': 1,
                    "download.default_directory" : f"{self.download_path}",
                'download.prompt_for_download': False,  # Optional, suppress download prompt
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True ,
                "profile.password_manager_enabled": True}
            options.add_experimental_option("prefs", prefs)
            options.add_argument('--no-sandbox')
            options.add_argument('--start-maximized')    
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--enable-javascript")
            options.add_argument("--enable-popup-blocking")
            try:
                driver = webdriver.Chrome()
                driver.get('https://site-ma.brazzers.com/store')
                break
            except Exception as e:
                print(e)
        
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
            self.ensure_click(ele)
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
    
    def ensure_click(self, element, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))
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
            date_obj = parser.parse(date_string)
            if date_obj < self.old_date :
                return True
        return False

    def starting_brazzers_bots(self):
        self.get_driver()

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

    def load_cookies(self,website :str):
        if 'vip4k' in website:
                path = os.path.join(self.cookies_path,f'{website}_cookietest.json')
                if os.path.isfile(path):
                    with open(path,'rb') as f:cookies = json.load(f)
                    for item in cookies:
                        if item.get("domain") == ".vip4k.com":
                            self.driver.add_cookie(item)
        else:
            path = os.path.join(self.cookies_path,f'{website}_cookietest.json')
            if os.path.isfile(path):
                with open(path,'rb') as f:cookies = json.load(f)
                for item in cookies: self.driver.add_cookie(item)
                self.random_sleep()
            
    def get_cookies(self,website :str):
        path = os.path.join(self.cookies_path,f'{website}_cookietest.json')
        cookies = self.driver.get_cookies()
        with open(path, 'w', newline='') as outputdata:
            json.dump(cookies, outputdata)
        return cookies
            
    def brazzers_login(self):
        self.load_cookies(self.brazzers.website_name)
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
                    self.input_text(str(self.brazzers.username),'Username','username',By.NAME)
                    self.random_sleep(1,1)
                    self.input_text(str(self.brazzers.password),'password','password',By.NAME)
                    self.random_sleep(1,1)
                    self.click_element('Submit','//button[@type="submit"]')
                    self.random_sleep(2,3)
                    for _ in range(4):
                        if "login" not in self.driver.current_url:
                            self.get_cookies(self.brazzers.website_name)
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
                if cate1.text.lower() == self.brazzers.category.lower() :
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
                            if cate1.text.lower() == self.brazzers.category.lower() :
                                found_category = True
                                cate1.click()
                                break
                else : break
                if found_category == True : break
        if found_category == True : 
            return True
        else: 
            return False
    
    def column_to_list(self,website_name : str,column_name :str)-> list:
        if '_videos' in website_name:website_name =website_name.replace('_videos','')
        df1 = pd.read_csv(os.path.join(self.csv_path,f'{website_name}_videos_details.csv'))
        list_of_column = df1[f'{column_name}'].values.tolist()
        return list_of_column
        
    def brazzers_get_videos_url(self):
        video_detailes = {'collection_name':'','video_list':[]}
        videos_urls = []
        self.calculate_old_date(self.brazzers.more_than_old_days_download)
        df_url = self.column_to_list(self.brazzers.website_name,'Url')
        page_number = 2
        driver_url = self.driver.current_url
        tags = driver_url.split('tags=')[-1]
        found_max_videos = self.brazzers.numbers_of_download_videos
        self.random_sleep(6,10)
        video_detailes['collection_name'] = self.get_collection_name()
        while len(videos_urls) < found_max_videos:
            all_thumb = self.driver.find_elements(By.XPATH,"//div[contains(@class, 'one-list-1vyt92m') and contains(@class, 'e1vusg2z1')]" )
            try :
                for thumb in all_thumb:
                    video_date = thumb.find_element(By.XPATH, "//div[contains(@class, 'one-list-1oxbbh0') and contains(@class, 'e1jyqorn24')]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", video_date)
                    time.sleep(0.3)
                    if video_date and self.date_older_or_not(video_date.text) :                            
                            video_url = thumb.find_element(By.TAG_NAME, 'a').get_attribute('href')
                            post_url = thumb.find_element(By.TAG_NAME, 'img').get_attribute('src')
                            if video_url and post_url and video_url not in df_url:
                                videos_urls.append({"video_url":video_url,'post_url':post_url})
                                if len(videos_urls) >= found_max_videos:
                                    break
            except Exception as e :
                print(e)
            if len(videos_urls) < found_max_videos:
                self.driver.get(f'https://site-ma.brazzers.com/scenes?page={page_number}&tags={tags}')
                self.random_sleep(2,4)
                page_number +=1
                
        video_detailes['video_list'] = videos_urls
        return video_detailes

    def set_data_of_csv(self,website_name :str, tmp :dict,video_name : str):
        if '_videos' in website_name:website_name =website_name.replace('_videos','')
        website_video_csv_path = os.path.join(self.csv_path,f'{website_name}_videos.csv')
        website_video_details_csv_path = os.path.join(self.csv_path,f'{website_name}_videos_details.csv')
        videos_collection = pd.read_csv(website_video_details_csv_path)
        videos_collection = videos_collection.to_dict(orient='records')
        videos_data = pd.read_csv(website_video_csv_path)
        videos_data = videos_data.to_dict(orient='records')
        videos_data.append({"Video-title": video_name,"video_url": tmp['video_download_url'],"downloaded_time": datetime.now()})    
        videos_collection.append(tmp)
        pd.DataFrame(videos_collection).to_csv(website_video_details_csv_path, index=False)
        pd.DataFrame(videos_data).to_csv(website_video_csv_path, index=False)

    def brazzers_download_video(self, videos_dict):
        videos_urls = videos_dict['video_list']
        collection_name = videos_dict['collection_name']
        collection_path = self.create_or_check_path(self.brazzers_category_path,sub_folder_=collection_name)
        for idx,videoss_urll in enumerate(videos_urls) :
            self.driver.get(videoss_urll['video_url'])
            self.random_sleep(10,15)
            video_name = f"{self.driver.current_url.split('https://site-ma.brazzers.com/')[-1].replace('/','_').replace('-','_')}"

            v_urllll = f'http://159.223.134.27:8000{collection_path.replace(self.base_path,"")}/{video_name}.mp4'
            p_urllll = f'http://159.223.134.27:8000{collection_path.replace(self.base_path,"")}/{video_name}.jpg'
            tmp = {
                "Likes" : "",
                "Disclike" :"",
                "Url" : videoss_urll['video_url'] ,
                "Category":str(collection_name).replace('_videos',''),
                "video_download_url" : v_urllll,
                "Title" : '',
                "Discription" : "",
                "Release-Date" : "",
                "Poster-Image_uri" : videoss_urll['post_url'],
                "poster_download_uri" : p_urllll,
                "Video-name" : f'{video_name}.mp4',
                "Photo-name" : f'{video_name}.jpg',
                "Pornstarts" : '',
                "Username" : self.brazzers.website_name,
            }
            try:
                response = requests.get(tmp['Poster-Image_uri'])
                with open(f'{collection_path}/{video_name}.jpg', 'wb') as f:f.write(response.content)
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
                file_name = self.wait_for_file_download()
                self.random_sleep(3,5)
                name_of_file = os.path.join(self.download_path, f'{video_name}.mp4')
                os.rename(os.path.join(self.download_path,file_name), name_of_file)
                self.random_sleep(2,4)
                self.copy_files_in_catagory_folder(name_of_file,collection_path)
                self.set_data_of_csv(self.brazzers.website_name,tmp,video_name=video_name)
            except Exception as e :
                print('Error :', e)

    def get_collection_name(self: str) -> str:
        if self.find_element('No results found','//*[text()="No results found"]',timeout=4):
            print('No video results found')
            return False
        else:
            name_of_collection =  self.find_element('catagory name','/html/body/div[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div/section/div/div[1]/div/h1')
            if name_of_collection:
                collection_name = name_of_collection.text.replace(' ','_').lower()
                return collection_name
            
    def get_videos_url(self,url=None):
        self.calculate_old_date(self.brazzers.more_than_old_days_download)
        video_detailes = {'collection_name':'','video_list':[]}
        videos_urls = []
        page_number = 2
        if not url:
            tags = driver_url.split('tags=')[-1]
        else:
            self.driver.get(url)
            tags = url.split('tags=')[-1]
        found_max_videos = self.brazzers.numbers_of_download_videos
        self.random_sleep(6,10)
        driver_url = self.driver.current_url
        collection_name = self.get_collection_name()
        if not collection_name:return False
        video_detailes['collection_name'] = collection_name
        self.make_csv(collection_name,new=True)
        df_url = self.column_to_list(collection_name,'Url')
        while len(videos_urls) < found_max_videos:
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
                                    videos_urls.append({"video_url":video_url,'post_url':post_url})
                                    if len(videos_urls) >= found_max_videos :
                                        break
            except Exception as e :
                print(e)
            if len(videos_urls) < found_max_videos :
                if 'tags' in driver_url:
                    self.driver.get(f'https://site-ma.brazzers.com/scenes?page={page_number}&tags={tags}')
                    page_number +=1
                else:
                    self.driver.get(f'{driver_url}&page={page_number}')
                    page_number +=1
                    
        video_detailes['video_list'] = videos_urls
        return video_detailes

    def download_videos(self, videos_dict):
        videos_urls = videos_dict['video_list']
        collection_name = videos_dict['collection_name']
        collection_path = self.create_or_check_path(collection_name)

        for idx, video_url in enumerate(videos_urls):
            self.driver.get(video_url['video_url'])
            self.random_sleep(10,15)
            video_name = f"{collection_name}_{self.driver.current_url.split('https://site-ma.brazzers.com/')[-1].replace('/','_').replace('-','_')}"
            v_url = f'http://159.223.134.27:8000{collection_path.replace(self.base_path,"")}/{video_name}.mp4'
            p_url = f'http://159.223.134.27:8000{collection_path.replace(self.base_path,"")}/{video_name}.jpg'
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
                    "Pornstarts" : '',
                    "Username" : self.brazzers.website_name,
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
                with open(f'{collection_path}/{video_name}.jpg', 'wb') as f:f.write(response.content)
                self.click_element('download btn', '//button[@class="sc-yox8zw-1 VZGJD sc-rco9ie-0 jnUyEX"]') 
                quality = self.click_element('download high_quality','//div[@class="sc-yox8zw-0 cQnfGv"]/ul/div/button[1]')
                file_name = self.wait_for_file_download()
                self.random_sleep(3,5)
                name_of_file = os.path.join(self.download_path, f'{video_name}.mp4')
                os.rename(os.path.join(self.download_path,file_name), name_of_file)
                self.random_sleep(3,5)
                self.copy_files_in_catagory_folder(name_of_file,collection_path)
                self.set_data_of_csv(collection_name,tmp,video_name=video_name)
            except Exception as e:
                print('Error:', e)

    def wait_for_file_download(self,timeout=20):
        print('waiting for download')
        seconds = 0
        new_video_download = ''
        while seconds < timeout :
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
                return  new_video_download[0].replace('.crdownload','').split('/')[-1]
            time.sleep(1)

    def create_or_check_path(self,folder_name, sub_folder_='',main=False):
        folder_name = folder_name if not os.path.isdir(folder_name) else os.path.basename(folder_name)
        base_path = os.path.join(os.getcwd(), 'downloads') if not main else os.getcwd()
        folder = os.path.join(base_path, folder_name)
        if sub_folder_: folder = os.path.join(folder, sub_folder_)
        os.makedirs(folder, exist_ok=True)
        return folder
    
    def copy_files_in_catagory_folder(self,src_file,dst_folder):
        shutil.move(src_file, os.path.join(dst_folder, os.path.basename(src_file)))
        
    def make_csv(self,website_name : str = '',new :bool = False):
        if not new:
            for object in configuration.objects.all():
                website_name = object.website_name
                website_video_csv_path = os.path.join(self.csv_path,f'{website_name}_videos.csv')
                website_video_details_csv_path = os.path.join(self.csv_path,f'{website_name}_videos_details.csv')
                if not os.path.exists(website_video_csv_path) :
                    column_names = ["Video-title","video_url","downloaded_time"]
                    df = pd.DataFrame(columns=column_names)
                    df.to_csv(website_video_csv_path, index=False)

                if not os.path.exists(website_video_details_csv_path) :
                    column_names = ["Likes","Disclike","Url","Title","Discription","Release-Date","Poster-Image_uri",'poster_download_uri',"Video-name",'video_download_uri',"Photo-name","Pornstarts","Category","Username"]
                    df = pd.DataFrame(columns=column_names)
                    df.to_csv(website_video_details_csv_path, index=False)
                    
        if new and website_name:
            if '_videos' in website_name:website_name =website_name.replace('_videos','')
            website_video_csv_path = os.path.join(self.csv_path,f'{website_name}_videos.csv')
            website_video_details_csv_path = os.path.join(self.csv_path,f'{website_name}_videos_details.csv')
            if not os.path.exists(website_video_csv_path) :
                column_names = ["Video-title","video_url","downloaded_time"]
                df = pd.DataFrame(columns=column_names)
                df.to_csv(website_video_csv_path, index=False)

            if not os.path.exists(website_video_details_csv_path) :
                column_names = ["Likes","Disclike","Url","Title","Discription","Release-Date","Poster-Image_uri",'poster_download_uri',"Video-name",'video_download_uri',"Photo-name","Pornstarts","Category","Username"]
                df = pd.DataFrame(columns=column_names)
                df.to_csv(website_video_details_csv_path, index=False)

    def delete_old_videos(self):
        self.delete_resume_file()
        files = os.listdir(self.csv_path)
        base_name_dict = defaultdict(list)
        for file in files:
            base_name = file.split('_')[0]            
            base_name_dict[base_name].append(file)
        for base_name, file_list in base_name_dict.items():
            if len(file_list) == 1:
                os.remove(file_list[0])
                df = pd.read_csv(os.path.join(self.csv_path,file_list[1]))
                df['downloaded_time'] = pd.to_datetime(df['downloaded_time'])
                df1 = pd.read_csv(os.path.join(self.csv_path,file_list[0]))
                temp_df = df[df['downloaded_time'] < (datetime.now() - timedelta(days=int(object.delete_old_days)))]
                if not temp_df.empty:
                    matching_titles = temp_df['Video-title'].unique()
                    matching_url = temp_df['video_url'].unique()
                    if matching_titles:
                        for idx,row in temp_df.iterrows():
                            self.find_and_delete_video('downloads',row['Video-title'])
                        df1 = df1[~df1['video_download_url'].isin(matching_url)]
                        df1.to_csv(os.path.join(self.csv_path,file_list[0]),index=False)
        
    def delete_resume_file(self):
        delete_resume_file = [i for i in os.listdir('downloads')if i.endswith('.crdownload')]
        if delete_resume_file:
            for i in delete_resume_file:
                file_path = os.path.join(self.download_path, i)
                os.remove(file_path)
        base_name_dict = defaultdict(list)
        for foldername, subfolders, filenames in os.walk(os.path.join(os.getcwd(), 'downloads')):
            for filename in filenames:
                base_name = os.path.splitext(os.path.basename(filename))[0]
                if os.path.basename(filename).endswith('.mp4') or os.path.basename(filename).endswith('.jpg'):
                    base_name_dict[base_name].append(os.path.join(foldername, filename))
        for base_name, file_list in base_name_dict.items():
            if len(file_list) == 1:
                os.remove(file_list[0])
                            
    def vip4k_login(self):
        for i in range(3):
            self.driver.get('https://vip4k.com/en/login')
            login = self.find_element('login button','//*[text()="Login"]')
            if login:
                self.load_cookies(self.vip4k.website_name)
                self.driver.get('https://vip4k.com/en/login')
                login = self.find_element('login button','//*[text()="Login"]')
                if login:
                    self.click_element('login button','//*[text()="Login"]')
                    self.random_sleep(2,4)
                    self.input_text(self.vip4k.username,'username','login-username',By.ID)
                    self.random_sleep(2,3)
                    self.input_text(self.vip4k.password,'password','login-password',By.ID)
                    self.random_sleep(2,3)
                    iframe = WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, f'//iframe[@title="reCAPTCHA"]')))
                    self.driver.execute_script('document.querySelector("#recaptcha-token").click()')
                    self.driver.switch_to.default_content()
                    self.random_sleep(2,3)
                    iframe = WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, f'//iframe[@title="recaptcha challenge expires in two minutes"]')))        
                    self.click_element('click extension btn','//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[4]')
                    
                    self.driver.switch_to.default_content()
                    
                    self.random_sleep(10,15)
                    self.click_element('submit','//input[@type="submit"]')
                    self.random_sleep(5,6)
            if self.find_element('check login','//div[@class="logout__text"]'):
                cookies = self.get_cookies(self.vip4k.website_name)
                member_cookies = [item for item in cookies if item.get("domain") != ".vip4k.com"]
                for item in member_cookies:self.driver.add_cookie(item)
                return True
        
    def vip4k_get_video(self,url :str):
        self.calculate_old_date(self.vip4k.more_than_old_days_download)
        video_detailes = {'collection_name':'','video_list':[]}
        videos_urls = []
        if self.vip4k.category: self.driver.get(f'https://members.vip4k.com/en/tag/{self.vip4k.category}')
        else:self.driver.get(url)
        self.random_sleep(10,15)
        collection_name = self.find_element('collection name','//h1[@class="section__title title title--sm"]', timeout=5)
        if not collection_name: collection_name = self.find_element('collection name','//h1')
        df_url = self.column_to_list(self.vip4k.website_name,'Url')
        max_video = self.vip4k.numbers_of_download_videos
        while len(videos_urls) < max_video:
            ul_tag = self.find_element('ul tag', 'grid.sets_grid', By.CLASS_NAME)
            li_tags = ul_tag.find_elements(By.TAG_NAME, 'li')
            for li in li_tags:
                video_date = li.find_element(By.CLASS_NAME, 'item__date').text
                if video_date and self.date_older_or_not(video_date):
                    video_url = li.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    post_url = li.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    if video_url and not post_url: 
                        self.random_sleep(5,7)
                        post_url = li.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    if video_url and post_url:
                        if video_url not in df_url and video_url not in [item['video_url'] for item in videos_urls]:
                            videos_urls.append({"video_url": video_url, 'post_url': post_url})
                            if len(videos_urls) >= max_video:break
                    if len(videos_urls) >= max_video:break
            if len(videos_urls) >= max_video:break
            show_more = self.find_element('show more','/html/body/div[2]/div/div[1]/div/section/div[5]/a')
            if show_more:
                self.driver.execute_script("arguments[0].scrollIntoView();", show_more)
                show_more.click()
            else:
                break
        video_detailes['collection_name'] = collection_name.text.lower().replace(' ','_')
        video_detailes['video_list'] = videos_urls
        return video_detailes

    def vip4k_download_video(self,videos_dict : dict):
        videos_urls = videos_dict['video_list']
        collection_name = videos_dict['collection_name']
        collection_path = self.create_or_check_path(self.vip4k_category_path,sub_folder_=collection_name)
        for idx, video_url in enumerate(videos_urls):
            self.driver.get(video_url['video_url'])
            self.random_sleep(10,15)
            tmp = {
                    "Likes" : "",
                    "Disclike" :"",
                    "Url" : video_url['video_url'],
                    "Category" : videos_dict['collection_name'],
                    "video_download_url" : '',
                    "Title" : '',
                    "Discription" : "",
                    "Release-Date" : "",
                    "Poster-Image_uri" : video_url['post_url'],
                    "poster_download_uri" : '',
                    "Video-name" : '',
                    "Photo-name" : '',
                    "Pornstarts" : '',
                    "Username" : self.vip4k.website_name,
                }
            try:
                likes_count = self.find_element('Likes count','//button[@class="player-vote__item player-vote__item--up "]')
                if likes_count :
                    tmp['Likes'] = likes_count.text

                # self.getvalue_byscript('document.querySelector("#root > div.sc-yo7o1v-0.hlvViO > div.sc-yo7o1v-0.hlvViO > div.sc-1fep8qc-0.ekNhDD > div.sc-1deoyo3-0.iejyDN > div:nth-child(1) > div > section > div.sc-1wa37oa-0.irrdH > div.sc-bfcq3s-0.ePiyNl > div.sc-k44n71-0.gbGmcO > span:nth-child(1) > strong").textContent')
                Disclike_count = self.find_element('Disclike count','//button[@class="player-vote__item player-vote__item--down "]')
                if Disclike_count :
                    tmp['Disclike'] = Disclike_count.text

                Title = self.find_element('Title','//h1[@class="player-description__title"]')
                if Title :
                    tmp['Title'] = Title.text

                Release = self.find_element('Release',"//li[@class='player-additional__item'][2]")
                if Release :
                    tmp['Release-Date'] = Release.text

                Discription = self.find_element('Discription','//div[@class="player-description__text"]')
                if Discription :
                    tmp['Discription'] = Discription.text

                porn_starts = self.driver.find_elements(By.XPATH,'//div[@class="model__name"]')
                if porn_starts:
                    porn_start_name = ''
                    for i in porn_starts:
                        porn_start_name += f'{i.text},'
                    tmp['Pornstarts'] = porn_start_name.rstrip(',')

                video_name = f"vip4k_{collection_name.replace('videos', '')}_{tmp['Title'].lower().replace(' ', '_')}"
                v_url = f'http://159.223.134.27:8000{collection_path.replace(self.base_path,"")}/{video_name}.mp4'
                p_url = f'http://159.223.134.27:8000{collection_path.replace(self.base_path,"")}/{video_name}.jpg'
                tmp['poster_download_uri'] = p_url
                tmp['video_download_url'] = v_url
                tmp['Photo-name'] = f'{video_name}.jpg'
                tmp['Video-name'] = f'{video_name}.mp4'
                response = requests.get(video_url['post_url'])
                with open(f'{collection_path}/{video_name}.jpg', 'wb') as f:f.write(response.content)
                js_script = """
                    var downloadLinks = document.querySelectorAll('.download__item');
                    for (var i = 0; i < downloadLinks.length; i++) {
                        var link = downloadLinks[i];
                        if (link.getAttribute('download').includes('FullHD.mp4')) {
                            link.click();
                            break;
                        }
                    }
                    """
                self.driver.execute_script(js_script)
                file_name = self.wait_for_file_download(timeout=30)
                self.random_sleep(3,5)
                name_of_file = os.path.join(self.download_path, f'{video_name}.mp4')
                os.rename(os.path.join(self.download_path,file_name), name_of_file)
                self.copy_files_in_catagory_folder(name_of_file,collection_path)
                self.set_data_of_csv(self.vip4k.website_name,tmp,video_name)
            except Exception as e:
                print('Error:', e)




    def login_Handjob_TV(self):
        self.cookies_dict = ''
        cookies_file = f'{self.cookies_path}/{self.handjob.website_name}_cookietest.json'
        url = "https://handjob.tv"
        if os.path.isfile(cookies_file):
            with open(cookies_file, 'r') as file:
                self.cookies_dict = json.load(file)
            response = requests.request("GET", url, cookies=self.cookies_dict)
            soup = BeautifulSoup(response.content, 'html.parser', cookies=self.cookies_dict)
            logout = soup.find('a', class_="logout")
            if logout:
                return True
            
        headers = {'Cookies':'_ga=GA1.1.1004529152.1702469470; PHPSESSID=rugc1hlu0itorhumpom12pk59q; _ga_HK7FVQ1HVZ=GS1.1.1702982456.7.1.1702982470.0.0.0'}
        response = requests.request("GET", url, headers=headers)
        hidden_input = soup.find('input', {'name': 'nocsrf_login_popup'})
        if hidden_input:
            value = hidden_input.get('value')
            payload = {'u': 'romeostream', 'p' : 'tub3S3bm1t', 'nocsrf_login_popup' : f'{value}'}
            print('value found')
        else:
            payload = {'u': 'romeostream', 'p' : 'tub3S3bm1t'}

        url = "https://handjob.tv/api/verifying"
        headers =   {
                        'Content-Type' :  'application/x-www-form-urlencoded'
                    }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            self.cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
            with open(cookies_file, 'w') as file:
                json.dump(self.cookies_dict, file)
            print("Cookies saved to cookies.json file.")
            soup = BeautifulSoup(response.content, 'html.parser', cookies=self.cookies_dict)
            logout = soup.find('a', class_="logout")
            if logout:
                return True
        return False


    def handjob_get_video(self,url=None):
        videos_urls = []
        df_url = self.column_to_list(self.handjob.website_name,'Url')
        self.calculate_old_date(self.handjob.more_than_old_days_download)
        response = requests.request("GET", f'https://handjob.tv/videos/{self.handjob.category}', cookies=self.cookies_dict)
        if response.status_code != 200:
            raise Exception('Failed to get the response')
        soup = BeautifulSoup(response.content, 'html.parser')
        last_page_div = soup.find('div', class_='pagination-btns').find_all('div')[-1]
        last_page_number = int(last_page_div.find('a').get('href').split('/')[-1].replace('page', ''))
        collection_path = self.create_or_check_path(self.handjob_category_path,sub_folder_=self.handjob.category)
        found_max_videos = self.handjob.numbers_of_download_videos
        for i in range(last_page_number-1):
            response = requests.request("GET",f'https://handjob.tv/videos/{self.handjob.category}/page{last_page_number}', cookies=self.cookies_dict)
            if response.status_code != 200:continue
            soup = BeautifulSoup(response.content, 'html.parser')
            all_thimb = soup.find_all('div', class_='thumb-all')
            for i in all_thimb:
                video_url = 'https://handjob.tv'+i.find('a').get('href')
                post_url = i.find('img').get('src')
                if video_url and post_url and video_url not in df_url:
                    response = requests.request("GET", video_url, cookies=self.cookies_dict)
                    if response.status_code ==200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        paragraphs = soup.find_all('p')
                        date_element = next((p for p in paragraphs if 'Added on' in p.get_text()), None)

                        # Extract the date
                        if date_element:
                            date = date_element.get_text(strip=True).split(': ')[1]
                            if date and self.date_older_or_not(date) :
                                tmp = {
                                        "Likes" : "",
                                        "Disclike" :"",
                                        "Url" : video_url,
                                        "Category" : self.handjob.category,
                                        "video_download_url" : '',
                                        "Title" : '',
                                        "Discription" : "",
                                        "Release-Date" : "",
                                        "Poster-Image_uri" : post_url,
                                        "poster_download_uri" : '',
                                        "Video-name" : '',
                                        "Photo-name" : '',
                                        "Pornstarts" : '',
                                        "Username" : self.handjob.website_name,
                                    }
                                video_title = soup.find('h1', class_='video-title').get_text(strip=True)
                                video_name = f"handjob_{self.handjob.category.replace('videos', '')}_{video_title.lower().replace(' ', '_')}"
                                v_url = f'http://159.223.134.27:8000{collection_path.replace(self.base_path,"")}/{video_name}.mp4'
                                p_url = f'http://159.223.134.27:8000{collection_path.replace(self.base_path,"")}/{video_name}.jpg'
                                model_tags_div = soup.find('div', class_='model-tags')
                                if model_tags_div:
                                    model_name_element = model_tags_div.find('a')
                                    if model_name_element:
                                        model_name = model_name_element.get_text(strip=True)
                                        tmp['Pornstarts'] = model_name                             
                             
                                video_link = soup.find('a', text='1080p').get('href')
                                discribe = soup.find('div', class_='video-text')
                                discription = ''
                                for i in discribe.find_all('p')[3:]:
                                    discription +=i.get_text(strip=True)
                                tmp['Title'] = video_title
                                tmp['Discription'] = discription
                                tmp['Release-Date'] = date
                                tmp['Video-name'] = f'{video_name}.mp4'
                                tmp['Photo-name'] = f'{video_name}.jpg'
                                tmp['poster_download_uri'] = p_url
                                tmp['video_download_url'] = v_url
                                response = requests.request("GET", video_link)
                                if response.status_code == 200:
                                    with open(f'{collection_path}/{video_name}.mp4', 'wb') as file:
                                        file.write(response.content)
                                response = requests.request("GET", post_url)
                                if response.status_code == 200:
                                    with open(f'{collection_path}/{video_name}.jpg', 'wb') as file:file.write(response.content)
                                self.set_data_of_csv(self.handjob.website_name,tmp,video_name)
                    videos_urls.append({"video_url":video_url,'post_url':post_url})
                    if len(videos_urls) >= found_max_videos :
                        break
            last_page_number-=1