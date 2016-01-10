# gutefrage-db-wrapper

## Dependencies

```
$ pip install redis
```

Also requires a redis instance (http://redis.io) running on localhost. You can install docker (http://docker.io) and then run `./start_redis.sh`.

## Usage

```python
import db

# Connect to local redis instance
r = db.connect()

# Write a question to the database
new_question = {
  "title": "Question?",
  "text": "Text..."
}
q = db.store_question(r, new_question)
# Question now has an 'id'
print q["id"]

# Load a random question from the database
q = db.random_question(r)
print q

# Vote for a question
q = db.vote_question(r, q["id"])
print q.votes

# Get a list of all questions
qs = db.list_questions(r)
print qs

```
