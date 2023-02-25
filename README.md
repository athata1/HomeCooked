# HomeCooked

## data structures
### User:
- user_id               (key)
- user_uname            (str)
- user_email            (str)
- user_pass             (str)
- user_address          (str)
- user_bio              (str)
- user_state            (str)
- user_city             (str)

### Event:
- event_id              (key)
- event_name            (str)
- event_desc            (str)
- event_date            (date)
- event_time            (time)
- event_location        (str)
- event_capacity        (int)
- event_host            (User)

### Recipe:
- recipe_id             (key)
- recipe_desc           (str)
- recipe_user           (User)
- recipe_name           (str)
- recipe_ingredients    (str)
- recipe_img            (str)

### Post:
- post_id               (key)
- post_title            (str)
- post_desc             (str)
- post_producer         (User)
- post_consumer         (User)
- post_created          (datetime)
- post_completed        (datetime)
- post_recipe           (Recipe)
- post_available        (boolean)

### Review:
- review_id             (key)
- review_desc           (str)
- review_user           (User)
- review_recipe         (recipe)
- review_rating         (int)
- review_post           (Post)

### Message:
- message_id            (key)
- message               (str)
- message_sender        (User)
- message_recipient     (User)
- message_sent          (datetime)

### DiscussionBoard:
- discussion_id         (key)
- discussion_desc       (str)
- discussion_sender     (User)
- discussion_event      (Event)
- discussion_data       (date)

## Urls:
/posts/      gives a list of all posts <br>
/posts/db<br>
    GET Request:<br>
        [producer] - posts producer by a user<br>
        [userid] - posts including a user<br>
        [id] - a specific post with a specific id<br>
        [] - all posts<br>
    POST Request:<br>
        [producer, recipe, title(str), desc(str)] - creates a new post<br>
        [id(int), title|desc|producer|consumer|recipe] - updates an existing post<br>
/users/<br>
    GET Request:<br>
        [email|uname] - finds a user by email or username<br>
        [id] - finds the coresponding user<br>
        [city, state] - finds all users in the coresponding city and state<br>
        TODO: [email|uname, pass] - confirm the email/uname pass works.<br>
    POST Request:<br>
        [email, uname, pass, *address, *bio, *state, *city] - creates a new user (TODO: confirm email and uname aren't taken)<br>
        [id|prev_email|prev_uname, email|uname|pass|address|bio|city|state] - updates an existing user<br>

###format:
/path<br>
    Request type<br>
        [param_option1|param_option2, *optional_param] - description<br>
