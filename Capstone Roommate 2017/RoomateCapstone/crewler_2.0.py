
# New version -> boost the method regular expression

# Anaconda3.6/python3
# Libraries are requests and re

# Connection of url
import requests

# regular expression
import re

# Function of CoferrencesList 
def CoferencesList_Core(page=1,search_content_index=0,search_content=["08","09","10"]):
    # Declare a dictionary for save the result {Acronym:[Title,Source,Rank,Changed,FoR,Comments,Average,"08|09|10"]}
    result = {}
    
    # Start to download each data from the url
    while True:

        url = "http://portal.core.edu.au/conf-ranks/?search=%s&by=all&source=CORE2017&sort=atitle&page=%s"%(search_content[search_content_index],str(page))
        get_signal = requests.get(url)

        # if not "200", the web page is not exit.
        if "".join(re.findall("\d",str(get_signal))) == "200":

            # Got the content of url
            html = get_signal.text
            
            # Download the content
            content = re.findall(r"<tr (.{1,500}) </tr>"," ".join(html.split()))
            total_number = len(content)
            print("Working on the core data collection, year in %s searching..., on the page of %s, and this page have %s number of datas."%(search_content[search_content_index],str(page),str(total_number)))
            
            # collect the detail
            for page_content_tp in range(total_number):
                Title,Acronym,Source,Rank,Changed,FoR,Comments,Average = re.findall(r"<td> (.*) </td><td .*> (.*)</td><td .*>(.*)</td><td .*>(.*)</td><td .*>(.*) </td><td .*>(.*) </td><td .*>(.*) </td><td .*>(.*) </td>",content[page_content_tp])[0]
                
                # Newest as the one
                if Acronym not in result:
                    result[Acronym] = [Title,Source,Rank,Changed,FoR,Comments,Average,search_content[search_content_index]]
            page+=1
        else:
            # change to anthor years to search if not end.
            if search_content[search_content_index] == search_content[-1]:
                print("---------------------------------------------------------------------------------")
                print("End of the core data collection.\n")
                return result
            else:
                search_content_index+=1
                page = 1

# Download the wikicfp
def ConferencesList_Wikicfp(page=1,end_page = 100):
    # declare a dictionary
    result = {}

    # begin to download
    while True:
        url = "http://www.wikicfp.com/cfp/call?conference=computer%%20science&page=%d"%page
        get_signal = requests.get(url)

        # if the url is right
        if "".join(re.findall("\d",str(get_signal))) == "200" and page <= end_page:
            print("Working on wificfp data collection, start to download the data from page of %d....(the page download will end page of %d)"%(page,end_page))
            html = get_signal.text

            # all the url in the page
            url_name = re.findall("<td rowspan=\"2\" align=\"left\"><a href=\"(.*)</a>",html)

            # check the child of each url, and collect the detail information
            for item in url_name:
                url = "http://www.wikicfp.com"+item.split("\">")[0]
                
                # the content of the child of url 
                data = requests.get(url).text
                
                # information of name
                Short = item.split(">")[1].split(" ")[0]
                Full_name = re.findall("<title>(.*)</title>",data)[0]
                
                # information of time
                all_time = re.findall("<span property=\"v:startDate\" content=\".{1,25}>(.*)</span>",data)
                if len(all_time) >= 2:
                    Submission_Date = all_time[1]
                else:
                    Submission_Date = None
                
                if len(all_time) >= 3:
                    Notification_time = all_time[2]
                else:
                    Notification_time = None
                
                if len(all_time) >= 4:
                    Conference_Start_Date = all_time[3]
                else:
                    Conference_Start_Date = None
                
                # information of location
                try:
                    Location = re.findall("th>Where</th>\n                <td align=\"center\">(.{1,50})</td>",data,re.MULTILINE|re.DOTALL)[0]
                except:
                    Location = None
                
                # information of descrition
                try:
                    Description = re.findall("<meta name=\"description\" content=\"(.{1,100})\">",data,re.MULTILINE|re.DOTALL)[0]
                except:
                    Description = None
                
                # information of wesite
                try:
                    Website = re.findall("Link: <a href=\"(.{1,100})\" target=",data,re.MULTILINE|re.DOTALL)[0]
                except:
                    Website = None

                # information of viewed, 
                try:
                    Viewed_number = re.findall("posted by .{1,20}: <a href=\".{1,100}</a>(.{1,2000})</table>",data,re.MULTILINE|re.DOTALL)[0].split("||")[1]
                    Tracked = re.findall("posted by .{1,20}: <a href=\".{1,100}</a>(.{1,2000})</table>",data,re.MULTILINE|re.DOTALL)[0].split("||")[2].split("users")[0]
                    Attended = re.findall("<a href=.{1,100}>(.{1,20})</a>",re.findall("posted by .{1,20}: <a href=\".{1,100}</a>(.{1,2000})</table>",data,re.MULTILINE|re.DOTALL)[0].split("||")[2])[:-1]
                    
                    if Short not in result:
                        result[Short] = [Full_name,Submission_Date,Notification_time,Conference_Start_Date,Location,Description,Website,Viewed_number,Tracked,Attended]
                except:
                    pass

            page+=1
        else:
            # return the dictionary
            print("---------------------------------------------------------------")
            print("End of collected data from wikicfp")
            return result

            break

