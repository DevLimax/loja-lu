LOJA-LU 

Esse projeto foi feito para demonstrar minha experiencia com o framework FastAPI que vem se tornando bastante promissor com sua simplicidade e funcionamento, 
nesse projeto busquei extrair o maximo do meu conhecimento com a linguagem.

O projeto é um modelo teste feito para a avaliação pratica de desenvolvedor back-end pela InfoG2 (empresa de tecnologia) fui selecionado e me passaram esse teste de codificação para realizar.
infelizmente pela falta de tempo e o prazo, acabei não realizando esse teste a tempo, ate por conta de ja estar em um emprego, mas seria um otimo começo na areá de desenvolvimento que tanto almejo,
então para testar a mim mesmo resolvi fazer esse teste e deixar salvo em meu github como aprendizagem e para revisão.

Problema do "cliente": 
A Lu Estilo é uma empresa de confecção que está buscando novas
oportunidades de negócio, mas o time comercial não possui nenhuma
ferramenta que facilite novos canais de vendas.

Para ajudar o time comercial, você deve desenvolver uma API RESTful
utilizando FastAPI que forneça dados e funcionalidades para facilitar a
comunicação entre o time comercial, os clientes e a empresa. Essa API deve ser
consumida por uma interface Front-End, que será desenvolvida por outro time.

Implemente uma funcionalidade adicional na API que permita o envio de
mensagens de WhatsApp para clientes utilizando WhatsApp API.

Banco de dados utilizado: PostgresSQL

Models:
<img width="1724" height="837" alt="Models" src="https://github.com/user-attachments/assets/11852451-28e6-4a80-9011-b31de9f6c4cb" />
usei o alembic para facilitar os processos de migrações no banco de dados e cheguei ao resultado final ilustrado nessa imagem,
o banco teve varias alterações que estavam interferindo no resultado final.

Swagger & Docs:  

<img width="1920" height="865" alt="Screenshot from 2025-08-04 09-52-03" src="https://github.com/user-attachments/assets/0ea90067-b639-40c8-8e53-2f2d8ce277d0" />
<img width="1920" height="865" alt="Screenshot from 2025-08-04 09-51-41" src="https://github.com/user-attachments/assets/2489d3a8-3181-47b6-be0e-2b0c52d01267" />
<img width="1920" height="865" alt="Screenshot from 2025-08-04 09-53-36" src="https://github.com/user-attachments/assets/16ce7e2c-3051-4fe1-b9e2-ede0e6c0ccec" />
O FastAPI facilita a documentação da API implementando o Swagger e o Doc automaticamente, sendo possivel validar ambos por meio do (docs) ou (redoc), isso facilita muito a vida do desenvolvedor
que tem somente o trabalho de configurar as respostas e textos para deixar a documentação ainda mais acessivel.                                                                                  


Endpoints: Usuário / Clientes / Produtos / Pedidos / Mensagens

-> Usuarios / Autenticação:

<img width="1463" height="301" alt="image" src="https://github.com/user-attachments/assets/f52b5a2e-10b6-47a8-a7fa-2b5a28d060af" />
Esse endpoint consiste em conectar o usuário (time de vendas) com a interface do sistema para que o usuário tenha acesso as demais funções que são protegidas com Token JWT, apartir disso o
usuário tera as permissões necessarias para realizar suas tarefas de acordo com seu nivel de permissão.



Exemplos:

POST /api/v1/auth/login:
<img width="1522" height="392" alt="Screenshot from 2025-08-04 10-42-55" src="https://github.com/user-attachments/assets/13172fb8-d076-41d7-ad7b-9cc3decfeaf6" />
realiza o login do usuário por FormData e retorna o access e refresh token.


POST /api/v1/auth/refresh-token:
<img width="1522" height="392" alt="Screenshot from 2025-08-04 10-45-18" src="https://github.com/user-attachments/assets/540a0101-b78b-419a-9069-209a6577a4d8" />
cria um novo access token e refresh token, apartir o refresh-token anterior, serve justamente para renovar o login do usuário sem a necessidade de fazer login novamente, o refresh-token tem
duração de 12 dias para expirar.


POST /api/v1/auth/register:
<img width="1519" height="408" alt="Screenshot from 2025-08-04 10-47-59" src="https://github.com/user-attachments/assets/90dd0a68-8d2c-4396-aa63-0ef1b4e08b5f" />
cria um novo usuário no sistema (vale lembrar que na criação de usuário a senha é codificada e guardada no banco para ter um maior grau de segurança, para realizar validações como login, a senha
é decoficida para validação.)


