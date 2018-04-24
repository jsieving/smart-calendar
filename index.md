# Smart Calendar-- The calendar of the future
Smart Calendar interfaces with Google Calendar to automatically schedule to-do items based on availability and user preference. Smart Calendar schedules what you want to do, when you want to do it. Over time it learns your work and rest patterns, for increased accuracy and improved user experience.
### How to Use
This section is a work in progress! At the current moment, the user should run webinterface.py, and follow the in-browser prompts. As features are added and completed, we will shift to a URL that a user can visit. All login and authentication is done through Google, and users should read their privacy and security policies if they have any concerns.
### Our Tech
Our frontend is still very much in progress! Please check back for updates.

Our backend is written in python, and relies heavily on matrix assignment algorithms. We have created our own algorithm, based off of SciPy's LinearAssignmentSum, which batches tasks in order of priority, then assigns them a few at a time with room for user feedback between batches. These priorities and costs are derived from a number of subprograms we have written that create cost matrices for different priorities, such as work/break time or preference for repeating routines. 

### Authors and Contributors
This project was created by William Fairman (@wfairmanolin), Jane Sieving (@jsieving), Vienna Scheyer (@vscheyer), and Micah Reid (@mhreid).
### Support or Contact
Email us at micah.reid@students.olin.edu and we will get back to you!
