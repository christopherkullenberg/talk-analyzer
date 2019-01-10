import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import networkx as nx
from collections import Counter
import numpy as np
import seaborn as sns
from datetime import datetime

''' talkanalyzer.py - A set of functions for
analyzing exported data from the Zooniverse Talk
forum.

Written by <anonymized for peer review>

Free software according to the MIT-license:
https://opensource.org/licenses/MIT

'''


class URLconstructor(object):
    '''Construct urls'''
    def __init__(self, idnumber, df):
        '''
        Takes idnumber (integer) and pandas dataframe
        '''

    @classmethod
    def commenturl(cls, idnumber, df):
        '''Takes an index number from the dataframe and
        returns a composite URL as a string for a specific comment.'''
        baseURL = "https://www.zooniverse.org/"
        directory = "projects/zooniverse/shakespeares-world/talk/"
        boardID = str(df.loc[idnumber].board_id)
        discussionID = str(df.loc[idnumber].discussion_id)
        commentID = str(df.loc[idnumber].comment_id)
        URL = (baseURL + directory + boardID + "/" +
               discussionID + "?comment=" + commentID)
        return URL

    @classmethod
    def threadturl(cls, idnumber, df):
        '''Takes an thread id number and returns
        returns a composite URL as a string for whole discussion'''
        baseURL = "https://www.zooniverse.org/"
        directory = "projects/zooniverse/shakespeares-world/talk/"
        boardID = ""
        for x in df[df.discussion_id == idnumber].board_id:
            boardID = str(x)  # Set the Board ID by iter through each comment
        #  boardID = str(192) # all boardIDs == 192 in this dataset.
        discussionID = str(idnumber)
        URL = baseURL + directory + boardID + "/" + discussionID
        return URL

    @classmethod
    def userurl(cls, idnumber, df):
        '''Takes a user name and returns the
        user's page URL as a string'''
        baseURL = "https://www.zooniverse.org/"
        userdir = "projects/zooniverse/shakespeares-world/users/"
        return baseURL + userdir + idnumber


class Printer(object):
    '''Printing forum content in various ways'''
    def __init__(self, searchstring, df):
        '''
        Takes search string as input and prints the results. The Output
        can be printed both in plaintext or html depending if the optional
        html is set to True or False. Default value is False.
        '''
    @classmethod
    def regexpsearch(cls, searchstring, df, html=False, context=True):
        '''Takes a regular expression and prints the results, either
        as plain text or html. '''
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
                    print("Date of post: " +
                          str(df.loc[row[0]].comment_created_at)[0:-7])

    @classmethod
    def usercomments(cls, searchstring, df, html=False):
        '''Input user name as string,
        Output: prints comments for the user'''
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
                      x[1][3] + '''</p>''')  # Comment body
                print('''<p>Comment URL: <a href="''' + commenturl +
                      '''">''' + commenturl + '''</a></p>''')
                print("<p>Date: " +
                      str(df.loc[x[0]].comment_created_at)[0:-7] +
                      "</p>")
        else:
            for x in comments.iterrows():
                commenturl = URLconstructor.commenturl(x[0], df)
                counter += 1
                print(str(counter) + ". " + x[1][9])  # Username
                print(x[1][3])  # Comment body
                print("Comment URL: " + commenturl)
                print("Date of post: " +
                      str(df.loc[x[0]].comment_created_at)[0:-7])
                print("\n")

    @classmethod
    def thread(cls, searchstring, df):
        '''Input: Thread number as integer
        Output: Prints thread URL and text body'''
        searchnumber = int(searchstring)
        comments = df[df.discussion_id == searchnumber]
        counter = 0
        print("Thread URL: " + URLconstructor.threadturl(searchnumber, df) +
              "\n")
        for x in comments.iterrows():
            counter += 1
            print(str(counter) + ". " + x[1][9])  # Username
            print(x[1][3])  # Comment body
            print("Comment URL: " + URLconstructor.commenturl(x[0], df))
            print("\n")

    @classmethod
    def hashtag(cls, searchstring, df, html=False):
        '''fix so that it prints also time, url, user etc. '''
        if html:
            print("<p>Searching for: " + searchstring + "</p>")

        for row in df.iterrows():
            regexp = '\#' + searchstring[1:] + "\s"
            match = re.findall(regexp, row[1][3], re.IGNORECASE)
            if match:
                if html:
                    print("<p>" + row[1][3] + "</p>")
                else:
                    print(row[1][3])


