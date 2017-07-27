from selenium import webdriver
import time
import re

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

user = input("Δώσε username: ")
password = input("Δώσε password: ")
xristis = input("Δώσε id χρήστη: ")

driver.get("http://www.facebook.com")
driver.find_element_by_id("email").send_keys(user)
driver.find_element_by_id("pass").send_keys(password)
driver.find_element_by_id("loginbutton").click()

driver.get("https://www.facebook.com/" + xristis + "/friends")

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(0.5)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

names = []
ids = []
links = []
counter = 0

id = driver.find_elements_by_xpath("//div[@class='fsl fwb fcb']")
for ii in id:
    name = ii.text
    link = re.findall(r'a href="(.*)\?f', ii.get_attribute('innerHTML'))
    counter += 1
    if len(link) > 0:
        fb_id = link[0].replace('//', '/').split('/')
        print(name, link[0], fb_id[2])
        names.append(name)
        ids.append(fb_id[2])
        links.append(link[0])

for i in range(len(names)):
    driver.get(links[i])
    try:
        driver.find_element_by_xpath("//img[@class='profilePic img']").click()
        time.sleep(2)
        driver.get(driver.find_element_by_class_name('spotlight').get_attribute('src'))
        driver.get_screenshot_as_file("img/" + names[i] + ".jpg")
    except:
        print("Could not save image for " + names[i])
    time.sleep(1)

driver.close()
