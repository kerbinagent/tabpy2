# tabpy2
An online tabulation system for WSDC format based on PowerMatch. Some features are: online ballot, automated matchup, viewing matchup onlines and viewing the full tab online.
## Starting a Tournament
Start by creating an admin account. If you are assigned a username/password already, use that. If not, create one by 'python manage.py createsuperuser'
### Setting Up
Go to /admin to get started. Go to Tournament_Settings and add the setting for your tournament
For now, you can change:
1. Tournament Name
2. The maximum margin of a ballot
3. The maximum and minimum score of speeches (limit reply score is 1/2 that of normal speech)
4. The total number of breaking teams and breaking novices
5. If the tab is released (at the bottom of all settings, check the tick after the tournament ends)
6. Set whether registration is open
### Inputting
Go to /admin and add a few stuff:
1. School:
You must add at least one school here (open). Teams and Speakers are assigned to schools. If some teams are hybrid, just add a school called open.
2. Team:
You must tell the school of the team. Don't change any of the default values except when the team is novice team. In that case, check that the team is novice.
3. Speaker:
You must give the speaker a name, a team a speaker id and a school.
Speaker id is a UNIQUE integer that is assigned to each speaker.
You can also specify whether the speaker is a novice.
4. Judge:
You must give the judge a name and a code.
The code is a UNIQUE string that has a maximum length of 8. This code should later be given to every judge so that they can fill in their online ballots.
Weight is a number to denote the importance of the judge. Judges with higher weight will get better rooms under the matchup system.
5. Room:
You must give a room its name.
Distance to hall is used in matchup. Better rooms are nearer to the hall. You can also ignore it and left it with its default value 0.
## Registration
When registration is open, give the address /registration to debaters/institutions. Notice that you should manually register Institutions that they can choose from.
## Runing Tournaments
Give the address /tournament to everyone in the tournament (judges, debaters) to run the tournament.
### Changing Judge for matchup
Changing the matchup manually is easy. Go to /admin/ and select 'Room_stats'. You can manually select the room and the chair here. It is highly recommended that you DO NOT change the prop and the oppo team.
### Instruction for Judges
Tell the judges to go to /tournament and input their assigned judge code. The online ballot has many validators and will prevent them from turning stupid ballots.
### Remedy for judge mistakes
In a extremely unlikely circumstance when a judge make a mistake, you can always remedy that at /admin/
There are a number of data you should change accordingly:
1. Go to Team, change total_sp (total speaker points) and total_wl (total wins) for BOTH prop and oppo
2. Go to Speaker, change total_sp(total speaker points) for ALL speakers in the round
3. Go to Speaker Point, change EVERY individual Speaker point data for ALL speakers.
