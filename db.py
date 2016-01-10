import redis
import datetime

UNVOTED = "unvoted_question_list"
QUESTION_SET = "question_set"
SCORED_QUESTION_SET = "scored_question_set"
MAX_UNVOTED_QUESTIONS = 100

def connect(host='localhost', port=6379, db=0):
  return redis.StrictRedis(host, port, db)

def _next_id(connection):
  return connection.incr("question_id")

def ensure_max_questions(connection, max_size):
  length = connection.llen(UNVOTED)
  if length >= max_size:
    question_hash_key = connection.rpop(UNVOTED)
    connection.srem(QUESTION_SET, question_hash_key)
    connection.zrem(SCORED_QUESTION_SET, question_hash_key)
    connection.delete(question_hash_key)

def store_question(connection, question):
  ensure_max_questions(connection, MAX_UNVOTED_QUESTIONS)

  id = _next_id(connection)
  question_hash_key = "question:%s" % id
  question["id"] = id
  question["date"] = datetime.datetime.now()

  p = connection.pipeline()

  p.hmset(question_hash_key, question)
  p.lpush(UNVOTED, question_hash_key)
  p.sadd(QUESTION_SET, question_hash_key)
  p.zadd(SCORED_QUESTION_SET, 0, question_hash_key)
  p.execute()

  return question

def random_question(connection):
  key = connection.srandmember(QUESTION_SET)
  return connection.hgetall(key)

def vote_question(connection, question_id):
  question_hash_key = "question:%s" % question_id

  if connection.exists(question_hash_key):
    p = connection.pipeline()
    p.hincrby(question_hash_key, "votes", 1)
    p.zincrby(SCORED_QUESTION_SET, question_hash_key, 1)
    p.lrem(UNVOTED, 1, question_hash_key)
    p.execute()

    return connection.hgetall(question_hash_key)

def list_questions(connection, max_num=10):
  question_ids = connection.zrevrange(SCORED_QUESTION_SET, 0, max_num)
  return [connection.hgetall(question_id) for question_id in question_ids]
