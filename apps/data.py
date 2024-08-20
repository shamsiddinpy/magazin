import requests
from bs4 import BeautifulSoup


def get_products_from_website():
    url = "https://www.carmodoo.com/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('div', class_='offer-wrapper')

        product_list = []
        for product in products:
            try:
                name = product.find('h3', class_='lheight22 margintop5').text.strip()
                price = product.find('div', class_='price').text.strip()
                description = product.find('p', class_='hidden-xs').text.strip()
                product_list.append({
                    "name": name,
                    "price": price,
                    "description": description
                })
            except (AttributeError, TypeError):
                continue
        return product_list
    except requests.exceptions.RequestException as e:
        print(f"Xatolik: {e}")
        return []


def send_products_to_backend(product_list):
    endpoint_url = "http://127.0.0.1:8000/api/products"
    for product in product_list:
        data = {
            "name": product['name'],
            "price": product['price'],
            "description": product['description']
        }

        response = requests.post(endpoint_url, json=data)
        if response.status_code == 201:
            print(f"Mahsulot yaratildi: {product['name']}")
        else:
            print(f"Xatolik: {response.status_code}, Mahsulot: {product['name']}")


if __name__ == "__main__":
    products = get_products_from_website()
    send_products_to_backend(products)

# knde
