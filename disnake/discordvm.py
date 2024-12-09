import requests
from disnake import Attachment
from disnake.ext import commands
from typing import Union
from typing import Any
import base64 as b64
import wave
import contextlib
from io import BytesIO
import json
from mutagen.mp3 import MP3
from mutagen.oggopus import OggOpus

class Cayonar():
    def __init__(self, token: str) -> None:
        self.base = 'https://discord.com/api/v10/'
        self.token = token
    async def cayona(self, method: str, path: str, content_type: str | None, data: Any) -> Any :
        self.content_type = content_type
        self.path = path
        self.method = method
        self.url: str = self.base + self.path
        self.data = data
        self.header = {
            "Content-Type": self.content_type,
            "Authorization": f"Bot {self.token}"
          }
        match self.method.lower(): #type: ignore
            case 'post':
                response = requests.post(url=self.url, headers=self.header, json=self.data)
                text = json.loads(response.text)
                if 'content' in text:
                  return response.text
                else: 
                  upload_url = text['attachments'][0]['upload_url']
                  upload_filename = text['attachments'][0]['upload_filename']
                  return {'upload_url': upload_url, 'upload_filename': upload_filename}
            case 'put':
                response = requests.put(url=self.path, headers=self.header, data=self.data)
                return response.text
                
                
class VoiceMessage:
    def __init__(self, bot: Union[commands.Bot, commands.InteractionBot, commands.AutoShardedBot]) -> None:
      self.bot = bot
    async def send(self, file: Attachment, channel_id: int):
      token = await self.bot.get_token()
      canar = Cayonar(token=token)
      datareq = {
        "files": [
          {
            "filename": file.filename,
            "file_size": file.size,
            "id": "2"
          }
        ]
      }
      gac = await canar.cayona(method='post', path=f'channels/{channel_id}/attachments', content_type="application/json", data=datareq)
      datafile = await file.read()
      await canar.cayona(method='put', path=gac['upload_url'], content_type=file.content_type, data=datafile)
      bytefile = BytesIO(datafile)
      if file.content_type.endswith('wav'): #type: ignore
        with contextlib.closing(wave.open(bytefile,'r')) as f:
          frames = f.getnframes()
          rate = f.getframerate()
          duration = frames / float(rate)
      elif file.content_type.endswith('mpeg'): #type: ignore
        duration = MP3(bytefile).info.length
      elif file.content_type.endswith('ogg'): #type: ignore
          duration = OggOpus(bytefile).info.length #type: ignore

      datapost = {
        "flags": 8192,
        "attachments": [
          {
            "id": "0",
            "filename": file.filename,
            "uploaded_filename": gac['upload_filename'],
            "duration_secs": duration, #type: ignore
            "waveform": b64.b64encode(datafile).decode()[:400],
          }
        ]
      }
      await canar.cayona(method='post', path=f'channels/{channel_id}/messages', content_type="application/json", data=datapost)
