from huggingface_hub.hf_api import HfFolder

HfFolder.save_token('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')

import transformers
import torch

model_id = "meta-llama/Meta-Llama-3-8B"

pipeline = transformers.pipeline("text-generation", model=model_id, device_map="auto")
res = pipeline("Hey how are you doing today?")
print(res)