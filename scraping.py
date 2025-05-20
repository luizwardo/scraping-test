import requests
import base64
import json
import os
from io import BytesIO
from PIL import Image

# Função para obter imagem do site
def scrape_image():
    url = "https://intern.aiaxuropenings.com/scrape/2eb66e0f-eba8-43b2-81ea-a96ae72ef603"
    print(f"Fazendo requisição para: {url}")
    response = requests.get(url)
    
    print(f"Status da resposta: {response.status_code}")
    if response.status_code != 200:
        raise Exception(f"Failed to scrape page: {response.status_code}")
    
    html_content = response.text
    print(f"HTML obtido (primeiros 100 caracteres): {html_content[:100]}...")
    
    img_start = html_content.find("<img")
    print(f"Posição da tag <img>: {img_start}")
    if img_start == -1:
        raise Exception("Imagem nao encontrada no HTML")
    
    src_start = html_content.find('src="', img_start) + 5
    src_end = html_content.find('"', src_start)
    img_url = html_content[src_start:src_end]
    print(f"URL da imagem encontrada: {img_url}")
    
    if img_url.startswith('data:image'):
        print("Imagem em formato base64 detectada, decodificando diretamente...")
        base64_data = img_url.split(',')[1]
        image_data = base64.b64decode(base64_data)
        print(f"Imagem decodificada com sucesso - {len(image_data)} bytes")
        return image_data
    else:
        if img_url.startswith("/"):
            base_url = "/".join(url.split("/")[:3])
            img_url = base_url + img_url
            print(f"URL absoluta da imagem: {img_url}")
        
        print(f"Baixando imagem de: {img_url}")
        img_response = requests.get(img_url)
        print(f"Status do download da imagem: {img_response.status_code}")
        if img_response.status_code != 200:
            raise Exception(f"Failed to download image: {img_response.status_code}")
        
        print(f"Imagem baixada com sucesso - {len(img_response.content)} bytes")
        return img_response.content

# Função para enviar imagem para análise da IA
def send_to_model(image_data, api_key):
    api_url = "https://intern.aiaxuropenings.com/v1/chat/completions"
    
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    payload = {
        "model": "microsoft-florence-2-large",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "<DETAILED_CAPTION>"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Erro model API: {response.status_code}, {response.text}")
    
    return response.json()

# Função para enviar resposta para validação
def submit_response(model_response, api_key):
    submit_url = "https://intern.aiaxuropenings.com/api/submit-response"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.post(submit_url, headers=headers, json=model_response)
    
    if response.status_code != 200:
        raise Exception(f"Erro de envio: {response.status_code}, {response.text}")
    
    return response.json()

# Função para verificar se a imagem é válida
def verify_image(image_path):
    file_size = os.path.getsize(image_path)
    print(f"Tamanho do arquivo: {file_size} bytes")

    try:
        img = Image.open(image_path)
        width, height = img.size
        print(f"Imagem válida - dimensões: {width}x{height}")
        return True
    except Exception as e:
        print(f"Erro ao abrir a imagem: {e}")
        return False

# Função principal
def main():
    api_key = "RO1fDD43SwAohzavFayjoHfouulyKHaW"
    
    print("Scraping...")
    image_data = scrape_image()
    print("Imagem baixada com sucesso!")
    
    with open("scraped_image.jpg", "wb") as f:
        f.write(image_data)
    print("Imagem salva como 'scraped_image.jpg'")
    
    print("Verificando a imagem...")
    is_valid = verify_image("scraped_image.jpg")
    if not is_valid:
        print("AVISO: A imagem pode não ser válida!")
    
    print("Enviando imagem para o AI model...")
    model_response = send_to_model(image_data, api_key)
    print("Resposta do modelo recebida!")
    
    with open("model_response.json", "w") as f:
        json.dump(model_response, f, indent=2)
    print("Model response saved as 'model_response.json'")
    
    print("Enviando resposta...")
    submission_result = submit_response(model_response, api_key)
    print("Resultado do envio:", submission_result) 

if __name__ == "__main__":
    main()