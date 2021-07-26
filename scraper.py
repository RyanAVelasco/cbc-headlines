from selenium import webdriver
import codecs

##for headless operation uncomment
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()

##saves headlines to these files, separated by region
world = open('world.txt', 'a')
manitoba = open('manitoba.txt', 'a')
british_columbia = open('british_columbia.txt', 'a')
calgary = open('calgary.txt', 'a')
edmonton = open('edmonton.txt', 'a')
saskatchewan = open('saskatchewan.txt', 'a')
saskatoon = open('saskatoon.txt', 'a')
thunder_bay = open('thunder_bay.txt', 'a')
sudbury = open('sudbury.txt', 'a')
windsor = open('windsor.txt', 'a')
london = open('london.txt', 'a')
kitchener_waterloo = open('kitchener_waterloo.txt', 'a')
hamilton = open('hamilton.txt', 'a')
toronto = open('toronto.txt', 'a')
ottawa = open('ottawa.txt', 'a')
montreal = open('montreal.txt', 'a')
new_brunswick = open('new_brunswick.txt', 'a')
prince_edward_island = open('prince_edward_island.txt', 'a')
nova_scotia = open('nova_scotia.txt', 'a')
newfoundland_labrador = open('newfoundland_labrador.txt', 'a')
north = open('north.txt', 'a')

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
headlines_articles = []
region_index = 0
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
                headline = driver.find_element_by_tag_name("h1").text
                
                subtitle = driver.find_element_by_tag_name('h2').text
                
                author_timestamp = driver.find_element_by_class_name('bylineDetails').text
                
                ##image url .placeholder attr=src and caption .image-caption // for now
                
                article = driver.find_element_by_class_name('story')
                paragraphs = article.find_elements_by_tag_name('p')

                ##begins saving the article here
                with codecs.open(region_files[region_index], 'a', 'utf-8-sig') as temp:
                    temp.write('[HEADLINE] ' + headline + '\n' + '[SUBTITLE] ' + subtitle + '\n' + '[AUTHOR/TIMESTEAMP] ' + author_timestamp + '\n')
                    temp.write('[ARTICLE]')
                    for paragraph in paragraphs:
                        temp.write(paragraph.text + '\n\n') 
                    temp.write('END OF ARTICLE\n\n')
                    temp.close()
                match_writing += 1

        #this empties list with the article links to prevent duplication
        headlines_articles = []

        #increments region_index to start search in next region
        region_index += 1

driver.quit
