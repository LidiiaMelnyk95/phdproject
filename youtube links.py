import urllib.request
import re

search_keyword="transsexueller+gesetz", "transgesetz", 'Transsexuellengesetz', \
               'transsexuellengesetz', "TSG+Gesetz", 'Selbstbestimmungsgesetz',\
               'transsexuellenrehct', 'reform+transsexuellengesetz', 'transsexuellengesetz+2021',\
             'transsexuellengesetz+2020', 'Neuregelung+des+Transsexuellengesetzes','trans-gesetz',\
               'reform+des+transgesetzes', 'neuer+transgesetz', 'das+Transsexuellengesetz',\
               'debatte+transsexuellengesetz', 'trans-recht+gesetz-entwurf', 'entwurf+transgesetz'
#search_keywords = 'homosexuelle+segnen', 'schwule+segnen', 'segen+homosexuelle'
links_array =  []
for i in search_keyword:
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + i)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    for i in video_ids:
        links_array.append("https://www.youtube.com/watch?v=" + i)


print(len(set(links_array)))
sorted_links = str(set(links_array)).replace(',','\n')
sorted_links = sorted_links.replace("'", '')
with open('/Users/lidiiamelnyk/Documents/links_LGBTQ_church.txt', 'w+', encoding= 'utf-8-sig') as myfile:
    myfile.write(sorted_links)