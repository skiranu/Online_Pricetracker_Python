#Importing libraries that are required
import requests as req
import smtplib
from bs4 import BeautifulSoup as bs
import time
from email.mime.text import MIMEText


#Create a txt file with 1) sender username 2) sender pw 3) receiver username
f = open("Credentials.txt", 'r')
Email1 = f.readline()
password = f.readline()
Email2 = f.readline()

# Getting the desired page for tracking the prices.
URL = "https://www.flipkart.com/apple-iphone-12-pro-max-pacific-blue-128-gb/p/itmd89812b558a03?pid=MOBFWBYZZABKHZQA&lid=LSTMOBFWBYZZABKHZQACQ9MLL&marketplace=FLIPKART&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_2_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_4_na_na_na&fm=SEARCH&iid=bf751ed9-675b-4aaf-8216-56322518faf3.MOBFWBYZZABKHZQA.SEARCH&ppt=hp&ppn=homepage&ssid=bx4yki9cn40000001612849994707&qH=5a7a12c4a730c1af"

while True:
    page = req.get(URL)
    soup = bs(page.content, "html.parser")

    # Use whatever class is present in inspect Element of the website; this changes on each website.
    price = soup.find("div", {"class":"CEmiEU"}).text
    product = soup.find("div", {"class":"aMaAEs"}).text
    # trim only the required product name from the html text
    product_name = product[:46]
    # iterate to remove the price symbol.
    price = price[1:]
    # This is used to remove the "," to make the data type as number.
    price_ar = price.split(",")
    price = ''.join(price_ar)
    price = int(price)


    # Comparing the price, creating a threshold value.
    if price < 129990:
        try:
            #port for gmail is 587
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login(Email1, password)

        except:
            print("Couldnt setup email with the given credentials")

        #Setting the product description:
        price1 = product_name + "/n Costs ₹" +str(price)
        msg = MIMEText(price1)
        msg['Subject'] = product_name
        msg['To'] = Email2
        msg['From'] = Email1
        try:
            gmail.send_message(msg)
        except:
            print("Couldnt send the mail")
        time.sleep(5)
