import requests as req
import smtplib
import time
from bs4 import BeautifulSoup as bs
from email.mime.text import MIMEText

#Reading the contents of this file in secure manner
f = open("Credentials.txt", 'r')
Email1 = f.readline()
password = f.readline()
Email2 = f.readline()
f.close()

URL = "https://www.flipkart.com/apple-iphone-12-pro-max-pacific-blue-128-gb/p/itmd89812b558a03?pid=MOBFWBYZZABKHZQA&lid=LSTMOBFWBYZZABKHZQACQ9MLL&marketplace=FLIPKART&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_2_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_4_na_na_na&fm=SEARCH&iid=bf751ed9-675b-4aaf-8216-56322518faf3.MOBFWBYZZABKHZQA.SEARCH&ppt=hp&ppn=homepage&ssid=bx4yki9cn40000001612849994707&qH=5a7a12c4a730c1af"

while True:
    page = req.get(URL)
    soup = bs(page.content, "html.parser")
    #Use whatever you get in inspect element of the website; changes from website to website
    price = soup.find("div", {"class":"_16Jk6d"}).text
    product = soup.find("div",{"class":"aMaAEs"}).text
    # trimming the product name/content name
    product = product[:46]
    # this is to remove the price symbol
    price = price[1:]
    # Lets remove the comma to convert the price into a number
    price_ar = price.split(",")
    price = ''.join(price_ar)
    price = int(price)


    #comparing logic/ threshold of price
    if price < 129990:
        try:
            #port for gmail
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login(Email1, password)

        except:
            print("Couldnt setup email with the given credentials")


        #setting the mail content:
        price1 = product + "/n Costs ₹" + str(price)
        msg = MIMEText(price1)
        msg['Subject'] = product
        msg['To'] = Email2
        msg['From'] = Email1
        try:
            gmail.send_message(msg)
        except:
            print('Couldnt send email!')
        time.sleep(10)
    else:
        print('Mail not sent as threshold values not met')
