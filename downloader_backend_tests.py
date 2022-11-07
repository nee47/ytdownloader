from main import DownloaderBackend

def test_wrong_youtube_link_false():
    url = 'https://youtub.e/gU1x5ODgKw4?t=1'
    assert DownloaderBackend().validate_url(url) == False

def test_correct_youtube_link_first_case_true():
    url = 'https://youtu.be/gU1x5ODgKw4?t=1'
    assert DownloaderBackend().validate_url(url) == True

def test_correct_youtube_link_second_case_true():
    url = 'https://www.youtube.com/watch?v=gU1x5ODgKw4'
    assert DownloaderBackend().validate_url(url) == True

def test_empty_youtube_link_is_false():
    url = ''
    assert DownloaderBackend().validate_url(url) == False

# Downlodaer