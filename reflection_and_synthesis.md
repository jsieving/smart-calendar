# Architectural Review: Reflection and Synthesis
### *Smart Calendar App*
Vienna Scheyer, Will Fairman, Micah Reid, and Jane Sieving

## Conclusions Drawn from Feedback

We asked our audience if they thought we were underestimating the challenge of part of our project. Several people said that making this calendar as smart as we hope for it to be will be difficult. Others pointed out that people have very different lifestyles, so it will be hard to make something that is useful to people with all different kinds of habits. Some people have very regular schedules, others have almost no regular activities. One person observed that for the calendar to learn effectively at the beginning, it might have to pester the user for a LOT of input. This could be very draining to users, and undermine the time-saving goals of our program.

The responses about user interface choices were all over the map. Some people thought a web interface was the most appropriate platform, but others thought a text interface would add convenience. Some thought that a text interface didn’t make sense and we should just have a dedicated interface for our program, but others said we shouldn’t try to build a whole new interface. People were split on how helpful or annoying notifications might be. There were a lot of ideas for the potential uses of SMS or phone notifications. However, the most consistent feedback was a reminder not to spread ourselves too thin. We have decided to focus on building a web interface instead of working on SMS integration, both because there seemed to be a slight preference for it and because we have judged that SMS adds too much complexity for the core goals of our project.

We got some interesting ideas for features we could include, some of which we had already considered. They include:
* Confirming if the user meant to schedule 2 things at the same time
* Interfacing with Outlook calendar
* Letting the user add details and/or color coding to events
* Knowing times that aren’t okay to schedule events (sleep, for example)
* Having multiple people join an event
* Having notifications be optional or filtered
* Making automatic scheduling optional
* Focusing on a to-do list with a prioritization algorithm

We definitely plan to block off certain times of day, and have recently discussed ways to preserve meal times, break times, and religious observances. The notifications aren’t really relevant if we’re only doing a web app. Automatic scheduling is kind of the interesting part of our project, but as a user-oriented product we might consider turning it off or at least making it less aggressive. Without scheduling, the prioritization could still be useful to users. The other suggested features are good ideas, but likely beyond the time frame we have for this project.

We asked people what they would suggest to improve the structure of our code, but many did not have suggestions since we presented our structure as a general overview. A couple reminded us that storage and security is an important issue that we haven’t addressed thoroughly. Handling logins needs to be done carefully, and we don’t want users’ information visible to everyone. Paul (Hi Paul) said that integration between parts of our program would likely take a lot of time and need to be done carefully. We will probably look for help in making sure our program is secure for users as we develop the web application.

In the ‘additional comments’ section, one person said,  “I would be interested to see how you implement the scheduling algorithm,” and another person said, “Seems very ambitious!...a lot of moving parts.” After the Architectural Review, we realized that we need to focus on prioritizing and dividing up work. We are focusing on breaking down our algorithm now, deciding how it should work and who can work on what piece of that so that it is manageable.

These comments underscored the difficulty surrounding the integration of our idea with existing platforms. To combat this task, we have split our workload as a team into two main categories: scheduling algorithm and code functionality.  Each week, each team member is planning on making contributions to both parts of the project.  This will hopefully allow for easier integration and implementation of our idea as we build additional features.

## Reflection on AR and Future Plans

The architectural review helped us realize where we are in the process of planning our project. For the algorithm, we had a general idea of what we want it to be able to do. We knew that we wanted to interface with google calendar and create a way to get user input. The AR prompted a team discussion about the central algorithm and led to the realization that we need to figure out how to distribute work since all of us share an interest in working on this algorithm. Additionally, we decided to use a web interface instead of SMS.

The reason we did not have very clear work distribution before the AR is because we had been having a hard time scheduling team meetings and keeping Trello up to date. We plan to meet more frequently now, and we are making an effort to use Trello as well.  In order to keep motivation high and make sure we are distributing the workload of the project evenly throughout the alloted time, we have created tasks to be finished in one week sprints.

For the next technical review, it would be helpful for us to actively distribute the conversation across the decisions we want the audience to help us make. We ended up talking a lot about the decision between web interface and SMS since the audience had a lot to say about that, but if we wanted to get more feedback about, for example, data storage, we could guide the conversation in that direction. Although our review could have been more defined and organized, we got useful feedback from our audience about what they would want from our project and difficulties we should be aware of.
