# Import packages and modules
import requests
import webbrowser
import pandas as pd
import re
from requests_html import HTMLSession
from requests_html import HTML

# Define a function to get the source code of the RSS feed URL
def get_source(url):
    """Return the source code for the provided URL
        
    Args:
        url (string): URL of the page to scrape
    
    Returns:
        response (object): HTTP response object from requests.html.
    """
    try:
        session = HTMLSession()
        response = session.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)

# Define a function to parse the RSS feed contents
def parse_feed(url):
    """Parse the RSS feed and return a list of entries.

    Args:
        url (string): URL of the RSS feed to parse.

    Returns:
        entries (list): A list of dictionaries contain the entry data.
    """
    response = get_source(url)
    xml = HTML(html=response.text)
    items = xml.xpath('//item')
    entries = []
    for item in items:
        entry = {
            'title': item.xpath('.//title')[0].text,
            'link': item.xpath('.//guid')[0].text, # Use guid instead of link
            'pub_date': pd.to_datetime(item.xpath('.//pubdate')[0].text),
            'description': item.xpath('.//description')[0].text
        }
        entries.append(entry)
    return entries

# Define a function to get the RSS feed URL from the user
def get_feed_urls():
    """Get the RSS feed URLs from the user.

    Returns:
        urls (string): The RSS feed URLs entered by the user.
    """
    urls_str = input("Enter the RSS feed URLs seperated by a comma or space: ")
    urls = [url.strip() for url in re.split(',|\s', urls_str) if url.strip()]
    return urls

def main():
    # Get the RSS feed URL from the user
    urls = get_feed_urls()

    # Parse the RSS feed from each URL and combine the results into a single dataframe
    entries = []
    for url in urls:
        entries += parse_feed(url)
    df = pd.DataFrame(entries)

    # Filter the dataframe by title containing 'free'
    free_games = df[df['title'].str.contains('free', case=False)]

    # Display the filtered dataframe
    print(free_games)

    # Export the filtered dataframe to a csv file
    free_games.to_csv('free_games.csv', index=False)

    # Open one of the links in a web browser
    # webbrowser.open(free_games['link'].iloc[0])

if __name__ == '__main__':
    main()