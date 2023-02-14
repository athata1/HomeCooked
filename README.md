# HomeCooked
## Hawk's Branch,

# Responsibilities:
1. Creating post backends
 - Creating class
 - upon creation, attatch a unique postid to each post
 - add each post to the database
 - Retrieve a post for a unique consumer
 - Query server for specificic meals within a certain area 
2. Creating toggle between consumer and producer modes
3. creating/implimenting a method to ensure no inaprorpriate words are used in posts / recipes / etc.

# Creating post backends:
sql shenanigans:
```
CREATE TABLE Posts(
    postid Number(8),
    producerid Number(16),
    recipeid Number(8),
    consumerid Number(8),
    available Bool(1)
    created date,
    compleated date
);

INSERT INTO Posts (postid, producerid, recipeid, available, created)
VALUES (postid, producerid, recipeid, avialable, timeStamp);

SELECT postid FROM Posts WHERE producerid=userid;

SELECT postid FROM Reviews WHERE postid=postid;

SELECT postid FROM Posts where consumerid=userid;

Update Posts SET consumerid=userid, available=False, compleated=timeStamp WHERE postid=postid;

SELECT MAX(postid) FROM Posts; //needs work, deff not right (probs just going to use a volitile variable)
```