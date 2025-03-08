import base64
import json
import pprint
import time

from openai import OpenAI
import csv
import requests

client = OpenAI(api_key="")


def encode_image_to_base64(url_path):
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


if __name__ == '__main__':
    result = []
    with open('/Users/bytedance/Downloads/zenarart.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[15]
            if not url.startswith('https'):
                continue
            print('start: ' + url)

            # Getting the Base64 string
            base64_image = encode_image_to_base64(url)
            if base64_image is None:
                continue

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                # "text": "What is in this image? Please give me some compliments on this painting, Such as color combinations、composition technique、emotional resonance、unique artistic choices etc",
                                "text": "Based on the uploaded image, please generate 50 user first names and their "
                                        "comments on their experience purchasing paintings from the Zenarart website. "
                                        "The comments should vary in length from 50 to 100 words, reflecting different "
                                        "personality types. Additionally, assign star ratings to these reviews, "
                                        "ranging from 1 to 5, with 1 being the worst and 5 being the best. "
                                        "please output as a JSON object:Name, Comment, Rating"
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpg;base64,{base64_image}"},
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

            result = []
            for d in data:
                result.append({
                    'Image': row[14],
                    'Name': d['Name'],
                    'Comment': d['Comment'],
                    'Rating': d['Rating']
                })

            csv_filename = "zenart_reviews.csv"

            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                # 定义CSV列名
                fieldnames = ['Image', 'Name', 'Comment', 'Rating']

                # 创建CSV writer对象
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # 写入表头
                if csvfile.tell() == 0:
                    writer.writeheader()

                # 写入数据行
                writer.writerows(result)

            print(f"CSV文件已保存为：{csv_filename}")

            time.sleep(1)

    pprint.pprint(result)
