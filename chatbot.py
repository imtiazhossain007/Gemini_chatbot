import google.generativeai as genai
API_key="AIzaSyAwsWGf7BfLUuO47rrXAXPjuHyAMvnyLNE"
genai.configure(api_key=API_key)

model= genai.GenerativeModel("gemini-1.5-flash")
chat=model.start_chat()
print("start chat with Gemini. type exit to quit")
while True:
   user=input("you:")
   if(user.lower()=="exit"):
      print("thank you")
      break
   response= chat.send_message(user)
   print("Gemini:",response.text)