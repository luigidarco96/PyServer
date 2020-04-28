import cv2
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import model_from_json

sess = tf.Session()
graph = tf.get_default_graph()

set_session(sess)
with open('ml_resources/facial_expression_model_structure.json', 'r') as f:
    model = model_from_json(f.read())
model.load_weights('ml_resources/facial_expression_model_weights.h5')

emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')


def make_scraper(image_path):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
    )

    print("Found {0} Faces!".format(len(faces)))

    if len(faces) <= 0:
        return None

    # Save only first face
    face = faces[0]
    x, y, w, h = face
    face_scraped = image[y:y + h, x:x + w]

    new_image_path = image_path.split(".")[0] + '_scraped.jpg'

    cv2.imwrite(new_image_path, face_scraped)

    return new_image_path


def predict_emotion(image_path):
    print("Image path: {}" .format(image_path))
    image = cv2.imread(image_path)

    detected_face = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # transform to gray scale
    detected_face = cv2.resize(detected_face, (48, 48))  # resize to 48x48

    img_pixels = np.expand_dims(detected_face, axis=0)

    img_pixels = np.expand_dims(img_pixels, axis=3)

    img_pixels = np.array(img_pixels, dtype=np.float64)
    img_pixels /= 255  # pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]

    global sess
    global graph
    with graph.as_default():
        set_session(sess)
        predictions = model.predict(img_pixels)  # store probabilities of 7 expressions

        max_index = np.argmax(predictions[0])

        if predictions[0][max_index] < 0.5:
            return None

    return emotions[max_index]
