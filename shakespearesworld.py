#!/usr/bin/python3
# coding: utf-8

#import csv
import matplotlib
matplotlib.use('Agg')

import re
import cgi, cgitb
import sys
import pandas as pd
import seaborn as sns
import re
import matplotlib.pyplot as plt
import talkanalyzer as ta # Requires pandas


sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

df = pd.read_json(".data/project-376-comments_2017-04-28.json")

print("Content-type:text/html; charset=utf-8\r\n\r\n")
print()

print('''
<center>
<head>
  <link rel="stylesheet" href="https://tools.christopherkullenberg.se/style.css">
</head>
<h1>Talkanalyzer: Shakespeare's World</h1>
</center


<!-- L E F T   B A R -->
<div class="wrap">
    <div class="fleft">

<div id="searchfield">

<form enctype="multipart/form-data" action="shakespearesworld.py" method="post">

  <h2>User data</h2>
    <p>
	<input type="text" name="search" placeholder="Username"> (ex. joolslee) <br>
        <input type="radio" name="viewuser" value="search_user_posts" checked>View user posts
        <input type="radio" name="viewuser" value="network_user" >View outdegree user network<br>
        <input type="radio" name="viewuser" value="network_hash"> View outdegree user/hashtag network
        <input type="radio" name="viewuser" value="timeline"> View timeline
      </p>


</div> <!-- / searchfield -->


   <div id="searchbutton">
     <input type="submit" value="Generate!" class="sun-flower-button"><br>
   </form>
  </div>
</div>

<!-- R I G H T   B A R -->
    <div class="fright">
     <form enctype="multipart/form-data" action="shakespearesworld.py" method="post">

        <h2>Search Forum</h2>
        	<input type="text" name="search" placeholder="Regular expression"> (ex. recip.*) <br>
                <input type="radio" name="viewuser" value="search_regexp_html" checked>Result as text
                <input type="radio" name="viewuser" value="search_regexp_plot" >Result as timeline
                <input type="radio" name="viewuser" value="search_regexp_network" >Result as user network
                <br>
                <input type="radio" name="viewuser" value="search_regexp_users" >Result as user frequency

                <div id="searchbutton">
                <input type="submit" value="Search!" class="sun-flower-button"><br>

       </form>
      </div>


    <form enctype="multipart/form-data" action="shakespearesworld.py" method="post">

        <h2>Hashtag search</h2>

        <input type="text" name="search" placeholder="hashtag"> (ex. #catholic) <br>
            <input type="radio" name="viewuser" value="search_hashtag_html" checked>Result as text
            <input type="radio" name="viewuser" value="search_hashtag_network" >Result as network
            <input type="radio" name="viewuser" value="search_co_occurrence" >Co-occurrence
            </br>
            <input type="radio" name="viewuser" value="hashtag_user_network"> View hashtag user network
            <input type="radio" name="viewuser" value="hashtag_users"> View hashtag users

            <div id="searchbutton">
            <input type="submit" value="Search!" class="sun-flower-button"><br>


   </form>
  </div>
</div>


    </div>

''')


form = cgi.FieldStorage()

usermode = form.getvalue('viewuser')

if usermode == 'search_user_posts':
    network_user = form.getvalue('search')
    ta.Printer.usercomments(network_user, df, html=True)

if usermode == 'network_user':
    network_user = form.getvalue('search')
    ta.Network.userusernetwork(network_user, df)
    print('''<img src="../results/''' + network_user + '''.png" />''')

if usermode == 'network_hash':
    network_user = form.getvalue('search')
    ta.Network.userhashtagnetwork(network_user, df)
    print('''<img src="../results/''' + network_user + '''.png" />''')

if usermode == 'timeline':
    network_user = form.getvalue('search')
    ta.TimeSeries.usersearch(network_user, df, html=True)
    print('''<img src="../results/''' + network_user + '''.png" />''')

if usermode == 'search_regexp_html':
    network_user = form.getvalue('search')
    ta.Printer.regexpsearch(network_user, df, html=True)
    print('''<img src="../results/''' + network_user + '''.png" />''')

if usermode == 'search_regexp_plot':
    network_user = form.getvalue('search')
    ta.TimeSeries.regexpsearch(network_user, df, html=True)
    print('''<img src="../results/''' + network_user + '''.png" width="800" />''')

if usermode == 'search_regexp_network':
    network_user = form.getvalue('search')
    ta.Network.regexpusernetwork(network_user, df, html=True)
    print('''<img src="../results/''' + network_user + '''.png" width="800" />''')

if usermode == 'search_regexp_users':
    network_user = form.getvalue('search')
    ta.Network.regexpusers(network_user, df, html=True)
    print('''<img src="../results/''' + network_user + '''.png" width="800" />''')

if usermode == 'search_hashtag_html':
    network_user = form.getvalue('search')
    ta.Printer.hashtag(network_user, df, html=True)

if usermode == 'search_hashtag_network':
    network_user = form.getvalue('search')
    ta.Network.hashtaghashtagnetwork(network_user, df, html=True)
    # Printer removes hash symbol
    print('''<img src="../results/''' + str(network_user[1:]) + '''.png" width="800" />''')

if usermode == 'search_co_occurrence':
    network_user = form.getvalue('search')
    ta.Network.hashtagcooccurrence(network_user, df, html=True)

if usermode == 'hashtag_user_network':
    network_user = form.getvalue('search')
    ta.Network.hashtagusernetwork(network_user, df, html=True)
    # Printer removes hash symbol
    print('''<img src="../results/''' + str(network_user[1:]) + '''.png" width="800" />''')

if usermode == 'hashtag_users':
    network_user = form.getvalue('search')
    ta.Network.hashtagusers(network_user, df, html=True)



print('<br><br>')
print('</center>')
