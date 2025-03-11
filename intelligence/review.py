import base64
import json
import pprint
from typing import Union, Any
from openai import OpenAI
import csv
import requests

client = OpenAI(
    api_key="sk-proj-wo0DW5qsuAb4AEFkJ86MbyrbloKX7NhSvQfnQ2hz8fyd3mGL9zESN2bAg-ymovs"
            "-4ufINy1GjPT3BlbkFJtv34mc4szd3eIVe-MEldJFR2SMV302wEEWNxMfDKXABpHnkGdGYV2zkX_0eEjf4NFVN7EkRbQA")
target_filename = "/Users/ipaperplane/Downloads/zenarart_reviews.csv"
source_filename = '/Users/ipaperplane/Downloads/zenarart.csv'


def encode_image(url_path):
    # Fetch the image data
    response = requests.get(url_path)

    # Check if the request was successful
    if response.status_code == 200:
        # Encode the image data into Base64
        base64_string = base64.b64encode(response.content).decode('utf-8')

        return base64_string
    else:
        print(f"Failed to fetch image. Status code: {response.status_code}")
        return None


def get_review(image_name, image_encode):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Based on the uploaded image, please generate 50 user first names and their "
                                "comments on their experience purchasing paintings from the Zenarart website. "
                                "The comments should vary in length from 50 to 100 words, reflecting different "
                                "personality types. Additionally, assign star ratings to these reviews, "
                                "ranging from 1 to 5, with 1 being the worst and 5 being the best. "
                                "please output as a JSON object:Name, Comment, Rating"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpg;base64,{image_encode}"},
                    },
                ],
            }
        ],
        max_tokens=8000,
    )

    choice = response.choices[0]
    content = choice.message.content
    b = content.split('[')[1].split(']')[0]
    c = '[' + b + ']'
    data = json.loads(c)

    review_list: list[dict[str, Union[str, Any]]] = []
    for d in data:
        review_list.append({
            'Image': image_name,
            'Name': d['Name'],
            'Comment': d['Comment'],
            'Rating': d['Rating']
        })
    return review_list


def write_review(reviews):
    with open(target_filename, 'a', newline='', encoding='utf-8') as csvfile:
        # 定义CSV列名
        fieldnames = ['Image', 'Name', 'Comment', 'Rating']

        # 创建CSV writer对象
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 写入表头
        if csvfile.tell() == 0:
            writer.writeheader()

        # 写入数据行
        writer.writerows(reviews)

    print(f"CSV文件已保存为：{target_filename}")


if __name__ == '__main__':
    with open('/Users/ipaperplane/Downloads/zenarart.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[15]
            name = row[14]
            if not url.startswith('https'):
                continue
            print('review: ' + url)

            # Getting the Base64 string
            base64_image = encode_image(url)
            if base64_image is None:
                continue

            res = get_review(name, base64_image)
            write_review(res)

            pprint.pprint(res)
