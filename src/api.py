from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import urllib.parse as p
import re
import os
import pickle


youtube = None
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
class YoutubeSearch:
    search_term= None
    search_results = []
    video_details = []
    def __init__(self):
        self.youtube = self.youtube_authenticate()
    def youtube_authenticate(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "credentials.json"
        creds = None
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # if there are no (valid) credentials availablle, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
                creds = flow.run_local_server(port=0)
                # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return build(api_service_name, api_version, credentials=creds)

     
    def get_video_details(self, **kwargs):
        return self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            **kwargs
        ).execute()

    def search(self,**kwargs):
        return self.youtube.search().list(
            part="snippet",
            **kwargs
        ).execute()

    def print_video_infos(self,video_response):
        items = video_response.get("items")[0]
        # get the snippet, statistics & content details from the video response
        snippet         = items["snippet"]
        
        channel_title   = snippet["channelTitle"]
        title           = snippet["title"] 

        self.video_details.append([f"""\
        Title: {title}
        
        """])
        print(f"""\
        Title: {title}
        Channel Title: {channel_title}
      
        """)

    def startSearch(self,videos,totalResults=4):
        self.video_details.clear()
        self.search_results.clear()
        
        for i in range(0,totalResults):
            video_id = videos[i]
            
            self.search_results.append(video_id)
            video_response = self.get_video_details(id=video_id)
            print("This is response\n\n ",video_response)
            # print the video details
            print("="*50)
            self.print_video_infos(video_response)
            print("="*50)
        return self.video_details

    def sstartSearch(self,search_term,totalResults=2):
        self.video_details.clear()
        self.search_results.clear()
        response = self.search(q=search_term,maxResults=totalResults)
        items = response.get("items")
        print("Items are \n",items)
        for item in items:
             # get the video ID
            video_id = item["id"]["videoId"]
        # get the video details
            self.search_results.append(video_id)
            video_response = self.get_video_details(id=video_id)
            print("This is response\n\n ",video_response)
         # print the video details
            print("="*50)
            self.print_video_infos(video_response)
            print("="*50)
        return self.video_details    








music = YoutubeSearch()

#music.startSearch()
#print(music.search_results)
#print(music.video_details)