# talk-analyzer
Some simple functions for analyzing Zooniverse Talk pages.

To be used with the forum data that can be exported from the
Talk admin interface (.json format).

These scripts rely on the pandas, matplotlib and networkx modules, besides the standard Python3 library.

## Contents

### 1. talkanalyzer.py

**1. Class URLconstructor**

To make URLs from the various data points, some functions are provided:

```Python
    print(ta.URLconstructor.commenturl(700, df)) # Make URL to a comment
    print(ta.URLconstructor.threadturl(40565, df)) # Make URL to thread
    print(ta.URLconstructor.userurl("Hannebambel", df)) # Make URL to user
```


**2. Class Printer**

For easier printing of information that you need from the data, some printing functions are provided. To print HTML, add the optional flag `html=True` (Boolean set to ``False`` by default):

```Python
    ta.Printer.regexpsearch("pippin.*", df) # Search/print regular expression
    ta.Printer.usercomments("Hannebambel", df, html=True) # Print html comments from specific user
    ta.Printer.thread(20690, df) # Print a thread.
```

**3. Class TimeSeries**

Returns a time series plot for easy tracking of words and users. By setting the optional flag `plot=False` it instead returns a time series as a dictionary.

```Python
    ta.TimeSeries.regexpsearch('women.*', df) # Returns plot for expression "women" / day.
    ta.TimeSeries.usersearch('Cuboctahedron', df, plot=False)# Returns time series as dictionary for user.
```

**4. Class Network**
Returns a network visualization of various entry-points to the data. The networks are outdegree networks and put either a search term, a user or a hashtag as focal point.


````Python
    ta.Network.hashtaghashtagnetwork(searchstring, df, plot=True, html=False)
    ta.Network.hashtagusernetwork(searchstring, df, plot=True, html=False)
    ta.Network.regexpusernetwork(searchstring, df, plot=True, html=False)
    ta.Network.userhashtagnetwork(searchstring, df, plot=True, html=False)
    ta.Network.userusernetwork(searchstring, df, plot=True, html=False)
````

### 2. shakespearesworldDataAnalysis.ipynb
A Jyputer notebook that analyses the forum data from a variety of approaches. Imports ``talkanalyzer.py``.

### 3. shapkespearesworld.py
A script for generating a web front end using cgi-bin to interact with
``talkanalyzer.py``.
