import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time
import random
# http://shaurong.blogspot.com/2017/03/useragent.html
# user agent的索引

def getSrc(figu):
    wid = figu.index("width=")+7
    tmpWid = figu[wid:]
    tmp = tmpWid.index("\"")
    tmpWid = tmpWid[:tmp]
    tmp = figu.index("src=")+5
    tmpFigu = figu[tmp:]
    tmp = tmpFigu.index("max/")+4
    tmpNext = tmpFigu[tmp:]
    tmpFigu = tmpFigu[:tmp]
    tmpL = tmpNext.index("/")
    tmpR = tmpNext.index("\"")
    tmpNext = tmpNext[tmpL:tmpR]
    return tmpFigu + tmpWid + tmpNext

def checkHref(tmpHref):
    if(tmpHref.startswith("/")):
        return "https://medium.com" + tmpHref
    return tmpHref
def getHref(aHref):
    tmp = aHref.index("href=")+6
    tmpHref = aHref[tmp:]
    tmp = tmpHref.index("\"")
    tmpHref = tmpHref[:tmp]
    return tmpHref
def construct(orin,tmpHref):
    tmp = orin.index("href=")+6
    tmpOrin = orin[tmp:]
    tmpR = tmpOrin.index("\"")
    return orin[:tmp] + tmpHref + orin[tmpR:]
def littleConstruct(orin,tmpHref):
    tmp = orin.index("href=")+6
    tmpOrin = orin[tmp:]
    tmpL = tmpOrin.index(">")+1
    tmpOrin = tmpOrin[tmpL:]
    tmpR = tmpOrin.index("<")
    tmpWord = tmpOrin[:tmpR]
    link = "<a href=\"" + tmpHref + "\" data-type=\"URL\" data-id=\"" + tmpHref + "\" target=\"_blank\" rel=\"noreferrer noopener\">"
    return link + tmpWord
def find(tmpArticle, tmpWord , tmpEnd):
    tmpNum = 0
    tmpR = 0
    if(tmpWord in tmpArticle):
        while(tmpWord in tmpArticle and tmpArticle.index(tmpEnd) > tmpArticle.index(tmpWord)):
            tmpL = tmpArticle.index(tmpWord)
            tmpArticle = tmpArticle[:tmpL] + tmpArticle[tmpL+len(tmpWord):]
            tmpNum = tmpNum + len(tmpWord)
            tmpR = find(tmpArticle , tmpWord , tmpEnd)
            tmpArticle = tmpArticle[:tmpR - len(tmpEnd)] + tmpArticle[tmpR:]
            tmpNum = tmpNum + len(tmpEnd)
    else:
        tmpR = tmpArticle.index(tmpEnd)
    return tmpArticle.index(tmpEnd) + len(tmpEnd) + tmpNum


