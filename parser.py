from fake_useragent import UserAgent
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests

#Youtube parser
#def parser():
    #link = 'https://youtube.com'
    #response = requests.get(link)
    #soup = BeautifulSoup(response.content, 'lxml')
    #music_response = soup.find('body')
    #return print(music_response)


#Yandex music parser
class My_parser:
    def __init__(self):
        self.data_id = 0
    
        #Settings, user_agent
        options = webdriver.ChromeOptions()
        user_agent = UserAgent(fallback = 'Chrome')
        options.add_argument(f'user-agent={user_agent}')
    
        #proxy
        #options.add_argument("--proxy-server=154.64.226.138:80")
    
        self.driver = webdriver.Chrome(options = options)
        
        
    def parser_do(self):
        try:
            self.get_music_each = self.driver.find_element(By.CSS_SELECTOR, f"[data-id='{self.data_id}']")
        except:
            self.driver.close()
            self.driver.quit()
        self.track_name = self.get_music_each.find_element(By.CLASS_NAME, 'd-track__name')
        self.track_author = self.get_music_each.find_element(By.CLASS_NAME, 'd-track__artists')
        self.driver.execute_script("window.scrollBy(0,100)","")
       
        
    def close_add(self): 
        try:
            xpath = '/html/body/div[1]/div[22]/div/span'
            bubble_close = self.driver.find_element(By.XPATH, xpath).click()
            time.sleep(3)
        except:
            print('Error: Cant click button')
        
        
    def get_all_music(self):
        url = 'https://music.yandex.ru/users/bratishkin192/playlists/3?utm_source=desktop&utm_medium=copy_link'
        try:
            #Connect
            self.driver.get(url = url)   
            #To do captcha
            time.sleep(30)

            #close add
            self.close_add()
            #Get all tracks and write it
            with open(os.path.abspath('music.txt'), 'w', encoding = 'utf-8') as file:    
                while self.data_id != 'NaN':
                    self.data_id += 1
                    self.parser_do()
                    file.write(f'{self.track_name.text.replace('\n', ' ')} {self.track_author.text.replace('\n', ' ')}\n')

        except Exception as _ex:
            print(_ex)
        finally:
            self.driver.close()
            self.driver.quit()


def main():
    My_parser().get_all_music()


if __name__ == '__main__':
    main()