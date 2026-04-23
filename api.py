# This Python file uses the following encoding: utf-8
import json
import urllib.parse
import urllib.request
import os
import ssl
import certifi
from rich.progress import Progress

class rule34api:
    domein: str
    api_key: str
    user_id: str

    progress: Progress

    def __init__(self, domein, api_key = "", user_id = ""):
        self.domein = domein
        self.api_key = api_key
        self.user_id = user_id

        self.progress = Progress()
        self.progress.start()

    def _get_url(self, post_count: int, page: int, tags: str) -> str:
        tags = urllib.parse.quote(tags)
        return f'https://{self.domein}/index.php?page=dapi&s=post&q=index&limit={post_count}&pid={page}&tags={tags}&api_key={self.api_key}&user_id={self.user_id}&json=1'

    def _fetch_json(self, url: str) -> list:
        context = ssl.create_default_context(cafile=certifi.where())
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request, context=context)
        resp = response.read().decode('utf-8')
        try:
            return json.loads(resp)
        except Exception as ex:
            print("[ERROR] server retuned something that not a json")
            print(f'[ERROR] {ex}: {resp} {len(resp)}')

    def get_posts(self, post_count: int, page: int, tags: str) -> list:
        url = self._get_url(post_count, page, tags)
        posts = self._fetch_json(url)
        return posts

    def download_post(self, url: str, destination: str) -> str:
        req = urllib.request.Request(url)
        file_path = os.path.join(destination, url.split('/')[-1])
        with urllib.request.urlopen(req) as resp:
            total = resp.getheader('Content-Length')
            total_bytes = int(total)
            task = self.progress.add_task(f"Downloading {url.split('/')[1]}", total=total_bytes)

            chunk_size = 64 * 1024
            downloaded = 0
            with open(file_path, 'wb') as out:

                while total_bytes != downloaded:
                    chunk = resp.read(chunk_size)
                    out.write(chunk)
                    downloaded += len(chunk)
                    self.progress.update(task, advance=len(chunk))
                self.progress.remove_task(task)
                print("Finished Downloading " + file_path.split(os.sep)[1])
                return (file_path)