GET /api/v1/auth/logged:
<img width="1799" height="264" alt="Screenshot from 2025-08-04 10-52-23" src="https://github.com/user-attachments/assets/4118fda5-3e01-455d-91d7-a6eccad66be2" />
retorna a instancia do usuário logado.


-> Clientes: 

<img width="1309" height="293" alt="Screenshot from 2025-08-04 10-53-27" src="https://github.com/user-attachments/assets/1fa19172-1170-4a36-85e1-2be2ffb79168" />
Esse Endpoint nós tras uma implementação basica de CRUD permitindo o usuário Criar,Editar e Deletar as instancias do modelo (Cliente).

Exemplos:

GET /api/v1/customers/:
<img width="1796" height="727" alt="Screenshot from 2025-08-04 11-36-03" src="https://github.com/user-attachments/assets/e814122a-5e20-4541-95ec-3006cf0050b5" />


GET /api/v1/customers/{customer_id}:
<img width="1793" height="295" alt="Screenshot from 2025-08-04 11-36-21" src="https://github.com/user-attachments/assets/865eb727-6484-4be6-bd7d-f0eee196d628" />


POST /api/v1/customers/
<img width="1796" height="462" alt="Screenshot from 2025-08-04 11-03-50" src="https://github.com/user-attachments/assets/19a515c9-8cde-4166-ac33-b4845e270539" />
nesse método há validações de Email, CPF e Telefone, se caso tenha um cliente com algum valor desse ja existente o Endpoint retorna um erro 409 (Conflict),
o CPF deve conter 11 caracteres, e o telefone deve conter o DDD do Brasil (55) junto do DDD do estado ex: (85) -> 5585921616652


PUT /api/v1/customers/{customer_id}
<img width="1799" height="416" alt="Screenshot from 2025-08-04 11-11-19" src="https://github.com/user-attachments/assets/60681e24-d430-42c0-bb2a-053218a5ccd5" />
as validações mencionadas anteriormente vale para essa função tambem.


DELETE /api/v1/customers/{customer_id}
204 - No content


-> Produtos:

<img width="1317" height="299" alt="products" src="https://github.com/user-attachments/assets/d5446f49-46f8-4bf8-ac05-872438437e4b" />
Esse Endpoint nós tras uma implementação basica de CRUD permitindo o usuário Criar,Editar e Deletar as instancias do modelo (Produto).

Exemplos:

GET /api/v1/products/:
<img width="1795" height="545" alt="Screenshot from 2025-08-04 11-52-28" src="https://github.com/user-attachments/assets/3d4acfc7-30bb-412e-b057-55fce49e9fda" />
- Filtros:
category, price, is_avaliable

GET /api/v1/products/{product_id}:
<img width="1802" height="446" alt="get-id" src="https://github.com/user-attachments/assets/a74717b4-f14e-412d-9415-ebd74e07d4d8" />


POST /api/v1/products/:
<img width="1798" height="732" alt="post" src="https://github.com/user-attachments/assets/bd2e1e0d-9690-45d1-bcae-3f1c79348646" />


PUT /api/v1/products/{product_id}:
<img width="1795" height="636" alt="put" src="https://github.com/user-attachments/assets/5fc9c106-b7d6-4a9e-9069-e9496b17187d" />

  
DELETE /api/v1/products/{product_id}:
204 - No content
  

-> Pedidos:

<img width="1317" height="299" alt="orders" src="https://github.com/user-attachments/assets/44bce57d-b72e-426b-b0ef-7942d055ad09" />
Esse Endpoint nós tras uma implementação basica de CRUD permitindo o usuário Criar,Editar e Deletar as instancias do modelo (Pedido).

Exemplos:

GET /api/v1/orders/:
<img width="1795" height="545" alt="get-all" src="https://github.com/user-attachments/assets/89409968-646a-423f-a1be-c2034892628e" />
- Filtros:
status, customer_id, start_date/end_date, category


GET /api/v1/orders/{order_id}:
<img width="1795" height="545" alt="get-id" src="https://github.com/user-attachments/assets/4214d7c6-30a2-45fa-8ca4-d4989ccdfdfa" />


POST /api/v1/orders/:
<img width="1795" height="729" alt="post" src="https://github.com/user-attachments/assets/114dceba-e95d-4e9c-9198-3437c518650d" />
(Quando um novo pedido é criado, a integração da loja com o whatssap envia uma mensagem automatica para o cliente cadastrado no pedido)


