import argparse
import os
from time import sleep

import requests


# PATH to config file with api key
CONFIG = '../config.txt'

# Be nice to tumblr servers
RATE_LIMIT = 3  # seconds


def main():
    args = get_args()
    blog = args.blog.lower()
    notes_min = args.notes if args.notes else None
    tag = args.tag.lower() if args.tag else None

    api_key = parse_api_key()

    make_dirs(blog, tag)

    find_images(blog, api_key, tag, notes_min)


def get_args():
    """User CLI arguments"""
    parser = argparse.ArgumentParser(
                        description="Download images from a tumblr blog")
    parser.add_argument("blog",
                        help="tumblr blog to scrape")
    parser.add_argument("-nc", "--notes",
                        help="only download images with >= this note count",
                        type=int)
    parser.add_argument("-t", "--tag",
                        help="only download images with this tag")
    return parser.parse_args()


def parse_api_key():
    """Parse API key from config file located in root directory"""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    try:
        with open(CONFIG) as file:
            api_key = file.readline().strip()
            return api_key
    except FileNotFoundError:
        raise SystemExit(f'\n[!] Config file {CONFIG} not found\n')


def make_dirs(blog, tag):
    """Create local folders"""
    path = blog
    if tag:
        path += f'/{tag}'
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except PermissionError as e:
        cwd = os.getcwd()
        raise SystemExit(f'\n[!] Can\'t create "{path}" at PATH "{cwd}"\n')
    os.chdir(path)


def find_images(blog, api_key, tag, notes_min):
    """Loop through JSON results to find image urls"""
    offset = 0

    print(f'[+] Targeting {tag or "ALL"} images with'
          f'>= {notes_min or "NO LIMIT"} notes\n')

    while True:
        js = get_json(blog, api_key, offset, tag)
        post_count = len(js['posts'])

        for post in range(post_count):
            post_id = js['posts'][post]['id']
            img_url = js['posts'][post]['photos'][0]['original_size']['url']
            note_count = js['posts'][post]['note_count']

            if (notes_min and notes_min > note_count) or not notes_min:
                dl_image(post_id, img_url, tag)

        if not post_count or post_count < 20:
            return print('\n[✓] Finished!\n')
        else:
            offset += 20
            print(f'\nOffset {offset}\n')
            sleep(RATE_LIMIT)


def get_json(blog, api_key, offset, tag):
    url = (f'https://api.tumblr.com/v2/blog/{blog}.tumblr.com/posts/photo?'
           f'api_key={api_key}&offset={offset}')
    if tag:
        url += f'&tag={tag}'

    resp = requests.get(url, timeout=10)
    if resp.status_code == 404:
        raise SystemExit('\n[!] 404 - JSON query\n')

    try:
        return resp.json()['response']
    except (ValueError, KeyError):
        raise SystemExit('\n[!] Error parsing JSON\n')


def dl_image(post_id, url, tag):
    filename = build_filename(url, post_id, tag)
    if os.path.exists(filename) is False:
        print(f'[..] Downloading #{post_id}')
        data = requests.get(url, timeout=10)
        with open(filename, 'wb') as file:
            for chunk in data:
                file.write(chunk)
        sleep(RATE_LIMIT)
    else:
        print(f'{filename} already exists')


def build_filename(url, post_id, tag):
    filename = f'{post_id}{url[-4:]}'
    if tag:
        filename = f'{tag}-{filename}'
    return filename


if __name__ == '__main__':

    main()
