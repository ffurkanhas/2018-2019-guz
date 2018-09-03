from selenium import webdriver
from pyvirtualdisplay import Display
import time

town = 1
district = 0
townName = ""
districtName = ""

options = webdriver.FirefoxOptions()
options.add_argument('-headless')

display = Display(visible=0, size=(800, 600))
display.start()

mainPageUrl = "https://www.sahibinden.com/kategori/emlak-konut"

def scraping(nextTown, nextDistrict):
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(mainPageUrl)

    driver.find_element_by_xpath("//div[@class='sahibindenSelect closed city']").click()  # click to city list
    cityDropDownMenu = driver.find_element_by_xpath("//div[@class='sahibindenSelect city activeSelect']")  # get city list
    ankara = cityDropDownMenu.find_element_by_xpath("//li[@data-value='6']")  # get "Ankara" in list
    ankara.click()  # it is clicking to "Ankara"
    time.sleep(2)
    townDropDownMenu = driver.find_element_by_xpath("//div[@class='sahibindenSelect closed town']")
    townDropDownMenu.click()
    townsPane = townDropDownMenu.find_elements_by_xpath("//div[@class='jspPane']")
    townsList = townsPane[2].find_elements_by_tag_name('li')  # get all "İlçe" list
    townsList[0].click()  # click "İlçe"
    areListsActive = False
    for i in range(nextTown, len(townsList)):
        global town
        town = i
        driver.find_element_by_xpath("//h3[@class='category-name']").click()  # click an empty space
        if (areListsActive == False):
            driver.find_element_by_xpath("//div[@class='sahibindenSelect town activeSelect closed']").click()
        else:
            driver.find_element_by_xpath("//div[@class='sahibindenSelect town closed']").click()
        time.sleep(3)
        global townName
        townName = townsList[i].text
        townsList[i].click()  # click to next "İlçe"
        time.sleep(1)
        if (areListsActive == False):
            districtDropDownMenu = driver.find_element_by_xpath(
                "//div[@class='sahibindenSelect closed district']")  # get "Mahalle" of selected district
        else:
            districtDropDownMenu = driver.find_element_by_xpath(
                "//div[@class='sahibindenSelect district closed']")  # get "Mahalle" of selected district
        districtDropDownMenu.click()
        districtList = districtDropDownMenu.find_elements_by_xpath(
            "//label[@class='quarter-label']")  # get *all* "Mahalle" of selected district
        for j in range(nextDistrict, len(districtList) - 1):
            global district
            district = j
            time.sleep(1)
            global districtName
            districtName = districtList[j].text
            districtList[j].click()  # click to next district in district drop down menu
            driver.find_element_by_xpath("//h3[@class='category-name']").click()  # click an empty space
            searchButton = driver.find_element_by_xpath("//a[@class='btn search']")  # get "Ara" button
            searchButton.click()  # click "Ara" button

            print(driver.current_url)  # print current page's url

            driver.get(mainPageUrl)  # go to the main page
            driver.find_element_by_xpath("//div[@class='sahibindenSelect closed city']").click()  # click to city list
            cityDropDownMenu = driver.find_element_by_xpath(
                "//div[@class='sahibindenSelect city activeSelect']")  # get city list
            cityDropDownMenu.find_element_by_xpath("//li[@data-value='6']").click()  # click to "Ankara"
            time.sleep(2)
            townDropDownMenu = driver.find_element_by_xpath("//div[@class='sahibindenSelect closed town']")
            townDropDownMenu.click()
            townsPane = townDropDownMenu.find_elements_by_xpath("//div[@class='jspPane']")
            townsList = townsPane[2].find_elements_by_tag_name('li')
            townsList[i].click()
            time.sleep(1)
            mahalleList2 = driver.find_element_by_xpath("//div[@class='sahibindenSelect closed district']")
            mahalleList2.click()
            time.sleep(1)
            districtList = mahalleList2.find_elements_by_xpath("//label[@class='quarter-label']")
        areListsActive = True

def main():
    print("naneB Sahibinden Crawler")
    print("Scraping is on process...")
    while True:
        try:
            scraping(town, district)
            break
        except Exception as e:
            print(str(e))
            print("Resuming on: " + townName + "(" + str(town) + ") " + districtName + "(" + str(district) + ")")
            pass

    print ("Proccess is completed")

if(__name__ == '__main__'):
    main()
    display.stop()
