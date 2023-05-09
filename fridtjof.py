"""
    Forberede dataset til treining og validering. Forhondsbehandling av bildene.   
""" 

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

"""
    Generering og kompilering av modellen
""" 

# En enkel Convolutional Neural Network (CNN) arkitektur

import tensorflow as tf

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)), 
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
# Lag 1: (32) lav filtere for å lære lavnivåmønster og teksturer. 
#   (3,3) Vanlig for konvolusjonskjerner balansert. ReLU populær og rask aktiveringsfunksjon.
# Lag 2,4,6: (2,2) Standard max-pooling-operasjoner. Reduseres dimensjonene til bildet med faktor 2.
# Lag 3,5: (64)(128) Øker filter for å la nettverket lære mer sammensatte funksjoner og mønster.
# Lag 7: Flatten, konverterer 2D-matrisen til 1D-vektor, nødvendig for fullt tilkoblet lag (Dense).
# Lag 8: (128) Vilkårlig valg av noder, kan justeres. ReLU samme som sist.
# Lag 9: (0.5) God balanse. 50% av nodene vil tilfeldig bli slått av under rening. Motarbeider overtilpasning.
# Lag 10: (1) 1 node siden binært klassifiseringsproblem (bil, ikke bil). 
#   Sigmoid gir kontinuerlig resultat mellom 0 og 1, som kan tolkes som sannsynlighetn for den positive klasse.

model.summary()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# Optimizer: Adam er populær og effektiv. Kombinerer RMSProp og AdaGrad.
# Loss: binary_crossentropy vanlig for binær klassifisering. 
#   Kvantifiserer forskjellen mellom de faktske etikettene og modellens prediksjoner.
# Metrics: accuracy andelen av riktig klassifiserte bilder i forhold til totalt antall bilder.
