from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pytesseract
import os
from PIL import Image
from io import BytesIO
import cv2


chrome_options = Options()
chrome_options.add_argument("window-size=1800,1200")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)



driver = webdriver.Chrome(options=chrome_options)

url = "https://mwpt.mma.go.kr/caisBMHS/index_mwps.jsp"
driver.get(url)

#보안문자 이미지 얻어내기
def imgbinary():
    element1 = driver.find_element(By.XPATH,'//*[@id="contents"]/div/form/table/tbody/tr[2]/th[4]/div[2]')
    location = element1.location
    size = element1.size
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    element_png = driver.get_screenshot_as_png()
    captcha_png = Image.open(BytesIO(element_png)).crop((left -10  , top-2, right-260, bottom))
    captcha_png.save("captcha{0}.png".format(numtry))
    #이진화
    binary_img = cv2.imread("captcha{0}.png".format(numtry))
    gray = cv2.cvtColor(binary_img, cv2.COLOR_BGR2GRAY)
    ret, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    #cv2.imshow("binary", dst)
    cv2.imwrite('grayImage.png',dst)

numtry =0
#이미지 ocr 처리
def imgocr():
    global numtry
    global image_ocr
    path = os.getcwd()
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    image_ocr = pytesseract.image_to_string(Image.open('grayImage.png'),config='digits')
    image_ocr = image_ocr.replace(" ","")
    
err_Occur =0   
#보안문자 시도  갯수 맞추기 
def tryChaptchaAgain():
    global err_Occur
    while len(image_ocr) != 6 or err_Occur ==1:
        driver.find_element(By.XPATH,'//*[@id="reLoad"]').click()
        time.sleep(0.03)
        imgbinary()
        imgocr()
        print("new",image_ocr)
        err_Occur =0
        
   
    
  
print("loading type 'ready'")
#인증전까지 자동 실행
ready = input()
if ready == "ready":
    driver.switch_to.frame('main')
    driver.find_element(By.CSS_SELECTOR, 'li.m3 > a').click()
    driver.find_element(By.CSS_SELECTOR,' span:nth-child(1) > a').click()
    #element = driver.find_element("input_element_name")
    #element.send_keys(Keys.RETURN)
    #element = driver.find_element(By.XPATH, "//body")
    #element.send_keys(Keys.ENTER)
    if WebDriverWait(driver, 3).until(EC.alert_is_present()):
        driver.switch_to.alert.dismiss()
    

print("type 'start'")

startkey = input()
if startkey == "start":
         
     driver.find_element(By.CSS_SELECTOR,'li:nth-child(1) > span > a').click()
     
    #창로딩될 때까지 확인후 전환
     while driver.window_handles[-1] == driver.window_handles[0]:
         print(driver.window_handles[-1])
     
     driver.switch_to.window(driver.window_handles[-1])
    #첫번째 날짜 선택까지 반복(예외처리)
     while True:
         try:
             #child 3번 부터 1번째 선택
            driver.find_element(By.CSS_SELECTOR, 'tr:nth-child(3) > td:nth-child(1) > a').click() #3번 부터 시작
            break  
         except:   
             pass
         
     print('current window1',driver.window_handles,len(driver.window_handles))
     
     print('-------------------')
     time.sleep(0.03)
     imgbinary()
     imgocr()
     print("is", image_ocr,len(image_ocr))
     driver.find_element(By.CSS_SELECTOR,'#answer').send_keys(image_ocr)
     driver.find_element(By.CSS_SELECTOR,'th:nth-child(6) > span > input[type=button]').click()
     numtry += 1
     try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            print("-----------------------------alert accur------------------------------")
            
            alert = driver.switch_to.alert
            err_Occur = 1
            alert.dismiss()
            
     except:
        print("no alert")
     
     
     
     while len(driver.window_handles) ==2:
        print(driver.window_handles)
        driver.find_element(By.XPATH,'//*[@id="reLoad"]').click()
        tryChaptchaAgain()
        driver.find_element(By.CSS_SELECTOR,'#answer').send_keys(image_ocr)
        driver.find_element(By.CSS_SELECTOR,'th:nth-child(6) > span > input[type=button]').click()
        numtry += 1
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            print("-----------------------------alert accur------------------------------")
            
            alert = driver.switch_to.alert
            err_Occur = 1
            alert.dismiss()
            
        except:
            print("no alert")
            
        
print("end")
time.sleep(2)
# driver.quit()
'''
while True:
    try:
        print("type 'start'")
        startkey = '0'
        startkey = input()
        print('1')
        if startkey == "start":
            print('2')
                
            driver.find_element(By.CSS_SELECTOR,'li:nth-child(1) > span > a').click()
            print('3')
            #창로딩될 때까지 확인후 전환
            while driver.window_handles[-1] == driver.window_handles[0]:
                print(driver.window_handles[-1])
            
            driver.switch_to.window(driver.window_handles[-1])
            #첫번째 날짜 선택까지 반복(예외처리)
            while True:
                try:
                    #child 3번 부터 1번째 선택
                    driver.find_element(By.CSS_SELECTOR, 'tr:nth-child(3) > td:nth-child(1) > a').click() #3번 부터 시작
                    break  
                except:   
                    pass
                
            print('current window1',driver.window_handles,len(driver.window_handles))
            
            print('-------------------')
            time.sleep(0.03)
            imgbinary()
            imgocr()
            print("is", image_ocr,len(image_ocr))
            driver.find_element(By.CSS_SELECTOR,'#answer').send_keys(image_ocr)
            driver.find_element(By.CSS_SELECTOR,'th:nth-child(6) > span > input[type=button]').click()
            numtry += 1
            try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    print("-----------------------------alert accur------------------------------")
                    
                    alert = driver.switch_to.alert
                    err_Occur = 1
                    alert.dismiss()
                    
            except:
                print("no alert")
            
            
            
            while len(driver.window_handles) ==2:
                print(driver.window_handles)
                driver.find_element(By.XPATH,'//*[@id="reLoad"]').click()
                tryChaptchaAgain()
                driver.find_element(By.CSS_SELECTOR,'#answer').send_keys(image_ocr)
                driver.find_element(By.CSS_SELECTOR,'th:nth-child(6) > span > input[type=button]').click()
                numtry += 1
                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    print("-----------------------------alert accur------------------------------")
                    
                    alert = driver.switch_to.alert
                    err_Occur = 1
                    alert.dismiss()
                    
                except:
                    print("no alert")
        
        print('4')

            # Switch to the new window
            
            
            
        print("end")
    except:
        print('error')
        pass
    time.sleep(3)
        
    driver.switch_to.window(driver.window_handles[0])
'''