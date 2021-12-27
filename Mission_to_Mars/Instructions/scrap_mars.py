#imports
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

#scrape all function
def scrape_all():
    # need to return a json that has data to load into database (MongoDB)
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # get datta from news page #2add variables for news title and paragraph
    news_title, news_paragraph = scrape_news(browser)
    
    # then add info to dictionary
    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featuredImage": scrape_images(browser),
        "facts": scrape_facts(browser),
        "hemispheres": scrape_hemisphere_pages(browser),
        "lastUpdated": dt.datetime.now()
    }
    
    #stop webdriver
    browser.quit()
    
    return marsData

#scrape the mars news page
def scrape_news(browser):
    
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)


    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
   
    slide_elem = news_soup.select_one('div.list_text')
    #get title
    news_title = slide_elem.find('div', class_='content_title').get_text()
    #get paragraph
    news_p= slide_elem.find('div', class_='article_teaser_body').get_text()
    
    #return title and para 
    return news_title, news_p


#scrape through the feature image page
def scrape_images(browser):
    #vist imagges page
    featured_image_url = 'https://spaceimages-mars.com'
    browser.visit(featured_image_url)
    
    # Find and click the full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()
    
    #parsing through with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    #locating mars image
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


#scrape through facts page to get table
#grabbing the html code 
def scrape_facts(browser):
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)
    
    html = browser.html
    fact_soup = soup(html, 'html.parser')
    
    #locating facts
    facts_loc = fact_soup.find('div', class_="diagram mt-4")
    fact_table = facts_loc.find('table') #getting html for fact table
    
    facts = ""
    
    #add text to facts
    facts += str(fact_table)
    
    return facts


#scrape hemisphere pages
def scrape_hemisphere_pages(browser):
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    
   # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Get a list of all of the hemispheres
    #links = browser.find_by_css('a.product-item img')

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(4):
    #make a dictionary for hemisphere
        hemisphereInfo = {}
    
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
    
        # Next, we find the Sample image anchor tag and extract the href
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo["img_url"] = sample['href']
    
        # Get Hemisphere title
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text
    
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphereInfo)
    
        # Finally, we navigate backwards
        browser.back()
    
    return hemisphere_image_urls
    

#run script
if __name__ == "__main__":
    print(scrape_all())