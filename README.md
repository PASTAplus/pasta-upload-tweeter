# PASTA Upload Tweeter
Tweets when a new data package is uploaded to the PASTA data repository!

## About

The PASTA Upload Tweeter is a Python 3 application that listens for PASTA data package upload notifications and responds with a "tweet" through the [@EDIgotdata](https://twitter.com/EDIgotdata) twitter account. Tweets include the PASTA package identifier, a link to the EDI Data Portal landing page for the data package, and the title of the data package (truncated if necessary).

![EDIgotdata new data package tweet](https://github.com/EDIorg/pasta-upload-tweeter/blob/master/EDI-tweet.png)

## Technical

The PASTA Upload Tweeter operates a Flask web applicagtion listening for POST requests on the `/tweet` route and pulls the simple PASTA package identifier from the request message body (no key-value here, just the identifier). If the package identifier is in a valid format, the application queries PASTA for the data package metadata in the Ecological Metadata Language format and parses out the title using the Python `lxml etree` package. With the package identifier and title in hand, the application constructs the twitter message (see above) and uses the Python `python-twitter` package as a wrapper for the Twitter REST API to post the new message to the @EDIgotdata feed.
