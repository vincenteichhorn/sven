import re
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import torch
from dotenv import load_dotenv

load_dotenv()

tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-3.2-1B-Instruct", token=os.environ.get("HF_TOKEN")
)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-1B-Instruct", token=os.environ.get("HF_TOKEN")
)


def get_prompt(user_answer, answer):
    template = [
        {
            "role": "system",
            "content": "Du bist an der Universtät angestellt und kontrollierst einzelne Antworten in einer Klausur. Dabei vergleichst du die Antwort der Studierenden mit der Musterlösung. Im folgenden sieht du die Musterlösung und die Antwort eines Studierenden. Bitte entscheide, ob die Antwort korrekt ist indem du diese mit der Musterlösung vergleichst. Gib dazu einen Score zwischen 0 und 100 aus wie sicher du dir bist, bzw. wie nah die Antwort an der Musterlösung ist. Wenn Antwort und Musterlösung gleich sind, dann sollte der Score maximal sein. Eine bessere Antwort als die Müsterlösung ist von den Studierenden nicht erforderlich, somit darfst du diese auch nicht verbessern. Achte darauf, dass Formulierungen und Rechtschreibung keine Rolle spielen. Es kommt alleine auf den Inhalt an. Wenn es um Aufzählungen geht, achte darauf, dass alle wichtigen Punkte genannt sind. Vielen Dank für deine Hilfe!",
        },
        {
            "role": "user",
            "content": f"Antwort auf der Klausur: {user_answer}\nMusterlösung: {answer}\nWas für einen Score gibst du?",
        },
    ]
    return template


def judge(*args, **kwargs):
    prompt = get_prompt(*args, **kwargs)
    tokenized_text = tokenizer.apply_chat_template(
        prompt, return_tensors="pt", tokenize=True, add_generation_prompt=True
    )
    output = model.generate(
        **{
            "input_ids": tokenized_text,
            "attention_mask": torch.ones_like(tokenized_text),
        },
        max_new_tokens=128,
        pad_token_id=tokenizer.eos_token_id,
    )
    resp = tokenizer.decode(output[0], skip_special_tokens=True)
    assisant_resp = resp.split("assistant")[1]
    score = re.search(r"\d+", assisant_resp).group()
    return score


if __name__ == "__main__":
    antwort = "Berlin"
    user_antwort = "Berlin"
    print(judge(user_antwort, antwort))
