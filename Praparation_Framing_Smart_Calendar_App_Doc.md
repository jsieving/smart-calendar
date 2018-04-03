

**Smart Calendar App Team - Preparation and Framing Document**

1. **Background and context** What information about your project does the audience need to participate fully in the technical review? You should share enough to make sure your audience understands the questions you are asking, but without going into unnecessary detail.

Our smart calendar app will be able to help users schedule future activities based on their current schedule and past tendencies. For our MVP, we are interfacing with Google Calendar and taking user input (possibly through text messaging, otherwise through a web interface).  We are working on a scheduling algorithm that takes parameters such as start time, end time, duration, etc. As an example, a user might have 5 hours of Linearity homework to do in the next week and the user needs to know where that activity fits into their current schedule. The smart calendar app can break the activity into appropriate sized chunks and add the work to the user&#39;s calendar. At a minimum, the user can enter only the activity name and the calendar will schedule the activity based on past event data. The user can further define an activity by filling in optional parameters like duration, minimum chunk size, etc. The calendar will ask the user how an event went after it happens to gauge whether the scheduling attempt was successful.

1. **Key questions** What do you want to learn from the review? What are the most important decisions your team is currently contemplating? Where might an outside perspective be most helpful? As you select key questions to ask during the review, bear in mind both the time limitations and background of your audience.

- What do people think of a text message interface for sending activities and feedback to the calendar? What about a web interface?
- How do we want to structure our scheduling algorithm? Is our current approach appropriate?

We have a set of available time blocks and a set of activities that need to be scheduled. Each activity has a &quot;preference&quot; (based on feedback from the user about the success of scheduling similar events in the past) for which time block it gets scheduled into, and the algorithm needs to take this preference into account along with considering when the activity due date.

Once we determine the preference level of each event for each time block, we are trying to decide whether to schedule activities linearly and then perform iterations or to schedule events non-linearly in order of preference.

- Is it appropriate to store event data as dictionaries in files? For example, if an activity is all the instances of a type of event (where an event is each instance of a math homework assignment), we would have a file to document all of the math homework activities. Similarly, we could have another file that saves all the instances of practicing piano. When the algorithm re-shuffles events in the calendar, events that get changed would be overwritten. Each file would save past data for the events that actually happened. If a user deletes an event because they don&#39;t like where it is scheduled, we will store that data numerically in a matrix.

1. **Agenda for technical review session** Be specific about how you plan to use your allotted time. What strategies will you use to communicate with your audience?

We plan to set our agenda for the review, give the audience a brief background of the project, and then start talking about program structure. We have a block diagram as a visual to help with our explanation, and then we will highlight some ideas we have about program structure and data storage. We will give an example of the program structure and then ask audience members for questions and feedback.

1. **Feedback form** Create a Google form that folks in the review will use to provide you with feedback or answers to various questions you pose to your audience. Since, at least for the first review, the time you have to present will be very short you should expect most of the feedback you get to come from this form rather than thoughts expressed orally during your session. Please [submit a link to your Google form](https://docs.google.com/forms/d/e/1FAIpQLSdDb4Q3wtGMyax6DCJGRD3zbzuo9uQNjGTNSEKS-97H9nIy_Q/viewform) using this other Google form! (you must have this submitted no less than 2 hours before class so we have time to post a link on the course website).
