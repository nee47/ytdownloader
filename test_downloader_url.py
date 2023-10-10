from download_url import EasyDownloader 

def test_ytdlp_already_updated():
    lines = EasyDownloader().update_ytdlp()
    assert  "yt-dlp is up to date" in lines[1]

# Downlodaer