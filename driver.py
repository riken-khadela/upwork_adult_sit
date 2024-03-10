from undetected_chromedriver import Chrome, ChromeOptions
import os

base_path = os.getcwd()


def opt():
    options = ChromeOptions()
    options.add_argument('--lang=en')  
    # options.add_argument('log-level=3')  
    options.add_argument('--mute-audio') 
    options.add_argument("--enable-webgl-draft-extensions")
    options.add_argument('--mute-audio')
    options.add_argument("--ignore-gpu-blocklist")
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--headless')

    prefs = {"credentials_enable_service": True,
            'profile.default_content_setting_values.automatic_downloads': 1,
            "download.default_directory" : f"downloads",
        'download.prompt_for_download': False, 
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
    options.add_extension(os.path.join(base_path,'Stay-secure-with-CyberGhost-VPN-Free-Proxy.crx'))
    options.add_extension(os.path.join(base_path,'Buster-Captcha-Solver-for-Humans.crx'))
    return options

def open_vps_driver():
    """Start webdriver and return state of it."""
    options = opt()
    driver = Chrome(options=options)
    return driver
    