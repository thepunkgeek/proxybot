#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display # To run Firefox in a headless mode

display = Display(visible=0, size=(1024,768))
display.start()
proxy_list = []

def get_profile(proxy_list, driver):
    proxy = proxy_list.pop()
    split_proxy = proxy.split(':')
    proxy_ip = split_proxy[0]
    proxy_port = split_proxy[1]
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", proxy_ip)
    profile.set_preference("network.proxy.http_port", proxy_port)
    profile.update_preferences()
    driver = webdriver.Firefox(firefox_profile=profile)
    # FirefoxProfile profile = new FirefoxProfile();
    # profile.setPreference("network.proxy.type", 1);
    firefox_profile = profile
    # print(firefox_profile)
    return driver


def get_list():
    driver = webdriver.Firefox()
    driver.get('http://freeproxylists.net/?c=US&pt=&pr=HTTPS&a%5B%5D=1&a%5B%5D=2&u=90')
    assert "Free Proxy Lists" in driver.title
    print("Getting proxy list...")
    for i in range(2,13):
        i = str(i)
        path = '/html/body/div[1]/div[2]/table/tbody/tr[' + i + ']/td[1]/a'
        try:
            elem = driver.find_element(By.XPATH, path)
            if elem.is_displayed():
                proxy_ip = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/table/tbody/tr[' + i + ']/td[1]/a')
                proxy_port = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/table/tbody/tr[' + i + ']/td[2]')
                # remove the comment below to grab the uptime of each proxy
                # proxy_uptime = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/table/tbody/tr[' + i + ']/td[8]')
                proxy = proxy_ip.text + ':' + proxy_port.text
                proxy_list.append(proxy)
                print(proxy_list)
                i = int(i)

        except NoSuchElementException:
            print("No More Proxies Found....")
            break
        return proxy_list

if __name__=='__main__':
    get_profile(proxy_list, driver)
