from flask import Flask, render_template, request
import mechanize
from bs4 import BeautifulSoup

app = Flask(__name__)

def initialize_browser():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    return br

def search_movie(br, searchname):
    br.open("https://www.fzmovies.net/")
    br.select_form(nr=0)
    br.form['searchname'] = searchname
    br.submit()
    return br.response().read()

def extract_movie_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all("div", {"class": "mainbox"})
    details = []
    links = []
    for div in divs:
        rows = div.find_all('a', href=True)
        for row in rows:
            links.append(row['href'])
        for tes in divs:
            details.append(tes.find_all(text=True))
    links = list(dict.fromkeys(links))
    perf_list = [i for i in links if i and 'movietags' not in i]
    return perf_list, details

def get_download_links(br, detail_url):
    detail_url = detail_url.replace(" ", "%20")
    br.open(detail_url)
    orders_html = br.response().read()
    soup = BeautifulSoup(orders_html, 'html.parser')
    divs = soup.find_all("ul", {"class": "moviesfiles"})
    li = [u['href'] for d in divs for u in d.find_all('a', href=True) if 'mediainfo.php' not in u['href']]
    
    # Navigate to the download page
    download_links = []
    for link in li:
        download_page_url = 'https://fzmovies.net/' + link
        br.open(download_page_url)
        download_html = br.response().read()
        download_soup = BeautifulSoup(download_html, 'html.parser')
        download_divs = download_soup.find_all("a", {"id": "downloadlink"})
        for d in download_divs:
            download_links.append('https://fzmovies.net/' + d['href'])

    return download_links

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        br = initialize_browser()
        html = search_movie(br, movie_name)
        perf_list, details = extract_movie_links(html)
        return render_template('index.html', perf_list=perf_list, details=details, zip=zip)
    return render_template('index.html', perf_list=[], details=[], zip=zip)

@app.route('/details', methods=['GET'])
def details():
    detail_url = request.args.get('url')
    br = initialize_browser()
    download_links = get_download_links(br, detail_url)
    return render_template('details.html', download_links=download_links)

if __name__ == "__main__":
    app.run(debug=True)