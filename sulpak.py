from bs4 import BeautifulSoup
import requests


with open("laptops.txt", "w", encoding="utf-8") as file:
    
    for page in range(1, 11):
        url = f'https://www.sulpak.kg/f/noutbuki?page={page}'
        response = requests.get(url)
        
        
        if response.status_code != 200:
            print(f"Ошибка при запросе {page}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "lxml")
        
        
        products = soup.find_all("div", class_="product__item")
        
        for product in products:
            name = product.find("div", class_="product__item-name").text.strip()
            
            price_tag = product.find("div", class_="product__item-price")
            price = price_tag.text.strip() if price_tag else "Цена не указана"
            
            img_tag = product.find("img", class_="product__item-image")
            img_url = img_tag['data-src'] if img_tag and 'data-src' in img_tag.attrs else "Изображение отсутствует"

            file.write(f"Название: {name}\nЦена: {price}\nФото: {img_url}\n\n")
            print(f"Название: {name}, Цена: {price}, Фото: {img_url}")

print("Парсинг завершен.")