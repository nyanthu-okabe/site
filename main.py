from bottle import Bottle, request, run, template, TEMPLATE_PATH, static_file
from duckduckgo_search import DDGS
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tempfile
import shutil
import uuid

# Set the template path to be relative to the script
TEMPLATE_PATH.insert(0, os.path.join(os.path.dirname(__file__), 'templates'))

# Create a temporary directory for downloaded images
# This directory will be cleaned up when the application exits
temp_image_dir = tempfile.mkdtemp()
print(f"Temporary image directory created at: {temp_image_dir}")

# Define generic headers to enhance anonymity
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

app = Bottle()

# Route for static files
@app.route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__), 'static'))

# Route for serving temporary downloaded images
@app.route('/temp_images/<filename:path>')
def serve_temp_image(filename):
    return static_file(filename, root=temp_image_dir)

@app.route('/')
def index():
    return template('index')

@app.route('/search')
def search():
    query = request.query.q
    region = request.query.region or 'wt-wt'  # Default to worldwide
    timelimit = request.query.timelimit or None # Default to all time
    safesearch = request.query.safesearch or 'moderate' # Default to moderate

    if not query or not query.strip():
        return template('search', query=query, results=[], error="検索ワードを入力してください。",
                        region=region, timelimit=timelimit, safesearch=safesearch)

    results = []
    error = None
    try:
        ddgs = DDGS(headers=headers)
        # Pass the search options to ddgs.text()
        results = ddgs.text(query, region=region, timelimit=timelimit, safesearch=safesearch, max_results=10)
    except Exception as e:
        print(f"Error during search: {e}")
        error = "検索中にエラーが発生しました。もう一度お試しください。"

    return template('search', query=query, results=results, error=error,
                    region=region, timelimit=timelimit, safesearch=safesearch)

@app.route('/all_image/<url:path>')
def all_image(url):
    display_image_urls = []
    error = None
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        for img_tag in soup.find_all('img'):
            img_url = img_tag.get('src')
            if img_url:
                absolute_img_url = urljoin(url, img_url)
                try:
                    img_response = requests.get(absolute_img_url, stream=True, headers=headers)
                    img_response.raise_for_status()
                    
                    # Generate a unique filename for the image
                    filename = str(uuid.uuid4()) + os.path.splitext(absolute_img_url)[1]
                    filepath = os.path.join(temp_image_dir, filename)
                    
                    with open(filepath, 'wb') as out_file:
                        shutil.copyfileobj(img_response.raw, out_file)
                    
                    display_image_urls.append(f"/temp_images/{filename}")
                except requests.exceptions.RequestException as img_e:
                    print(f"Could not download image {absolute_img_url}: {img_e}")
                    # Optionally, add a placeholder or skip this image
                except Exception as img_e:
                    print(f"Error processing image {absolute_img_url}: {img_e}")

    except requests.exceptions.RequestException as e:
        error = f"ウェブサイトの取得中にエラーが発生しました: {e}"
    except Exception as e:
        error = f"画像の抽出中にエラーが発生しました: {e}"

    return template('image_list', url=url, image_urls=display_image_urls, error=error)

if __name__ == "__main__":
    try:
        run(app, host='0.0.0.0', port=8080, debug=True)
    finally:
        # Clean up the temporary directory when the application exits
        if os.path.exists(temp_image_dir):
            shutil.rmtree(temp_image_dir)
            print(f"Temporary image directory removed: {temp_image_dir}")