class TimeSeries(object):
    '''Various ways of creating time series'''
    def __init__(self, searchstring, df):
        '''
        Takes search string and dataframe as input.
        Returns various time series as dicts.
        '''
    @classmethod
    def regexpsearch(cls, searchstring, df, plot=True, html=False, freqs=False):
        timefreq = {}
        for row in df.iterrows():
            match = re.findall(searchstring, str(row[1][3]), re.IGNORECASE)
            if match:
                # print(str(row[0]))
                matchcounter = 0
                for m in match:
                    matchcounter += 1
                # print(str(matchcounter))
                timefreq[row[1][4]] = matchcounter
        ts = pd.Series(timefreq)
        hitsperday = ts.resample('1440T', base=60).count()
        hitsperday = hitsperday[hitsperday != 0]  # Remove empty values
        if plot:
            #  fig = plt.figure(figsize=(15, 7))
            plt.title("Search: " + searchstring, size=16)
            plt.plot(hitsperday)
            plt.xlabel('Date')
            plt.ylabel('Hits')
        if html:
            plt.savefig("../results/" + searchstring + ".png")
        if freqs:
            return hitsperday

    @classmethod
    def usersearch(cls, searchstring, df, plot=True, html=False):
        '''Search users'''
        timefreq = {}
        for row in df.iterrows():
            matchcounter = 0
            if row[1][9] == searchstring:
                matchcounter += 1
                timefreq[row[1][4]] = matchcounter
        ts = pd.Series(timefreq)
        hitsperday = ts.resample('1440T', base=60).count()
        hitsperday = hitsperday[hitsperday != 0]  # Remove empty values
        if plot:
            # fig = plt.figure(figsize=(15,7))
            plt.title("User: " + searchstring, size=16)
            plt.plot(hitsperday)
            plt.xlabel('Date')
            plt.ylabel('Posts')
        if html:
            plt.savefig("../results/" + searchstring + ".png")
        # else:
        #     return hitsperday # for debugging


class Network(object):
    '''Create networks for visual inspections.'''
    def __init__(self, searchstring, df):
        '''Takes a username or hashtag as input
        and returns a directed network.'''

    @classmethod
    def getnodes(cls, searchstring, df, source='user', target='user'):
        nodes = []
        # counter = 0
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
                                nodes.append(h.lower())
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

    @classmethod
    def makegraph(cls, searchstring, nodefreq, users=True, plot=True):
        '''Make a graph of the distribution of users.'''
        #  print(nodefreq)
        G = nx.Graph()
        #  color_map = []
        totalfreq = 0
        userlist = []
        freqarray = []
        for key, value in nodefreq:
            G.add_edge(searchstring, key, weight=value)
            print(key, value)
            userlist.append(key)
            freqarray.append(value)
            totalfreq += value
        print("-----")
        print("Total value: " + str(totalfreq))
        ten = np.percentile(freqarray, 10)
        twentyfive = np.percentile(freqarray, 25)
        fifty = np.percentile(freqarray, 50)
        seventyfive = np.percentile(freqarray, 75)
        ninety = np.percentile(freqarray, 90)
        print("Ten percentile: " + str(ten))
        print("Twentyfive percentile: " + str(twentyfive))
        print("Fifty percentile: " + str(fifty))
        print("Seventyfive percentile: " + str(seventyfive))
        print("Ninety percentile: " + str(ninety))
        print("Total users: " + str(len(set(userlist))))
        plt.plot(freqarray)
        plt.xlabel('Number of users')
        plt.ylabel('Number of hashtags')
        plt.show()
        plt.figure(figsize=(8, 8))
        nx.draw(G, with_labels=True, font_size=16)

    @classmethod
    def userusernetwork(cls, searchstring, df, plot=True, html=False):
        '''Takes a username and makes a graph,
        '''
        Network.makegraph(searchstring,
                          Network.getnodes(searchstring, df,
                                           source='user', target='user'))

    @classmethod
    def userhashtagnetwork(cls, searchstring, df, plot=True, html=False):
        '''Takes a username and makes a
        graph of hashtags'''
        Network.makegraph(searchstring,
                          Network.getnodes(searchstring, df,
                                           source='user', target='hash'))

    @classmethod
    def hashtaghashtagnetwork(cls, searchstring, df, plot=True, html=False):
        '''Takes a username and makes a graph,
        '''
        Network.makegraph(searchstring,
                          Network.getnodes(searchstring, df,
                                           source='hash', target='hash'))

    @classmethod
    def hashtagusernetwork(cls, searchstring, df, plot=True, html=False):
        '''Takes a hashtag and makes a graph of its users,
        searchstring, nodefreq, regexp=False, users=True, plot=True
        '''
        Network.makegraph(searchstring,
                          Network.getnodes(searchstring, df,
                                           source='hash', target='user'))

    @classmethod
    def hashtagusers(cls, searchstring, df, plot=True, html=False):
        '''Takes a hashtag and returns frequency of users,
        '''
        results = Network.getnodes(searchstring, df,
                                   source='hash', target='user')
        for r in results:
            print("<p>" + r[0] + "   " + str(r[1]) + "</p>")

    @classmethod
    def hashtagcooccurrence(cls, searchstring, df, plot=False, html=False):
        '''Takes a hashtag and prints co-occurrence,
        '''
        results = Network.getnodes(searchstring, df,
                                   source='hash', target='hash')
        for r in results:
            print("<p>" + r[0] + "   " + str(r[1]) + "</p>")

    @classmethod
    def regexpusernetwork(cls, searchstring, df, plot=True, html=False):
        Network.makegraph(searchstring,
                          Network.getnodes(searchstring, df,
                                           source='regexp',
                                           target='user'), regexp=True)

    @classmethod
    def regexpusers(cls, searchstring, df, plot=True, html=False, data=False):
        results = Network.getnodes(searchstring, df,
                                   source='regexp', target='user')
        if data:
            return results
        for r in results:
            print("<p>" + r[0] + "   " + str(r[1]) + "</p>")


