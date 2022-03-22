import json
from os import link
import requests
from bs4 import BeautifulSoup
data=[]
headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
    }
def getProductLink():
    urlId=1
    for i in range(1):
        url1="https://www.trendyol.com/erkek-t-shirt-x-g2-c73?pi=1"+str(urlId)
        page=requests.get(url1, headers=headers)
        htmlPage= BeautifulSoup(page.content,'html.parser')
        products=htmlPage.find_all("div", class_="p-card-chldrn-cntnr")
        for product in products:
            links=product.find("a")
            link="https://www.trendyol.com"+links.get("href")
            getProductDetail(link)
        urlId+=1
    print(data)   
    print("data")
def getProductDetail(link):
    productData={"productUrl":"", "productName":"", "productPrice":"", "productImageUrl":{}, "productDetail":{}}
    page=requests.get(link, headers=headers)
    productPage= BeautifulSoup(page.content,'html.parser')
    imagesProduct=productPage.find_all("img")
    for imageProduct in imagesProduct:
        productData["productImageUrl"][imageProduct.get("alt")]=imageProduct.get("src")
    productData["productUrl"]=link
    productData["productName"]=(productPage.find("h1", class_="pr-new-br").getText())
    productData["productPrice"]=(float(productPage.find("span", class_="prc-dsc").getText().split("TL")[0].replace(".","").replace(",",".")))
    productsDetail=productPage.find_all("li", class_="detail-attr-item")
    for productDetail in productsDetail:
        productData["productDetail"][productDetail.find("span").getText()]=(productDetail.find("b").getText())
    data.append(productData)
getProductLink()