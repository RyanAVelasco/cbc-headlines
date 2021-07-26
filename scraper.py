from selenium import webdriver
import codecs

##for headless operation uncomment
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()

##saves headlines to these files, separated by region
##this will stay in 'w' until I make it so that we don't write duplicate headlines
world = open('world.txt', 'w')
manitoba = open('manitoba.txt', 'w')
british_columbia = open('british_columbia.txt', 'w')
calgary = open('calgary.txt', 'w')
edmonton = open('edmonton.txt', 'w')
saskatchewan = open('saskatchewan.txt', 'w')
saskatoon = open('saskatoon.txt', 'w')
thunder_bay = open('thunder_bay.txt', 'w')
sudbury = open('sudbury.txt', 'w')
windsor = open('windsor.txt', 'w')
london = open('london.txt', 'w')
kitchener_waterloo = open('kitchener_waterloo.txt', 'w')
hamilton = open('hamilton.txt', 'w')
toronto = open('toronto.txt', 'w')
ottawa = open('ottawa.txt', 'w')
montreal = open('montreal.txt', 'w')
new_brunswick = open('new_brunswick.txt', 'w')
prince_edward_island = open('prince_edward_island.txt', 'w')
nova_scotia = open('nova_scotia.txt', 'w')
newfoundland_labrador = open('newfoundland_labrador.txt', 'w')
north = open('north.txt', 'w')

world.close()
manitoba.close()
british_columbia.close()
calgary.close()
edmonton.close()
saskatchewan.close()
saskatoon.close()
thunder_bay.close()
sudbury.close()
windsor.close()
london.close()
kitchener_waterloo.close()
hamilton.close()
toronto.close()
ottawa.close()
montreal.close()
new_brunswick.close()
prince_edward_island.close()
nova_scotia.close()
newfoundland_labrador.close()
north.close()

#files names of regions
region_files = [
    'world.txt', 'manitoba.txt', 'british_columbia.txt', 'calgary.txt', 'edmonton.txt', 'saskatchewan.txt', 'saskatoon.txt', 'thunder_bay.txt', 'sudbury.txt', 'windsor.txt', 'london.txt', 'kitchener_waterloo.txt', 'hamilton.txt', 'toronto.txt', 'ottawa.txt', 'montreal.txt', 'new_brunswick.txt', 'prince_edward_island.txt', 'nova_scotia.txt', 'newfoundland_labrador.txt', 'north.txt'
]

##list of regions and their associated urls
sectionURL = {
    'world': 'https://www.cbc.ca/news/world', 
    'manitoba': 'https://www.cbc.ca/news/canada/manitoba', 
    'british-columbia': 'https://www.cbc.ca/news/canada/british-columbia', 
    'calgary': 'https://www.cbc.ca/news/canada/calgary', 
    'edmonton': 'https://www.cbc.ca/news/canada/edmonton', 
    'saskatchewan': 'https://www.cbc.ca/news/canada/saskatchewan', 
    'saskatoon': 'https://www.cbc.ca/news/canada/saskatoon', 
    'thunder-bay': 'https://www.cbc.ca/news/canada/thunder-bay', 
    'sudbury': 'https://www.cbc.ca/news/canada/sudbury', 
    'windsor': 'https://www.cbc.ca/news/canada/windsor', 
    'london': 'https://www.cbc.ca/news/canada/london',
    'kitchener-waterloo': 'https://www.cbc.ca/news/canada/kitchener-waterloo', 
    'hamilton': 'https://www.cbc.ca/news/canada/hamilton', 
    'toronto': 'https://www.cbc.ca/news/canada/toronto', 
    'ottawa': 'https://www.cbc.ca/news/canada/ottawa', 
    'montreal': 'https://www.cbc.ca/news/canada/montreal', 
    'new-brunswick': 'https://www.cbc.ca/news/canada/new-brunswick', 
    'prince-edward-island': 'https://www.cbc.ca/news/canada/prince-edward-island', 
    'nova-scotia': 'https://www.cbc.ca/news/canada/nova-scotia', 
    'newfoundland-labrador': 'https://www.cbc.ca/news/canada/newfoundland-labrador', 
    'north': 'https://www.cbc.ca/news/canada/north'
}

##empty list to store headline article urls
headlines_articles = []

##region_index is used for changing between regions to scrape
region_index = 0

##match_writing is used to make sure we switch to the next region once all articles are saved
match_writing = 1

##main code
##if you don't want to go headless remove options=fireFoxOptions in next line
with webdriver.Firefox(options=fireFoxOptions) as driver: 
    for region, url in sectionURL.items():
        driver.get(url)

        print(region_files[region_index].replace('.txt', '').upper())
        articles = driver.find_elements_by_class_name('card')
        for links in articles:
            
            ##link = links.find_elements_by_tag_name('a')
            link = links.get_attribute('href')

            ##gets and places in list urls of articles that are from the current region
            if not link == None and sectionURL[region] in link : headlines_articles.append(link)
        
        for writing in range(0, len(headlines_articles)):

            ##navigate to current article
            driver.get(headlines_articles[writing])
            if writing == 1 : match_writing = 1    

            ##begin scraping article here
            if 'https://www.cbc.ca/player/play/' in driver.current_url or not driver.find_element_by_tag_name('h1'):
                continue
            else:
                #saves aritcle headline to variable
                headline = driver.find_element_by_tag_name("h1").text
                
                #saves aritcle subtitle to variable
                subtitle = driver.find_element_by_tag_name('h2').text
                
                #saves aritcle author/timestamp to variable
                author_timestamp = driver.find_element_by_class_name('bylineDetails').text
                
                ##image url .placeholder attr=src and caption .image-caption // for now
                
                #saves looks at article body and saves it o variable
                article = driver.find_element_by_class_name('story')
                paragraphs = article.find_elements_by_tag_name('p')

                ##begins saving the article here
                with codecs.open(region_files[region_index], 'a', 'utf-8-sig') as temp:
                    temp.write('[HEADLINE] ' + headline + '\n' + '[SUBTITLE] ' + subtitle + '\n' + '[AUTHOR/TIMESTEAMP] ' + author_timestamp + '\n')
                    temp.write('[ARTICLE]')
                    for paragraph in paragraphs:
                        temp.write(paragraph.text + '\n\n') 
                    temp.write('[END OF ARTICLE]\n\n')
                    temp.close()
                match_writing += 1

        #this empties list with the article links to prevent duplication
        headlines_articles = []

        #increments region_index to start search in next region
        region_index += 1

driver.quit
