from typing import List, Optional, Union
from vllm.engine.llm_engine import LLMEngine
from vllm.engine.arg_utils import EngineArgs
from vllm.usage.usage_lib import UsageContext
from vllm.utils import Counter
from vllm.outputs import RequestOutput
from vllm import SamplingParams
from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast
import gradio as gr
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
        
        request_id = str(next(self.request_counter))
        self.outputs[request_id] = ""
        self.llm_engine.add_request(request_id, prompt, sampling_params)

        # current_output = ""
        
        while self.llm_engine.has_unfinished_requests():
            step_outputs = self.llm_engine.step()
            for output in step_outputs:
                #for chunk in output:outputs[request_id]
                #print(output.outputs[0].text[len(self.outputs[output.request_id]):])# post(output.outputs[0].text[len(current_output):], output.request_id)#output.request_id)
                # current_output = output.outputs[0].text
                self.outputs[output.request_id] = output.outputs[0].text
                #yield output

        return self.outputs[output.request_id]

llm = StreamingLLM(model="Models/llama-3-8b-instruct-awq", quantization="AWQ", dtype="float16")
tokenizer = llm.llm_engine.tokenizer.tokenizer
sampling_params = SamplingParams(temperature=0.6,
                                    top_p=0.9,
                                    max_tokens=4096,
                                    stop_token_ids=[tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")]
                                    )

while True:
    question = input()
    prompt_pieces = []
    prompt_pieces.append({"role": "system", "content": """
        You are an AI Agent that determines what the task being asked is. You output must be a single word answer matching the task you chose.
        Possible tasks:
        Weather: Allows users to search for weather at various locations and times
        Calculator: Handles all math related questions
        General: If no other tasks can fulfill the request
        """})
    prompt_pieces.append({"role": "user", "content": question})

    prompt = tokenizer.apply_chat_template(prompt_pieces, tokenize=False)

    answer1 = llm.generate(prompt, sampling_params=sampling_params)
    print(answer1)

    if answer1 == "Weather":
        prompt_pieces = []
        prompt_pieces.append({"role": "system", "content": """
            You are an entity extractor that pulls out either named locations or coordinates from a query.
            The output must be in json format ONLY.
            Examples:
            Query: weather in Mariupol | Output: {location: Mariupol}
            Query: weather at 35N, 23E | Output: {lat: 35, lon: 23}
            Query: weather at 26.235, 12.235 | Output: {lat: 26.235, lon: 12.235}                              
            """})
        prompt_pieces.append({"role": "user", "content": question})

        prompt = tokenizer.apply_chat_template(prompt_pieces, tokenize=False)

        answer2 = llm.generate(prompt, sampling_params=sampling_params)
        print(answer2)
    
    elif answer1 == "Calculator":
        prompt_pieces = []
        prompt_pieces.append({"role": "system", "content": """
            You are a math tutor. You will break down the steps required to solve the math problem given step by step. You will only output the steps.
            Examples:
            Query: what is 6 + 4 | Output: 1. Add 6 and 4                   
            Query: what is 6 * 5 + 4 | Output: 1. Multiply 6 and 5 2. Add (6 * 5) and 4                         
            """})
        prompt_pieces.append({"role": "user", "content": question})

        prompt = tokenizer.apply_chat_template(prompt_pieces, tokenize=False)

        answer2 = llm.generate(prompt, sampling_params=sampling_params)
        print(answer2)
    else:
        print("Failed")
