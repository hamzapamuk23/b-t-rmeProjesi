import json
import requests
from bs4 import BeautifulSoup
data=[]
headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
    }
def getToolBars():
    response=json.loads(requests.get("http://localhost:8080/toolbar").text)
    return response["_embedded"]["toolbars"]


def getCategoryLink():
    toolbarData=getToolBars()
    toolbarID=""
    # productData={"navigationDrawer":{}, "productName":"", "productPrice":"", "productImageUrl":{}, "productDetail":{}}
    categoryPage=BeautifulSoup(requests.get("https://www.trendyol.com/", headers=headers).content,'html.parser')
    topCategory=categoryPage.find_all("li", class_="tab-link")
    for category in topCategory:
        navigationDrawerLink=category.find("a").get("href")
        navigationDrawerName=category.find("a").getText()
        print("-------"+navigationDrawerName+"---**-----")
        subcategory=category.find_all("div", class_="normal-column")
        for j in subcategory:
            deneme=j.find_all("li")
            print("--------"+j.find("a").getText()+"----------")
            # datass={"name":"", "toolbar":{"id":""}}
            # deneme1="2369ee30-bf84-4eb6-beb2-e3c7e3faf2e3"
            # datass["toolbar"]["id"]=deneme1
            # datass["name"]=j.find("a").getText()
            # x=requests.post("http://localhost:8080/subcategory",json=datass)
            # print(x.text)
            
            for i in range(len(toolbarData)):
                if toolbarData[i]["name"]==j.find("a").getText():
                    toolbarID=j.find("a").getText()
            print(toolbarID)
            for x in deneme:
                print("Url: https://www.trendyol.com:"+x.find("a").get("href")+" "+"Name:"+x.find("a").getText())    

def getProductLink():
    urlId=1
    for i in range(1):
        url1="https://www.trendyol.com/cep-telefonu-x-c103498?pi="+str(urlId)
        page=requests.get(url1, headers=headers)
        print("Success")
        print(page)
        htmlPage= BeautifulSoup(page.content,'html.parser')
        print(htmlPage)
        products=htmlPage.find_all("div", class_="p-card-chldrn-cntnr")
        for product in products:
            links=product.find("a")
            link="https://www.trendyol.com"+links.get("href")
            print(link)
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
# getToolBars()
# getCategoryLink()
# data={"name":"asdasd"}
# x=requests.post("http://localhost:8080/toolbar",json=data)
# print(json.loads(x.text))