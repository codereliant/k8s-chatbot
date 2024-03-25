# k8s-chatbot
A chatbot that can chat with your Kubernetes cluster.
It uses OpenAI's GPT-3 to generate responses, and OpenAI's function calling to interact with the Kubernetes cluster.

https://www.codereliant.io/chat-with-your-kubernetes-cluster/


### Set up
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run
```
export OPENAI_API_KEY=your_api_key
python chat_with_k8s.py
```
