import speech_recognition as sr

def micRec():
    def googleRec(audio):
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Failed to recognise audio"
        except sr.RequestError as e:
            return "Google request failed"
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
    	r.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
    	print("Say something!")
    	audio = r.listen(source)
    return googleRec(audio)

print(micRec())
