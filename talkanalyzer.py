import re
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import numpy as np
from scipy import stats

class URLconstructor(object):
    def __init__(self, idnumber, df):
        '''
        Takes idnumber (integer) and pandas dataframe
        '''
    def commenturl(idnumber, df):
        """Takes an index number from the dataframe and
        returns a composite URL as a string for a specific comment."""
        baseURL = "https://www.zooniverse.org/"
        directory = "projects/zooniverse/shakespeares-world/talk/"
        boardID = str(df.loc[idnumber].board_id)
        discussionID = str(df.loc[idnumber].discussion_id)
        commentID = str(df.loc[idnumber].comment_id)
        URL = baseURL + directory +  boardID + "/" + discussionID + "?comment=" + commentID
        return URL

    def threadturl(idnumber, df):
        """Takes an thread id number and returns
        returns a composite URL as a string for whole discussion"""
        baseURL = "https://www.zooniverse.org/"
        directory = "projects/zooniverse/shakespeares-world/talk/"
        boardID = ""
        for x in df[df.discussion_id == idnumber].board_id:
            boardID = str(x) # Set the Board ID by iterating through each comment
        #boardID = str(192) # Ugly hack, but all boardIDs == 192 in this dataset.
        discussionID = str(idnumber)
        URL = baseURL + directory +  boardID + "/" + discussionID
        return URL

    def userurl(idnumber, df):
        """Takes a user name and returns the
        user's page URL as a string"""
        baseURL = "https://www.zooniverse.org/"
        userdir = "projects/zooniverse/shakespeares-world/users/"
        return baseURL + userdir + idnumber


class Printer(object):
    def __init__(self, searchstring, df):
        '''
        Takes search string as input and prints the results. The Output
        can be printed both in plaintext or html depending if the optional
        html is set to True or False. Default value is False.
        '''
    def regexpsearch(searchstring, df, html=False, context=True):
        """Takes a regular expression and prints the results, either
        as plain text or html. """
        datacolumn = df.comment_body
        for row in datacolumn.iteritems():
            if context:
                match = re.findall('.{40}' + searchstring + '.{40}',
                row[1], re.IGNORECASE)
            else:
                match = re.findall(searchstring, row[1], re.IGNORECASE)
            if match:
                if html:
                    for m in match:
                        url = URLconstructor.commenturl(row[0], df)
                        print("<p>" + m + "</p>")
                        print('''<p><a href="''' +
                        url + '''">''' + url + '''</a></p>''')
                        print("<p>Date: " +
                        str(df.loc[row[0]].comment_created_at)[0:-7] +
                        "</p>")
                else:
                    print("\n")
                    print("Index ID: " + str(row[0]))
                    for m in match:
                        print("\t" + m)
                    print(URLconstructor.commenturl(row[0], df))
                    print("Thread: " + URLconstructor.threadturl(row[0], df))
                    # Get date of post by locating by index number:
                    print("Date of post: " +
                    str(df.loc[row[0]].comment_created_at)[0:-7])

    def usercomments(searchstring, df, html=False):
        """Input user name as string,
        Output: prints comments for the user"""
        comments = df[df.comment_user_login == searchstring]
        userurl = URLconstructor.userurl(searchstring, df)
        if html:
            print('''<p>Analysing user: <a href="''' + userurl + '''">''' +
            searchstring + '''</a></p>''')
        else:
            print("Analysing user: " + searchstring + ": " +
              URLconstructor.userurl(searchstring, df) + "\n")
        counter = 0

        if html:
            for x in comments.iterrows():
                commenturl = URLconstructor.commenturl(x[0], df)
                counter += 1
                print('''<p>''' + str(counter) + '''. ''' +
                x[1][3] + '''</p>''') # Comment body
                print('''<p>Comment URL: <a href="''' + commenturl +
                '''">''' + commenturl + '''</a></p>''')
                print("<p>Date: " +
                str(df.loc[x[0]].comment_created_at)[0:-7] +
                "</p>")
        else:
            for x in comments.iterrows():
                commenturl = URLconstructor.commenturl(x[0], df)
                counter += 1
                print(str(counter) + ". " + x[1][9]) # Username
                print(x[1][3]) # Comment body
                print("Comment URL: " + commenturl)
                print("Date of post: " +
                str(df.loc[x[0]].comment_created_at)[0:-7])
                print("\n")

    def thread(searchstring, df):
        """Input: Thread number as integer
        Output: Prints thread URL and text body"""
        searchnumber = int(searchstring)
        comments = df[df.discussion_id == searchnumber]
        counter= 0
        print("Thread URL: " + URLconstructor.threadturl(searchnumber, df) + "\n")
        for x in comments.iterrows():
            counter += 1
            print(str(counter) + ". " + x[1][9]) # Username
            print(x[1][3]) # Comment body
            print("Comment URL: " + URLconstructor.commenturl(x[0], df))
            print("\n")

    def hashtag(searchstring, df, html=False):
        """fix so that it prints also time, url, user etc. """
        if html:
            print("<p>Searching for: " + searchstring + "</p>")

        for row in df.iterrows():
            regexp = '\#' + searchstring[1:] + "\s"
            match = re.findall(regexp, row[1][3], re.IGNORECASE)
            if match:
                if html:
                    print("<p>" +  row[1][3] + "</p>")
                else:
                    print(row[1][3])

