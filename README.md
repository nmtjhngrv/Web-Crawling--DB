# Web-Crawling&DB
DubaiMarine


Özet.

*Python programlama dilinde 'BeatifulSoup' kütüphanesini kullanarak   , 
 
https://www.propertyfinder.ae/en/searchc=1&l=50&ob=mr&page=2&t=1 projede istenilen linkten tüm <div>  ve  pagination_links taglarini  soup ettim.



*Daha sonra islemler tekrar etmesin diye en alt tarafda olan sayfa numarasin page1'den  baslatip page10'a scan ettim.
10.pagination linke geldigim zaman 15 oluyor , bu problemi çözmek için kurdugum mantik pagination linkleri array seklinde götürüyoruz.
 
*Yani aldigimiz sayf son sayfadan küçükse orani almiyor devam ediyor.

*Program günde 1 kere çalistirmak lazim, satilip satimadigi bilgisine burdan ulasa biliriz.

1.gün fiyat link aktiv , 2.gün ayni belli bir günde olmadigi zaman ilan satilmistir sonucuna ulasa biliriz.


from database import Database
from bs4 import BeautifulSoup
import requests, re, json

# database class i burda tanimla 
db = Database()
# table lari oluştur
# Bunun için bizde iki table olucak. 1. Listing: property lerin bilgilerin kayt etmek için
# 2.PRICE: Propertyilerin hangi tarihde hangi fiyata olduklarini kayt edicez.
# Bu programi her gün çalıştırdgimizda bütün property lerin günlere göre fiyatlarini database kayt edicez
# örneğin property 3 gün fiyatlari database kayt edildi 4.günde bu property orda yoksa o zaman bu property satılmıştır.
db.create_tables()

# crawling yapacagimiz url in base domaini
BASE_URL = "https://www.propertyfinder.ae"

# request library ile sayfanin contenti götürcez.
page = requests.get("https://www.propertyfinder.ae/en/search?c=1&l=50&ob=mr&page=2&t=1")
content = page.content
# soupu  tanımlıycaz
soup = BeautifulSoup(content, 'html.parser')

# sayfada en alt tarafda olan pagination linklerini götürcez.
paginationDiv = soup.find("div",{"class":"pagination_links"})

# paginationDiv içinde olan pagination_link a taglerini arraya tanımlıycaz.
pagination = paginationDiv.findAll("a",{"class":"pagination_link"})

# Şimdiye kadar ne kadar property göturdugumuzu kayd etmek için variable oluşturcaz.
propertyCount = 0
# En son hangi page i taradigimizi kaytetmek için variable olusturcaz.
lastScannedPageNumber = 0;

# En son taradigimiz page pagination array in en son uyegisine beraber olmadikca dongude kal
# Burda yapmak istedigimiz mantik her sayfada 10 pagination_link gozukuyor ve en sona geldigimizde 
# 5 tane daha sayfa cikiyor. örnek. 1 i page de 1 den 10 a kadar pagination_link gozukuyor
# 10 cu sayfada 5 den 15 e kadar pagination_link ler gozukuyor. 
# Fakat en son sayfaya geldigimizde yeni pagination_link gozukmuyor bu yuzden en son 
# taradigimiz sayfa yeni pagination_list in en son uyesine beraber ise o zaman butun 
# sayfalar taranmiş olcak.
while int(pagination[len(pagination) - 1].text) != lastScannedPageNumber:

    # Pagination array in kacinci uyesinde oldugumuzu kayt edelim
    pageIndex = 0;


    # Arrayin her bir uyesini goturelim
    for page in pagination:
        # Tarayagacigimiz sayfanin URL i goturuyoruz
        pageURL = BASE_URL + page['href']

        # pageIndexi her dongude bir kez artir
        pageIndex += 1;

        # Eger simdiki oldugumuz sayfanin rakami en son taradigimiz sayfanin numarasindan buyukse 
        # o zaman taramaya basla. Bunu yaparak daha once taradigimiz sayfayi ikinci kez taramakdan önluyoruz
        if int(page.text) > lastScannedPageNumber:

            
            print ("Page: {} - LastIndex : {}".format(page.text, lastScannedPageNumber))
            # request library ile page in content in gotur
            propertyPage = requests.get(pageURL)
            # bu page ichin soup tanimla
            pageSoup = BeautifulSoup(propertyPage.content, 'html.parser')

            # Her bir property bilgisini <div class="cardlist_item"> tag-in de 
            # oldugu ichin bu sayfada olan butun propertyleri goturuyoruz
            for item in pageSoup.findAll("div",{"class":"cardlist_item"}):
                # Property goturduyumuz anda count u bir kere artir
                propertyCount += 1;
                # Property in URL i gotur
                url = BASE_URL + item.find("a")['href']
                # Property in Price ini gotur
                price = item.find("span",{"class":"card_pricevalue"}).get_text()
                # Property in Ismini gotur
                title = item.find("h2",{"class":"card_title"}).get_text()
                # Property in Konomunu gotur
                location = item.find("p",{"class":"card_location"}).get_text()
                print("Count: {}\nURL: {}\nPrice: {}\nTitle: {}\nLocation: {}\n".format(propertyCount ,url, price, title, location))

                # Her bir property de URL farkli oldugu ichin boyle bir property in 
                # URL ile bizim database de olup olmadigini yokluycaz
                data = db.get_listing_by_url(url=url)
                if data:
                    # Bu property bizim database de varsa o zaman price table ina bugunun tarihine olan fiyatini yazcaz
                    db.add_price(listing_id=data[0], price = int(price.replace(",","")))
                else:
                    # Bu property bizim database de yoksa o zaman database e ekle
                    id = db.add_listing(title, url, location)
                    # ve ekledikden sonra bugunun tarihine olan fiyatini yaz
                    db.add_price(listing_id = id, price = int(price.replace(",","")))
            # Pagination Array in en son uyegisinde olup olmadigini yokla
            if pageIndex == len(pagination):
                # En son uyegisine geldiyimiz zaman pagination array ni yukarida yaptigimiz gibi 
                # Yeniden tara ve yeni malumatlari buraya yaz 

                # sayfada en alt tarafda olan pagination linklerini gotur
                paginationDiv = pageSoup.find("div",{"class":"pagination_links"})

                # paginationDiv icherisinde olan pagination_link a taglerini arraya tanimla
                pagination = paginationDiv.findAll("a",{"class":"pagination_link"})

                # En son bu hangi page numarasini taradigimiz kayd et 
                lastScannedPageNumber = int(page.text)

# Database i kapat        
db.close()
