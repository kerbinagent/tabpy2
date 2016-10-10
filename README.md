# tabpy2

## 1. Introduction
tabpy2 is an online tabulation software. Currently it only supports powermatch based [WSDC](http://schoolsdebate.com/) tournament.
Current Features include:
1. Online Registration
2. Online ballot input
3. Automated Match-Up (pairing and judge assignments)
4. Manual Manipulation of Match-Up
5. Online feedback on judge/tournament
6. Showing final tab

The website has a navbar at top of every page. On the navbar, "Registration" is for team registration, "Tournament" redirects to the homepage, "Feedback" is for judge and tournament feedback, "Admin" redirects to the admin panel. At the top right corner is the login button for judges/admin

## 2. Tournament Set-up
### 2.1 User account Set-up
There are two type of users that needs an account:
- The Admin
- Judges

#### 2.1.1 The Admin account
This account has access to:
- Tournament Setting (view and add/edit)
- Judges (view and add)
- Rooms (view and add)
- Schools (view and add)
- Current Match-Up (view and edit)
- Past Match-Up (view)
- All ballots in the current round (view and add/edit)
- Past ballots (view)

Register this account by clicking "login" on the navbar and then click "Register" (or visit "/admpanel/registration"). You need to provide correct admin code given to you prior to tournament to register an Admin Account. Choose none at the judge selection item. MULTIPLE admin accounts are allowed.

#### 2.1.2 Judge account
This account has access to:
- Individual current ballot (view and edit)

Register this account by clicking "login" on the navbar and then click "Register" (or visit "/admpanel/registration"). You should provide correct judge code to your judges for them to register an Judge Account. Let them choose the name of the judge they are registering at the judge selection item. Each judge can only register ONE judge account.

### 2.2 Initialization

*This requires admin login*

To Start a tournament, you need:
- Enough Rooms
- Enough Judges
- At least one school (it can be open)
- More than two teams

If any one of the above is missing, anyone who is visiting the homepage will be redirected to "/admpanel/init" to finish the work (see further notes to view the complete list of possible errors). He will need to login as admin to finish initialization. Here he can see a initialization page that contains 4 tabs:
1. General: show all missing stuff
2. Judge: show all judges and a button to add new judge
3. Room: show all rooms and a button to add new room
4. School: show all schools and a button to add new school

If everything is initialized, the admin can click Admin on the navbar to go to admin panel.

### 2.3 Team Registration

Registration page can be viewed by clicking "Registration" on the navbar. **Remember to add at least one school before you give the website to possible debaters**

Currently we support recording of the following details of a team:

- name of three speakers
- email and phone of the contact person
- novice status for the entire team and for individual speakers

## 3. Run a round of debate

### 3.1 Admin Panel

*This requires admin login*

Admin runs the tournament through Admin Panel ("Admin" on the navbar).

The Admin Panel contains the following tabs:
- Ballot

  View all ballots from the current round and previous rounds here. For current ballot, you can click edit to edit the ballot

- Judge

  Check if all judges have turned in their ballots.

- Matchup

  A preview of Match-Ups for current round

- General Setting

  Update general setting of the tournament, including:
  - Name of Tournament
  - Maximum of margin
  - Max and min scores
  - Total rounds
  - Number of breaking teams
  - Number of breaking novices
  - Registration open or closed
  - Tab released or not
  - admin code and judge code for user registration

### 3.2 Collect Ballots

*This requires admin login*

Click on the judge tab in admin panel to view judges that havn't turned in their ballots. Once all ballots are collectd, there will be a button for you generate a preview of Match-Ups

### 3.3 Modify Match-Ups

*This requires admin login*

After you have generated Match-Ups, go to matchup tab to view all the Match-Ups for the coming round. Edit if you want. **To ensure fairness, it is strong advised that you DO NOT change the pairing of the automated matchup.** However, it's ok to change judges manually.

When you are done, click the button provided to generate the actual ballots for this round.

**When you see any error message displayed, DO NOT PROCEED**

## 4. Enter Result

Judges should enter their ballots online after logins

### 4.1 Judge login

You need to tell your judges to register an account (see 2.1.2) before login. To login, click on login on the navbar.

### 4.2 Fill in ballots

*This requires judge login*

Tell your judges to go to the homepage. Click the button prepared for them to fetch their ballots and fill them. A number of checks are already set to prevent mistakes. See further notes to view a complete list of error prevention we use in ballots

## 5. Fix mistakes

Human makes mistakes. We have a number of ways to make remedy for mistakes in tournament

### 5.1 Judge and wrong ballot

*This requires judge login*

The judge can edit their current round's ballot at any time PRIOR to next round's ballot come out. However, as explained earlier, as we have a two step process for ballot generation (matchup review and ballot creation, see 3.2 and 3.3), it may be possible that the judge update their ballots before the final ballots are out but **AFTER** the matchup previews have been generated (see further explanation in further notes). Thus:

**ALWAYS CONTACT THE ADMIN BEFORE UPDATE YOUR BALLOT**

### 5.2 Admin and wrong ballot

*This requires admin login*

The admin can view all ballots and edit them at Admin Panel. The same with judge, **NO EDIT AFTER Match-Up PREVIEW**

## 6. Installation

That version uses MySQL as database instead of the default sqlite3. If you want to run the software on your own (or do some customization), Remember to turn debug off (some idea of django/python is strongly recommended in that case)

## 7. Further notes
- Possible errors in initialization
  - No Tournament Setting
  - No school
  - Judge not enough
  - Room not enough
  - Odd team number (admin can solve this by registering a swing team)
- Current ballot validation:
  - max margin
  - max and min score (reply's limit is a half of that of normal speeches)
  - winner with lower score
  - same score
- Two step Match-Up explanation

  The software undergoes two steps to generate next round's ballot:

  1. In the judge tab, when you click the button. **This is when every ballots are collected, scores sumed up and added to team and individual total.** This step creates a preview of matchup
  2. In the matchup tab, when you click the button. Here the software takes the matchups after your manipulation and generates ballots for the next round

  THis means that any edit of ballot after the first step **WILL HAVE NO EFFECT ON THE TEAM TOTAL SCORE AND INDIVIDUAL TOTAL SCORE**, which is why all ballot editting should happen **BEFORE STEP ONE**

- Current Match-Up mechanism is the following:
  1. Teams with the same winning records are put into same pool
  2. If the pool contains odd number of teams, the team in the next lower pool with highest speaker points will be pulled up
  3. Teams can only be pulled up once unless all the teams in the pool are pulled up
  4. In a pool, teams are paired by "folding": the highest match the lowest
  5. In a pairing, the mechanism that decides prop/oppo is the following:
    1. The two teams are first given a prop/oppo position randomly
    2. For each pairing, check the numbers of props each team has already got. If it is desirable for both team to be assgined on         the other side, swap the teams' positions
    3. Check if any of the team has gotten four prop/oppo consecutively including the current round. If so, swap the teams' positions
- Planned Update
  - Updated breaking system
  - Customized team tagging
  - Alternate matchup mechanisms
- Support

  If anything else that troubles you, feel free to shoot an email to wanghouze@uchicago.edu
