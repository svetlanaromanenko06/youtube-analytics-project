from googleapiclient.discovery import build
import os

class Video:


    def __init__(self, video_id):
        self.video_id = video_id
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.url: str = f'https://youtu.be/{self.video_id}'
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']


    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, id_video, id_playlist) -> None:
        super().__init__(id_video)
        self.id_playlist = id_playlist

"""
video1 = Video('AWX4JnAnjBE')
print(str(video1))
print(video1.video_id)
print(video1.video_title)
print(video1.url)
"""