import requests

# Function to download video and save as video.mp4
def download_video(url):
    response = requests.get(url)

    if response.status_code == 200:
        with open("video.mp4", "wb") as file:
            file.write(response.content)
            file.close()

        print("Video downloaded successfully!")
        return True
    else:
        print(f"Failed to download the video: {response.status_code}")
        return False