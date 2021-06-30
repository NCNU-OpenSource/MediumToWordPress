# 把 Medium 弄成 WordPress 的形狀


## Concept Development
- 想要從一個類似部落格的地方，將自己全部的文章內容轉移到另一個自架網站上
- 嘗試從 Medium 轉移到 Wordpress
- 將 Medium 的所有文章轉成 Wordpress 格式，並匯入 Wordpress 進行架設
## Implementation Resources
- python 3
- python standard library：
    - bs4
    - selenium
    - selenium.webdriver.chrome.options
    - webdriver_manager.chrome
    - webdriver_manager.utils
    - time
    - random
    - flask
## Existing Library/Software
曾經[有人做過](https://medium.com/rar-design/%E5%B0%8F%E5%AD%A9%E5%AD%90%E6%89%8D%E8%A6%81%E5%81%9A%E9%81%B8%E6%93%87-%E5%BE%9E-medium-%E6%90%AC%E5%AE%B6%E5%88%B0-wordpress-%E7%B6%B2%E7%AB%99%E5%BE%9E%E4%BB%8A%E4%BB%A5%E5%BE%8C%E6%96%87%E7%AB%A0%E5%90%8C%E6%AD%A5%E7%99%BC-7dcfbb61fd9c)，可惜因為改版不能用了。


## Implementation Process
-  爬蟲前先設定一個 User Agent
```python=
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
```
:::info
**User Agent 介紹**

http://shaurong.blogspot.com/2017/03/useragent.html
:::
-  從輸入抓作者的名字
```python=
url = input()
if checkinput(url):
    name = url.replace('https://','').replace('.medium.com/','')
else:
    name = url.replace('https://medium.com/@','') # 把作者名字篩出來
# 輸入的格式有兩種:
# "https://" + name + ".medium.com/"
# "https://medium.com/@" + name
```
:::danger
爬 url 之前，需要先看看能不能按 "show more" 按鈕，因為網頁限制一次呈現的文章 ( 也就是直接爬蟲 ) 能爬到的最大數量是 10 篇
:::
- 使用 selenium 以確認能不能按按鈕
    - 用 selenium 開啟瀏覽器
    - 使用 headless 的方式來開啟瀏覽器以避免佔用 CPU 效能
    - 設定 User Agent
    - 確認一下 chrome 的版本，並且會去下載相對應的 chrome driver
    - 爬蟲
    - 確認看看有沒有按鈕能按
    - 分兩種狀況
        - 沒按鈕: 文章數小於 10
        - 有按鈕: 文章數大於 10
    - 按照各種情況去按按鈕
```python=
chrome_options = Options()
# 以不開啟瀏覽器的方式來使用 Chrome Selenium 爬蟲
chrome_options.add_argument("--headless")
# 設定 User Agent
chrome_options.add_argument("user-agent={}".format(GET_UA()))
driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),options=chrome_options)
driver.get(url)

try : # check whether i need to click the button or not
    result = driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div/div[2]/div/div[10]/div[1]/button").is_displayed()
    div_place = '10'  # the number in the div of button
    # 判斷還能不能按按鈕( show more )
    while result == True:
        driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div/div[2]/div/div["+div_place+"]/div[1]/button").click()
        time.sleep(1)
        div_place = int(div_place)
        div_place += 10  # the number in the div of button plus 10 to turn into the next button
        div_place = str(div_place)
        try :   # check whether the button exists
            result = driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div/div[2]/div/div["+div_place+"]/div[1]/button").is_displayed()
        except:
            # 點完 show more 之後，要再拉到底(拖曳到底部)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
            result = False
    except:
        # 全部處理完就能去爬這個網頁所有文章的 url
        pass
```
-  爬作者 po 過的文章的 url
```python=
def GET_url(res,name):  # 抓取每個文章的連結
    soup = bs(res,'html.parser')
    all_content = soup.select("section h1 a")
    newurl = []
    for i in all_content:     # 呼叫判斷網址 (抓到的文章連結) 需不需要加"https://<name>.medium.com"
        if checkurl(i.get("href")):
            newurl.append("https://"+name+".medium.com"+i.get("href"))
        else :
            newurl.append(i.get("href"))
    return newurl
def checkurl(href_web):  # 判斷爬到的網址
    if ("https" in href_web):  # 判斷爬到的 url 有沒有出現過"https://medium.com"
        return False
    return True

postlist = []   # 裝所有post過的文章的url
postlist = GET_url(driver.page_source,name)
```
-  從文章的 url 爬取文章內容
```python=
def GET_article(urllist):  # 抓取每篇文章
    # 設定 User Agent
    headers = {"User-Agent": GET_UA()}
    newlist = [] # 裝所有文章的 list
    for i in range(len(urllist)):
        res = requests.get(urllist[i]).text
        soup = bs(res,'html.parser')
        all_content = soup.select("section")
        newlist.append(all_content)
    return newlist

# 將所有爬到的文章列印出來
for x in range(len(articlelist)):
    for i in articlelist[x]:
        print(i.text)

# 最後結束這個process
driver.quit() 
```
## 遇到的問題
### Q1: 受到網頁限制的影響，每次只能爬 10 篇文章
#### 解決方法 1
- 發現網頁可以轉成 json 去查看，因此嘗試去爬看看這份 json 檔...
- 先將圈起來的部分改成想要爬的作者名稱
![](https://i.imgur.com/DPfCXIS.png)

- 丟進去 json [分析結構的網頁](https://jsonformatter.curiousconcept.com/#)，看一下它的結構
![](https://i.imgur.com/yHVmA3O.png)
![](https://i.imgur.com/cbGXAu1.png)

- 發現文章的 url 都放在 streamItems 裡的 postId
![](https://i.imgur.com/TTCmvWE.png)

- 回去看看本來的那份 json 資料，發現能用的 postId 只有 3 個 
( 其他的搜尋結果都是空值 )
![](https://i.imgur.com/yrL312W.png)
![](https://i.imgur.com/Zv5beDg.png)

- **放棄爬 json 檔**
#### 解決方法 2
- 用 selenium 去爬，並且每次爬之前都會不停的確認 "show more" 還能不能按，等到全部按到底之後，才去爬作者所有文章的 url
### Q2: 抓不到按鈕的 id
- 因為按鈕沒有 id ，且因為它的 css 是用 functional CSS ，所以不知道怎麼抓到按鈕的位置
- 在求助姊姊之後，發現可以去抓它的 Xpath
![](https://i.imgur.com/km26YGF.png)
### Q3: 按鈕按下去之後，還是抓不到新的資料？
- 在按完按鈕之後，需要將網頁拖曳到底部，並且等待一點時間讓網頁仔入，因此要加上：
```python=
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')`
time.sleep(1)
```
### Q4: 按鈕每按一次，它的 Xpath 都會改變，直接將 Xpath 寫死會導致只能抓到第一次出現的按鈕
- 觀察規律發現按鈕每出現一次，其中 div 裡面的值會加 10 
- 因此寫個變數來進行運算
- 每次運算完都要將這個變數轉回 string 再放進去它的 Xpath 裡
```python=
div_place = '10'  # 第一次的按鈕

div_place = int(div_place)
div_place += 10  # the number in the div of button plus 10 to turn into the next button
div_place = str(div_place)
```
:::info
[邪魔歪道還是苦口良藥？Functional CSS 經驗分享](https://blog.techbridge.cc/2019/01/26/functional-css/)
:::

## Installation

- `pip install requests`
- `pip install bs4`
- `pip install selenium`
- `pip install webdriver-manager`
## Usage

1. ![](https://i.imgur.com/BFqwc8z.png)
    輸入你的 medium 網址與你自己的暱稱 ( 暱稱拜託避免中文
2. 等他
3. ![](https://i.imgur.com/45FH38P.png)
    下載
4. 開啟 wordPress
5. ![](https://i.imgur.com/IK8fh07.png)
6. ![](https://i.imgur.com/5pC0tHy.png)
7. ![](https://i.imgur.com/kTWnWTT.png)
    在這個頁面匯入
8. ![](https://i.imgur.com/oAtUe2f.png)
    選一個人當作者
9. ![](https://i.imgur.com/kjAxM1G.png)
    成功
## Job Assignment

![](https://i.imgur.com/FNpBS9b.png)
陳柏瑋 45% 轉換
歐哲安 45% 爬蟲
BlueT 10% (建議分)
## References

- [期末 project 的架構](https://github.com/NCNU-OpenSource/final-project-readme-template/tree/master/template)
- [網路爬蟲 Day3 - html 檔的取得及常見問題(續)](https://ithelp.ithome.com.tw/articles/10191165)
- [Medium 爬蟲進化史](https://blog.huli.tw/2019/07/12/medium-crawler/)
- [使用 Chrome headless 教學](http://python-learnnotebook.blogspot.com/2018/10/chrome-headless.html)
- [webdriver-manager 套件](https://pypi.org/project/webdriver-manager/)
- [selenium 套件](https://pypi.org/project/selenium/)
- [selenium 基礎用法](https://tw511.com/a/01/7542.html)
- [selenium 基礎用法 2 ](https://www.itread01.com/content/1548241045.html)
:::info
無頭騎士
![](https://i.imgur.com/3xtD7K8.png)
:::
## Thanks
[lulala88](https://github.com/lulala88)
