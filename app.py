from flask import Flask, render_template, request
import openai
import requests
import json
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

openai.api_key = os.getenv('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')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    model = "image-alpha-001"
    num_images = 1
    size = "512x512"
    response_format = "url"
    
    # set up headers for API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    
    # set up payload for API request
    payload = {
        "model": model,
        "prompt": prompt,
        "num_images": num_images,
        "size": size,
        "response_format": response_format
    }
    
    # send API request
    url = "https://api.openai.com/v1/images/generations"
    response = requests.post(url, headers=headers, data=json.dumps(payload))
  
    # decode response
    response_data = json.loads(response.content.decode('utf-8'))
    
    # extract image URL from response
    image_url = response_data['data'][0]['url']
    
    # download image from URL
    image_data = requests.get(image_url).content
    
    # convert image data to PIL Image object
    pil_image = Image.open(BytesIO(image_data))
    
    # save image to static folder
    filename = f"{prompt.replace(' ', '_')}.png"
    filepath = f"static/{filename}"
    pil_image.save(filepath)
    
    # render the result page, passing the filename to the template
    return render_template('result.html', filename=filename)

@app.route('/static/<filename>')
def display_image(filename):
    return render_template('image.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
