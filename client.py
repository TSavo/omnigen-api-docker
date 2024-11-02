import requests
import json
import base64

class ImageGenerationClient:
    def __init__(self, url):
        self.url = url

    def generate_image(self, prompt, height=None, width=None, guidance_scale=None, seed=None, input_images=None):
        # Encode input images to base64
        encoded_images = []
        if input_images is not None:
            for image_path in input_images:
                with open(image_path, 'rb') as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                    encoded_images.append(encoded_image)
        
        data = {
            'prompt': prompt,
        }
        if height is not None:
            data['height'] = height
        if width is not None:
            data['width'] = width
        if guidance_scale is not None:
            data['guidance_scale'] = guidance_scale
        if seed is not None:
            data['seed'] = seed
        if input_images is not None:
            data['input_images'] = encoded_images

        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            with open('generated_image.png', 'wb') as f:
                f.write(response.content)
            print('Image saved as generated_image.png')
        else:
            print(f'Failed to generate image. Status code: {response.status_code}')

if __name__ == '__main__':
    client = ImageGenerationClient('http://45.63.6.200:5000/generate-image')
    image = client.generate_image(
        prompt='A curly-haired man <img><|image_1|></img> but hes eating a flaming torch.',
        input_images=['generated_image.png']
    )