def sta(url,name,n,nickname):
    res = requests.get(url).text
    # 抓文章段落
    tmp = res.index("<article>")+9
    article = res[tmp:]
    tmp = article.index("</article>")
    article = article[:tmp]
    while('id="' in article):
        tmp = article.index('id="')
        tmpArticle = article[tmp+4:]
        tmp1 = tmpArticle.index('"')
        article = article[:tmp-1] + tmpArticle[tmp1 + 1:]
    while('class="' in article):
        tmp = article.index('class="')
        tmpArticle = article[tmp+7:]
        tmp1 = tmpArticle.index('"')
        article = article[:tmp-1] + tmpArticle[tmp1 + 1:]
    content = []

    while(len(article) > 0):
        tmpL = article.index('<')
        tmpR = article.index('>')
        if(" " in article):
            tmpCheck = article.index(' ')
        else:
            tmpCheck = tmpR + 1
        tmpWord = article[tmpL:tmpR+1]
        if(tmpL > 0):
            article = article[tmpL:]
            continue
        if(tmpWord.startswith("<!--")):
            article = article[len(tmpWord)+1:]
            continue
        if(article.startswith("<noscript>")):
            tmp = article.index("</noscript>") + len("</noscript>")
            article = article[tmp:]
            continue
        if(article.startswith("<img")):
            if("src" in article[tmpL:tmpR-1]):
                content.append(article[tmpL:tmpR-1]+">")
            article = article[tmpR+1:]
            continue

        if(tmpR > tmpCheck):
            tmpEnd = tmpWord[0] + "/" + tmpWord[1:tmpCheck] + ">"
        else:
            tmpEnd = tmpWord[0] + "/" + tmpWord[1:]
        tmpArticle = article[tmpL + len(tmpWord):]
        tmpR = find(tmpArticle , tmpWord , tmpEnd ) + len(tmpWord)
        if(article.startswith("<a ") or article.startswith("<h1") or article.startswith("<h2") or article.startswith("<figcaption") or article.startswith("<p") or article.startswith("<ol") or article.startswith("<ul") or article.startswith("<pre") or article.startswith("<blockquote")):
            content.append(article[tmpL:tmpR])
            article = article[tmpR:]
        else:
            article = article[tmpL + len(tmpWord):tmpR - len(tmpEnd)] + article[tmpR:]
    index = 0
    title ="None"
    for i in range(len(content)):
        if(content[i].startswith("<h1")):
            tmp = content[i].index(">")
            title = content[i][tmp+1:]
            print(title)
            tmp = title.index("<")
            title = title[:tmp]
            break
    wordPress = ["" for i in range(len(content))]
    filea.write("<item>\n<title><![CDATA["+title+"]]></title>\n<link>"+url+"</link>\n<pubDate>Mon, 15 Mar 2021 03:24:43 +0000</pubDate>\n<dc:creator><![CDATA["+name+"]]></dc:creator>\n<description></description>\n<content:encoded><![CDATA[")
    


    for i in range(len(content)):
        if("<a " in content[i]):
            tmpHref = getHref(content[i])
            tmpHref = checkHref(tmpHref)
            tmp = content[i].index("<a ")
            tmpA = content[i][:tmp]
            tmpB = content[i][tmp+3:]
            tmp = tmpB.index("</a>")
            tmpB = tmpB[tmp:]
            content[i] = tmpA + littleConstruct(content[i],tmpHref) + tmpB
        if(content[i].startswith("<h1>")):
            wordPress[i] = "\n<!-- wp:heading \textAlign\":\"center\",\"level\":1} -->\n"+content[i]+"\n<!-- /wp:heading -->\n"
        if(content[i].startswith("<h2>")):
            wordPress[i] = "\n<!-- wp:heading -->\n"+content[i]+"\n<!-- /wp:heading -->\n"
        if(content[i].startswith("<a target=\"_blank\"")):
            tmpHref = getHref(content[i])
            tmpHref = checkHref(tmpHref)
            content[i] = construct(content[i],tmpHref)
            wordPress[i] = "\n<!-- wp:html -->\n<div style=\"border-style:solid;border-width:1px;\">"+content[i]+"\n</div>\n<!-- /wp:html -->\n"
        if(content[i].startswith("<img")):
            src = getSrc(content[i])
            if(content[i+1].startswith("<figcaption>")):
                wordPress[i] = "\n<!-- wp:image {\"sizeSlug\":\"large\"} -->\n<figure class=\"wp-block-image size-large\"><img src=\""+src+"\" alt=\"\"/>"+content[i+1]+"</figure>\n<!-- /wp:image -->\n"
            else:
                wordPress[i] = "\n<!-- wp:image {\"sizeSlug\":\"large\"} -->\n<figure class=\"wp-block-image size-large\"><img src=\""+src+"\" alt=\"\"/></figure>\n<!-- /wp:image -->\n"
        if(content[i].startswith("<p>")):
            wordPress[i] = "\n<!-- wp:paragraph {\"align\":\"center\"} -->\n"+content[i]+"\n<!-- /wp:paragraph -->\n"
        if(content[i].startswith("<ul")):
            wordPress[i] = "\n<!-- wp:list -->\n"+content[i]+"\n<!-- /wp:list -->\n"
        if(content[i].startswith("<ol")):
            wordPress[i] = "\n<!-- wp:list -->\n"+content[i]+"\n<!-- /wp:list -->\n"
        if(content[i].startswith("<pre")):
            wordPress[i] = "\n<!-- wp:code -->\n"+content[i]+"\n<!-- /wp:code -->\n"
        if(content[i].startswith("<blockquote")):
            wordPress[i] = "\n<!-- wp:quote -->\n"+content[i]+"\n<!-- /wp:quote -->\n"

    wordPress[-1] = wordPress[-1][:-1]
    for i in wordPress:
        i = i.replace("<h1>","<h1 class=\"has-text-align-center\">")
        i = i.replace("<href=\"/","<href=\"medium.com/")
        i = i.replace("<p>","<p style=\"text-align: left;\">")
        i = i.replace("<blockquote>","<blockquote class=\"wp-block-quote\">")
        i = i.replace("<pre>","<pre class=\"wp-block-code\"><code>")
        i = i.replace("</pre>","</code></pre>")
        filea.write(i)
    t = time.localtime()
    filea.write("]]></content:encoded>\n<excerpt:encoded><![CDATA[]]></excerpt:encoded>\n<wp:post_id>"+str(n)+"</wp:post_id>\n<wp:post_date><![CDATA[2021-03-15 11:24:43]]></wp:post_date>\n<wp:post_date_gmt><![CDATA[2021-03-15 03:24:43]]></wp:post_date_gmt>\n<wp:post_modified><![CDATA[2021-06-24 05:47:34]]></wp:post_modified>\n<wp:post_modified_gmt><![CDATA[2021-06-23 21:47:34]]></wp:post_modified_gmt>\n<wp:comment_status><![CDATA[open]]></wp:comment_status>\n<wp:ping_status><![CDATA[open]]></wp:ping_status>\n<wp:post_name><![CDATA["+title+"]]></wp:post_name>\n<wp:status><![CDATA[publish]]></wp:status>\n<wp:post_parent>0</wp:post_parent>\n<wp:menu_order>0</wp:menu_order>\n<wp:post_type><![CDATA[post]]></wp:post_type>\n<wp:post_password><![CDATA[]]></wp:post_password>\n<wp:is_sticky>0</wp:is_sticky>\n<category domain=\"category\" nicename=\"uncategorized\">")


