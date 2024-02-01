import requests
from bs4 import BeautifulSoup
import openai
import os

# OpenAI GPT-3 API key
api_key = os.environ['OPENAI_API_KEY']
client = openai.Client(api_key=api_key)


# Function to scrape the blog content
def scrape_blog_content(url):
  try:
    response = requests.get(url)
    if response.status_code == 200:
      soup = BeautifulSoup(response.content, 'html.parser')
      blog_content=""
      paragraph_counter = 0
      for paragraph in soup.find_all('p'):
        blog_content += paragraph.get_text() + "\n"
        paragraph_counter += 1
        if paragraph_counter >= 10:
          break
      return blog_content.strip()
  except Exception as e:
    print(f"Error: {e}")
    return None 


# Function to summarize using OpenAI GPT API
def summarize_with_gpt(content):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages = [{"role": "system", "content":f"Please summarize the following blog content:\n{content}\n"}],
    temperature=0.5
  )
  return response.choices[0].message.content

# Main function
def main():
  # URL of the blog you want to scrape
  blog_url_input=input("Enter the URL of the blog you want to scrape: ")
  #blog_url = "https://www.engadget.com/the-morning-after-apples-vision-pro-is-almost-here-and-samsungs-ai-gambit-150028059.html?_fsig=Awn7oW7jHOoOf36SHh3iRg--%7EA"
  content = scrape_blog_content(blog_url_input)

  if content:
    summary = summarize_with_gpt(content)
    print("SUMMARY:\n")
    print(summary)


if __name__ == "__main__":
  main()
