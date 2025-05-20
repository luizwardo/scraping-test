import requests
import base64
import json
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from PIL import Image, ImageTk
from io import BytesIO
import threading
from bs4 import BeautifulSoup
import re
from datetime import datetime

class ImageScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Scraper & Descriptor")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Configuração da API key
        self.api_key = tk.StringVar()
        
        # Criar pasta para salvar imagens
        self.output_folder = "downloaded_images"
        os.makedirs(self.output_folder, exist_ok=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="Image Scraper & AI Description Generator", 
                              font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=(0, 20))
        
        # Frame para API key
        api_frame = tk.Frame(main_frame, bg="#f0f0f0")
        api_frame.pack(fill=tk.X, pady=(0, 10))
        
        api_label = tk.Label(api_frame, text="OpenAI API Key:", bg="#f0f0f0")
        api_label.pack(side=tk.LEFT, padx=(0, 5))
        
        api_entry = tk.Entry(api_frame, textvariable=self.api_key, show="*", width=50)
        api_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Frame para URL
        url_frame = tk.Frame(main_frame, bg="#f0f0f0")
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        url_label = tk.Label(url_frame, text="URL:", bg="#f0f0f0")
        url_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.url_entry = tk.Entry(url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.scrape_button = tk.Button(url_frame, text="Scrape Images", 
                                      command=self.start_scraping, bg="#4CAF50", fg="white")
        self.scrape_button.pack(side=tk.LEFT)
        
        # Frame para status e progresso
        status_frame = tk.Frame(main_frame, bg="#f0f0f0")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(status_frame, text="Status: Ready", bg="#f0f0f0")
        self.status_label.pack(side=tk.LEFT)
        
        self.progress_bar = ttk.Progressbar(status_frame, orient=tk.HORIZONTAL, length=300, mode="determinate")
        self.progress_bar.pack(side=tk.RIGHT)
        
        # Log área
        log_label = tk.Label(main_frame, text="Activity Log:", bg="#f0f0f0", anchor="w")
        log_label.pack(fill=tk.X)
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        # Área de resultado
        result_label = tk.Label(main_frame, text="Results:", bg="#f0f0f0", anchor="w")
        result_label.pack(fill=tk.X, pady=(10, 0))
        
        self.result_text = scrolledtext.ScrolledText(main_frame, height=10)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)
    
    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")
        self.root.update_idletasks()
    
    def update_result(self, message):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def start_scraping(self):
        # Reset UI
        self.progress_bar["value"] = 0
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        url = self.url_entry.get().strip()
        api_key = self.api_key.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
            
        if not api_key:
            messagebox.showerror("Error", "Please enter your OpenAI API key")
            return
        
        # Desabilitar o botão durante o scraping
        self.scrape_button.config(state=tk.DISABLED)
        
        # Iniciar o scraping em uma thread separada
        threading.Thread(target=self.scrape_url, args=(url, api_key), daemon=True).start()
    
    def scrape_url(self, url, api_key):
        try:
            self.update_status("Connecting to URL...")
            self.log(f"Connecting to: {url}")
            
            response = requests.get(url)
            if response.status_code != 200:
                self.update_status("Failed")
                self.log(f"Failed to access URL: Status code {response.status_code}")
                messagebox.showerror("Error", f"Failed to access URL: Status code {response.status_code}")
                self.scrape_button.config(state=tk.NORMAL)
                return
            
            # Usando BeautifulSoup para extrair imagens
            self.update_status("Parsing HTML...")
            self.log("Successfully connected. Parsing HTML...")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')
            
            if not img_tags:
                self.update_status("No images found")
                self.log("No images found on the page")
                messagebox.showinfo("Info", "No images found on the page")
                self.scrape_button.config(state=tk.NORMAL)
                return
            
            self.log(f"Found {len(img_tags)} images on the page")
            
            # Filtrar imagens válidas
            valid_images = []
            for img in img_tags:
                src = img.get('src')
                if src:
                    # Completar URLs relativas
                    if src.startswith('data:image'):
                        valid_images.append(src)
                    elif src.startswith('//'):
                        valid_images.append('https:' + src)
                    elif src.startswith('/'):
                        base_url = '/'.join(url.split('/')[:3])
                        valid_images.append(base_url + src)
                    elif not src.startswith(('http://', 'https://')):
                        # URL relativa
                        if url.endswith('/'):
                            valid_images.append(url + src)
                        else:
                            base_path = '/'.join(url.split('/')[:-1]) + '/'
                            valid_images.append(base_path + src)
                    else:
                        valid_images.append(src)
            
            if not valid_images:
                self.update_status("No valid images found")
                self.log("No valid image sources found on the page")
                messagebox.showinfo("Info", "No valid images found")
                self.scrape_button.config(state=tk.NORMAL)
                return
            
            self.log(f"Processing {len(valid_images)} valid images")
            self.progress_bar["maximum"] = len(valid_images)
            
            # Baixar e processar cada imagem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_folder = os.path.join(self.output_folder, f"results_{timestamp}")
            os.makedirs(results_folder, exist_ok=True)
            
            results = []
            processed_count = 0
            
            for i, img_src in enumerate(valid_images):
                try:
                    self.update_status(f"Processing image {i+1}/{len(valid_images)}")
                    self.log(f"Processing image {i+1}: {img_src[:60]}...")
                    
                    img_data = self.download_image(img_src)
                    if not img_data:
                        self.log(f"  Skipped: Failed to download")
                        continue
                    
                    # Salvar imagem
                    img_filename = f"image_{i+1}.jpg"
                    img_path = os.path.join(results_folder, img_filename)
                    with open(img_path, 'wb') as f:
                        f.write(img_data)
                    
                    # Gerar descrição com OpenAI
                    self.log(f"  Generating AI description...")
                    description = self.generate_image_description(img_data, api_key)
                    
                    # Salvar descrição
                    desc_filename = f"image_{i+1}_description.txt"
                    desc_path = os.path.join(results_folder, desc_filename)
                    with open(desc_path, 'w', encoding='utf-8') as f:
                        f.write(description)
                    
                    results.append({
                        "image": img_filename,
                        "description": description
                    })
                    
                    # Atualizar resultados na UI
                    self.update_result(f"Image {i+1}: {description[:100]}...")
                    
                    processed_count += 1
                    self.progress_bar["value"] = i + 1
                    
                except Exception as e:
                    self.log(f"  Error processing image: {str(e)}")
            
            # Salvar resultados JSON
            results_json = os.path.join(results_folder, "results.json")
            with open(results_json, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            
            self.update_status("Completed")
            self.log(f"Completed! Processed {processed_count} images successfully")
            self.log(f"Results saved to: {results_folder}")
            messagebox.showinfo("Success", f"Processed {processed_count} images. Results saved to: {results_folder}")
            
        except Exception as e:
            self.update_status("Error")
            self.log(f"Error during scraping: {str(e)}")
            messagebox.showerror("Error", f"Scraping failed: {str(e)}")
        
        finally:
            self.scrape_button.config(state=tk.NORMAL)
    
    def download_image(self, img_src):
        try:
            if img_src.startswith('data:image'):
                # Imagem base64
                img_format, img_str = img_src.split(';base64,')
                return base64.b64decode(img_str)
            else:
                # URL de imagem
                response = requests.get(img_src, timeout=10)
                if response.status_code == 200:
                    return response.content
                return None
        except Exception as e:
            self.log(f"  Error downloading image: {str(e)}")
            return None
    
    def generate_image_description(self, image_data, api_key):
        try:
            # Converter imagem para base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Preparar payload para OpenAI API
            payload = {
                "model": "gpt-4-vision-preview",  # Modelo da OpenAI com capacidade de visão
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Descreva esta imagem de forma simples e concisa em um parágrafo."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }
            
            # Enviar para OpenAI API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                error_msg = f"OpenAI API error: {response.status_code}, {response.text}"
                self.log(error_msg)
                return f"Error generating description: {response.status_code}"
            
            response_data = response.json()
            description = response_data['choices'][0]['message']['content']
            return description
            
        except Exception as e:
            self.log(f"  Error generating description: {str(e)}")
            return "Failed to generate description"

# Iniciar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageScraperApp(root)
    root.mainloop()