# talk-analyzer
Some simple functions for analyzing Zooniverse Talk pages.

To be used with the forum data that can be exported from the
Talk admin interface (.json format).

This software was used in **>>insert article when published<<**. In the folder ``supplementary files`` there are search terms and classificatory protocols for refining the data and in the folder ``Figures`` there are high resolution images from the article.  

For questions, please contact Christopher Kullenberg <christopher.kullenber AT gu.se>.

## Requirements

These scripts rely on the pandas, matplotlib and networkx modules, besides the standard Python 3 library.

For hashtag visualizations rendered as javascript/html, [Vis.js](http://visjs.org/) is incorporated (see html folder).

### 1. talkanalyzer.py

Generally, you can ``import talkanalyzer as ta`` for shorter typing.

**URLconstructor**

To make URLs from the various data points, some functions are provided:

```Python
    print(ta.URLconstructor.commenturl(700, df)) # Make URL to a comment
    print(ta.URLconstructor.threadturl(40565, df)) # Make URL to thread
    print(ta.URLconstructor.userurl("username", df)) # Make URL to user
```


**Printer**

For easier printing of information that you need from the data, some printing functions are provided. To print HTML, add the optional flag `html=True` (Boolean set to ``False`` by default):

```Python
    ta.Printer.regexpsearch("pippin.*", df) # Search/print regular expression
    ta.Printer.usercomments("username", df, html=True) # Print html comments from specific user
    ta.Printer.thread(20690, df) # Print a thread.
```

**TimeSeries**

Returns a time series plot for easy tracking of words and users. By setting the optional flag `plot=False` it instead returns a time series as a dictionary.

```Python
    ta.TimeSeries.regexpsearch('women.*', df) # Returns plot for expression "women" / day.
    ta.TimeSeries.usersearch('username', df, plot=False)# Returns time series as dictionary for user.
```

**Network**
Returns a network visualization of various entry-points to the data. The networks are outdegree networks and put either a search term, a user or a hashtag as focal point.


```Python
    ta.Network.hashtaghashtagnetwork("#women", df, plot=True, html=False)
    ta.Network.hashtagusernetwork("#beer", df, plot=True, html=False)
    ta.Network.regexpusernetwork("recip.*", df, plot=True, html=False)
    ta.Network.userhashtagnetwork("username", df, plot=True, html=False)
    ta.Network.userusernetwork("username", df, plot=True, html=False)
```
.




### 2. shakespearesworld.py
A script for generating a web front end using cgi-bin to interact with
``talkanalyzer.py``.


### 3. HashtagRolesAnalysis.ipynb
A notebook using the `Coreset.hashtagroles()` and `Coreset.vis()` methods to create hashtag-mentions visualisations and networks. 


