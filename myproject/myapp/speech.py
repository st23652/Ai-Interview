import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()

# Use the Microphone class to capture live audio
with sr.Microphone() as source:
    print("Please say something")
    # Adjust for ambient noise
    r.adjust_for_ambient_noise(source)
    # Listen to the audio from the microphone
    audio = r.listen(source)

try:
    # Recognize speech using Google Web Speech API
    text = r.recognize_google(audio)
    print("Recognized Text: ", text)
except sr.UnknownValueError:
    print("Google Web Speech API could not understand the audio")
except sr.RequestError as e:
    print("Could not request results from Google Web Speech API; {0}".format(e))
