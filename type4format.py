from asyncio import wait
import json
import os
import platform
import time 
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException ,StaleElementReferenceException
import pandas as pd
import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from browsermobproxy import Server
options = Options()
options.add_argument("--headless")
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'}) 
# import undetected_chromedriver as uc 
driver = webdriver.Chrome(options=options)
anodri = webdriver.Chrome(options=options)
class Type4scrappers():
    def __init__(self,id,url):
        self.id =id
        self.url =url
        self.final_data =[]
        print(f"processing the {self.id}")
        current_time = datetime.datetime.now()

        # Extract the year
        self.current_year = current_time.year

    async def mainscrapper(self):
        try:
            driver.get(self.url)
            time.sleep(2)
            Selectlist = driver.find_element(By.CSS_SELECTOR,"select[name='p_term']")  
            Selectlist = Select(Selectlist)
            options = Selectlist.options

            for opt in range(len(options)):
                if opt!=0:
                    driver.get(self.url)
                    time.sleep(2)
                Selectlist = driver.find_element(By.CSS_SELECTOR,"select[name='p_term']")  
                Selectlist = Select(Selectlist)
                options = Selectlist.options
                option = options[opt]
                if option.text =='None':
                    continue
                if str(self.current_year-1) in option.text:
                    break
                if option.is_enabled:
                    termtext = option.text
                    Selectlist.select_by_visible_text(termtext)
                    print(f"selecting the {termtext}")
                    time.sleep(2)
                rowdatatitle, rowdata = self.searchbuttonapply()

                if len(rowdata) == len(rowdatatitle):
                    print("yes proceed")
                else:
                    print("problem")
                for idx in range(len(rowdata)):

                    print(idx)
                    try:
                        dictData = {"Cengage Master Institution ID":self.id,'Source URL':self.url,'Course Name': " ","Course Description":"","Class Number":"","Section":"","Instructor":"","Enrollment":"","Course Dates":"","Location":"","Textbook/Course Materials":""}
                        self.everyrowprocess(idx, dictData)


                        self.final_data.append(dictData)
                    except Exception as e:
                        print(e.args)


            df=pd.DataFrame(self.final_data)
            df.to_excel(f"{self.id}_course_catalog.xlsx",index=False)

        except Exception as e:
            pass

    def everyrowprocess(self, idx, dictData):
        rowdatatitle = driver.find_elements(By.CSS_SELECTOR,'.ddtitle a')
        rowdata = driver.find_elements(By.CSS_SELECTOR,"[summary='This layout table is used to present the sections found'] > tbody > tr > td")
        row = rowdata[idx]
        row1 = rowdatatitle[idx]
        anodri.get(row1.get_attribute('href'))
        courseName = anodri.find_element(By.CSS_SELECTOR,"[summary='This table is used to present the detailed class information.'] > tbody > tr > th").text.strip()

        dictData['Course Name'] = courseName.split("-")[0] if len(courseName.split("-"))>0 else ""
        dictData['Class Number'] = courseName.split("-")[2] if len(courseName.split("-"))>1 else ""

        enrollmentavail = anodri.find_element(By.CSS_SELECTOR,'.dddefault tr:nth-of-type(2) td:nth-of-type(1)').text.strip()
        enrollmentcapacity = anodri.find_element(By.CSS_SELECTOR,".dddefault tr:nth-of-type(2) td:nth-of-type(3)").text.strip()

        dictData['Enrollment'] = f"{enrollmentavail}/{enrollmentcapacity}"

        dictData['Instructor'] = row.find_element(By.CSS_SELECTOR,'tr tr td:nth-of-type(7)').text.strip()
        dictData['Course Dates'] = row.find_element(By.CSS_SELECTOR,'tr tr td:nth-of-type(5)').text.strip()

        dictData['Location'] = row.find_element(By.CSS_SELECTOR,'tr tr td:nth-of-type(4)').text.strip()
        try:
            coursedesclink =driver.find_elements(By.LINK_TEXT,"View Catalog Entry")[idx]
            anodri.get(coursedesclink.get_attribute('href')) 

            dictData['Course Description'] = anodri.find_element(By.CSS_SELECTOR,"[summary='This table lists all course detail for the selected term.'] td.ntdefault").text.strip()

        except Exception as e: 
            dictData['Course Description'] = ''   
        # self.final_data.append(dictData)
 
    def searchbuttonapply(self):
        searchbutton = driver.find_element(By.CSS_SELECTOR,'input[type="submit"]') 
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", searchbutton)
        driver.execute_script("arguments[0].click();",searchbutton)
        time.sleep(2)
        actions = ActionChains(driver)
                
        selectbutton = driver.find_elements(By.XPATH, "//*[contains(text(), 'Subject:')]")
        # selectbutton =driver.find_elements(By.CSS_SELECTOR,"span[class='fieldlabeltext']")
        if selectbutton:
            selectbutton = selectbutton[0]
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", selectbutton)
            driver.execute_script("arguments[0].click();",selectbutton)
        # else:
        #     selectbutton =driver.find_elements(By.CSS_SELECTOR,"select[name='sel_subj']")
        #     selectbutton = selectbutton[0]
        #     driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", selectbutton)
        #     driver.execute_script("arguments[0].click();",selectbutton)
            # selctlist.select_by_visible_text(selctlist.options[0].text)
        
        if platform.system() == 'Darwin':  # Mac OS
            actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND).perform()
        else:  # Windows or Linux
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()


        button = driver.find_element(By.CSS_SELECTOR,"input[value='Class Search']")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        driver.execute_script("arguments[0].click();",button)
        time.sleep(10)
        rowdatatitle = driver.find_elements(By.CSS_SELECTOR,'.ddtitle a')
        rowdata = driver.find_elements(By.CSS_SELECTOR,"[summary='This layout table is used to present the sections found'] > tbody > tr > td")
        return rowdatatitle,rowdata 