class TimeSeries(object):
    def __init__(self, searchstring, df):
        '''
        Takes search string and dataframe as input.
        Returns various time series as dicts.
        '''
    def regexpsearch(searchstring, df, plot=True, html=False, freqs=False):
        timefreq = {}
        for row in df.iterrows():
            match = re.findall(searchstring, str(row[1][3]), re.IGNORECASE)
            if match:
                #print(str(row[0]))
                matchcounter = 0
                for m in match:
                    matchcounter += 1
                #print(str(matchcounter))
                timefreq[row[1][4]] = matchcounter
        ts = pd.Series(timefreq)
        hitsperday = ts.resample('1440T', base=60).count()
        hitsperday = hitsperday[hitsperday != 0] # Remove empty values
        if plot:
            fig = plt.figure(figsize=(15,7))
            plt.title("Search: " + searchstring, size=16)
            plt.plot(hitsperday)
            plt.xlabel('Date')
            plt.ylabel('Hits')
        if html:
            plt.savefig("../results/" + searchstring + ".png")
        if freqs:
            return hitsperday

    def usersearch(searchstring, df, plot=True, html=False):
        timefreq = {}
        for row in df.iterrows():
            matchcounter = 0
            if row[1][9] == searchstring:
                matchcounter += 1
                timefreq[row[1][4]] = matchcounter
        ts = pd.Series(timefreq)
        hitsperday = ts.resample('1440T', base=60).count()
        hitsperday = hitsperday[hitsperday != 0] # Remove empty values
        if plot:
            fig = plt.figure(figsize=(15,7))
            plt.title("User: " + searchstring, size=16)
            plt.plot(hitsperday)
            plt.xlabel('Date')
            plt.ylabel('Posts')
        if html:
            plt.savefig("../results/" + searchstring + ".png")
        #else:
        #    return hitsperday # for debugging


