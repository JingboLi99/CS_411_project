from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd
import time

def main():
    urls = [
        'https://www.youtube.com/channel/UCg0m_Ah8P_MQbnn77-vYnYw/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/channel/UCg0m_Ah8P_MQbnn77-vYnYw/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/c/ChineseCookingDemystified/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/c/ChineseCookingDemystified/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/channel/UCBJmYv3Vf_tKcQr5_qmayXg/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/channel/UCBJmYv3Vf_tKcQr5_qmayXg/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/c/%E6%BB%87%E8%A5%BF%E5%B0%8F%E5%93%A5dianxixiaoge/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/c/%E6%BB%87%E8%A5%BF%E5%B0%8F%E5%93%A5dianxixiaoge/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/c/MagicIngredients/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/c/MagicIngredients/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/c/sheephoho/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/c/sheephoho/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/channel/UCRIGdUaQnVSIcIGP5w8N8SA/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/channel/UCRIGdUaQnVSIcIGP5w8N8SA/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/channel/UC5PuVQaBn52bdLu2DKVHUgQ/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/channel/UC5PuVQaBn52bdLu2DKVHUgQ/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/channel/UC5kMwlFEuLvKejXRJnh5tFQ/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/channel/UC5kMwlFEuLvKejXRJnh5tFQ/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/channel/UCbCV1RAyKMMgL0UzEH6dBXg/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/channel/UCbCV1RAyKMMgL0UzEH6dBXg/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/channel/UCyBG1_4AXYwOtV2UHOdg09Q/videos?view=0&sort=da',
        'https://www.youtube.com/channel/UCyBG1_4AXYwOtV2UHOdg09Q/videos?view=0&sort=dd',
        'https://www.youtube.com/c/HAPPYWOK/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/c/HAPPYWOK/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/channel/UCNAfaoF_f7pVx90E6yWgHyg/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/channel/UCNAfaoF_f7pVx90E6yWgHyg/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/c/MrHongKitchen%E9%98%BF%E9%B8%BF%E5%8E%A8%E6%88%BF/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/c/MrHongKitchen%E9%98%BF%E9%B8%BF%E5%8E%A8%E6%88%BF/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/channel/UCJUBD1WjRbthEb6F7o5Ltrw/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/channel/UCJUBD1WjRbthEb6F7o5Ltrw/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/user/MsCnck/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/user/MsCnck/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/c/MadeWithLau/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/c/MadeWithLau/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/user/dailycuisine/videos?view=0&sort=da&flow=grid',
        'https://www.youtube.com/user/dailycuisine/videos?view=0&sort=dd&flow=grid',
        'https://www.youtube.com/c/SpiceNPans/videos?view=0&sort=da&flow=grid',   
        'https://www.youtube.com/c/SpiceNPans/videos?view=0&sort=dd&flow=grid'   
    ]
    driver = webdriver.Chrome()

    for url in urls:    
        driver.get('{}'.format(url))
        
        #SCROLL twice (because we can only get 50 results anyways, so do not need to scroll all the way
        # down. Without scroll, we can only get 30)
        scrollCount = 2
        while scrollCount >= 0:
            scroll_height = 2000
            document_height_before = driver.execute_script("return document.documentElement.scrollHeight")
            driver.execute_script(f"window.scrollTo(0, {document_height_before + scroll_height});")
            time.sleep(1.5)
            scrollCount -= 1
            # document_height_after = driver.execute_script("return document.documentElement.scrollHeight")
            # if document_height_after == document_height_before:
            #     break
            
        #END OF SCROLL    
        
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, 'html.parser')
        found = False
        # print('here')
        while not found:
            channel_raw = soup.find('yt-formatted-string', class_="style-scope ytd-channel-name", id="text")
        # print(channel_raw)
            match = re.match(r".*?\>(.*)\<.*", str(channel_raw))
            if not match:
                continue
            channel_name = match.group(1)
            found = True
        # print(channel_name)
        titles = soup.findAll('a', id = 'video-title')
        # views =  soup.findAll('span', class_='style-scope ytd-grid-video-renderer')    
        urls = soup.findAll('a', id = 'video-title')
        thumbnails = soup.findAll('yt-img-shadow', class_="style-scope ytd-thumbnail no-transition")
        videos = [] #blank pandas dataframe
        
        # print('url: ',str('https://www.youtube.com/' + urls[8].get('href')),'\nthumbnail: ', thumbnails[9])
        i = j = 0
        for title in titles[:50]: #print first 50 titles
            # print('Title: {}\tViews: {}\tPublished: {}\tURL: {}'.format(title.text, views[i].text, views[i+1].text, urls[j].get('href')) )
            match = re.match(r".*?src=\"(.*)\".*", str(thumbnails[j+1]))
            tn = match.group(1) if match is not None else 'None'
            # print(tn)
            curr_vid = {
                # 'title': title.text,
                # 'views': views[i].text,
                # 'posted': views[i+1].text,
                'url': str('https://www.youtube.com/' + urls[j].get('href')),
                'thumbnail': tn
            }
            videos.append(curr_vid)
            i += 2
            j += 1
        df = pd.DataFrame(videos)
        print(df)
        df.to_csv('testicles.csv', mode='a', index=False, header=False, encoding='utf_8_sig')
main()