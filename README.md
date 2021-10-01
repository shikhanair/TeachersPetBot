<p align="center"><img src="https://github.com/shikhanair/TeachersPetBot/blob/main/images/teacherspet.png" alt="alt text" width=200 height=200>
  
  <h1 align="center"> Teacher's Pet </h1>
  
<h2 align="center"> Streamline Your Class Discord</h1>


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5542626.svg)](https://doi.org/10.5281/zenodo.5542626)
![Python](https://img.shields.io/badge/python-v3.7+-brightgreen.svg)
![GitHub](https://img.shields.io/github/license/shikhanair/TeachersPetBot)
![GitHub issues](https://img.shields.io/github/issues/shikhanair/TeachersPetBot)
![GitHub closed issues](https://img.shields.io/github/issues-closed/shikhanair/TeachersPetBot)
![Lines of code](https://img.shields.io/tokei/lines/github/shikhanair/TeachersPetBot)
[![codecov](https://codecov.io/gh/shikhanair/TeachersPetBot/branch/main/graph/badge.svg?token=ZQUQ8UC2Y6)](https://codecov.io/gh/shikhanair/TeachersPetBot)

  Click Below to Watch Our Video!
[![Watch the video](https://github.com/shikhanair/TeachersPetBot/blob/main/images/teacherspetbot.png)](https://youtu.be/tExF88LHqgE)
  
  

Software Engineering Project 1 for CSC 510

Teacher's Pet is a Discord Bot for class instructors to streamline their Discord servers. Discord is a great tool for communication and its functionalities can be enhanced by bots and integrations. There are many tools for organizing classes, but they are often hard to manage. They rarely have good communication mechanisms or ability to connect with other tools. This bot allows instructors to host their classes on Discord, combining communication tools with functionality for assignments, scheduling, and office hours. Instructors and students no longer have to go between platforms to view course details, forums, events, calls, and more.

<h2 align="center"> Bot Commands </h2>

`!setInstructor @<member>` Set a server member to be an instructor (Instructor command)

`!ask "<question>"` Ask a question  

`!answer <question_number> "<answer>"` Answer a question  

`!oh enter` Enter an office hour queue as an individual student  

`!oh enter <group_id>` Enter an office hour queue with a group of students  

`!oh exit` Exit the office hour queue  

`!oh next` Go to next student in queue as an instructor (Instructor command)  

`!create` Start creating an event (Instructor command)  


<h2 align="center"> Installation and Running </h2>

#### Tools and Libraries Used
In addition to the packages from [requirements.txt](https://github.com/shikhanair/TeachersPetBot/blob/main/requirements.txt) which need to be installed, please have the following installed on your machine:
* [Python 3.9.7](https://www.python.org/downloads/)
* [Sqlite](https://www.sqlite.org/download.html)

To install and run Teacher's Pet, follow instructions in the [Installation and Testing Guide](https://github.com/shikhanair/TeachersPetBot/blob/main/Installation.md).

<h2 align="center"> Testing </h2>

To run tests on the Teacher's Pet, follow instructions in the [Installation and Testing Guide](https://github.com/shikhanair/TeachersPetBot/blob/main/Installation.md#Run-Tests).

<h2 align="center"> TeachersPetBot Features </h2>

### Initialization

When Teacher's Pet has been added to a new server as a bot, it will do the following:

* Create a new role called Instructor with Administrative permissions if one does not already exist
* Add the owner of the guild to the Instructor role
* Create a #q-and-a channel if one doesn't already exist
* Create a #calendar channel if one doesn't already exist

In addition to this auto-set up, there is also a command which allows a user with the Instructor role to give the same role to another user. This command will only work for users with the Instructor role already (for example, the guild owner).

![alt text](https://github.com/shikhanair/TeachersPetBot/blob/main/images/bot_join.png)

### Q&A
The Q&A functionality allow students to ask and answer questions anonymously. The questions are numbered and when answers are sent, they are combined with the question so they can be easily found. Answers are also marked with `Student Ans` and `Instructor Ans` to distinguish between the sources.  
To ask a question, type `!ask "Question"` in the #q-and-a channel. Example: `!ask "When is the midterm?"`.  
![image](https://user-images.githubusercontent.com/32313919/135383816-430792aa-b8c3-4d6b-8176-1621293d089e.png)  
To answer a question type `!answer <question_number> "Answer"` in the #q-and-a channel. Example: `!answer 1 "Oct 12"`.  
Student answer:  
![image](https://user-images.githubusercontent.com/32313919/135383913-4a7431c3-9e14-466b-9a07-683df39bc1bc.png)  
Instructor answer:  
![image](https://user-images.githubusercontent.com/32313919/135383932-551850ef-6f6c-4349-b3a4-d36ce583de14.png)


### Events/Calendar
Events are items relevant to a class that are time-sensitive. Currently, the types of events include office hours, exams, and assignments. Events in a class are kept track of, and assignments/exams are displayed in a calendar for students and instructors to see.

Events can be created by instructors. Creation of an event can be initiated in the private `instructor-commands` channel with the `!create` command. The bot will ask the instructor about various details for the event. Once the event is created, it should exist persistently within the system and will be added to the event list.

The calendar is updated at the creation of any new event that gets displayed on the calendar. Everything is ordered by date and sorted into two categories, past events and future events. Links attached to assignments are displayed in the calendar as well. The footer of the calendar is tagged with the last time it was updated.

![image](https://github.com/shikhanair/TeachersPetBot/blob/main/images/calendar.png)

### Office Hours
The bot contains functionality for handling TA office hours. After a TA office hour event is added and it is time for a TA's office hour to open, the bot will automatically create office hour channels in the server, allowing students to enter the office hour queue and instructors to help students based on the queue. Once the closing time for the office hour is reached, the channels related to the TA's office hour are automatically deleted.

##### Entering an office hour (as a student)
Students may wish to receive individual help from a TA or they may want to join other students for help as a group (when they need help with a group project, etc); TeachersPetBot supports both of these use cases. A student may enter the queue as an individual using the `!oh enter` command within the text channel for an ongoing office hour. Upon doing so, a new group will be created and the student will become the sole member of that group. Student may enter existing groups by inputting `!oh enter <group_id>`, where `group_id` is the ID of the group the student wishes to join (group IDs will be displayed in the queue). Once it is an individual's (or group's) turn to be helped by the instructor, all members of the group will be invited into a voice channel where they will be able to talk with the TA.

##### Exiting the office hour queue (as a student)
A student may wish to exit the office hour queue for whatever reason; they may do so by typing `!oh exit` in the channel they are in the queue for.

##### Traversing the queue (as an instructor)
Once the instructor is ready to help the next student in the queue, they may enter `!oh next` in the office hour text channel. Upon doing so, DMs will be sent to all group members next in the queue notifying them that it is their turn, and they will be able to enter the office hour voice channel.


### Profanity Censoring 

Using the Python package better-profanity, Teacher's Pet will catch profane words sent by members of the guild, delete the message, and re-send the exact message with the bad word(s) censored out. It will also catch profane words in messages which have been edited to incude bad words. This package supports censoring based off any non-alphabetical word dividers and swears with custom characters. NOTE: Currently the Bot does not censor swears which have had extra alphabetical characters added.

![alt text](https://github.com/shikhanair/TeachersPetBot/blob/main/images/profanity_example.PNG)

<h2 align="center"> Future Scope </h2>

This bot has endless possibilities for functionality. Features which we are interested in adding but did not have time for include but are not limited to:
* Class Polls
* Multi-Guild Handling
* Cloud Hosting
* Detailed Error Handling

For a full list of future features, upgrades, and bug fixes, please visit our [Project 1 Board](https://github.com/shikhanair/TeachersPetBot/projects/1).

<h2 align="center"> How to Contribute? </h2>

Check out our [CONTRIBUTING.md](https://github.com/shikhanair/TeachersPetBot/blob/main/CONTRIBUTING.md) for instructions on contributing to this repo and helping enhance this Discord Bot, as well as our [Code of Conduct](https://github.com/shikhanair/TeachersPetBot/blob/main/CODE_OF_CONDUCT.md) guidelines.

<h2 align="center"> License </h2>

This project is licensed under the [MIT License](https://github.com/shikhanair/TeachersPetBot/blob/main/LICENSE).

<h2></h2>

<h3> Team Members </h3>

#### Pradhan Chetan
#### Tanya Chu
#### Steve Jones
#### Shikha Nair
#### Alex Snezhko

