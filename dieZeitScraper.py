import newspaper, bs4, requests, time, sys, webbrowser, re, datetime, os, json

baseUrl = 'https://www.zeit.de'
numberPages = 0
searcher = '/suche/index?p='
searcher2 = '/suche/index?q='
#index = 1
timeStamp = datetime.date.today().strftime("%d-%m-%Y")
hrefRegex = re.compile('https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}

notArticles = [
'https://www.zeit.de/index',
'https://www.zeit.de/impressum/index',
'https://www.zeit.de/administratives/agb-kommentare-artikel',
'https://www.zeit.de/hilfe/datenschutz',
'https://www.zeit.de/christ-und-welt',
'https://www.zeit.de/angebote/schule/index',
'https://www.zeit.de/hilfe/hilfe',
'https://www.zeit.de/hilfe/hilfe#rss',
'https://www.zeit.de/index',
'https://www.zeit.de/index',
'https://www.zeit.de/exklusive-zeit-artikel',
'https://www.zeit.de/index',
'https://www.zeit.de/angebote/derauftrag/index',
'https://www.zeit.de/angebote/partnersuche/index?pscode=01_100_20003_0001_0001_0005_empty_AF00ID_GV00ID',
'https://www.zeit.de/archiv',
'https://www.zeit.de/politik/index',
'https://www.zeit.de/gesellschaft/index',
'https://www.zeit.de/wirtschaft/index',
'https://www.zeit.de/kultur/index',
'https://www.zeit.de/kultur/literatur/index',
'https://www.zeit.de/kultur/film/index',
'https://www.zeit.de/kultur/musik/index',
'https://www.zeit.de/kultur/kunst/index',
'https://www.zeit.de/angebote/buchtipp/index',
'https://www.zeit.de/wissen/index',
'https://www.zeit.de/digital/index',
'https://www.zeit.de/campus/index',
'https://www.zeit.de/campus/angebote/forschungskosmos/index',
'https://www.zeit.de/arbeit/index',
'https://www.zeit.de/entdecken/index',
'https://www.zeit.de/sport',
'https://www.zeit.de/zeit-magazin/index',
'https://www.zeit.de/podcasts',
'https://www.zeit.de/video/index',
'https://www.zeit.de/mobilitaet/index',
'https://www.zeit.de/spiele/index',
'https://www.zeit.de/hamburg/index',
'https://www.zeit.de/news/index',
'https://www.zeit.de/angebote/weltderdaten/index',
'https://www.zeit.de/exklusive-zeit-artikel',
'https://www.zeit.de/index',
'https://www.zeit.de/impressum/index',
'https://www.zeit.de/administratives/agb-kommentare-artikel',
'https://www.zeit.de/hilfe/datenschutz',
'https://www.zeit.de/christ-und-welt',
'https://www.zeit.de/angebote/schule/index',
'https://www.zeit.de/hilfe/hilfe',
'https://www.zeit.de/hilfe/hilfe#rss',
'https://www.zeit.de/angebote/nachhaltiger-kaffee/index',
'https://www.zeit.de/index',
'https://www.zeit.de/exklusive-zeit-artikel',
'https://www.zeit.de/angebote/derauftrag/index',
'https://www.zeit.de/angebote/partnersuche/index?pscode=01_100_20003_0001_0001_0005_empty_AF00ID_GV00ID',
'https://www.zeit.de/archiv',
'https://www.zeit.de/politik/index',
'https://www.zeit.de/wirtschaft/index',
'https://www.zeit.de/kultur/index',
'https://www.zeit.de/kultur/literatur/index',
'https://www.zeit.de/kultur/film/index',
'https://www.zeit.de/kultur/musik/index',
'https://www.zeit.de/kultur/kunst/index',
'https://www.zeit.de/angebote/buchtipp/index',
'https://www.zeit.de/wissen/index',
'https://www.zeit.de/digital/index',
'https://www.zeit.de/campus/index',
'https://www.zeit.de/campus/angebote/forschungskosmos/index',
'https://www.zeit.de/arbeit/index',
'https://www.zeit.de/entdecken/index',
'https://www.zeit.de/sport',
'https://www.zeit.de/zeit-magazin/index',
'https://www.zeit.de/podcasts',
'https://www.zeit.de/video/index',
'https://www.zeit.de/mobilitaet/index',
'https://www.zeit.de/spiele/index',
'https://www.zeit.de/hamburg/index',
'https://www.zeit.de/news/index',
'https://www.zeit.de/gesellschaft/index',
'https://www.zeit.de/angebote/weltderdaten/index',
'https://www.zeit.de/exklusive-zeit-artikel',
'https://www.zeit.de/suche/index?p=',
'https://www.zeit.de/index',
'https://www.zeit.de/impressum/index',
'https://www.zeit.de/administratives/agb-kommentare-artikel',
'https://www.zeit.de/hilfe/datenschutz',
'https://www.zeit.de/christ-und-welt',
'https://www.zeit.de/angebote/schule/index',
'https://www.zeit.de/hilfe/hilfe',
'https://www.zeit.de/hilfe/hilfe#rss',
'https://www.zeit.de/suche/index'
    ]


def findNumberPagesSearcher(searcherUrl): ##This function looks fur the number of pages in the search results, while looking for a white space ''

    global baseUrl
    global numberPages

    res = requests.get(searcherUrl, headers=headers)
    res.raise_for_status()
    dieZeitSearch = bs4.BeautifulSoup(res.text, 'lxml')
    lastPage = dieZeitSearch.select('li.pager__page:nth-child(7) > a:nth-child(1)')
    numberRegex = re.compile(r'\d{1,3}')
    numberPagesSearch = numberRegex.search(str(lastPage))
    numberPages = int(numberPagesSearch.group())

    print(str(numberPages))

    return numberPages

def grabPagesSearcher(word, file):
    
    global baseUrl
    global numberPages
    global timestamp

    pageIndex = 1
    pageSelector = '&p='
    url = baseUrl + searcher2 + word + pageSelector + str(pageIndex)
    numberPages = findNumberPagesSearcher(baseUrl + searcher2 + word) 
    articleUrls = []
    
    for i in range(1, numberPages):
        notArticles.append(baseUrl + searcher2 + word + str(i))
    
    with open(file + '.txt', mode = 'wt', encoding = 'utf-8')  as linksFile:

        for i in range(1, numberPages):

            print('Page ' + str(i) + ' of ' + str(numberPages))

            res = requests.get(baseUrl + searcher2 + word + pageSelector + str(i))
            res.raise_for_status()
            #print(res.url)
            dieZeitSearch = bs4.BeautifulSoup(res.text, 'lxml')

            for link in dieZeitSearch.findAll("a", href=re.compile("https://www.zeit.de/")):
                if 'href' in link.attrs:
                    if str(link.attrs['href']) not in notArticles and (baseUrl + searcher2) not in str(link.attrs['href']) :
                        print(link.attrs['href'])
                        articleUrls.append(str(link.attrs['href']))

        
        #linksFile = open(str(file), 'w')
        linksFile.writelines('List of articles from with the word ' + word + ' from ' + str(timeStamp) + ' — Die Zeit \n')
        for line in articleUrls:
            linksFile.writelines(line + '\n') 
        linksFile.close()
        print(articleUrls)
        print('Done')

    return linksFile.name



def grabPagesArchive(year): ##based on a year, grab all the editions from that year and save them to 'file' as individual lines

    global baseUrl
    global notArticles

    if 'editions-year-' + str(year) +'.txt' in os.listdir('editions/'):

        answer = confirmRepeat(year)

        if answer == True:
            grabFlag = True
            
        elif answer == False:
            grabFlag = False
            
    else:
        grabFlag = True

    if grabFlag == True:
        archiveYear = baseUrl + '/' + str(year) + '/index'
        notArticles.append(archiveYear)

        res = requests.get(archiveYear, headers=headers)
        res.raise_for_status()
        dieZeitArchiv = bs4.BeautifulSoup(res.text, 'lxml')
        indexedPages = []
        
        for link in dieZeitArchiv.findAll("a", href=re.compile("https://www.zeit.de/")):
            if 'href' in link.attrs:
                if str(year) in str(link.attrs['href']) and str(link.attrs['href']) not in notArticles:
                    print(link.attrs['href'])
                    indexedPages.append(str(link.attrs['href']))

        with open('editions/editions-year-' + str(year) + '.txt', mode = 'wt', encoding = 'utf-8') as linksFile:
            linksFile.writelines('List of articles from ' + timeStamp + ' — Die Zeit \n')
            linksFile.write('\n'.join(indexedPages))
        
        print(linksFile.name)
        #print(indexedPages)
        print('Done compiling edition links for the year ' + str(year))
        
        return linksFile.name
    
    else:

        if 'editions-year-' + str(year) + '.txt' in os.listdir('editions/'):
            return 'skip ' + (str(year))
        else:
            print('No file for that year ' + str(year))

def grabArticleLinksEdition(file): ## based on a file resulting from the previous function, grab all the articles from every edition and save them as individual lines

    global notArticles
    editions = []
    yearRegex = re.compile(r'\d\d\d\d')
    articleLinks = []
    editionYear = int(yearRegex.search(file).group())
    
    if file == 'skip ' + str(editionYear):

        return 'articles/articles-year-' + str(editionYear) + '.txt'

    else:

        with open(str(file), 'r') as yearLinks:
            for line in yearLinks:
                line = line.strip()
                editions.append(line)
            
            editionYear = int(yearRegex.search(str(editions[1])).group())

        for i in range(1, len(editions)):
            notArticles.append(editions[i])
            res = requests.get(editions[i], headers=headers)
            #res = requests.post(editions[i], headers=headers)
            res.raise_for_status()

            dieZeitEdition = bs4.BeautifulSoup(res.text, 'lxml')
            for link in dieZeitEdition.findAll("a", href=re.compile("https://www.zeit.de/")):
                if 'href' in link.attrs:
                    if str(link.attrs['href']) not in notArticles and str(link.attrs['href']) not in editions:
                        #print(link.attrs['href'])
                        articleLinks.append(link.attrs['href'])
                        print('Processing URLs...')
        with open('articles/articles-year-' + str(editionYear) + '.txt', mode = 'wt', encoding = 'utf-8')  as articleLinksFile:
            articleLinksFile.writelines('List of articles from the year ' + str(editionYear) + ' compiled on ' + timeStamp + ' — Die Zeit \n')
            articleLinksFile.write('\n'.join(articleLinks))

            print('Done with ' + str(articleLinksFile.name))
            return articleLinksFile.name
    
    # global baseUrl

        # editionLink = baseUrl + '/' + str(year) + '/index'

        # res = requests.get(archiveYear)
        # res.raise_for_status()
        # dieZeitArchiv = bs4.BeautifulSoup(res.text, 'lxml')
        # indexedPages = []
def lookForWord(inputLinks, outputFile, word, wordPlural):
    # with open(str(file), 'r') as yearLinks:
    #     for line in yearLinks:
    #         line = line.strip()
    #         editions.append(line)
    

    
    # for i in range(1,len(articles)):
    #     article = newspaper.Article(articles[i])
    #     article.download()
    #     article.parse() 
    #     if word in article.text:
    #         selectedArticles.append({article, article.title, article.text})
    #         print(selectedArticles[-1])

    articles = []
    foundArticlesUrls = []
    foundArticles = []
    scrapedArticles = []
    searchRegex = re.compile(word, re.IGNORECASE)
    searchRegexPlural = re.compile(wordPlural, re.IGNORECASE)
    

    with open(str(inputLinks), 'r') as articleLinks:
        for line in articleLinks:
            line = line.strip()
            articles.append(line)
    
    with open('scrapedArticles.txt', 'r') as scrapedArticlesFile:
        for line in scrapedArticlesFile:
            line = line.strip()
            scrapedArticles.append(line)

    outputCreator = open(outputFile + '.txt', mode = 'w+', encoding = 'utf-8')
    outputCreator.close()

    #The resulting article text is a list, of which each paragraph is a string
    with open('scrapedArticles.txt', mode = 'a+', encoding = 'utf-8')  as scrapedArticlesFile:
            
        for i in range(1,len(articles)):
            
            try:
                res = requests.get(articles[i] + '/komplettansicht')
                res.raise_for_status()
                print('Multiple page article at ' + res.url)
            except:
                try:
                    res = requests.get(articles[i])
                    res.raise_for_status()
                    print('Single page article at ' + res.url)
                except:
                    print('Page not available at ' + articles[i])
                    continue
            appendableArticle = {}
            
            try:
                if (searchRegex.search(str(res.text.encode('utf-8'))) != None) or (searchRegexPlural.search(str(res.text)) != None) and res.url not in scrapedArticles:
                    try:
                        print('Condition met, word found')
                        appendableArticle['url'] = res.url
                        foundArticlesUrls.append(res.url)
                        dieZeitArticle = bs4.BeautifulSoup(res.text, 'lxml')
                        dieZeitSelectTime = dieZeitArticle.select('.metadata__date')
                        dieZeitSelectText = dieZeitArticle.select('p.paragraph')
                        dieZeitTimeSoup = bs4.BeautifulSoup(str(dieZeitSelectTime), 'lxml')
                        dieZeitArticleSoup = bs4.BeautifulSoup(str(dieZeitSelectText), 'lxml')
                        dieZeitArticleTime = str(dieZeitTimeSoup.getText())
                        dieZeitArticleText = str(dieZeitArticleSoup.getText())[1:-2]
                        appendableArticle['date'] = dieZeitArticleTime
                        dieZeitArticleTextList = dieZeitArticleText.split('\n,')
                        for line in dieZeitArticleTextList:
                            line = line.replace('\n', '')
                        
                        appendableArticle['article'] = dieZeitArticleTextList
                        
                        print('About to open output file')
                        with open(outputFile + '.txt', mode = 'a+', encoding = 'utf-8') as foundArticlesFile:
                            print('output file opened')
                            if appendableArticle['url'] not in foundArticles:
                                print('url not in list')
                                try:
                                    json.dump(appendableArticle,foundArticlesFile, ensure_ascii=False)
                                    print('Article found')
                                    print(appendableArticle['url'])
                                except:
                                    print('Not found at ' + appendableArticle['url'] )
                            else:
                                print('url in list, not appended')
                        foundArticles.append(appendableArticle['url'])
                        #foundArticlesFile.write(appendableArticle)

                    except:
                        
                        print('Error at ' + res.url)
                else:
                    print('Word not detected at ' + res.url)
                scrapedArticlesFile.write('\n')
                scrapedArticlesFile.write(articles[i])
                print('Searching...')
                scrapedArticles.append(articles[i])    
            
            except:
                print('Error at ' + articles[i])
            
            # if appendableArticle not in foundArticlesFile.readlines():
            #     for key, value in appendableArticle.items():
            #         foundArticlesFile.write('%s:%s\n' % (key, value))
            #         foundArticlesFile.write('\n')
                
            

    
    

        

            
        
        # for paragraph in dieZeitArticle.findall('p.paragraph'):
        #     print(str(paragraph))
        #     print('Fin')



def grabLinksSearch(index, file):
    
    global baseUrl
    global numberPages
    global timeStamp

    res = requests.get(baseUrl + searcher + str(index))
    res.raise_for_status()
    dieZeitSearch = bs4.BeautifulSoup(res.text, 'lxml')
    
    articleUrls = []

    #hrefRegex = re.compile('https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')


    for link in dieZeitSearch.findAll("a", href=re.compile("https://www.zeit.de/")):
        if 'href' in link.attrs:
            if str(link.attrs['href']) not in notArticles and (baseUrl + searcher) not in str(link.attrs['href']) :
                #print(link.attrs['href'])
                articleUrls.append(str(link.attrs['href']))

    
    linksFile = open(str(file), 'w')
    linksFile.writelines('List of articles from ' + timeStamp + ' — Die Zeit \n')
    for line in articleUrls:
        linksFile.writelines(line + '\n') 
    linksFile.close()
    print(articleUrls)
    print('Done')

def confirmRepeat(year, default="no"):

    question = 'There is already an index for the year ' + str(year) + '. Do you want to compile it again?'
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

#grabPagesArchive(2000, 'test4')
#grabArticleLinksEdition('test4')
#lookForWord('articles-year2000.txt', 'testFoundFile2', 'Reise')
# for i in range(1,10):
#     article = dieZeitSearch.select('article.zon-teaser-standard:nth-child(' + str(i) + ') > a:nth-child(1)') 
#     #.zon-teaser-standard__combined-link')
    
#     urlSearch = hrefRegex.search(str(article))
#     #print(urlSearch)
#     #url = urlSearch.group()
#     links = str(article)
#     print(len(article))
#     #print(article[0].getText())
#     # print(article)

#print(res.links)
# for article in testPage.article_urls:
#     print(article)

# for i in range(numberPages + 1):
    # newspaper
     #url = baseUrl str(index)
     #     index += 1


#step 1: 
    #consolidate archive of links
        #get links of editions per year
        #get links of articles per edition
    #or get links per search
#step 2:
    #get through article links

##consolidation!
#for i in range(2000, 2003):
    #grabArticleLinksEdition(grabPagesArchive(i))
grabPagesSearcher('reisepass', 'search/reisepassTest')

#scraping!

for i in range(0, len(os.listdir('search/'))):
    lookForWord('search/' + os.listdir('search/')[i], 'testFoundZeit', 'reisepass', 'reisepässen')

#grabPagesSearcher('reisepass')
# editions = []
# for i in range(2000, 2020):
#     editions.append(grabPagesArchive(i))
# for i in range(0, len(editions)):
