# -*- coding: utf-8 -*-
import os
os.environ["PYTHONUTF8"] = "1"
from datasets import load_dataset

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    BitsAndBytesConfig
)

from peft import (
    LoraConfig,
    get_peft_model
)

from trl import SFTTrainer

import torch

# =====================================
# MODEL
# =====================================

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# =====================================
# TOKENIZER
# =====================================

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

tokenizer.pad_token = tokenizer.eos_token

# =====================================
# QLORA CONFIG
# =====================================

bnb_config = BitsAndBytesConfig(

    load_in_4bit=True,

    bnb_4bit_quant_type="nf4",

    bnb_4bit_compute_dtype=torch.float16
)

# =====================================
# LOAD MODEL
# =====================================

model = AutoModelForCausalLM.from_pretrained(

    MODEL_NAME,

    quantization_config=bnb_config,

    device_map="auto"
)

# =====================================
# LORA CONFIG
# =====================================

lora_config = LoraConfig(

    r=16,

    lora_alpha=32,

    target_modules=[
        "q_proj",
        "v_proj"
    ],

    lora_dropout=0.05,

    bias="none",

    task_type="CAUSAL_LM"
)

# =====================================
# APPLY LORA
# =====================================

model = get_peft_model(
    model,
    lora_config
)

# =====================================
# LOAD DATASET
# =====================================

dataset = load_dataset(

    "json",

    data_files="../outputs/training_dataset.jsonl",

    split="train"
)

# =====================================
# FORMAT DATA
# =====================================

def formatting_func(example):

    return f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}
"""

    return [text]

# =====================================
# TRAINING CONFIG
# =====================================

training_args = TrainingArguments(

    output_dir="../models",

    per_device_train_batch_size=1,

    gradient_accumulation_steps=4,

    learning_rate=2e-4,

    num_train_epochs=1,

    logging_steps=10,

    save_steps=50,

    fp16=True,

    optim="paged_adamw_8bit"
)

# =====================================
# TRAINER
# =====================================

trainer = SFTTrainer(

    model=model,

    train_dataset=dataset,

    formatting_func=formatting_func,

    args=training_args,

    max_seq_length=1024
)

# =====================================
# TRAIN MODEL
# =====================================

trainer.train()

# =====================================
# SAVE MODEL
# =====================================

trainer.model.save_pretrained(
    "../models/llama_resume_screener"
)

tokenizer.save_pretrained(
    "../models/llama_resume_screener"
)

print("Fine-tuning complete.")