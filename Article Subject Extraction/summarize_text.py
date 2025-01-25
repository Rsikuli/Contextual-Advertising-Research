from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re


# Initialize the tokenizer and model
model_name = "csebuetnlp/mT5_multilingual_XLSum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def WHITESPACE_HANDLER(text):
    return re.sub('\s+', ' ', re.sub('\n+', ' ', text.strip()))


def summarize_text(text):
    input_ids = tokenizer(
        [WHITESPACE_HANDLER(text)],
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=716
    )["input_ids"]

    output_ids = model.generate(
        input_ids=input_ids,
        max_length=128,
        no_repeat_ngram_size=2,
        num_beams=4
    )[0]

    summary = tokenizer.decode(
        output_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )

    return summary