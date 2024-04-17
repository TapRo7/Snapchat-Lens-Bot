import requests

# Function to save the entire website HTML so we can scrape needed data from it
def save_html(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Write the HTML content to a file
        with open('website.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        print('HTML content saved to website.html')
        return True
    else:
        print('Failed to download the HTML:', response.status_code)
        return False