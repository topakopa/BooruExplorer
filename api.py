# This Python file uses the following encoding: utf-8
import json
import urllib.parse
import urllib.request
import os
import ssl
from dinamicThings import Progress

# import certifi
# from rich.progress import Progress
from console import console


class rule34api:
    domein: str
    api_key: str
    user_id: str

    # progress: Progress

    def __init__(self, domein, api_key="", user_id=""):
        self.domein = domein
        self.api_key = api_key
        self.user_id = user_id

        # self.progress = Progress()
        # self.progress.start()

    def _get_url(self, post_count: int, page: int, tags: str) -> str:
        tags = urllib.parse.quote(tags)
        return f"https://{self.domein}/index.php?page=dapi&s=post&q=index&limit={post_count}&pid={page}&tags={tags}&api_key={self.api_key}&user_id={self.user_id}&json=1"

    def _fetch_json(self, url: str) -> list:
        # context = ssl.create_default_context(cafile=certifi.where())
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        resp = response.read().decode("utf-8")
        try:
            return json.loads(resp)
        except Exception as ex:
            console.error("[ERROR] server retuned something that not a json")
            console.error(f"[ERROR] {ex}: {resp} {len(resp)}")

    def get_posts(self, post_count: int, page: int, tags: str) -> list:
        url = self._get_url(post_count, page, tags)
        console.debug(url)
        posts = self._fetch_json(url)
        return posts

    def download_post(
        self, url: str, destination: str, progress: Progress = Progress()
    ) -> str:
        req = urllib.request.Request(url)
        file_path = os.path.join(destination, url.split("/")[-1])
        with urllib.request.urlopen(req) as resp:
            total = resp.getheader("Content-Length")
            total_bytes = int(total)
            # task = progress.add_task(f"Downloading {url.split('/')[1]}", total=total_bytes)
            progress.maximum = total_bytes
            console.debug(progress)
            console.log("Downloading " + file_path, "Downloader")

            chunk_size = 64 * 1024
            downloaded = 0
            with open(file_path, "wb") as out:
                while total_bytes != downloaded:
                    chunk = resp.read(chunk_size)
                    out.write(chunk)
                    downloaded += len(chunk)
                    # self.progress.update(task, advance=len(chunk))
                    progress.value = downloaded
                # self.progress.remove_task(task)
                console.log("Finished Downloading " + file_path, "Downloader")
                return file_path
