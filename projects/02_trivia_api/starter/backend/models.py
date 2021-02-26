import os
from sqlalchemy import Sequence, Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "trivia"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'
  # question_seq = Sequence('questions_id_seq', start=1, increment=1)
  # print('seq ')

  # print('seq ',question_seq.next_value())
  # id = Column(Integer, question_seq, primary_key=True, server_default = question_seq.next_value())
  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(Integer)
  # category = Column(String)

  difficulty = Column(Integer)

  def __init__(self, id,question, answer, category, difficulty):
    # self.id = Sequence('questions_id_seq').next_value()
    self.id=id
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }