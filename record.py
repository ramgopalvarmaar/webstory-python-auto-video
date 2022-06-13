import requests
from bs4 import BeautifulSoup
from pprint import pprint
import urllib
from moviepy.editor import *

my_data = []

pagecounter = 0
index = 0
while index < 1:
  data = requests.get("https://googlesguide.com/web-stories/page/"+str(pagecounter))  
  html = BeautifulSoup(data.text, 'html.parser')
  articles = html.select('article')

  for article in articles[:1]:
    #print(article)
    webstory = article.find('h2', {"class" : "entry-title"})
    webstorylink = webstory.find('a', href=True)
    link = webstorylink['href']
    pprint(link)

    storydata = requests.get(link)
    storyhtml = BeautifulSoup(storydata.text, 'html.parser')
    story = storyhtml.find('amp-story')
    storytexts = story.find_all('p', {"class" : "text-wrapper"})
    storyimages = story.find_all('amp-img')
    storycounter = 0

    texts = []
    for storytext in storytexts:
      text = str(storytext.find('span').text)
      #print(text)
      texts.append(text)

    
    clips = []
    for index, storyimage in enumerate(storyimages):
      imageurl=storyimage['src']
      print(texts[index])
      image_clip = ImageClip(imageurl).set_duration(2)

      text_clip = TextClip(txt=texts[index].upper(),
                     size=(.8*image_clip.size[0], 0),
                     font="Lane",
                     color="black").set_position('center').set_duration(2)

      im_width, im_height = text_clip.size
      color_clip = ColorClip(size=(int(im_width*1.1), int(im_height*1.4)),
                       color=(0, 255, 255))
      color_clip = color_clip.set_opacity(.6).set_duration(2)

      clip_to_overlay = CompositeVideoClip([color_clip, text_clip]).set_position('center').set_duration(2)

      final_clip = CompositeVideoClip([image_clip, clip_to_overlay]).set_duration(2)

      clips.append(final_clip)

    print(clips)
    storycounter = storycounter + 1

    video = CompositeVideoClip(clips, size=(720,460))
    video.write_videofile('test'+str(storycounter)+'.mp4', fps=24)

  index += 1

#/html/body/amp-story/amp-story-page[1]/amp-story-grid-layer[2]/div/div/div[2]/div/p