class Network(object):
    def __init__(self, searchstring, df):
        """Takes a username or hashtag as input
        and returns a directed network."""

    def getnodes(searchstring, df, source='user', target='user'):
        nodes = []
        counter = 0
        if source == "user":
            for row in df.iterrows():
                if row[1][9] == searchstring:
                    if target == 'user':
                        talksto = re.findall(r'\@[a-zA-Z0-9]+',
                                             row[1][3], re.IGNORECASE)
                    elif target == 'hash':
                        talksto = re.findall(r'\#[a-zA-Z0-9]+',
                                             row[1][3], re.IGNORECASE)
                    if talksto:
                        #print(talksto[0])
                        #odes[counter] = talksto[0]
                        nodes.append(talksto[0])
        if source == "hash":
            if target == "hash":
                print("Searching for: " + str(searchstring))
                for row in df.iterrows():
                    regexp = '\#' + searchstring[1:] + "\s"
                    match = re.findall(regexp, row[1][3], re.IGNORECASE)
                    if match:
                        hashhit = re.findall(r'\#[a-zA-Z0-9]+',
                        row[1][3], re.IGNORECASE)
                        if hashhit:
                            for h in hashhit:
                                nodes.append(h)
            if target == "user":
                print("Searching for: " + str(searchstring))
                for row in df.iterrows():
                    regexp = '\#' + searchstring[1:] + "\s"
                    match = re.findall(regexp, row[1][3], re.IGNORECASE)
                    if match:
                        nodes.append(row[1][9])
        if source == "regexp":
            print("Searching for: " + searchstring)
            for row in df.iterrows():
                match = re.findall(searchstring, row[1][3])
                if match:
                    nodes.append(row[1][9])

        nodefreq = Counter(nodes).most_common()
        return nodefreq

    def makegraph(searchstring, nodefreq, regexp=False):
        #print(nodefreq)
        G = nx.Graph()
        color_map = []
        totalfreq = 0
        userlist = []
        freqarray = []
        for key, value in nodefreq:
            '''
            if value >= 4:
                color_map.append('red')
            else:
                color_map.append('orange')
            '''
            if regexp:
                G.add_edge(searchstring, key, weight=value)
                print(key, value)
                userlist.append(key)
                freqarray.append(value)
                totalfreq += value
            else:
                G.add_edge(searchstring, key, weight=value)
                print(key, value)
                userlist.append(key)
                freqarray.append(value)
                totalfreq += value
        print("-----")
        print("Total value: " + str(totalfreq))
        ten = np.percentile(freqarray, 10)
        twentyfive= np.percentile(freqarray, 25)
        fifty = np.percentile(freqarray, 50) 
        seventyfive = np.percentile(freqarray, 75) 
        ninety = np.percentile(freqarray, 90) 
        print("Ten percentile: " + str(ten))
        print("Twentyfive percentile: " + str(twentyfive))
        print("Fifty percentile: " + str(fifty))
        print("Seventyfive percentile: " + str(seventyfive))
        print("Ninety percentile: " + str(ninety))
        print("Total users: " + str(len(set(userlist))))
        #slope, intercept, r_value, p_value, std_err = stats.linregress(list(range(totalfreq)), freqarray)
        plt.figure(figsize=(8,8))
        nx.draw(G,with_labels=True, font_size=16)
        if regexp:
            plt.savefig("../results/" + str(searchstring) + ".png")
        else:
            plt.savefig("../results/" + str(searchstring[1:]) + ".png") # rm hash symbol

    def userusernetwork(searchstring, df, plot=True, html=False):
        """Takes a username and makes a graph,
        """
        Network.makegraph(searchstring,
                        Network.getnodes(searchstring, df,
                        source='user', target='user'))

    def userhashtagnetwork(searchstring, df, plot=True, html=False):
        """Takes a username and makes a
        graph of hashtags"""
        Network.makegraph(searchstring,
                        Network.getnodes(searchstring, df,
                        source='user', target='hash'))

    def hashtaghashtagnetwork(searchstring, df, plot=True, html=False):
        """Takes a username and makes a graph,
        """
        Network.makegraph(searchstring,
                        Network.getnodes(searchstring, df,
                        source='hash', target='hash'))

    def hashtagusernetwork(searchstring, df, plot=True, html=False):
        """Takes a hashtag and makes a graph of its users,
        """
        Network.makegraph(searchstring,
                        Network.getnodes(searchstring, df,
                        source='hash', target='user'))

    def hashtagusers(searchstring, df, plot=True, html=False):
        """Takes a hashtag and returns frequency of users,
        """
        results = Network.getnodes(searchstring, df,
                        source='hash', target='user')
        for r in results:
            print("<p>" + r[0] + "   " + str(r[1]) + "</p>")

    def hashtagcooccurrence(searchstring, df, plot=False, html=False):
        """Takes a hashtag and prints co-occurrence,
        """
        results = Network.getnodes(searchstring, df,
                                    source='hash', target='hash')
        for r in results:
            print("<p>" + r[0] + "   " + str(r[1]) + "</p>")

    def regexpusernetwork(searchstring, df, plot=True, html=False):
            Network.makegraph(searchstring,
                            Network.getnodes(searchstring, df,
                            source='regexp', target='user'), regexp=True)

    def regexpusers(searchstring, df, plot=True, html=False, data=False):
        results = Network.getnodes(searchstring, df,
                            source='regexp', target='user')
        if data:
            return(results)
        for r in results:
            print("<p>" + r[0] + "   " + str(r[1]) + "</p>")
