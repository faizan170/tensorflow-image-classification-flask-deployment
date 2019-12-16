from flask import Flask, render_template, request
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import cv2
import numpy as np

from flask_cors import CORS, cross_origin

names = ["daisy", "dandelon", "roses", "sunflowers", "tulips"]



# Process image and predict label
def processImg(IMG_PATH):
    # Read image
    model = load_model("flower.model")
    
    # Preprocess image
    image = cv2.imread(IMG_PATH)
    image = cv2.resize(image, (199, 199))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    res = model.predict(image)
    label = np.argmax(res)
    print("Label", label)
    labelName = names[label]
    print("Label name:", labelName)
    return labelName


# Initializing flask application
app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def main():
    return """
        Application is working
    """

# About page with render template
@app.route("/about")
def postsPage():
    return render_template("about.html")

# Process images
@app.route("/process", methods=["POST"])
def processReq():
    data = request.files["img"]
    data.save("img.jpg")

    resp = processImg("img.jpg")


    return resp


if __name__ == "__main__":
    app.run(debug=True)
