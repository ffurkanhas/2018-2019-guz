import urllib.request  as urllib2
from bs4 import BeautifulSoup
import json
import datetime
import time
import os

baseUrl = "https://www.sahibinden.com"

dataJsonFile = open('data.json', 'a')
dataJsonFile.write("[")
logFile = open("log.txt", 'a')

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
logFile.write("----------------\nThe last time: " + str(st) + "\n")

lineNumber = 0

request = urllib2.Request(baseUrl + "/satilik/ankara", headers={"User-Agent": "request"})
contents = urllib2.urlopen(request).read()
soup = BeautifulSoup(contents, "html.parser")

totalAdvText = soup.find("div", attrs={"class": "result-text"}).findAll('span')[1].text
totalAdv = str(totalAdvText[0:str(totalAdvText).index(" ")])

totalAdvAsNumber = int(totalAdv.replace(".", ""))

def parseQuarterPage(quarterLink):
    request = urllib2.Request(quarterLink, headers={"User-Agent": "request"})
    contents = urllib2.urlopen(request).read()
    soup = BeautifulSoup(contents, "html.parser")

    if (soup.find("div", attrs={"class": "pageNavTable"}) is None): #tek sayfa ilan varsa eger
        if(soup.find("div", attrs={"class": "sortedTypes"}) is not None): #ilan var
            print(quarterLink.strip() + " one page is processing...")
            logFile.write(quarterLink.strip() + " one page is processing...\n")
            parseAdvertisementPage(quarterLink)
        else: #ilan yok
            print("there is no advertisement: " + quarterLink.strip())
    else:
        pageTable = soup.find("div", attrs={"class": "pageNavTable"})
        allPages = pageTable.findAll('a')
        lastPageNumber = int(allPages[len(allPages) - 2].text) #?pagingOffset=20
        for i in range(1, lastPageNumber + 1):
            print(quarterLink.strip() + " " + str(i) + "/" + str(lastPageNumber) + " page" + " is processing...")
            logFile.write(quarterLink.strip() + " " + str(i) + "/" + str(lastPageNumber ) + "page" + " is processing...\n")
            calculatedOffset = str((int(i) - 1) * 20)
            quarterLink = quarterLink.strip()
            wholePageLink = (quarterLink + "?pagingOffset=" + calculatedOffset)
            parseAdvertisementPage(wholePageLink)

def parseAdvertisementPage(pageLink):
    request = urllib2.Request(pageLink, headers={"User-Agent": "request"})
    contents = urllib2.urlopen(request).read()
    soup = BeautifulSoup(contents, "html.parser")

    advertLinks = soup.findAll("a", attrs={"class": "classifiedTitle"})
    for link in advertLinks:
        parseAdvertiseInfo(baseUrl + link['href'])

def parseAdvertiseInfo(advertiseLink):
    request = urllib2.Request(advertiseLink, headers={"User-Agent": "request"})
    contents = urllib2.urlopen(request).read()
    soup = BeautifulSoup(contents, "html.parser")

    advNameH1 = soup.find("h1")
    advName = str(advNameH1.text).strip()

    allInfos = soup.find("div", attrs={"class": "classifiedInfo "})
    h3Info = allInfos.find("h3")
    h2Info = allInfos.find("h2")
    locationsInfo = h2Info.findAll("a")
    location = str(locationsInfo[0].text).strip() + "\\" + str(locationsInfo[1].text).strip() + "\\" + str(locationsInfo[2].text).strip()

    unneccessaryTextIndex = int(h3Info.text.index("Emlak Endeksi"))
    price = str(h3Info.text[0:unneccessaryTextIndex]).strip()

    turkceKarakter = str.maketrans("ÇĞİÖŞÜçğıöşü", "CGIOSUcgiosu")

    dictionary = {}
    dictionary["Ilan Ismi"] = advName.translate(turkceKarakter)
    dictionary["Fiyat"] = price
    dictionary["Adres"] = location

    otherInfos = allInfos.findAll("li")

    for otherInfo in otherInfos:

        tagName = str(otherInfo.find("strong").text).strip()
        tagName = tagName.translate(turkceKarakter)

        tagInfo = str(otherInfo.find("span").text).strip()
        tagInfo = tagInfo.translate(turkceKarakter)

        dictionary[tagName] = tagInfo

    json.dump(dictionary, dataJsonFile, indent=4,ensure_ascii=False)
    dataJsonFile.write(",")
    global lineNumber
    lineNumber += 1

    print("Process completed: " + str(lineNumber) + "/" + str(totalAdv) + " %" + "{0:.5f}".format(float(lineNumber/totalAdvAsNumber * 100)) )

def readSpecificLineOfFile(lineNumber):
    allQuarterListFile = open("links.txt", 'r')
    tmpLineNumber = 0
    specificLine = ""
    for readedLine in allQuarterListFile:
        if (tmpLineNumber == lineNumber):
            specificLine = readedLine
            break
        tmpLineNumber += 1
    return specificLine

def main():
    allQuarterListFile = open("links.txt", 'r')
    print("naneB Sahibinden Scraper")
    print("Scraping is on process...")
    continueLine = 0
    while True:
        try:
            breakPoint = readSpecificLineOfFile(int(continueLine))
            parseQuarterPage(breakPoint)
            continueLine += 1
            if continueLine == 1486:
                break
        except Exception as e:

            duration = 3  # second
            freq = 800  # Hz
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))

            print(str(e))
            print("Resuming on: " + breakPoint)
            pass

    dataJsonFile.write("{}]")
    dataJsonFile.close()
    logFile.close()
    allQuarterListFile.close()

if(__name__ == '__main__'):
    main()
    exit(0)