# Journal  List, Database ---> core
def JournalList_Core(page=1,search_content_index=0,search_content=["08","09","10"]):
    # Declare a dictionary for save the result {Acronym:[Title,Source,Rank,Changed,FoR,Comments,Average,"08|09|10"]}
    result = {}
    
    # Start to download each data from the url
    while True:

        url = "http://portal.core.edu.au/jnl-ranks/?search=%s&by=all&source=CORE2017&sort=atitle&page=%s"%(search_content[search_content_index],str(page))
        get_signal = requests.get(url)

        # if not "200", the web page is not exit.
        if "".join(re.findall("\d",str(get_signal))) == "200":

            # Got the content of url
            html = get_signal.text
            
            # Download the content
            content = re.findall(r"<tr (.{1,500}) </tr>"," ".join(html.split()))
            total_number = len(content)
            print("Working on the core data collection, year in %s searching..., on the page of %s, and this page have %s number of datas."%(search_content[search_content_index],str(page),str(total_number)))
            
            # collect the detail
            for page_content_tp in range(total_number):

                Title,Source,Rank,Changed,FoR,Comments,Average = re.findall(r"<td> (.*) </td><td .*>(.*)</td><td .*>(.*)</td><td .*>(.*) </td><td .*>(.*) </td><td .*>(.*) </td><td .*>(.*) </td>",content[page_content_tp])[0]
                
                # Newest as the one
                if Title not in result:
                    result[Title] = [Source,Rank,Changed,FoR,Comments,Average,search_content[search_content_index]]
            page+=1
        else:
            # change to anthor years to search if not end.
            if search_content[search_content_index] == search_content[-1]:
                print("---------------------------------------------------------------------------------")
                print("End of the core data collection.\n")
                return result
            else:
                search_content_index+=1
                page = 1



if __name__ == "__main__":
    # Coferences List -> Core
    # -> {Acronym:[Title,Source,Rank,Changed,FoR,Comments,Average,"08|09|10"]}
    cofference_list_core_result = CoferencesList_Core()
    # for testing
    print(cofference_list_core_result)


    # Coferences List -> wikicfp
    # ->{Short:[Full_name,Submission_Date,Notification_time,Conference_Start_Date,Location,Description,Website,Viewed_number,Tracked,Attended]}
    cofference_list_wikicfp_result = ConferencesList_Wikicfp(end_page=2) 
    print(cofference_list_wikicfp_result)


    # Journal List -> Core
    # -> {Title:[Source,Rank,Changed,FoR,Comments,Average,"08|09|10"]}
    journal_list_core_result = JournalList_Core()
    # for testing
    print(journal_list_core_result)



