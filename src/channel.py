import json
import os
from googleapiclient.discovery import build




class Channel:

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        youtube_channels = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics')
        self.__info_to_print = youtube_channels.execute()
        self.title = self.__info_to_print["items"][0]["snippet"]["title"]
        self.description = self.__info_to_print["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/{self.__info_to_print['items'][0]['snippet']['customUrl']}"
        self.subscriber_count: int = int(self.__info_to_print["items"][0]["statistics"]["subscriberCount"])
        self.video_count: int = self.__info_to_print["items"][0]["statistics"]["videoCount"]
        self.view_count: int = self.__info_to_print["items"][0]["statistics"]["viewCount"]

    @property
    def channel_id(self):
        return self.__channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__info_to_print, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename):
        """Сохраняет значения атрибутов экземпляра Channel в файл в формате JSON."""
        channel = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'customUrl': self.url,
            'subscriberCount': self.subscriber_count,
            'videoCount': self.video_count,
            'viewCount': self.view_count
        }
        with open(filename, "w", encoding="UTF-8") as file:
            json.dump(channel, file, ensure_ascii=False)
