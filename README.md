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
