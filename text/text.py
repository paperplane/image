import requests
from PIL import Image
from transformers import BlipProcessor, AutoTokenizer, AutoModelForTokenClassification
from huggingface_hub import hf_hub_download


def download():
    model_id = "Salesforce/blip-image-captioning-large"
    filenames = ["pytorch_model.bin", "config.json", "tokenizer.json", "tokenizer_config.json"]

    for filename in filenames:
        hf_hub_download(repo_id=model_id, filename=filename, cache_dir="/Users/ipaperplane/Downloads/local_model")


def process():
    tokenizer = AutoTokenizer.from_pretrained("/Users/ipaperplane/Downloads/local_model", local_files_only=True)
    model = AutoModelForTokenClassification.from_pretrained("/Users/ipaperplane/Downloads/local_model", local_files_only=True)

    processor = BlipProcessor.from_pretrained("/Users/ipaperplane/Downloads/local_model", local_files_only=True)

    img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg'
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

    # conditional image captioning
    text = "a photography of"
    inputs = processor(raw_image, text, return_tensors="pt")

    out = model.generate(**inputs)
    print(processor.decode(out[0], skip_special_tokens=True))

    # unconditional image captioning
    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)
    print(processor.decode(out[0], skip_special_tokens=True))


if __name__ == '__main__':
    download()
    process()
