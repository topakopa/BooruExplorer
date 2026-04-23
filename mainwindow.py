# This Python file uses the following encoding: utf-8
import sys
import os
import threading
import json
import ast
from pathlib import Path
from api import rule34api
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QPixmap, QDesktopServices
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    debug: int = 0
    max_threads: int = 8
    page: int = 0
    lock_scroll: bool = False
    posts_per_page: int = 42
    current_tags: str = ''
    openedimages_folder: str = 'tmp'
    thumbnails_folder: str = 'tmp'
    download_folder: str = 'output'
    domein: str = 'safebooru.org'
    api_key: str = ''
    user_id: str = ''
    postlist: list = []
    pending_thumbs: list = []
    pending_images: list = []
    api: rule34api
    is_loading: bool = False

    def __init__(self, parent=None):
        # Наштралочки
        self._init_config()
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scrollbar = self.ui.listWidget.verticalScrollBar()
        self.scrollbar.setSingleStep(20)

        # Стартовые приколы
        self.api = rule34api(self.domein, self.api_key, self.user_id)
        self.ui.searchBox_2.setText(self.current_tags)
        self.search_posts()


        # Ивенты
        self.ui.searchButton.clicked.connect(self.searchButton_Clicked)
        self.scrollbar.valueChanged.connect(self.listWidget_onScroll)
        self.ui.listWidget.itemDoubleClicked.connect(self.listWidget_itemDoubleClicked)
        # self.ui.searchBox_2.textChanged.connect(self.searchBox.textChanged)
        # app.aboutToQuit.connect(self.quiting)

    def searchButton_Clicked(self):
        self.reset_everything()
        self.search_posts()

    def listWidget_onScroll(self, value):
        if not self.is_loading and not self.lock_scroll and value >= self.scrollbar.maximum() - 1000:
            thread = threading.Thread(target=self.search_posts, args=[])
            thread.start()

    def _init_config(self):
        if not Path('config.json').exists():
            data = {
                "debug": self.debug,
                "domein": self.domein,
                "api_key": self.api_key,
                "user_id": self.user_id,
                "temp_opened_files_folder": self.openedimages_folder,
                "temp_thumbnails_folder": self.thumbnails_folder,
                "download_folder": self.download_folder
            }
            with open('config.json', 'w') as file:
                json.dump(data, file)
        file = open('config.json', 'r', encoding='utf-8')
        config = json.load(file)
        self.debug = config['debug']
        self.domein = config['domein']
        self.api_key = config['api_key']
        self.user_id = config['user_id']
        file.close()

        for i in range(len(sys.argv)):
            arg = sys.argv[i]
            next_arg = '' if i == len(sys.argv) - 1 else sys.argv[i + 1]

            try:
                if arg in ['--max-threads', '-T']:
                    self.max_threads = int(next_arg)
                elif arg in ['--posts-per-page', '-c']:
                    self.posts_per_page = int(next_arg)
                elif arg in ['--tags', '-t']:
                    self.current_tags = next_arg
                elif arg in ['--debug']:
                    self.debug = 1
            except Exception:
                print(f'Invalid arguments! Use {sys.argv[0]} --help')
        os.makedirs(self.thumbnails_folder, exist_ok=True)
        os.makedirs(self.openedimages_folder, exist_ok=True)
        os.makedirs(self.download_folder, exist_ok=True)

    def search_posts(self) -> list:
        print('[Loader] Fetching post links...')
        self.is_loading = True
        posts = self.api.get_posts(self.posts_per_page, self.page, self.current_tags)
        pi = 0

        if posts is None:
            print("PostsList is Empty")
            self.ui.statusbar.showMessage("Постов по этому запросу больше нет увы", 5000)
            self.lock_scroll = True
            return

        for post in posts:
            if len(self.pending_thumbs) == pi % self.max_threads:
                self.pending_thumbs.append([post])
            else:
                self.pending_thumbs[pi % self.max_threads].append(post)
            pi += 1

        self.threads_finished = 0
        thread_count = len(self.pending_thumbs)
        print(f'Starting {thread_count} threads...')

        def search_posts_async_node(self, index):
            for post in self.pending_thumbs[index]:
                path = os.path.join(self.thumbnails_folder, post['preview_url'].split(os.sep)[-1])

                if any(p['id'] == post['id'] for p in self.postlist):
                    print("File " + path.split(os.sep)[-1] + " already on the list. Skipping...")
                    continue

                self.ui.statusbar.text = "test"

                if os.path.exists(path):
                    print("File " + path.split(os.sep)[-1] + " already exist.")
                    self.add_image(path, str(post), type="local")
                else:
                    self.add_image(post['preview_url'], str(post))
                self.postlist.append(post)

        for i in range(thread_count):
            thread = threading.Thread(target=search_posts_async_node, args=[self, i])
            thread.start()

        self.page += 1
        self.is_loading = False
        return posts



    def reset_everything(self):
        self.ui.listWidget.clear()
        self.ui.listWidget.verticalScrollBar().value = 0
        self.postlist.clear()
        self.current_tags = self.ui.searchBox_2.text()
        self.pending_images.clear()
        self.pending_thumbs.clear()
        self.page = 0
        self.lock_scroll = False

    def add_image(self, image_path, post, type='url'):
        actual_path = ''
        if type == 'url':
            actual_path = self.api.download_post(image_path, self.thumbnails_folder)
        elif type == 'local':
            actual_path = image_path
        pixmap = QPixmap(actual_path)
        scaled_pix = pixmap.scaled(
            self.ui.listWidget.iconSize(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        icon = QIcon(scaled_pix)
        item = QListWidgetItem(icon, '')
        item.setData(Qt.ItemDataRole.UserRole, post)
        self.ui.listWidget.addItem(item)

    def listWidget_itemDoubleClicked(self, item):
        self.open_file(item)

    def open_file(self, item):
        post_str = item.data(Qt.ItemDataRole.UserRole)
        post = ast.literal_eval(post_str)
        file_path = os.path.abspath(self.api.download_post(post["file_url"], self.openedimages_folder))
        if not os.path.exists(file_path):
            print(f"Файл не найден: {file_path}")
            self.ui.statusbar.showMessage("Ошибка: Фаил не скачался :<", 5000)
            return

        file_local_url = QUrl.fromLocalFile(file_path)
        QDesktopServices.openUrl(file_local_url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