def GET_UA():
    user_agent_strings =["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                         "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)",\
                         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.6 OPR/38.0.2220.41",\
                         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                         "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                         "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",\
                         "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",\
                         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"\
                        ]
    return random.choice(user_agent_strings)

def GET_url(res,name):  # 抓取每個文章的連結
    headers = {"User-Agent": GET_UA()}
    #res = requests.get(url).text
    soup = bs(res,'html.parser')
    all_content = soup.select("section h1 a")
    newurl = []
    for i in all_content:     # 呼叫判斷網址 (抓到的文章連結) 需不需要加"https://<name>.medium.com"
        if checkurl(i.get("href")):
            newurl.append("https://"+name+".medium.com"+i.get("href"))
        else :
            newurl.append(i.get("href"))
    return newurl


def checkurl(href_web):  # 判斷網址
    if ("https" in href_web):  # 判斷爬到的 url 有沒有出現過"https://medium.com"
        return False
    return True
def checkinput(href_input):  # 判斷輸入的網址
    if ("@" in href_input):  # 判斷輸入的 url 是哪一種
        return False
    return True
def start(url,nickname):
    # https://bluet.medium.com/
    if checkinput(url):
        name = url.replace('https://','').replace('.medium.com/','')
    else:
        name = url.replace('https://medium.com/@','')
    # driver不去自動開啟瀏覽器
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent={}".format(GET_UA()))
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),options=chrome_options)
    driver.get(url) #  here the adress of page
    # 透過 xpath 找到 button("show more") 的位置
    try : # check whether i need to click the button or not
        result = driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div/div[2]/div/div[10]/div[1]/button").is_displayed()
        div_place = '10'  # the number in the div of button
        # 判斷還能不能按按鈕( show more )
        while result == True:
            driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div/div[2]/div/div["+div_place+"]/div[1]/button").click()
            time.sleep(1)
            # 點 show more 之後，要再拉到底(拖曳到底部)
            div_place = int(div_place)
            div_place += 10  # the number in the div of button plus 10 to turn into the next button
            div_place = str(div_place)
            try :   # check whether the button exists
                result = driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div/div[2]/div/div["+div_place+"]/div[1]/button").is_displayed()
            except:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(1)
                result = False
    except:
        pass
    global filea
    filea = open("download/wordPress.xml","w+",encoding="utf8")
    filea.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<rss version=\"2.0\"\nxmlns:excerpt=\"http://wordpress.org/export/1.2/excerpt/\"\nxmlns:content=\"http://purl.org/rss/1.0/modules/content/\"\nxmlns:wfw=\"http://wellformedweb.org/CommentAPI/\"\nxmlns:dc=\"http://purl.org/dc/elements/1.1/\"\nxmlns:wp=\"http://wordpress.org/export/1.2/\"\n>\n<channel>\n<title>"+nickname+"</title>\n<link>http://localhost/wordpress</link>\n<description>全新的繁體中文 WordPress 網站</description>\n<pubDate>Wed, 23 Jun 2021 23:47:15 +0000</pubDate>\n<language>zh-TW</language>\n<wp:wxr_version>1.2</wp:wxr_version>\n<wp:base_site_url>http://localhost/wordpress</wp:base_site_url>\n<wp:base_blog_url>http://localhost/wordpress</wp:base_blog_url>\n<wp:author><wp:author_id>1</wp:author_id><wp:author_login><![CDATA[penglairenou]]></wp:author_login><wp:author_email><![CDATA[p120478230@gmail.com]]></wp:author_email><wp:author_display_name><![CDATA[penglairenou]]></wp:author_display_name><wp:author_first_name><![CDATA[]]></wp:author_first_name><wp:author_last_name><![CDATA[]]></wp:author_last_name></wp:author>\n<generator>https://wordpress.org/?v=5.7.2</generator>\n")
    
    postlist = []   # 裝所有post過的文章的url
    postlist = GET_url(driver.page_source,name)
    n = 0
    for i in postlist:
        n = n + 1
        tmp = i.index("?source")
        sta(i,name,n,nickname)
        
        filea.write("<![CDATA[未分類]]></category>\n<wp:comment>\n<wp:comment_id>1</wp:comment_id>\n<wp:comment_author><![CDATA[WordPress 示範留言者]]></wp:comment_author>\n<wp:comment_author_email><![CDATA[wapuu@wordpress.example]]></wp:comment_author_email>\n<wp:comment_author_url>https://wordpress.org/</wp:comment_author_url>\n<wp:comment_author_IP><![CDATA[]]></wp:comment_author_IP>\n<wp:comment_date><![CDATA[2021-03-15 11:24:43]]></wp:comment_date>\n<wp:comment_date_gmt><![CDATA[2021-03-15 03:24:43]]></wp:comment_date_gmt>\n<wp:comment_content><![CDATA[網站管理員你好，這是一則預留內容留言。\n如需開始審閱、編輯及刪除留言，請前往 [控制台] 的 [留言] 頁面進行必要的操作。\n留言者個人頭像來源為 <a href=\"https://zh-tw.gravatar.com\" target=\"_blank\">Gravatar</a>。]]></wp:comment_content>\n<wp:comment_approved><![CDATA[1]]></wp:comment_approved>\n<wp:comment_type><![CDATA[comment]]></wp:comment_type>\n<wp:comment_parent>0</wp:comment_parent>\n<wp:comment_user_id>0</wp:comment_user_id>\n</wp:comment>\n</item>\n")
    filea.write("\n</channel>\n</rss>")


    # 最後結束這個process
    driver.quit() 
# start("https://bluet.medium.com/")

