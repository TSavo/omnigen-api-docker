from flask import Flask, request, send_file
from OmniGen import OmniGenPipeline
from io import BytesIO
import base64

app = Flask(__name__)

# Load the model
pipe = OmniGenPipeline.from_pretrained("Shitao/OmniGen-v1")
@app.route('/', methods=["GET"])
def test():
    return "ok"

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    if data is None:
        return 'No data provided', 400
    prompt = data.get('prompt', 'A curly-haired man in a red shirt is drinking tea.')
    height = data.get('height', 1024)
    width = data.get('width', 1024)
    guidance_scale = data.get('guidance_scale', 2.5)
    seed = data.get('seed', 0)
    input_images = data.get('input_images', [])
    #base64 decode the input_images
    for i in range(len(input_images)):
        input_images[i] = base64.b64decode(input_images[i])
    #write the input_images to disk
    for i in range(len(input_images)):
        with open(f'input_image_{i}.png', 'wb') as f:
            f.write(input_images[i])
    # Generate the image
    images = pipe(
        prompt=prompt,
        height=height,
        width=width,
        guidance_scale=guidance_scale,
        seed=seed,
        input_images=[f'input_image_{i}.png' for i in range(len(input_images))]
    )

    # Save the image to a BytesIO object
    img_io = BytesIO()
    images[0].save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    print("Server running.")