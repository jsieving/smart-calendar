# Smart Calendar-- The calendar of the future
Smart Calendar interfaces with Google Calendar to automatically schedule to-do items based on availability and user preference. Smart Calendar schedules what you want to do, when you want to do it. Over time it learns your work and rest patterns, for increased accuracy and improved user experience.

### Our Goal
As overworked engineering students, we know what it's like to feel like you don't have enough free time. Sometimes when you look at a long to do list and a busy calendar, it looks like they will never fit together. By automating this scheduling process, we aim to reduce the stress of feeling overbooked, and take out overwhelming and repetitive decision making out of the process. We started this project with the intention to learn about applications of matrix algebra in user-facing applications. Luckily for us, this form of data storage and predictive algorithm applies perfectly to scheduling problems. Together, we have combined these learning goals and product goals to create what you see today.

### How to Use
This section is a work in progress! At the current moment, the user should run webinterface.py, and follow the in-browser prompts. As features are added and completed, we will shift to a URL that a user can visit. All login and authentication is done through Google, and users should read their privacy and security policies if they have any concerns. For a detailed explanation, click [here](../howto).

### Our Tech
Our frontend is still very much in progress! Please check back for updates.

Our backend is written in python, and relies heavily on matrix assignment algorithms. We have created our own algorithm, based off of SciPy's LinearAssignmentSum, which batches tasks in order of priority, then assigns them a few at a time with room for user feedback between batches. These priorities and costs are derived from a number of subprograms we have written that create cost matrices for different priorities, such as work/break time or preference for repeating routines. 

