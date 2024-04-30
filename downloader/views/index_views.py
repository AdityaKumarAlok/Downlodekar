from django.shortcuts import render,redirect
from django.http import HttpResponse
from pytube import YouTube
import os
from django.http import FileResponse
from urllib.parse import urlparse
import instaloader 
import requests
from ..helpers.twitter_downloader import download_twitter_video
from ..helpers.clear import delete_items_in_folder
from django.http import HttpResponseBadRequest, FileResponse


def index(request):
    return render(request, 'index.html')
def features(request):
    return render(request, 'features.html')
def pricing(request):
    return render(request, 'pricing.html')
def donate(request):
    return render(request, 'donate.html')

def download_video(request):
    if request.method == 'POST':
        video_link = request.POST.get('video_link')
        domain_response = get_domain_name(video_link)
        if domain_response == "youtube.com":
            if video_link:
                try:
                    delete_items_in_folder('Media/Youtube_Media')
                    yt = YouTube(video_link)
                    stream = yt.streams.get_highest_resolution()
                    if stream:
                        save_path = 'Media/Youtube_Media'
                        video_path = stream.download(output_path=save_path)
                        filename = os.path.basename(video_path)
                        response = FileResponse(open(video_path, 'rb'), as_attachment=True)
                        return response
                    else:
                        return HttpResponse("No stream available for this video.")
                except Exception as e:
                    return HttpResponse(f"An error occurred: {str(e)}")

            else:
                return HttpResponse("No video URL provided.")
        elif domain_response=="instagram.com":
            if video_link:
                shortcode = str(video_link.split('/')[4])
                try:
                    delete_items_in_folder('Media/Insareel')
                    L = instaloader.Instaloader()
                    L.login(os.environ.get("INSTA_USERNAME"), os.environ.get("PASSWORD"))
                    try:
                        post = instaloader.Post.from_shortcode(L.context, shortcode)
                    except instaloader.exceptions.InstaloaderException as e:
                        error_message = f"Error occurred: {e}"
                        return HttpResponse(error_message)
                    video_url = post.video_url
                    response = requests.get(video_url, stream=True)
                    file_path = os.path.join('Media', 'Instareel', f'{shortcode}.mp4')
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    return FileResponse(open(file_path, 'rb'), as_attachment=True)
                except Exception as e:
                    error_message = f"Error occurred: {e}"
                    return HttpResponse(error_message)
            return HttpResponse("Invalid request method.")
        elif domain_response == "twitter.com":
            if video_link:
                shortcode = str(video_link.split('/')[5])
                try:
                    delete_items_in_folder('Media/Twitter')
                    file_path = download_twitter_video(str(video_link), shortcode)
                    return FileResponse(open(file_path, 'rb'), as_attachment=True)
                except Exception as e:
                    return HttpResponseBadRequest(str(e))
            else:
                return HttpResponseBadRequest('URL parameter is missing.')  
        else:
            return HttpResponse("Unsuppoted domain")
    else:
        return redirect('/')
def get_domain_name(link):
        try:
            parsed_link = urlparse(link)
            domain = parsed_link.netloc
            if domain.startswith('www.'):
                domain = domain[4:]  
            return domain
        except Exception as e:
            return None
        