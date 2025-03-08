import google.generativeai as genai

# ✅ Configure API Key
GOOGLE_API_KEY = "AIzaSyBv1OdaOSIY83PKobrEJNPmTUVdY4iqsiU"
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ List Available Models (Run this once to verify models)
models = genai.list_models()
for model in models:
    print(model.name)  # Check if "gemini-1.0-pro" or another model is available

# ✅ Use the Correct Model Name
model = genai.GenerativeModel("gemini-1.0-pro")  # Change this if needed