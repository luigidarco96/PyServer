import cv2


def make_scraper(image_path):
    image = cv2.imread(image_path)

    print(image)

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
        return False, "No face found"

    # Save only first face
    face = faces[0]
    x, y, w, h = face
    face_scraped = image[y:y + h, x:x + w]

    new_image_path = image_path.split(".")[0] + '_scraped.jpg'

    cv2.imwrite(new_image_path, face_scraped)

    return True, new_image_path
