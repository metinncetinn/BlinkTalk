import google.generativeai as genai

genai.configure(api_key="Kişisel api anahtarınız.")#Kişisel api key.

# Model özellikleri
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 100,
}
#Güvenlik ayarları.
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]
#Kullanılacak model sürümü.
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
])

#soru="İstanbul nerededir"
def yapayZekaSor(soru):
  kalip=" sorusuna gündelik hayata uygun 2 kısa cevap verir misin? İlk satırda 1. cevap, ikinci satırda 2. cevap olsun. Ayrıca satırlar direkt cevap ile başlasın"
  SoruKalip='"'+soru+'"'+kalip
  #print(SoruKalip)
  convo.send_message(SoruKalip)
  satirlar=convo.last.text.splitlines()
  return satirlar

#print(yapayZekaSor(soru)[0])
#print(yapayZekaSor(soru)[1])

