import csv
import speech_recognition as sr
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
from google.cloud import speech_v1p1beta1 as speech

archivo_csv = 'products.csv'
medications = []

# Load medication names from 
# CSV
with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
    # Leer el archivo CSV
    lector_csv = csv.reader(csvfile, delimiter=';')
    # Iterar sobre cada fila del archivo
    for fila in lector_csv:
        # Agregar el elemento de la segunda columna a la lista
        medications.append(fila[1])
    medications = medications[1:]
    #print("Medications:", medications)

def recognize_speech_1():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language='es-ES')
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return ""

# def recognize_speech_2():
#     client = speech.SpeechClient()

#     config = {
#         "language_code": "es-ES",
#         "enable_automatic_punctuation": True,
#     }

#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
#         audio = recognizer.listen(source)

#     try:
#         print("Recognizing...")
#         audio_content = audio.get_wav_data()
#         response = client.recognize(config=config, audio={"content": audio_content})
#         text = response.results[0].alternatives[0].transcript
#         return text.lower()
#     except IndexError:
#         print("Sorry, I couldn't understand what you said.")
#         return ""
#     except Exception as e:
#         print("An error occurred: {}".format(e))
#         return ""

def find_medication(input_text):
    max_similarity = 0
    best_match = None
    print("Input text:", input_text)
    for medication in medications:
        similarity = fuzz.ratio(input_text, medication.lower())
        if similarity > max_similarity:
            print("Similarity:", similarity, "Medication:", medication)
            max_similarity = similarity
            best_match = medication
    return best_match

if __name__ == "__main__":
    while True:
        user_input = recognize_speech_1()
        if user_input:
            print("You said:", user_input)
            best_match = find_medication(user_input)
            if best_match:
                print("Best match:", best_match)
            else:
                print("No match found.")