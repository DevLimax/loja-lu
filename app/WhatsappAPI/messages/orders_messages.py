import requests

from models.order_model import OrderModel

url = "http://localhost:8080/message/sendText/loja-lu"
headers = {
        "apikey": "ws4qopmz3jhuzmond6qm7d",
        "Content-Type": "application/json"
    }

async def send_message_new_order(number: str,
                                 order: OrderModel,
                                 products_str: str
):  
    payload = {
        "number": str(number),
        "textMessage": {"text": f"""LOJA LU👕
Ola, {str(order.customer.first_name).title()}!
Segue Abaixo Os Dados Do Seu Pedido!\n
🧾Pedido #{order.id}
💰Preço Total: R${order.total_price:.2f}
📍Status: {str(order.status.value).title()}
📦Produtos:
  {products_str}"""}
}
    
    response = requests.request("POST", 
                                url=url, 
                                headers=headers,
                                json=payload)
    
    if response.status_code == 201:
        print("Mensagem Automatica Enviada!")
        return True
    
    else:
        print(f"Error ao enviar mensagem: {response.status_code, response.text}")
        return False

async def send_message_update_status(number: str,
                                     order: OrderModel,
                                     ):
    first_name: str = order.customer.first_name
    status: str = order.status.value

    payload = {
        "number": str(number),
        "textMessage": {"text": f"""ATUALIZAÇÃO DE STATUS\n\nOla {first_name.title()}\nSeu Pedido #{order.id}\nAtualizou o Status Para: {status.title()}"""}
    }

    response = requests.request("POST", 
                                url=url, 
                                headers=headers,
                                json=payload)
    
    if response.status_code == 201:
        print("Mensagem Automatica Enviada!")
        return True
    
    else:
        print(f"Error ao enviar mensagem: {response.status_code, response.text}")
        return False


if __name__ == "__main__":
    ...
