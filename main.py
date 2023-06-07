from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import speech_recognition as sr
from pydub import AudioSegment
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# create a new Firefox browser instance
driver = webdriver.Firefox()

# navigate to the webcast page
driver.get("https://events.q4inc.com/attendee/703125331/guest")

# find the form elements and fill them out
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'GuestRegistrationFirstNameInput'))
)

print("Page Loaded")
first_name_field = driver.find_element("id","GuestRegistrationFirstNameInput")
last_name_field = driver.find_element("id","GuestRegistrationLastNameInput")
email_field = driver.find_element("id","GuestRegistrationEmailInput")

first_name_field.send_keys("Apurv")
last_name_field.send_keys("Singh")
email_field.send_keys("apurvsingh98@gmail.com")


driver.find_element(By.CLASS_NAME,"nui-toggle-input-base_label-text").click()


# find the registration button and click it
registration_button = driver.find_element("id","GuestRegistrationSubmitButton")
registration_button.click()



#Audio downloading 

audio_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'video-replay_audio'))
)

# get the URL of the audio file
audio_url = audio_element.get_attribute('src')

# use requests to download the file
response = requests.get(audio_url, stream=True)
response.raise_for_status()  # ensure we notice bad responses

# write the content of the request to a file
with open('audio.wav', 'wb') as fp:
    for chunk in response.iter_content(chunk_size=8192):
        fp.write(chunk)



# Specify the audio file path
audio_file_wav = "audio.wav"


# Initialize the recognizer
r = sr.Recognizer()

# Load the audio file
with sr.AudioFile(audio_file_wav) as source:
    # Read the audio data from the file
    audio = r.record(source)

    # Perform speech recognition
    transcript = r.recognize_google(audio)

# Print the transcript
print("Transcript:")
print(transcript)

pdf_file = "transcript.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)

# Set the font properties
c.setFont("Helvetica", 12)

# Set the position for text
x = 50
y = 750

# Write the transcript to the PDF
c.drawString(x, y, "Transcript:")
c.setFont("Courier", 10)
transcript_lines = transcript.split("\n")
for line in transcript_lines:
    y -= 15
    c.drawString(x, y, line)

# Save and close the PDF file
c.save()

print(f"Transcript saved as {pdf_file}")