PUT /api/v1/orders/{order_id}:
<img width="1798" height="589" alt="Screenshot from 2025-08-04 13-15-07" src="https://github.com/user-attachments/assets/a7a27534-eda8-4e27-ba2e-b3723c5717f2" />
(Caso uma das alterações seja o status do pedido, é enviado uma mensagem automatica informando o novo status do pedido para o cliente cadastrado no pedido)


DELETE /api/v1/orders/{order_id}:
204 - No content


-> Mensagens (integração com Whatssap)

<img width="1312" height="153" alt="messages" src="https://github.com/user-attachments/assets/a179eb1b-2bbe-4117-9c4d-f2e6ccd51958" />
para resolver esse desafio pesquisei mais a fundo sobre a API do whatsapp, como a API original é cobrado um valor para uso, resolvi utilizar outro meio que é o EvolutionAPI, uma API muito facil
de usar e que permite a nós enviar de um simples texto a um chatbot sem custo nenhum.

não consegui ter muita criatividade para mensagens prontas, mas consegui colocar o Basico como o envio de peças em promoção e pedidos feitos.

Exemplos:

POST /api/v1/messages/send_order/{order_id}:
<img width="1794" height="221" alt="Screenshot from 2025-08-04 13-31-36" src="https://github.com/user-attachments/assets/83185d31-9556-4575-a117-020d71b29d05" />
nessa rota é algo simples e facil de se entender, oque acontece nesse Endpoint é que ele necessita de um pedido criado para funcionar, o usuário coloca o ID do pedido e o endpoint busca no banco de dados o pedido e todos os seus dados contidos, logo após achar o pedido o endpoint aciona uma função que envia uma mensagem automatica para o número do cliente cadastrado no pedido. enviando assim dados como: ID do pedido, Preço total, Peças, Nome do cliente, Status do pedido, (essa função de mensagem automatica está implementada na criação do pedido, quando um pedido é criado, automaticamente essa função é ativada e envia a mensagem para o cliente, sendo assim esse Endpoint so é necessario caso haja algum erro no Endpoint de criação de pedido ou o cliente solicite novamente os dados do seu pedido.)

Mensagem:
  
  <img width="286" height="238" alt="Screenshot from 2025-08-04 13-45-34" src="https://github.com/user-attachments/assets/ae37ed8b-9e1a-40c3-8390-ef1666ad9621" />


POST /api/v1/messages/send_promotion/{product_id}
<img width="1805" height="387" alt="Screenshot from 2025-08-04 13-40-59" src="https://github.com/user-attachments/assets/c5be1cd0-f31d-4951-ac42-1007bfcd0f05" />
aqui é necessario preencher os campos customer_id e promotion_price, e automaticamente o endpoint envia uma mensagem automatica de promoção do produto escolhido para o cliente

Mensagem:
  
  <img width="271" height="116" alt="Screenshot from 2025-08-04 13-47-03" src="https://github.com/user-attachments/assets/5108245d-56eb-45f0-b974-8a6ac57cd9cc" />


Como rodar o projeto ?

1 - Certifique-se de que o python está instalado na sua maquina.

2 - Copie a pasta do projeto no Github para sua maquina e abra no seu editor de texto (Vscode, Cursor, etc)

3 - Crie um Ambiente Virtual com o codigo -> python3 -m venv venv

4 - Entre no seu ambiente virtual e baixe as dependencias -> pip install -r requirements.txt

5 - Configurar o banco de dados:
<img width="661" height="119" alt="Screenshot from 2025-08-04 13-59-13" src="https://github.com/user-attachments/assets/33775e6d-8344-4478-8ea5-29a1815929be" />
Não se esqueça de criar um banco para o projeto (pode ser de sua preferencia, PostgresSQL, SQLITE, MongoDB) 
altere o (lima) e (postgres) para seu usuario e senha do banco. 

6 - Rodar o arquivo (main.py)

Conclusões:

Esse projeto foi essencial para testar minha capacidade com o framework FASTAPI, é uma tecnologia muito simples e que promete se tornar uma das mais utilizadas para desenvolvimento WEB com python, estou em constante desenvolvimento com as tecnologias que a linguagem tem a proporcionar, e em breve irei continuar alimentando meu portfolio com mais projetos com FastAPI, Django e afins. agradeço desde ja pelo tempo que tiveram para ler esse documento.
