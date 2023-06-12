import os
from googleapiclient.discovery import build
import isodate
import datetime

class MixinAPI:
    """
    Класс-миксин для предоставления доступа к API ютуба.
        """
    __api_key: str = os.getenv('YT_API_KEY')
    @classmethod
    def get_service(cls):
        '''Возвращает специальный объект для работы с API'''

        youtube = build('youtube', 'v3', developerKey=cls.__api_key)
        return youtube


class PlayList(MixinAPI):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist = self.get_service().playlists().list(part='snippet', id=self.playlist_id).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'



    @property
    def data_playlist(self):
        '''Возвращает данные плейлиста'''

        playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                      part='contentDetails',
                                                                      maxResults=50).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(video_ids)
                                                              ).execute()

        return video_response


    @property
    def total_duration(self):
        '''Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста'''
        time_playlist = datetime.timedelta(hours=0, minutes=0, seconds=0)
        for video in self.data_playlist['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time_playlist += duration


        return time_playlist



    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        count = 0
        pop_video = ''
        for i in self.data_playlist['items']:
            like_count = i['statistics']['likeCount']
            if int(like_count) > int(count):
                pop_video = i['id']
        return f'https://youtu.be/{pop_video}'





