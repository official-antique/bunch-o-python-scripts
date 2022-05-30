from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import cv2, os, praw, pytesseract, re, requests

load_dotenv()

imgur_api_key = os.getenv('IMGUR_API_KEY')
local_image_path = os.getcwd() + '\\image.png'

pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')
reddit = praw.Reddit(client_id=os.getenv('PRAW_CLIENT_ID'), client_secret=os.getenv('PRAW_CLIENT_SECRET'), user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0')


def get_album_id_from_submission(id: str) -> str:
    submission_url = reddit.submission(id=id).url.rstrip('/').rsplit('/', 1)
    return submission_url[-1]

def get_image_links_from_album(response: requests.Response) -> list[str]:
    links = []
    for image_dict in response.json()['data']:
        links.append(image_dict['link'])
    return links

def save_and_return_grayscale_image(response: requests.Response) -> cv2.Mat:
    bytes = BytesIO(response.content)
    image = Image.open(bytes).save('image.png')

    return cv2.imread(local_image_path, cv2.IMREAD_GRAYSCALE)

def find_and_return_code_from_match(match) -> str:
    if len(match) > 10:
        return match
    else:
        return None


if __name__ == '__main__':
    album_id = get_album_id_from_submission(id='SUBMISSION_ID_HERE') # change this
    album = requests.get(f'https://api.imgur.com/3/album/{album_id}/images', headers={
        'Authorization' : f'Client-ID {imgur_api_key}'
    })

    codes = []
    image_links = get_image_links_from_album(response=album)
    for index, link in enumerate(image_links):
        print(f'[+]: Scanning {index + 1} of {len(image_links)}')

        try:
            response = requests.get(link)
            grayscale_image = save_and_return_grayscale_image(response=response)

            string_from_image = pytesseract.image_to_string(grayscale_image)
            matches_from_string = re.findall('[A-Z0-9]+', string_from_image)
            for match in matches_from_string:
                code = find_and_return_code_from_match(match=match)
                if code is not None:
                    codes.append(code)
        except RuntimeError as error:
            print(error)

    print(codes)