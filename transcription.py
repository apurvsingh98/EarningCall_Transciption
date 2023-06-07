import whisper
import ffmpeg

model = whisper.load_model("medium.en")
result = model.transcribe("audio.mp4")
text = result["text"]

with open("Transcribed.txt", "w") as text_file:
    text_file.write("LivaNova's earning call transciption: %s" % text)