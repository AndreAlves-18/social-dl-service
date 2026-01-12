from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp
import os
import uuid

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def remove_file(path: str):
    try:
        os.remove(path)
    except Exception:
        pass

@app.post("/extract_info")
def extract_info(request: VideoRequest):
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True, 'format': 'best[ext=mp4]/best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=False)
            return {
                "title": info.get('title'),
                "direct_url": info.get('url'),
                "thumbnail": info.get('thumbnail'),
                "platform": info.get('extractor')
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/download_video")
def download_video(request: VideoRequest, background_tasks: BackgroundTasks):
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': filepath,
        'merge_output_format': 'mp4',
        'quiet': True,
        'force_ipv4': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    # Carrega cookies se o arquivo existir
    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = 'cookies.txt'

    # Headers especificos para Instagram
    if "instagram.com" in request.url:
        ydl_opts['http_headers'] = {
            'Referer': 'https://www.instagram.com/',
            'Accept-Language': 'en-US,en;q=0.9',
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([request.url])
            
        background_tasks.add_task(remove_file, filepath)
        
        return FileResponse(
            path=filepath, 
            filename=filename, 
            media_type='video/mp4'
        )
            
    except Exception as e:
        print(f"Erro: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))