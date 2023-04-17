from speech_recognition import Recognizer, Microphone, AudioFile


class AssesRecognizer(Recognizer):
    def __init__(self):
        super().__init__()

    def recognize_asses(self, audio_data):
        return self.recognize_google(audio_data)

    def recognize_asses_from_file(self, file_path):
        with AudioFile(file_path) as source:
            audio_data = self.record(source)
            return self.recognize_asses(audio_data)

    def recognize_asses_from_mic(self):
        with Microphone() as source:
            audio_data = self.listen(source)
            return self.recognize_asses(audio_data)

recognizer = AssesRecognizer()
recognizer.recognize_asses_from_file("clean.wav")
