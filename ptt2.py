
# coding: utf-8

# In[50]:

from bs4 import BeautifulSoup
import requests
import re
import datetime


# In[51]:

# 輸入url，回傳post字典檔案

def GetPost(url):
    if "Gossiping" in url:
        res = requests.get(url, cookies={'over18': '1'}, verify=True)
    else:
        res = requests.get(url)

    soap = BeautifulSoup(res.text, "html5lib")

    id_regex = re.compile(r'(\w+)')

    post_dict = {}

    # post meta-data

    meta_values = soap.select('.article-meta-value')

    try:
        post_dict['post_id'] = id_regex.match(meta_values[0].string).group(0)
        post_dict['post_board'] = meta_values[1].string
        post_dict['post_title'] = meta_values[2].string
        post_dict['post_time'] = datetime.datetime.strptime(meta_values[3].string, "%a %b %d %H:%M:%S %Y")

        post_dict['post_link'] = url
    except:
        print("no meta data ", url)
        return 111

    # push
    push_list = []

    push_values = soap.select(".push")

    for push in push_values:
        try:
            push_dict = {}
            push_dict['push_tag'] = push.select('.push-tag')[0].string
            push_dict['push_id'] = push.select('.push-userid')[0].string
            push_dict['push_content'] = push.select('.push-content')[0].string
            date_string = str(post_dict['post_time'].year)+"/ "+push.select('.push-ipdatetime')[0].string
            push_dict['push_ipdatetime'] = datetime.datetime.strptime(date_string, "%Y/ %m/%d  %H:%M\n")
            push_list.append(push_dict)
        except:
            pass

    post_dict['push_list'] = push_list

    return post_dict


# In[52]:

# 輸入頁面url，取得該頁面之所有文章連結以及上一頁連結
def GetPostLink(url):

    if "Gossiping" in url:
        res = requests.get(url, cookies={'over18': '1'}, verify=True)
    else:
        res = requests.get(url)

    soap = BeautifulSoup(res.text, "html5lib")
    r_ents = soap.select('.r-ent')
    links = []
    for r_ent in r_ents:
        if "-" != r_ent.select(".author")[0].text:
            try:
                links.append("https://www.ptt.cc"+r_ent.a['href'])
            except:
                print("unable to add post link "+url)
    pre = "https://www.ptt.cc"+soap.select('a.btn.wide')[1]['href']
    return links, pre


# In[53]:

def SaveToSQL(post_dict):
    return 0

def TestNew(post_dict):
    return 0

