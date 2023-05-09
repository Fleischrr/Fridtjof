import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split

#funksjon for å forhåndsbehandle bildene (endre størrelsen og normaliserer)
def preprocess_image(image_path, target_size=(150, 150)):
    img = Image.open(image_path)
    img = img.convert('RGB')    # Konverter bildet til RGB-fromat
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0  # Normaliserer bildet
    return img_array

##  forhåndsbehandler bildene ved å endre størrelse og normalisere intensitetsverdiene. ##
##  Deler deretter datasettet inn i trening og valideringssett med et 80/20-forhold.    ##

IMAGES_DIR = "images"
CAR_IMAGES_DIR = os.path.join(IMAGES_DIR, "car")
NO_CAR_IMAGES_DIR = os.path.join(IMAGES_DIR, "no_car")

# Forbered data og etiketter
X = []
y = []

# Henter og forhåndsbehandler bildene med biler
for file_name in os.listdir(CAR_IMAGES_DIR):
    image_path = os.path.join(CAR_IMAGES_DIR, file_name)
    img_array = preprocess_image(image_path)
    X.append(img_array)
    y.append(1)  # Legger til etiketten 1 for biler

# Henter og forhåndsbehandler bildene uten biler
for file_name in os.listdir(NO_CAR_IMAGES_DIR):
    image_path = os.path.join(NO_CAR_IMAGES_DIR, file_name)
    img_array = preprocess_image(image_path)
    X.append(img_array)
    y.append(0)  # Legger til etiketten 0 for ikke-biler

# Konverterer listene til numpy-arrays
X = np.array(X)
y = np.array(y)

# Deler datasettet i trening og validering. 20% til valideringssett. Setter seed=42 for evt recreation.
# X inneholder bilder, y inneholder tilhørende etikett (1 for bil, 0 for ikke bil)
X_train, X_temp, Y_train, Y_temp = train_test_split(X, Y, test_size=0.2, random_state=42)
X_val, X_test, Y_val, Y_test = train_test_split(X_temp, Y_temp, test_size=0.5, random_state=42)

print("Training set size:", len(X_train))
print("Validation set size:", len(X_val))
print("Testing set size:", len(X_test))
