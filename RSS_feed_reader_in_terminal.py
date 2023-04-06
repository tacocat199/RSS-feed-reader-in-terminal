# Import packages and modules
import requests
import webbrowser
import pandas as pd
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
    # Get the source code of the RSS feed
    response = get_source(url)
    # Convert the source code to an HTML object
    xml = HTML(html=response.text)
    # Find all the entry elements in the XML document
    items = xml.xpath('//item')
    # Initialize an empty list to store the entries
    entries = []
    # Loop through each item element
    for item in items:
        # Extract the title element text
        title = item.xpath('.//title')[0].text
        # Extract the link element text
        link = item.xpath('.//guid')[0].text # Use guid instead of link
        # Extract the pubDate element text and convert it to a datetime object
        pub_date = pd.to_datetime(item.xpath('.//pubdate')[0].text)
        # Extract the description element text
        description = item.xpath('.//description')[0].text
        # Create a dictionary with the entry data
        entry = {
            'title': title,
            'link': link,
            'pub_date': pub_date,
            'description': description
        }
        # Append the entry dictionary to the entries list
        entries.append(entry)
    # Return the entries list
    return entries

# Define a function to get the RSS feed URL from the user
def get_feed_url():
    """Get the RSS feed URL from the user.

    Returns:
        url (string): The RSS feed URL entered by the user.
    """
    url = input("Enter the RSS feed URL: ")
    return url

# Get the RSS feed URL from the user
url = get_feed_url()

# Parse the RSS feed from Epic Games Store
entries = parse_feed(url)

# Convert the entries list to a pandas dataframe
df = pd.DataFrame(entries)

# Display the first 5 rows of the dataframe
print(df.head())

# Filter the dataframe by title containing 'free'
free_games = df[df['title'].str.contains('free', case=False)]

# Display the filtered dataframe
print(free_games)

# Export the filtered dataframe to a csv file
free_games.to_csv('free_games.csv', index=False)

# Open one of the links in a web browser
webbrowser.open(free_games['link'].iloc[0])