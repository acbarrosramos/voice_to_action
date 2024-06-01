
##### 1. Criar uma conta no Twilio e subistituir no arquivo .env TWILIO_ACCOUNT_SID TWILIO_AUTH_TOKEN pelo que sera fornecido assim que a conta for criada:

##### 2. Entrar no site do ngrok e seguir os passos da instalação para seu sistema operacional:

https://dashboard.ngrok.com/login

##### 3. Instalar as dependencias:
pip install -r requirements.txt

##### 4. Para rodar a aplicação:
python api.py

##### 5. Em um outro terminal digitar o comando:
ngrok http 5000 (ou outra porta que o flask estiver rodando)

###### passo 1
![Alt text](/img/image.png)

###### passo 2
![Alt text](/img/image-1.png)

###### 6. Acessar a plataforma do Twilio:

###### 7. Escanear o qrcode com o celular

###### passo 1
![Alt text](/img/image-2.png)
###### passo 2
##### 8. Ir me sandboxsetting e colocar a url que o ngrok formeceu (toda vez que rodar o ngrok ele fornece um url diferente). Colocar /voice na url fornecida pelo ngrok:

![Alt text](/img/image-4.png)

##### 9. No celular enviar um audio para o Twilio e prosseguir com o teste:
