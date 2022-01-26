from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1

url = "https://api.us-east.text-to-speech.watson.cloud.ibm.com/instances/51d2629a-5c70-4a8e-ae64-06ac0b089c91"
apikey = "GiFLTDMBeRg0MQeKck3qEKP2JzwcaYaODgxP9LQqqTGg"

authenticator = IAMAuthenticator(apikey)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)

with open('tts/speech.mp3', 'wb') as audio_file:
    res = tts.synthesize('P.O.V you just sold a N F T for over $65,000 & earned your professors entire salary after finishing college', accept='audio/mp3', voice = 'en-US_AllisonV3Voice').get_result()
    audio_file.write(res.content)