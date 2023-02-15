# HomeCooked

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

UPDATE Posts SET consumerid=userid, available=False, compleated=timeStamp WHERE postid=postid;

SELECT MAX(postid) FROM Posts; //needs work, deff not right (probs just going to use a volitile variable)
```