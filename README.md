
##### 1. Criar uma conta no Twilio e subistituir no arquivo .env TWILIO_ACCOUNT_SID TWILIO_AUTH_TOKEN pelo que sera fornecido assim que a conta for criada:

##### 2. Entrar no site do ngrok e seguir os passos da instalação para seu sistema operacional:

https://dashboard.ngrok.com/login

##### 2.1 Para Linux
sudo apt update
sudo apt install ffmpeg

##### 2.2 Para windows
https://ffmpeg.org/download.html


##### 3. instalando com docker:
###### 3.1 criando imagem:
docker build -t voice .
###### 3.2 exportando .env
docker run -p 8000:8000 --env-file .env voice
###### 3.4 subindo a aplicação sem dockerfile:
python src/api.py

##### 4. Instalar as dependencias:
pip install -r requirements.txt

##### 5. Para rodar a aplicação:
python3 src/app.py

##### 6. Em um outro terminal digitar o comando:
ngrok http 8000

###### passo 1
![Alt text](/img/image.png)

###### passo 2
![Alt text](/img/image-1.png)

###### 7. Acessar a plataforma do Twilio:

###### 8. Escanear o qrcode com o celular

###### passo 1
![Alt text](/img/image-2.png)
###### passo 2
##### 9. Ir me sandboxsetting e colocar a url que o ngrok formeceu (toda vez que rodar o ngrok ele fornece um url diferente). Colocar /voice na url fornecida pelo ngrok:

![Alt text](/img/image-4.png)

##### 10. No celular enviar um audio para o Twilio e prosseguir com o teste:
