from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import html5lib


# class Scraper:


class WebObject:
    def __init__(self, m_parent):
        self.bootstrap: str = []
        self.cssBoolean: str = []
        self.cssContinuous: float = []
        self.children: WebObject = []
        self.parent: WebObject = m_parent


if __name__ == '__main__':
    var = requests.get("https://bootstrapmade.com/demo/templates/FlexStart/")
    my_soup = BeautifulSoup(var.content, "html5lib")
    lis = []
    flag = False
    for i in my_soup.find_all():
        if i.name == 'body':
            flag = True
        if flag == True:
            print(i.name)
            try:
                print(i.attrs['class'])
            except:
                continue
            # for j in i.find_all():
            #     try:
            #         print(j.name)
            #         print(j.attrs['class'])
            #     except:
            #         pass

    """
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path="chromedriver", options=options)
    driver.set_window_size(1280, 720)
    time.sleep(60)
    driver.quit()
    print("Done")
    """
