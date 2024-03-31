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
from main.models import configuration, send_mail
import urllib.request
from anticaptchaofficial.recaptchav2proxyless import *
from mail import SendAnEmail
from main.utils import naughty_convert_relative_time
from driver import open_vps_driver

class scrapping_bot():
    
    def __init__(self,brazzers_bot = False):
        
        self.emailss = [mail.email for mail in send_mail.objects.all()]
        self.base_path = os.getcwd()
        [ os.remove(os.path.join(os.getcwd(),'downloads',i)) for i in os.listdir('downloads') if i.endswith('.crdownload')]

            
        self.driver = ''
        self.download_path = self.create_or_check_path('downloads',main=True)
        self.csv_path = self.create_or_check_path('csv',main=True)
        self.cookies_path = self.create_or_check_path('cookies',main=True)
        self.brazzers_category_path = self.create_or_check_path('brazzers_category_videos')
        self.vip4k_category_path = self.create_or_check_path('vip4k_category_videos')
        self.handjob_category_path = self.create_or_check_path('handjob_category_videos')
        self.naughty_america_category_path = self.create_or_check_path('naughty_america')
        self.brazzers = configuration.objects.get(website_name='brazzers')
        self.vip4k = configuration.objects.get(website_name='vip4k')
        self.handjob = configuration.objects.get(website_name='handjob')
        self.naughty = configuration.objects.get(website_name='naughtyamerica')
        self.solver = recaptchaV2Proxyless()
        self.solver.set_verbose(1)
        self.solver.set_key("e49c2cc94651faab912d635baec6741f")
        self.make_csv()
        self.delete_old_videos()
        if brazzers_bot == True:
            self.downloaded_videos_list = os.listdir('downloads')
            self.videos_urls = []
            self.brazzers_category_url = 'https://site-ma.brazzers.com/categories'

    def driver_arguments(self):
        self.options.add_argument('--lang=en')  
        # self.options.add_argument('log-level=3')  
        # self.options.add_argument('--mute-audio') 
        self.options.add_argument("--enable-webgl-draft-extensions")
        # self.options.add_argument('--mute-audio')
        self.options.add_argument("--ignore-gpu-blocklist")
        self.options.add_argument('--disable-dev-shm-usage')
        # self.options.add_argument('--headless')

        prefs = {"credentials_enable_service": True,
                'profile.default_content_setting_values.automatic_downloads': 1,
                "download.default_directory" : f"{self.download_path}",
            'download.prompt_for_download': False, 
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True ,
            "profile.password_manager_enabled": True}
        self.options.add_experimental_option("prefs", prefs)
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')    
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--enable-javascript")
        self.options.add_argument("--enable-popup-blocking")
        self.options.add_extension(os.path.join(self.base_path,'Stay-secure-with-CyberGhost-VPN-Free-Proxy.crx'))
        self.options.add_extension(os.path.join(self.base_path,'Buster-Captcha-Solver-for-Humans.crx'))
        # self.options.add_argument("download.default_directory=/path/to/your/default/directory")
        # self.options.add_argument(f"user-data-dir={os.path.join(os.getcwd(),'profiles')}")
        # self.options.add_argument("profile-directory=Defualt")
    
    def get_driver(self):
        # self.get_local_driver()
        # return
        
        for _ in range(30):
            from undetected_chromedriver import Chrome, ChromeOptions

            """Start webdriver and return state of it."""
            self.options = ChromeOptions()
            self.driver_arguments()
            self.options.add_argument('--headless')
            
            try:
                self.driver = Chrome(options=self.options,version_main=123)
                break
            except Exception as e:
                print(f"Error: {e}")
        
        return self.driver

    def get_local_driver(self):
        """Start webdriver and return state of it."""
        from selenium import webdriver
        for _ in range(30):
            self.options = webdriver.ChromeOptions()
            self.driver_arguments()
            try:
                self.driver = webdriver.Chrome(options=self.options)
                break
            except Exception as e:
                print(e)
        
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

    def random_sleep(self,a=3,b=7,reson = ""):
        random_time = random.randint(a,b)
        print('time sleep randomly :',random_time) if not reson else print('time sleep randomly :',random_time,f' for {reson}')
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
            return date_obj < self.old_date 
        return False

    def starting_bots(self):
        self.get_driver()
        return self.driver

    def connect_cyberghost_vpn(self):
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
        try:
            if 'vip4k' in website:
                path = os.path.join(self.cookies_path,f'{website}_cookietest.json')
                if os.path.isfile(path):
                    with open(path,'rb') as f:cookies = json.load(f)
                    for item in cookies:
                        if item.get("domain") == ".vip4k.com":
                            self.driver.add_cookie(item)
                self.driver.refresh()
            else:
                path = os.path.join(self.cookies_path,f'{website}_cookietest.json')
                if os.path.isfile(path):
                    with open(path,'rb') as f:cookies = json.load(f)
                    for item in cookies: self.driver.add_cookie(item)
                    self.random_sleep()
        except : 
            SendAnEmail('The coockies could not be loaded')

    def get_cookies(self,website :str):
        path = os.path.join(self.cookies_path,f'{website}_cookietest.json')
        cookies = self.driver.get_cookies()
        with open(path, 'w', newline='') as outputdata:
            json.dump(cookies, outputdata)
        return cookies
            
    def brazzers_login(self):
        self.load_cookies(self.brazzers.website_name)
        while True :
            try:
                self.driver.get('https://site-ma.brazzers.com/store')
                break
            except Exception as  e: 
                print(e) 
                self.CloseDriver()
                self.get_driver()
                self.connect_cyberghost_vpn()
                # self.connect_cyberghost_vpn()
            
        while not self.driver.execute_script("return document.readyState === 'complete'"):pass
        
        self.random_sleep(5,7)
        if self.driver.current_url != "https://site-ma.brazzers.com/store":
            for _ in range(3):
                time.sleep(1.5)
                if not self.find_element('Login form','//*[@id="root"]/div[1]/div[1]/div/div/div/div/form/button') :
                    self.click_element('try again',"//a[@href='https://site-ma.brazzers.com' and @rel='nofollow']",timeout=5)
                    return False
                if self.find_element('Login form','//*[@id="root"]/div[1]/div[1]/div/div/div/div/form/button') :
                    self.input_text(str(self.brazzers.username),'Username','username',By.NAME)
                    self.input_text(str(self.brazzers.password),'password','password',By.NAME)
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
        page_number = 0
        driver_url = self.driver.current_url
        tags = driver_url.split('tags=')[-1]
        found_max_videos = self.brazzers.numbers_of_download_videos
        self.random_sleep(6,10)
        video_detailes['collection_name'] = self.get_collection_name()
        
        
        while len(videos_urls) < found_max_videos:
            all_thumb = self.driver.find_elements(By.XPATH,"//div[contains(@class, 'one-list-1vyt92m') and contains(@class, 'e1vusg2z1')]" )
            try :
                for thumb in all_thumb: 
                    video_date = thumb.find_element(By.XPATH, "//div[2]/div/div[2]/div/div[2]")
                    video_date = thumb.find_element(By.XPATH, "//div[contains(@class, 'one-list-1oxbbh0') and contains(@class, 'e1jyqorn27')]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", video_date)
                    time.sleep(0.3)
                    if video_date and self.date_older_or_not(video_date.text) :                            
                            video_url = thumb.find_element(By.TAG_NAME, 'a').get_attribute('href')
                            post_url = thumb.find_element(By.TAG_NAME, 'img').get_attribute('src')
                            if video_url and post_url and video_url not in df_url:
                                print(f'add video url in lists')
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
            video_name = self.sanitize_title(self.driver.current_url.split('https://site-ma.brazzers.com/')[-1])

            v_urllll = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.mp4'
            p_urllll = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.jpg'
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
        name_of_collection = self.find_element('category name', '//h1')
        return name_of_collection.text.replace(' ', '_').lower() if name_of_collection else False

            
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
            all_thumb = self.driver.find_elements(By.XPATH,"//div[contains(@class, 'one-list-1vyt92m') and contains(@class, 'e1vusg2z1')]" )
            try :
                for thumb in all_thumb: 
                    video_date = thumb.find_element(By.XPATH, ".//div/div[2]/div/div[2]")
                    self.driver.execute_script("arguments[0].scrollIntoView();", video_date)
                    time.sleep(0.3)
                    if video_date and self.date_older_or_not(video_date.text) :                            
                            video_url = thumb.find_element(By.TAG_NAME, 'a').get_attribute('href')
                            post_url = thumb.find_element(By.TAG_NAME, 'img').get_attribute('src')
                            if video_url and post_url and video_url not in df_url:
                                print(f'add video url in lists')
                                videos_urls.append({"video_url":video_url,'post_url':post_url})
                                if len(videos_urls) >= found_max_videos:
                                    break
            except Exception as e :
                self.driver.save_screenshot('zz.png')
                
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
            video_name = f"{collection_name}_{self.sanitize_title(self.driver.current_url.split('https://site-ma.brazzers.com/')[-1])}"
            v_url = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.mp4'
            p_url = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.jpg'
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
                self.click_element('download high_quality','//div[@class="sc-yox8zw-0 cQnfGv"]/ul/div/button[1]')
                file_name = self.wait_for_file_download()
                self.random_sleep(3,5)
                name_of_file = os.path.join(self.download_path, f'{video_name}.mp4')
                os.rename(os.path.join(self.download_path,file_name), name_of_file)
                self.random_sleep(3,5)
                self.copy_files_in_catagory_folder(name_of_file,collection_path)
                self.set_data_of_csv(collection_name,tmp,video_name=video_name)
            except Exception as e:
                print('Error:', e)

    def wait_for_file_download(self,timeout=600):
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
        # self.CloseDriver()
        # self.get_driver()
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

    def sanitize_title(self,title : str):
        formatted_title = ''.join(c.lower() if c.isalnum() else '_' for c in title)
        formatted_title = '_'.join(filter(None, formatted_title.split('_')))
        return formatted_title
    
    def vip4k_download_video(self,videos_dict : dict):
        videos_urls = videos_dict['video_list']
        collection_name = videos_dict['collection_name']
        
        collection_path = self.create_or_check_path(self.vip4k_category_path,sub_folder_=collection_name)
        
        for idx, video_url in enumerate(videos_urls):
            self.driver.get(video_url['video_url'])
            # self.find_element()
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
                video_name = f"vip4k_{collection_name.replace('videos', '')}_{self.sanitize_title(tmp['Title'])}"
                v_url = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.mp4'
                p_url = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.jpg'
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
        url = "https://handjob.tv/login"
        self.driver.get(url)
        handjob_obj = configuration.objects.filter(website_name='handjob').first()
        self.input_text(handjob_obj.username,'username','//input[@id="username"]')
        self.input_text(handjob_obj.password,'password','//input[@id="password"]')
        self.click_element('Submit btn','//button[@id="login"]')
        self.input_text(handjob_obj.category,'password','//input[@id="search"]')
        # self.driver.get(f'https://handjob.tv/search/{handjob_obj.category}/')
        if self.find_element('Logout btn','//a[@class="logout"]') :
            cookies = self.get_cookies(self.vip4k.website_name)
            member_cookies = [item for item in cookies if item.get("domain") == "handjob.tv"]
            for item in member_cookies:self.driver.add_cookie(item)
            
            return True
        else : return False
        
        
        self.cookies_dict = ''
        cookies_file = f'{self.cookies_path}/{self.handjob.website_name}_cookietest.json'
        if os.path.isfile(cookies_file):
            with open(cookies_file, 'r') as file: 
                self.cookies_dict = json.load(file)
            response = requests.request("GET", url, cookies=self.cookies_dict)
            soup = BeautifulSoup(response.content, 'html.parser')
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
            soup = BeautifulSoup(response.content, 'html.parser')
            logout = soup.find('a', class_="logout")
            if logout:
                return True
        return False


    def handjob_get_video(self,url=None):
        videos_urls = []
        VideosNumberDone = 0
        self.driver.page_source
        self.driver.get(f'https://handjob.tv/search/{self.handjob.category}/')
        df_url = self.column_to_list(self.handjob.website_name,'Url')
        self.calculate_old_date(self.handjob.more_than_old_days_download)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        collection_path = self.create_or_check_path(self.handjob_category_path,sub_folder_=self.handjob.category)
        found_max_videos = self.handjob.numbers_of_download_videos
        # all_thimb = soup.find_all('div', class_='thumb-all')
        # video_links = soup.find_all('a', href=lambda value: value and '/video/' in value)
        video_links = soup.find_all('a', href=lambda value: value and '/video/' in value)
        for link in video_links:
            video_url = link['href']
            
            img_tag = link.find('img', alt='', src=True)
            if not img_tag or not video_url : continue
            
            video_date_ele = link.select_one('span.bio-videos-date')
            if not video_date_ele : continue
            
            date_string = video_date_ele.get_text(strip=True)
            if not self.date_older_or_not(date_string) : continue

            video_url = 'https://handjob.tv' + video_url
            img_src = 'https:'+img_tag['src']
            if video_url in df_url : continue
            print("Video URL:", video_url)
            print("Image Source:", img_src)
            self.driver.get(video_url)
            
            video_ele = self.find_element('Video Link','video',By.TAG_NAME)
            video_title_ele = self.find_element('Video Title','h1',By.TAG_NAME)
            if not video_ele or not video_title_ele: continue
            
            video_title = video_title_ele.text
            
            video_link = video_ele.get_attribute('src')
            video_name = f"handjob_{self.handjob.category.replace('videos', '')}_{self.sanitize_title(video_title)}"
            
            VideoDdownloaded = False
            try :VideoDdownloaded = urllib.request.urlretrieve(video_link, f'{collection_path}/{video_name}.mp4')
            except Exception as e : print('Error : Videos downloading in handjob :',e)
            
            try :ImgDownloaded = urllib.request.urlretrieve(img_src, f'{collection_path}/{video_name}.jpg')
            except Exception as e : print('Error : image downloading in handjob :',e)
            if not VideoDdownloaded or not ImgDownloaded : 
                print('error : Video or Image could not download in hand job')
                continue
            
            tmp = {"Likes" : "","Disclike" :"","Url" : video_url,"Category" : self.handjob.category,"video_download_url" : '',"Title" : '',"Discription" : "","Release-Date" : "","Poster-Image_uri" : img_src,"poster_download_uri" : '',"Video-name" : '',"Photo-name" : '',"Pornstarts" : '',"Username" : self.handjob.website_name}
            
            model_name_ele = self.find_element('models name','//div[@class="model-tags"]')
            if model_name_ele :
                model_name = model_name_ele.text.replace('Model:','').strip()
            else : model_name

            
            v_url = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.mp4'
            p_url = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.jpg'
            
            discription = ''
            All_Ptag = self.driver.find_elements(By.TAG_NAME,'p')
            for Ptag in All_Ptag : 
                PtagText = Ptag.text.strip()
                if not PtagText or PtagText.startswith('Lenght') or PtagText.startswith('Photos') or  PtagText.startswith('Added on: '):continue
                discription += PtagText
                
            tmp['Title'] = video_title
            tmp['Discription'] = discription
            tmp['Release-Date'] = date_string
            tmp['Video-name'] = f'{video_name}.mp4'
            tmp['Photo-name'] = f'{video_name}.jpg'
            tmp['poster_download_uri'] = p_url
            tmp['video_download_url'] = v_url
            tmp['Pornstarts'] = model_name                             
            self.set_data_of_csv(self.handjob.website_name,tmp,video_name)
            
            VideosNumberDone += 1
            if VideosNumberDone >= found_max_videos :return
            
            # 
        # for i in all_thimb:
            # video_url = 'https://handjob.tv'+link.find('a').get('href')
            # post_url = i.find('img').get('src')
            # if video_url and post_url and video_url not in df_url:
            #     self.driver.get(video_url)
            #     soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            #     paragraphs = soup.find_all('p')
            #     date_element = next((p for p in paragraphs if 'Added on' in p.get_text()), None)

            #     if date_element:
            #         date = date_element.get_text(strip=True).split(': ')[1]
            #         if date and self.date_older_or_not(date) :
            #             tmp = {
            #                     "Likes" : "",
            #                     "Disclike" :"",
            #                     "Url" : video_url,
            #                     "Category" : self.handjob.category,
            #                     "video_download_url" : '',
            #                     "Title" : '',
            #                     "Discription" : "",
            #                     "Release-Date" : "",
            #                     "Poster-Image_uri" : post_url,
            #                     "poster_download_uri" : '',
            #                     "Video-name" : '',
            #                     "Photo-name" : '',
            #                     "Pornstarts" : '',
            #                     "Username" : self.handjob.website_name,
            #                 }
            #             video_title = soup.find('h1', class_='video-title').get_text(strip=True)
            #             video_name = f"handjob_{self.handjob.category.replace('videos', '')}_{video_title.lower().replace(' ', '_')}"
            #             v_url = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.mp4'
            #             p_url = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.jpg'
            #             model_tags_div = soup.find('div', class_='model-tags')
            #             if model_tags_div:
            #                 model_name_element = model_tags_div.find('a')
            #                 if model_name_element:
            #                     model_name = model_name_element.get_text(strip=True)
            #                     tmp['Pornstarts'] = model_name                             
                        
            #             video_link = soup.find('a', text='1080p').get('href')
            #             discribe = soup.find('div', class_='video-text')
            #             discription = ''
            #             for i in discribe.find_all('p')[3:]:
            #                 discription +=i.get_text(strip=True)
            #             tmp['Title'] = video_title
            #             tmp['Discription'] = discription
            #             tmp['Release-Date'] = date
            #             tmp['Video-name'] = f'{video_name}.mp4'
            #             tmp['Photo-name'] = f'{video_name}.jpg'
            #             tmp['poster_download_uri'] = p_url
            #             tmp['video_download_url'] = v_url
            #             
            #             response = requests.request("GET", video_link)
            #             if response.status_code == 200:
            #                 with open(f'{collection_path}/{video_name}.mp4', 'wb') as file:
            #                     file.write(response.content)
            #             response = requests.request("GET", post_url)
            #             if response.status_code == 200:
            #                 with open(f'{collection_path}/{video_name}.jpg', 'wb') as file:file.write(response.content)
            #             self.set_data_of_csv(self.handjob.website_name,tmp,video_name)
            #     videos_urls.append({"video_url":video_url,'post_url':post_url})
            #     if len(videos_urls) >= found_max_videos :return

    def Sovle_captcha(self):
        site_key_ele = self.find_element('SITE-KEY','g-recaptcha',By.CLASS_NAME)
        
        if site_key_ele : 
            # to solvee the captcha
            site_key = site_key_ele.get_attribute('data-sitekey')
            self.solver.set_website_url(self.driver.current_url)
            self.solver.set_website_key(site_key)
            self.solver.set_soft_id(0)
            g_response = self.solver.solve_and_return_solution()
            
            if g_response == 0:
                
                print ("task finished of captcha solver with error "+self.solver.error_code)
                return False
            print ("g-response: "+g_response)
            
            captcha_text_area_id = 'g-recaptcha-response'
            captcha_response = self.find_element('Captcha-text-area',captcha_text_area_id,By.ID,timeout=3)
            if not captcha_response :
                captcha_text_area_id = 'g-recaptcha-response-1'
                captcha_response = self.find_element('captcha 2 text area',captcha_text_area_id,By.ID,timeout=3)
            
            if not captcha_response : return False
            self.driver.execute_script("arguments[0].style.display = 'block';", captcha_response)
            captcha_response = self.driver.find_element(By.ID, captcha_text_area_id)
            captcha_response.send_keys(g_response)
            
            if g_response : return True
            
        return False

    
    def naughty_ame_login(self):
        self.click_element('Login','//a[text()="LOGIN"]')
        self.random_sleep(10,15)
        
        if self.find_element('user btn','//*[@id="right-side-containter"]/div/div[2]/a/i') : 
            return True
        # self.load_cookies(self.naughty.website_name)
        # self.driver.get('https://members.naughtyamerica.com/postLogin')
        self.click_element('Login','//a[text()="LOGIN"]')
        self.input_text(self.naughty.username,'Username','//*[@id="login-top"]/input[1]')
        self.input_text(self.naughty.password,'Password','//*[@id="login-top"]/input[2]')
        if self.Sovle_captcha():
            login_button = self.driver.find_element(By.ID, 'login')
            login_button.click()
            self.random_sleep(10,15)
            self.driver.refresh()
        
        
            if self.find_element('user btn','//*[@id="right-side-containter"]/div/div[2]/a/i'):
                cookies = self.get_cookies(self.naughty.website_name)
                member_cookies = [item for item in cookies if item.get("domain") == ".naughtyamerica.com"]
                for item in member_cookies:self.driver.add_cookie(item)
                return True
        
        return False
       
    def Open_new_tab_with_link(self,link): 
        self.driver.execute_script(f"window.open('{link}')")
        
    def get_naughty_video_links(self):
        if not os.path.exists(os.path.join(os.getcwd(),'csv','naughty_america_videos_details.csv')) :
            df = pd.DataFrame(columns= ["Likes","Disclike","Url","Category","video_download_url","Title","Discription","Release-Date","Poster-Image_uri","poster_download_uri","Video-name","Photo-name","Pornstarts","Username"])
            df.to_csv(os.path.join(os.getcwd(),'csv','naughty_america_videos_details.csv'),index=False)
        
        df = pd.read_csv(os.path.join(os.getcwd(),'csv','naughty_america_videos_details.csv'))   
        downloaded_vd_title = df['Title'].tolist()
        
        all_videos_link_li = []
        for _ in range(100):
                
            all_videos = self.driver.find_elements(By.XPATH, '//*[@id="sceneList"]//div[contains(@class, "scene-item") and contains(@class, "countable")]')
            for videos in all_videos:
                
                Video_a_tag = videos.find_elements(By.TAG_NAME,'a')
                if not Video_a_tag : continue
                
                Video_a_tag = Video_a_tag[0]
                vd_title=  Video_a_tag.get_attribute('title')
                
                if not vd_title in  downloaded_vd_title:
                    url__ = Video_a_tag.get_attribute('href')
                    if url__ :
                        all_videos_link_li.append(url__)
                        continue
            
            if len(all_videos_link_li) >= self.naughty.numbers_of_download_videos :
                return all_videos_link_li
            
            if not self.click_element('View more','view-all-button',By.CLASS_NAME):
                SendAnEmail('Could not find more videos into naughty america cetegories!',email=self.emailss)
                return
            
            self.random_sleep(10,15)
        return all_videos_link_li
        
    def naughty_video_download(self):
        """This functions helps to download the video at his place and save the details which is needed to save in csv"""
        
        
        collection_path = self.create_or_check_path(self.naughty_america_category_path,sub_folder_=self.naughty.category)
        
        # click on more info
        self.click_element('more info','more-info',By.ID)
        
        # get and store the video details in dict
        data_dict = {}
        data_dict['Likes'] = ""
        data_dict['Disclike'] = ""
        data_dict['Url'] = self.driver.current_url
        data_dict['Category'] = self.naughty.category
        data_dict['video_download_url'] = self.naughty.category
        
        pornstar_ele = self.find_element('porn star','//*[@id="more-info-container"]/div[1]/p[2]')
        data_dict['Pornstarts'] = ""
        if not pornstar_ele : SendAnEmail('Could not find pornstars into naughty america!',email=self.emailss)
        else : data_dict['Pornstarts'] = pornstar_ele.text
        
        data_dict['Title'] = ""
        vd_title_ele = self.find_element('title','//p[@class="new-title"]')
        if not vd_title_ele : SendAnEmail('Could not find pornstars into naughty america!',email=self.emailss)
        else : data_dict['Title'] = vd_title_ele.text
        
        data_dict['Title'] = ""
        vd_title_ele = self.find_element('title','//p[@class="new-title"]')
        if not vd_title_ele : SendAnEmail('Could not find pornstars into naughty america!',email=self.emailss)
        else : data_dict['Title'] = vd_title_ele.text
        
        video_name = f"naughty_{self.naughty.category.replace('videos', '')}_{self.sanitize_title(data_dict['Title'])}"
        data_dict['Video-name'] = f'{video_name}.mp4'
        data_dict['Photo-name'] = f'{video_name}.jpg'
        v_url = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.mp4'
        p_url = f'http://208.122.217.49:8000{collection_path.replace(self.base_path,"")}/{video_name}.jpg'
        data_dict['video_download_url'] = v_url
        data_dict['poster_download_uri'] = p_url
        
        data_dict['Release-Date'] = ""
        vd_Release_ele = self.find_element('Release date','//*[@id="more-info-container"]/div[1]/p[10]')
        if not vd_Release_ele : SendAnEmail('Could not find pornstars into naughty america!',email=self.emailss)
        else : data_dict['Release-Date'] = naughty_convert_relative_time(vd_Release_ele.text)
        
        
        data_dict['Discription'] = ""
        vd_Discription_ele = self.find_element('Discription','//*[@id="more-info-container"]/div[1]/p[6]')
        if not vd_Discription_ele : SendAnEmail('Could not find description into naughty america!',email=self.emailss)
        else : data_dict['Discription'] = naughty_convert_relative_time(vd_Discription_ele.text)
        
        self.set_data_of_csv(self.naughty.website_name,data_dict,video_name)
        
        cur_url = self.driver.current_url
        self.click_element('4k download btn','//*[@id="download-options-menu"]/table/tbody/tr[3]/td[2]/a')
        self.Sovle_captcha()
        self.find_element('captcha form',"//form[contains(@action, 'captcha')]").submit()
        
        self.random_sleep(10,15,reson="for downloading naughty america videos")
        while True :
            new_video_download = [i for i in os.listdir('downloads')if i.endswith('.crdownload')]
            if not new_video_download:
                break    
        # self.click_element('download btn','//button[@type="submit" and @disabled="disabled" and contains(@class, "btn-download")]')
        return True
        
    def naughty_ame(self):
        try:
            download_com_videos = 0
            videos_cat_url = ''
            self.driver.get('https://members.naughtyamerica.com/')
            if self.click_element('Enter naughty america','//*[@id="banner"]/div/div/div[2]/p[1]/a'):
                self.random_sleep(10,15)
            if self.find_element('Login','//a[text()="LOGIN"]'):
                if not self.naughty_ame_login() : 
                    SendAnEmail('Could not login into naughty america!',email=self.emailss)
                    return
            
            
            if not self.find_element('categories','//*[@id="header-tags"]'):
                SendAnEmail('Could not find cetegories into naughty america!',email=self.emailss)
                return
            
            categories = []
            for _ in range(3) :
                categories = self.driver.find_elements(By.XPATH,'//*[@id="header-tags"]/*')
                if len(categories) > 5 : break
                self.random_sleep()
            else:
                SendAnEmail('Could not find cetegories into naughty america!',email=self.emailss)
                return
            
            # [ i.get_attribute('href') for i in categories if  i.text.lower() == "latina"]
            
            for cat in categories : 
                if cat.text.lower() == self.naughty.category.lower():
                    videos_cat_url = cat.get_attribute('href')
                    self.driver.get(videos_cat_url)
                    break
            else:
                SendAnEmail('Could not find cetegories Entered and looking for, into naughty america!',email=self.emailss)
                return
            
            for _ in range(5):
                all_videos_link_li = self.get_naughty_video_links()
                for vd_link in all_videos_link_li:
                    self.driver.get(vd_link)
                    # if self.naughty_video_download(): download_com_videos+= 1
                    download_com_videos+= 1
                    
                    if download_com_videos == self.naughty.numbers_of_download_videos:
                        return True
            
        except Exception as e :
                SendAnEmail('Could not complete the naughty america scrapping!'+f'\n{e}',email=self.emailss)
            
        
        
                
        