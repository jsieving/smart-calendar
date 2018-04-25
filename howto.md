---
title: How To
layout: template
filename: howto
--- 
# Using Our Web App
The files for our application.
Our application was built to run off the linux terminal. If you are also using the linux terminal follow the steps below. If not skip to the [Windows installation section](#contact_form).

### Installing Dependencies
The use of third-party code for interactions with Google and SciPy requires additional libraries. Copy and paste the line below into the terminal in order to install all the necessary packages:

```
pip install datetime httplib2 oauth2client apiclient ortools flask
```
### Connecting the Program to Google Calendar
In order to interact with your personal Google Calendar, the program needs an api key from your google account. This [link](https://developers.google.com/calendar/quickstart/python) will show you how to download the right file (follow step 1 only).

### Running the Code
With the correct Google Api key and setup process, using our app is easy! Simply run this line of code `python webInterface.py`
and click [here](http://127.0.0.1:5000/). Currently our application does not support firefox so make sure to stick with chrome.


### <a id="contact_form"></a>Windows Installation
The main portion of our code runs locally on the computer using python. Downloading and using [Anaconda](https://www.anaconda.com/download/#download) will make this process easier.

As of right now we have not tried the smart-calendar in Windows. Further documentation will be provided when we can make sure it will work.
