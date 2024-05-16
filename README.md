packaging
vllm==0.4.0.post1
autoawq==0.2.3
flash-attn==2.5.7
python-socketio

def handle_query(data):

    print(data)
    print("Received Query")
    if data['prompt'] == "base":
        prompt = "You are an AI assistant. You will answer questions accurately and prioritize shorter response if possible."
    
    elif data['prompt'] == "json":
        prompt = "Generate a json for the content using the following rules/examples.\nExamples:" + data['altprompt'] + "\n-----\nOnly output the json object."
        
    elif data['prompt'] == "summarize":
        prompt = "Generate an accurate summary of the text you are provided. Do not use outside sources. Only output the summary!"
    
    elif data['prompt'] == "cypher":
        prompt = """You are an experienced graph databases developer. This is the schema representation of a Neo4j database.
        
        Nodes: 
            Pokemon:
                Properties: name, hp, attack, defense, sp_attack, sp_defense, speed, total
            Type:
                Properties: name
            Ability:
                Properties: name
            EggGroup:
                Properties: name
        Relationships: 
            TYPE: Pokemon - TYPE -> Type
            ABILITY: Pokemon - ABILITY -> Ability
            EGGGROUP: Pokemon - EGGGROUP -> EggGroup


        All names begin with a capital letter.
        Based on this schema, create a Cypher query to get the data needed to answer the question. Only output the Cyper Query.
        """
    socketio.emit('query', {'query': data['query'], 'prompt': prompt, 'sid': request.sid}, room=llm_id)

.img {
    max-width: 75%; /* Maximum width of the image container */
    max-height: 75%; /* Maximum height of the image container */
    height: auto; /* Maintain aspect ratio */
    display: block;
    margin: 0 auto;
}
const createImageMessageElement = (message) => `
  <div class="message ${message.sender === 'John' ? 'blue-bg' : 'gray-bg'}">
    <div class="message-sender">${message.sender}</div>
    <img class="img" src="data:image/jpeg;base64, ${message.imageData}" alt="Image">
    <div class="message-timestamp">${message.timestamp}</div>
  </div>
`

    with open('static/startup.jpg', 'rb') as img_file:
        # Encode the image to base64
        encoded_img = base64.b64encode(img_file.read()).decode('utf-8')
        socketio.emit("image_message", encoded_img, room=request.sid)

        
