import re
from bs4 import BeautifulSoup
import os

# Function to scrape needed URLs for Lens icon, video and creator name
# The html_file_path input is optional in case the storage location is ever changed, it will default to website.html
# in the bot's folder as we will always save it there with the same name and delete later

def scrape_data(html_file_path = "website.html"):
    try:
        # Check if the provided file path exists otherwise exit with return value 1 to signify invaid path error
        if not os.path.exists(html_file_path):
            return 1

        # Read HTML content from file
        with open(f'{html_file_path}', 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Define the pattern for the src attribute
        pattern = r'src="([^"]*)"'

        # Find all matches using regex
        src_values = re.findall(pattern, html_content)

        # Define patterns for URLs we want to extract, in this case the image and video URLs
        snapcode_pattern = r'app\.snapchat\.com/web/deeplink/snapcode'
        community_lens_pattern = r'(https://(?:community-lens\.storage\.googleapis\.com|lens-storage\.storage\.googleapis\.com)\S*)'

        # Filter src values based on patterns
        snapcode_src_values = [src for src in src_values if re.search(snapcode_pattern, src)]
        community_lens_src_values = [src for src in src_values if re.search(community_lens_pattern, src)]

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the title tag
        title_tag = soup.find('title')

        # Check if title tag exists
        if title_tag:
            # Get the lens creator name text by splitting the title as following
            username = title_tag.text.split("by")[1].split("-")[0].strip()
            lens_name = title_tag.text.split("by")[0].strip()
        else:
            # In case the title is not found, set lens creator to Unkown
            username = "Unknown"
            lens_name = "Lens"

        # Get the first link in the lists of matching values, since the image and video links appear twice in the HTML
        # Remove amp; as links cannot be opened with that in the URL
        # Change type from svg to png so we can download the image without a problem
        lens_icon_link = snapcode_src_values[0].replace("amp;", "").replace("type=svg", "type=png")
        lens_video_link = community_lens_src_values[0]
        lens_creator_name = username

        # Return a list of all the scraped data
        return_values = [lens_icon_link, lens_video_link, lens_creator_name, lens_name]

        return return_values
    except Exception as error:
        # In case of an unexpected error print the error and return false signifying something went wrong
        print(f"Error Occured in Data Scraping: {error}")
        return False