class CoreSet(object):
    '''This class has various functions that analyze
    the core set of users and how they interact.'''
    def __init__(self, searchstring, df):
        '''
        Takes search string and dataframe as input.
        Returns various time series as dicts.
        Seaborn distplot docs:
        https://seaborn.pydata.org/tutorial/distributions.html
        '''

    @classmethod
    def frequency(cls, searchstring, df):
        distribution = Network.getnodes(searchstring, df,
                                        source='hash', target='user')
        return distribution

    @classmethod
    def frequencypercent(cls, searchstring, df):
        totalhashtags = 0
        percentlist = []
        distribution = Network.getnodes(searchstring, df,
                                        source='hash', target='user')
        for d in distribution:  # get total
            totalhashtags += d[1]
        print("Total hashtags: " + str(totalhashtags))
        for d in distribution:
            percentlist.append((d[0], round((d[1] / totalhashtags), 2)))
        return percentlist

    @classmethod
    def percentile(cls, searchstring, df):
        '''To be fixed'''
        distribution = Network.getnodes(searchstring, df,
                                        source='hash', target='user')
        return distribution

    @classmethod
    def histogram(cls, searchstring, df):
        freqdict = CoreSet.frequency(searchstring, df)
        freqarray = []
        for tple in freqdict:
            freqarray.append(tple[1])
        plt.plot(freqarray)
        plt.xlabel('Number of users')
        plt.ylabel('Number of hashtags')
        plt.show()

    @classmethod
    def distplot(cls, searchstring, df):
        freqdict = CoreSet.frequency(searchstring, df)
        freqarray = []
        for tple in freqdict:
            freqarray.append(tple[1])
        sns.distplot(freqarray, bins=len(freqarray), kde=False, rug=True)
        plt.show()

    @classmethod
    def kerneldistplot(cls, searchstring, df):
        freqdict = CoreSet.frequency(searchstring, df)
        freqarray = []
        for tple in freqdict:
            freqarray.append(tple[1])
        sns.distplot(freqarray, hist=False, rug=True)

    @classmethod
    def hashtagtimeseries(cls, searchstring, df):
        '''Takes a hashtag as input, for example "womanwriter",
        then returns a time series describing the formation of hashtag.'''
        ts = pd.DataFrame(columns=["User", "Timestamp",
                                   "Hashtag", "ThreadURL", "Role"])
        datadict = {}
        for row in df.iterrows():
            singular = '\#' + searchstring[1:] + '.*'
            plural = '\#' + searchstring[1:] + 's\s'
            regexp = '[' + singular + '|' + plural + ']' #hashtag search
            #regexp = '\#' + searchstring[1:] + "\s"
            #  print(regexp)
            match = re.findall(singular, str(row[1][3]),
                               flags=re.IGNORECASE | re.DOTALL | re.MULTILINE)
            if match:
                datadict = {}
                matchcounter = 0
                for m in match:
                    matchcounter += 1
                    datadict["User"] = row[1][9]
                    datadict["Timestamp"] = row[1][4]
                    datadict["Hashtag"] = m
                    datadict["ThreadURL"] = URLconstructor.commenturl(row[0],
                                                                      df)
                    datadict["Role"] = row[1][11]
                    ts = ts.append(datadict, ignore_index=True)
        # ts = pd.Series(timefreq)
        # hitsperday = ts.resample('1440T', base=60).count()
        # hitsperday = hitsperday[hitsperday != 0]  # Remove empty values
        return ts

    @classmethod
    def hashtagroles(cls, df):
        '''This creates a directed network file between a mentioned
        user and the hashtags in a post. The purpose is to find which
        users are pinged when certain hashtags are used.'''
        G = nx.DiGraph()
        edgecounter = 0
        for post in df['comment_body']:
            hashtaglist = []
            userspingedlist = []
            hashtag = re.findall(r'\#[a-zA-Z0-9_-]+', str(post),
                                 re.IGNORECASE | re.DOTALL)
            userpinged = re.findall(r'\@[a-zA-Z0-9]+', str(post),
                                    re.IGNORECASE | re.DOTALL)
            #questionmark = re.findall(r'\?', str(post),
            #                          re.IGNORECASE | re.DOTALL)
            if hashtag:
                for h in hashtag:
                    if h == "#v":  # Note #v is a false positive generated
                        continue
                    else:
                        hashtaglist.append(h.lower())
            if userpinged:
                #  if questionmark: # This can be used to detect questions.
                    #  print(post)
                for u in userpinged:
                    userspingedlist.append(u.lower())
                if hashtaglist:
                    # print("Hashtags: " + str(hashtaglist))
                    # print("Users: " + str(userspingedlist))
                    # print(post)
                    # print("---")
                    for h in hashtaglist:
                        for u in userspingedlist:
                            # print(h, u)
                            if G.has_edge(h, u):
                                G[h][u]['weight'] += 1
                            else:
                                G.add_edge(h, u, weight=1)
                            edgecounter += 1

        print("Edgecounter: " + str(edgecounter))
        nx.write_gexf(G, "hashtaguserinteractions.gexf")

    @classmethod
    def vis(cls, hashtag, df, excludeusers = None):
        '''Create html files with VIS visualizations'''
        hashtag = hashtag.lower()
        header = ('''<!DOCTYPE HTML>
                    <html>
                    <head>
                      <title>Shakespeare's world | Hashtag timeline analysis
                      </title>
                      <style type="text/css">
                        body, html {
                          font-family: sans-serif;
                            font-size: 15pt;
                        }
                        .vis-item.researcher {
                          background-color: greenyellow;
                          border-color: greenyellow;
                        }
                        .vis-item.moderator {
                          background-color: pink;
                          border-color: pink;
                        }
                        .vis-item.superuser {
                          background-color: lightblue;
                          border-color: lightblue;
                        }
                              .vis-item.active {
                          background-color: grey;
                          border-color: grey;
                        }
                              .vis-item.casual {
                          background-color: white;
                          border-color: grey;
                        }
                      </style>

                      <script src="node_modules/vis/dist/vis.js"></script>
                      <link href="node_modules/vis/dist/vis.css" rel="stylesheet" type="text/css" />
                    </head>
                    <body>
                    <div id="visualization"></div>
                    <script type="text/javascript">
                      var items = new vis.DataSet([
                        \n''')

        htmlfile = open("html/" + hashtag[1:] + ".html", "w")
        htmlfile.write(header)
        iterator = 1

        for t in CoreSet.hashtagtimeseries(hashtag, df).iterrows():
            # print(t[1][0])
            color = ""
            if excludeusers:
                if t[1][0] in excludeusers:
                    continue
            if t[1][4] == 'researcher':
                color = "className: 'researcher'"
                username = t[1][0] #  Sets real usernam
            elif t[1][4] == 'moderator':
                color = "className: 'moderator'"
                username = "moderator" #  Anonymizes username
            elif t[1][4] == 'superuser':
                color = "className: 'superuser'"
                username = "superuser"
            elif t[1][4] == 'active':
                color = "className: 'active'"
                username = "active"
            else:
                color = "className: 'casual'"
                username = "casual"

            htmlfile.write("{id: " + str(iterator) + ", content: '"
                           + "', start: '" + str(t[1][1])[0:10]
                           + "', type: 'box', " + color + "}, \n")
            iterator += 1

        footer = (''']);
          // DOM element where the Timeline will be attached
          var container = document.getElementById('visualization');

          // Configuration for the Timeline
          var options = {
            editable: true
          };

          // Create a Timeline
          var timeline = new vis.Timeline(container);
          timeline.setOptions(options);
          timeline.setItems(items);
        </script>
        </body>
        </html>
        ''')
        htmlfile.write(footer)
        htmlfile.close()
        print("Wrote " + str(iterator) + " interactions for hashtag #"
              + hashtag[1:] + " as " + hashtag[1:] + ".html")




    @classmethod
    def htmltosvg(cls, hashtag, df, excludeusers = None):
        '''Create html files with VIS visualizations'''
        hashtag = hashtag.lower()
        header = ('''<html>
          <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8">

            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
              google.charts.load('current', {'packages':['timeline']});
              function drawChart() {
                var container = document.getElementById('timeline');
                var chart = new google.visualization.Timeline(container);
                var dataTable = new google.visualization.DataTable();

                dataTable.addColumn({ type: 'string', id: 'Role' });
                dataTable.addColumn({ type: 'date', id: 'Start' });
                dataTable.addColumn({ type: 'date', id: 'End' });
                dataTable.addRows([''')

        svgfile = open("html/" + hashtag[1:] + ".html", "w")
        svgfile.write(header)
        iterator = 1

        for t in CoreSet.hashtagtimeseries(hashtag, df).iterrows():
            # print(t[1][0])
            color = ""
            if excludeusers:
                if t[1][0] in excludeusers:
                    continue
            if t[1][4] == 'researcher':
                color = "className: 'researcher'"
                username = t[1][0] #  Sets real usernam
            elif t[1][4] == 'moderator':
                color = "className: 'moderator'"
                username = "moderator" #  Anonymizes username
            elif t[1][4] == 'superuser':
                color = "className: 'superuser'"
                username = "superuser"
            elif t[1][4] == 'active':
                color = "className: 'active'"
                username = "active"
            else:
                color = "className: 'casual'"
                username = "casual"

            '''
                  [ 'Washington', new Date(1789, 3, 30), new Date(1797, 2, 4) ],
                  [ 'Adams',      new Date(1797, 2, 4),  new Date(1801, 2, 4) ],
                  [ 'Jefferson',  new Date(1801, 2, 4),  new Date(1809, 2, 4) ]
            '''
            newdate = str(t[1][1] + pd.DateOffset(1))

            svgfile.write("[' " + username + "', new Date('" + str(t[1][1])[0:10]
                         + "'), new Date('" + str(newdate)[0:10] + "') ],\n")
            iterator += 1

        footer = (''']);
                    google.visualization.events.addListener(chart, 'ready', allReady); // ADD LISTENER
                    chart.draw(dataTable);
                    }
                    function allReady() {
                    var e = document.getElementById('timeline');
                    // svg elements don't have inner/outerHTML properties, so use the parents
                    console.log(e.getElementsByTagName('svg')[0].outerHTML);

                    }
                    google.charts.setOnLoadCallback(drawChart);

                    </script>

                    </head>
                    <body>
                    <div id="timeline" style="height: 180px;"></div>
                    </body>
                    </html>
                    ''')
        svgfile.write(footer)
        svgfile.close()
        print("Wrote " + str(iterator) + " interactions for hashtag #"
              + hashtag[1:] + " as " + hashtag[1:] + ".html")
