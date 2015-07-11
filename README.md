#![the hunt-logo 1](https://cloud.githubusercontent.com/assets/11861609/8622322/aae7563e-26df-11e5-952b-fe647a505921.png)

To minimize the chaotic experience job seekers​ ​face, The Hunt provides a fun and interactive website for a job seeker to easily track, view and organize successful job applications. The Hunt lets a user bookmark job vacancies/listings, track progress on active job applications, store relevant supporting documents for a job application and take notes during the interview process. ​​

This app was built in 4.5 weeks during the Spring 2015 cohort of Hackbright Academy's Software Engineering Fellowship.

###**Technology Stack**
####Backend:
* Python 
* Flask
* SQLAlchemy
* SQLite

####Frontend:
* JavaScript 
* HTML
* Bootstrap
* CSS 
* Jinja

#![features-logo 1](https://cloud.githubusercontent.com/assets/11861609/8629033/79ea7fde-270c-11e5-97dc-e7b18d98e382.png)
###Register
New users are prompted to register to the site. This page collects the user's profile information and commits them to the User table within the app's database.
![the_hunt_register_page](https://cloud.githubusercontent.com/assets/11861609/8622882/86a685e4-26e2-11e5-8f5a-662ec0e9e3c5.gif)
###Log In 
Once a user's information is stored within the SQL built database, the user is allowed to log-in and they're stored within a flask session. This helps to track a user's committed positions, notes and status updates into the database. 
![the_hunt_log-in](https://cloud.githubusercontent.com/assets/11861609/8627315/14291b4a-26ff-11e5-8b9a-6cc247fb3268.gif)
###Dashboard
A user's dashboard is customized with Jinja reflecting the information stored within a user's and position table. From the dashboard, a user can delete a position, add a position, and review the positions stored within the position table in our database. 
![the_hunt_dashboard](https://cloud.githubusercontent.com/assets/11861609/8627729/a7768796-2701-11e5-8773-f8ee3bfb89e3.gif)
###Add a Position
 A user has the ability to bookmark positions they wish to eventually apply to by filling out the 'Add a Position' page:
![the_hunt_add_a_position](https://cloud.githubusercontent.com/assets/11861609/8627860/cb8f941e-2702-11e5-9480-f0f3773a676b.gif)
###Position Page
All of the user's positions are stored within the position table inside our database and rendered to Position page's HTML. From this view, A user can select a specific role and make updates on that role's expanded page view. 
![the_hunt_position_page](https://cloud.githubusercontent.com/assets/11861609/8630541/f9be3278-271b-11e5-867b-a942b3390a61.gif)
###Update an Application's Status and Store Contacts to a specific role
The Hunt provides the user the ability to track their progress in completing an application. A user has the options to update that the application status on a specific position to: not yet started, in progress, complete or rejected. In addition to, a user has the ability to attach a contact to a specific role -- contact such as: recruiters, colleagues,associates, etc.  
![the hunt application status](https://cloud.githubusercontent.com/assets/11861609/8631879/897e08cc-2738-11e5-8e74-d0cda6671bdb.gif)
###Documents and Notes 
The Hunt provides a user the ability to store a specific document relative to a position. For example, at times a job seeker may not remember which resume they have sent in the past to a specific role. The Hunt provides the user the ability to store their documents to a position within the database. 
![the hunt documents and notes](https://cloud.githubusercontent.com/assets/11861609/8631947/5ea2c65e-273a-11e5-99df-05c3dbb87169.gif)
![the hunt documents and notes2](https://cloud.githubusercontent.com/assets/11861609/8631958/ebc1d44e-273a-11e5-81eb-18fc8441b9a1.gif)
###Delete and Log Out 
The Hunt provides the user the ability to delete a specific role from the database and log out of their flask session. All actions performed within their flask session is committed and stored within the database. 
![the hunt delete and log out](https://cloud.githubusercontent.com/assets/11861609/8631989/f7ea1d84-273b-11e5-9149-89ad057b0d47.gif)
#![get the hunt-logo](https://cloud.githubusercontent.com/assets/11861609/8629119/63125df8-270d-11e5-84c3-2fb6d8c4d9e0.png)
Clone or fork this repo: 
```
http://github.com/violadolayinka/The_Hunt.git
```
Create and activate a virtual environment inside your project directory:
```
virtualenv env

source env/bin/activate
```
Install the requirements:
```
pip install -r requirements.txt
```
Create the database:
```
python -i model.py

db.create_all()

quit()
```
Run you local server:
```
python server.py
```
Navigate to ```localhost:5000``` to work towards a successful job hunt!
#![next steps-logo](https://cloud.githubusercontent.com/assets/11861609/8629165/cdbe89d8-270d-11e5-8b55-10a3001653bc.png)
Deployment coming soon! In the meantime, check out the [issues log](https://github.com/violadolayinka/The_Hunt/issues) for this project to see what's next!
