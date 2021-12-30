# ER Model
![Alt Image](/Docs/DataBase/Images/ER_Diagram.png)
# Description of database
We have four entities: user_profile_user(Information about user), posts_post(Description about posts), posts_hashtag_post(Keep information about hashtags related to post), posts_hashtag(Information about hashtags)  
Each entity has attributes.
User_profile_user: Id(Privacy key), Username(Login) its UNIQUE, password(Password), FirstName, LastName, Pantronymic, Email its UNIQUE, Is_active, Is_admin, RegistrationDate(automatically), Country  
Posts_post: Id(Privace key), Text(part of posts text), Created_date, Is_active, Is_favourite(Like), user_id(foreign key).  
Posts_hashtag_post: Id(Privacy key), HashTag_id(foreign key), Post_id(foreign key) 
Posts_hashtag: Id(privacy key), Name(name of hashtag)  
I have one-to-many relationship between entires. Because user can have a lot of post and posts can have a lot of hashtags  
All attributes are unambiguous.  
# EER Model  
![Alt Image](/Docs/DataBase/Images/Даталогическая_модель.png)