from typing import List, Optional, Union
from vllm.engine.llm_engine import LLMEngine
from vllm.engine.arg_utils import EngineArgs
from vllm.usage.usage_lib import UsageContext
from vllm.utils import Counter
from vllm.outputs import RequestOutput
from vllm import SamplingParams
from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast
import torch
import time

global queries
queries = []

class StreamingLLM:
    def __init__(
        self,
        model: str,
        dtype: str = "auto",
        quantization: Optional[str] = None,
        **kwargs,
    ) -> None:
        engine_args = EngineArgs(model=model, quantization=quantization, dtype=dtype, enforce_eager=True)
        self.llm_engine = LLMEngine.from_engine_args(engine_args, usage_context=UsageContext.LLM_CLASS)
        self.request_counter = Counter()
        self.outputs = {}

    def generate(
        self,
        prompt: Optional[str] = None,
        sampling_params: Optional[SamplingParams] = None,
        sid = None
    ) -> List[RequestOutput]:
        
        print(prompt)
        request_id = sid #str(next(self.request_counter))
        self.outputs[request_id] = ""
        self.llm_engine.add_request(request_id, prompt, sampling_params)

        # current_output = ""
        
        # while self.llm_engine.has_unfinished_requests():
        #     step_outputs = self.llm_engine.step()
        #     for output in step_outputs:
        #         #for chunk in output:outputs[request_id]
        #         post(output.outputs[0].text[len(self.outputs[output.request_id]):], output.request_id)# post(output.outputs[0].text[len(current_output):], output.request_id)#output.request_id)
        #         # current_output = output.outputs[0].text
        #         self.outputs[output.request_id] = output.outputs[0].text
                # yield output
import socketio

# Initialize Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')
    sio.emit('llm', {"text": ""})

@sio.on('query')
def query(data):
    print('Received Query')
    queries.append(data)
    question = queries.pop(0)
    prompt_pieces = []
    prompt_pieces.append({"role": "user", "content": question['prompt'] + "\n" + question['query']})
    # prompt_pieces.append({"role": "user", "content": question['query']})

    prompt = tokenizer.apply_chat_template(prompt_pieces, tokenize=False)

    llm.generate(prompt, sampling_params=sampling_params, sid=question['sid'])
    
def post(text, sid):
    sio.emit('tokens', {"text": text, "sid": sid})

model_path = "Models/Mistral-7B-Instruct-v0.2-AWQ"
llm = StreamingLLM(model=model_path, quantization="AWQ", dtype="float16")
tokenizer = llm.llm_engine.tokenizer.tokenizer
sampling_params = SamplingParams(temperature=0.6,
                                    top_p=0.9,
                                    max_tokens=4096,
                                    stop_token_ids=[tokenizer.eos_token_id]
                                    )

sio.connect('http://127.0.0.1:8000')

import asyncio

async def main():
    while True:
        while llm.llm_engine.has_unfinished_requests():
            step_outputs = llm.llm_engine.step()
            for output in step_outputs:
                #for chunk in output:outputs[request_id]
                post(output.outputs[0].text[len(llm.outputs[output.request_id]):], output.request_id)# post(output.outputs[0].text[len(current_output):], output.request_id)#output.request_id)
                # current_output = output.outputs[0].text
                llm.outputs[output.request_id] = output.outputs[0].text

asyncio.run(main())
# while True:
#     a = 1

    # while(True):
    #     if len(queries) == 0:
    #         time.sleep(1)
        
    #     else:
    #         question = queries.pop(0)
            
    #         print("Query received:", question)
    #         prompt_pieces = []
    #         prompt_pieces.append({"role": "system", "content": "You are an AI assistant. You will answer questions accurately and prioritize shorter response if possible."})
    #         prompt_pieces.append({"role": "user", "content": question['text']})
      
    #         prompt = tokenizer.apply_chat_template(prompt_pieces, tokenize=False)

    #         llm.generate(prompt, sampling_params=sampling_params, sid=question['sid'])
               
# Event handler for 'connect' event
