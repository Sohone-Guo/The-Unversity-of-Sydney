# This code is based on python3.6 (Anaconda3.6) 

import requests
import re

# Conferences List, Database
# core
def Coferences_Cores(page=1,search_content_index=0,search_content=["08","09","10"]):
    while True:
        url = "http://portal.core.edu.au/conf-ranks/?search=%s&by=all&source=CORE2017&sort=atitle&page=%s"%(search_content[search_content_index],str(page))
        get_signal = requests.get(url)
        if "".join(re.findall("\d",str(get_signal))) == "200":
            html = get_signal.text
            
            # Download the content
            content = re.findall(r"<tr (.{1,500}) </tr>"," ".join(html.split()))
            total_number = len(content)
            print("%s searching..., on the page of %s, and this page have %s number of datas."%(search_content[search_content_index],str(page),str(total_number)))
            
            for page_content_tp in range(total_number):
                title = re.findall(r"<td> (.*) </td><td class=",content[page_content_tp])[0].split("</td>")[0]
                try:
                    Acronym,Source,Rank,Changed,FoR,Comments,Average = re.findall(r"<td .{1,20}> (.{1,20}) </td>",content[page_content_tp])
                except Exception as e:
                    Acronym = "None"
                    Source,Rank,Changed,FoR,Comments,Average = re.findall(r"<td .{1,20}> (.{1,20}) </td>",content[page_content_tp])
            page+=1
        else:
            if search_content[search_content_index] == search_content[-1]:
                print("end")
                break
            else:
                search_content_index+=1
                page = 1


# Conferences List, Database ---> wikicfp
def Coferences_Wikicfp(page=1):
    while True:
        url = "http://www.wikicfp.com/cfp/call?conference=computer%%20science&skip=%d"%page
        get_signal = requests.get(url)
        if "".join(re.findall("\d",str(get_signal))) == "200":
            html = get_signal.text

            url_name = re.findall("<td rowspan=\"2\" align=\"left\"><a href=\"(.*)</a>",html)
            for item in url_name:
                url = "http://www.wikicfp.com"+item.split(">")[0]
                name = item.split(">")[1].split(" ")[0]

                # download dataset
                try:
                    data = requests.get(url).text
                    Short = name
                    Full_name = re.findall("<title>(.*)</title>",data)[0]
                    Submission_Date = re.findall("<span property=\"v:startDate\" content=\".{1,25}>(.*)</span>",data)[-3]
                    Notification_time = re.findall("<span property=\"v:startDate\" content=\".{1,25}>(.*)</span>",data)[-2]
                    Conference_Start_Date = re.findall("<span property=\"v:startDate\" content=\".{1,25}>(.*)</span>",data)[-1]
                    Location = re.findall("th>Where</th>\n                <td align=\"center\">(.{1,50})</td>",data,re.MULTILINE|re.DOTALL)[0]
                    Description = re.findall("<meta name=\"description\" content=\"(.{1,150})\">",data,re.MULTILINE|re.DOTALL)[0]
                    Website = re.findall("Link: <a href=\"(.{1,100})\" target=",data,re.MULTILINE|re.DOTALL)[0]
                    Viewed_number = re.findall("posted by .{1,20}: <a href=\".{1,100}</a>(.{1,2000})</table>",data,re.MULTILINE|re.DOTALL)[0].split("||")[1]
                    Tracked = re.findall("posted by .{1,20}: <a href=\".{1,100}</a>(.{1,2000})</table>",data,re.MULTILINE|re.DOTALL)[0].split("||")[2].split("users")[0]
                    Attended = re.findall("<a href=.{1,100}>(.{1,20})</a>",re.findall("posted by .{1,20}: <a href=\".{1,100}</a>(.{1,2000})</table>",data,re.MULTILINE|re.DOTALL)[0].split("||")[2])[:-1]
                except Exception as e:
                    print(e)
            page+=1
        else:
            break

# Journal  List, Database ---> core

def Journal_core(page=1,search_content_index=0,search_content = ["08","09","10"]):

    while True:
        url = "http://portal.core.edu.au/jnl-ranks/?search=%s&by=all&source=CORE2017&sort=atitle&page=%s"%(search_content[search_content_index],str(page))
        get_signal = requests.get(url)
        if "".join(re.findall("\d",str(get_signal))) == "200":
            html = get_signal.text
            
            # Download the content
            content = re.findall(r"<tr (.{1,500}) </tr>"," ".join(html.split()))
            total_number = len(content)
            print("%s searching..., on the page of %s, and this page have %s number of datas."%(search_content[search_content_index],str(page),str(total_number)))
            
            for page_content_tp in range(total_number):
                title = re.findall(r"<td> (.*) </td><td class=",content[page_content_tp])[0].split("</td>")[0]
                try:
                    Acronym,Source,Rank,Changed,FoR,Comments,Average = re.findall(r"<td .{1,20}> (.{1,20}) </td>",content[page_content_tp])
                except Exception as e:
                    try:
                        Acronym = "None"
                        Source,Rank,Changed,FoR,Comments,Average = re.findall(r"<td .{1,20}> (.{1,20}) </td>",content[page_content_tp])
                    except Exception as e:
                        print(re.findall(r"<td .{1,20}> (.{1,20}) </td>",content[page_content_tp]))
            page+=1
        else:
            if search_content[search_content_index] == search_content[-1]:
                print("end")
                break
            else:
                search_content_index+=1
                page = 1


