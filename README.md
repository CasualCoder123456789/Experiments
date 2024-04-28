packaging
vllm==0.4.0.post1
autoawq==0.2.3
flash-attn==2.5.7

def handle_query(data):

    print(data)
    print("Received Query")
    if data['prompt'] == "base":
        prompt = "You are an AI assistant. You will answer questions accurately and prioritize shorter response if possible."
    
    elif data['prompt'] == "json":
        prompt = "Generate a json for the content using the following rules/examples.\nExamples:" + data['altprompt'] + "\n-----\nOnly output the json object."
        
    elif data['prompt'] == "summarize":
        prompt = "Generate an accurate summary of the text you are provided. Do not use outside sources. Only output the summary!"
    socketio.emit('query', {'query': data['query'], 'prompt': prompt, 'sid': request.sid}, room=llm_id)
