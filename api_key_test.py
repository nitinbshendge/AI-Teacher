import requests
import json

# ✅ Replace with your actual Groq API Key
GROQ_API_KEY = "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"
GROQ_MODEL = "mistral-7b-8192"  # Ensure this model exists

url = "https://api.groq.com/v1/chat/completions"  # Correct API URL

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json",
}

# ✅ Test with a simple prompt
data = {
    "model": GROQ_MODEL,
    "messages": [{"role": "user", "content": "Hello, how are you?"}],
    "temperature": 0.5,
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()

    print("Response Status Code:", response.status_code)
    print("Response JSON:", json.dumps(response_json, indent=4))

except Exception as e:
    print("Error:", str(e))
