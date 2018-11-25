# Web-Crawling--DB
DubaiMarine


Özet.

*Python programlama dilinde 'BeatifulSoup' kütüphanesini kullanarak   , 
 
https://www.propertyfinder.ae/en/searchc=1&l=50&ob=mr&page=2&t=1 projede istenilen linkten tüm <div>  ve  pagination_links taglarini  soup ettim.



*Daha sonra islemler tekrar etmesin diye en alt tarafda olan sayfa numarasin page1'den  baslatip page10'a scan ettim.
10.pagination linke geldigim zaman 15 oluyor , bu problemi çözmek için kurdugum mantik pagination linkleri array seklinde götürüyoruz.
 
*Yani aldigimiz sayf son sayfadan küçükse orani almiyor devam ediyor.

*Program günde 1 kere çalistirmak lazim, satilip satimadigi bilgisine burdan ulasa biliriz.

1.gün fiyat link aktiv , 2.gün ayni belli bir günde olmadigi zaman ilan satilmistir sonucuna ulasa biliriz.
