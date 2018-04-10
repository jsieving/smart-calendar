## Software Design Final Project Proposal
### Smart Calendar

Team members: Will Fairman, Micah Reid, Vienna Scheyer, Jane Sieving

### Main Idea
We want to make a smart calendar application that allows users to schedule events in google calendars with very little input and receive recommendations for planning their future days based on their previous behavior.  For some types of tasks, it will use past choices and feedback from the user to determine the preferred timing and how long a job will *actually* take. The user will be able to modify suggested activities if they want.

The minimum viable product for our project is an app that runs on a computer and interfaces with the user’s Google Calendar using the Google Calendar API. It would have a minimal graphical user interface that will most likely run off of the bokeh python library. The MVP will create additional features for google calendars and implement various algorithms for appropriate day planning.

The stretch goal for our project is to create a server based system that allows any users on the local network to access our smart calendar features. The calendar application will be able to create a unique schedule that helps the user optimize their work day. Our application will hopefully have a very intuitive interface that makes the process of scheduling one’s day pain free. Other ‘stretch’ features include user login via our app’s interface and scheduling events based on multiple peoples’ calendars (like an automated when2meet).

### Learning Goals

Will:
* Work on having readable and well organized code
* Learn how to effectively implement algorithms with a project.
* Gain experience with multi-machine communication.

Micah:
* Integrate Algorithms with real frameworks
* Focus on backend development
* Work more effectively with GitHub

Vienna:
* Interfacing between platforms
* Making/using scheduling algorithms effectively
* Working on a bigger team than before (good code organization)

Jane:
* Creating an algorithm that can learn and infer a user’s preferences
* Interfacing with lots of different platforms (calendar, texting, app hosting)
* Delegating tasks and working productively in a larger team coding project

### Implementation Plan
We will use the Google Calendar API to read and schedule events in the user’s calendar. Our initial plan is to use the bokeh python library to create a starting user interface. However, we want to research the idea of using SMS as an interface for scheduling and feedback (‘How long did this take you?’). The schedule planning part of our project will most likely involve implementing an existing scheduling algorithm with additional features that account for user preferences.

### Project Schedule
Week 1 Goals:
* Basic GUI (WF)
* Research APIs (All)
* Make a google calendar event through Python (MR)
* Send a text through Python (VS)
* Find a scheduling algorithm as a starting point or to build a basic one (JS)

Roadmap for rest of project:
1. Implementing suggested events
2. Taking feedback from previous events
3. Algorithm for learning from feedback
4. Testing
5. Polishing UI

### Collaboration Plan
* Frequent (every other day) but short meetings
* Push to github often, but ensure that the main code can be run no matter what (create dummy code if you have a partial feature that would break the code or throw errors)
* Using Trello to organize tasks that need to be accomplished and assigned
* Make short term goals very clear at each meeting and make sure everyone has a task/each task has a person
* Good commenting so we can understand each other’s code
* Divide and conquer with very frequent check ins

### Risks
* Disconnected programming could lead to exaggerated problems
* Searching algorithms may be ineffective in improving one’s schedule
* There could be errors and limitations with the google calendar API
* We need to keep the MVP in mind so as not to get too spread out
* People may not enjoy using our software for daily use

### Additional Course Content
* Advanced API usage (both getting and sending information)
* Web security (i.e. for login)
* Local vs. online storage
* Algorithm implementation
