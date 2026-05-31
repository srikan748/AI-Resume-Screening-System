import torch

from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
from transformers import BitsAndBytesConfig

from peft import PeftModel


BASE_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"

LORA_PATH = "./llm_model/resume_lora_model"


bnb_config = BitsAndBytesConfig(

    load_in_4bit = True,

    bnb_4bit_quant_type = "nf4",

    bnb_4bit_compute_dtype = torch.float16,

    bnb_4bit_use_double_quant = True,
)


print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token

print("Loading LLaMA-3-8B base model...")

base_model = AutoModelForCausalLM.from_pretrained(

    BASE_MODEL,

    quantization_config = bnb_config,

    device_map = "auto",

    torch_dtype = torch.float16
)


print("Loading recruiter LoRA adapters...")

model = PeftModel.from_pretrained(

    base_model,

    LORA_PATH
)


model.eval()

print("LLaMA-3-8B Recruiter LLM loaded successfully.")