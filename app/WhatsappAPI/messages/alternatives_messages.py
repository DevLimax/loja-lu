import requests

from typing import List

from models.product_model import ProductModel
from models.product_image import ProductImage

url = "http://localhost:8080/message/sendText/loja-lu"
headers = {
        "apikey": "ws4qopmz3jhuzmond6qm7d",
        "Content-Type": "application/json"
}


async def send_message_promotion_product(number: str,
                                         product: ProductModel,
                                         promotion_price: float
):
    promotion_percent: int = ((product.price - promotion_price) / product.price) * 100

    payload = {
        "number": str(number),
        "textMessage": {"text" : f"LOJA LU\nEstamos Com Promoções Imperdiveis!!\n{product.productName} de R${product.price:.2f}\nPor Apenas R${promotion_price:.2f}\nItens Com Ate {promotion_percent:.0f}% De Desconto"}
    }
    
    response = requests.request("POST",
                                headers=headers,
                                url=url,
                                json=payload)
    if response.status_code == 201:
        print("Mensagem automatica enviada!")

    else: 
        print(f"Error ao enviar mensagem: {response.text} - {response.status_code}")    
        
    return response