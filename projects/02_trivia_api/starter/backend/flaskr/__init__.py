import os
import sys

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TO DO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  Done 
  '''
  CORS(app,resources={'/*': {'origins': '*'}})
  # CORS(app)

  '''
  @TO DO: Use the after_request decorator to set Access-Control-Allow
  Done
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,PATCH,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')


    return response

  '''
  @TO DO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def retrieve_categories():
    categories = Category.query.order_by(Category.id).all()
    categories_list = {}
    for category in categories:
        categories_list[category.id] = category.type
  
    return jsonify({
      'success': True,
      'categories': categories_list,
      'total_categories': len(Category.query.all())
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  # TO DO get categories in ques & test

  @app.route('/questions')
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)
    categories = Category.query.all()
    categoriesList = {}
    for category in categories:
        categoriesList[category.id] = category.type
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': categoriesList
    })




  '''
  @TO DO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)

  '''
  @TO DO: 
 Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab. 

  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    print(body)
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    new_difficulty = int(new_difficulty)
    new_category = int(new_category)
    if ((new_question is None) or (new_answer is None)
              or (new_difficulty is None) or (new_category is None)):
      print('empty')
      abort(422)
    try:
      previousId = Question.query.order_by(Question.id.desc()).first()
      currID = int(previousId.id)+1
      print('currID id ', currID)
      question = Question(id=currID,question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
      question.insert()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      })
    except:
      print(sys.exc_info())

      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  # @cross_origin
  def search_question():
    body = request.get_json()
    print(body)
    search = body.get('search', None)
    print(search)
    try:
      if search:
        print("search")

        searchKeyword='%'+search+'%'
        print("searchKey ", searchKeyword)

        selection = Question.query.filter(Question.question.ilike(searchKeyword)).all()
        print(selection)

        current_questions = paginate_questions(request, selection)
        return jsonify({
          'success': True,
          'questions': current_questions,
          "current_category": None,
          'total_questions': len(selection)
        }) 
    except:
      abort(500)
    

  '''
  @TO DO: 
  Create a GET endpoint to get questions based on category. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_based_on_category(id):
    category = Category.query.filter_by(id=id).one_or_none()
    if (category is None):
      abort(400)
    questionsInCategory = Question.query.filter_by(category=category.id).all()
    print("questionsInCategory", len(questionsInCategory))
    paginatedQuestions = paginate_questions(request, questionsInCategory)
    print("paginatedQuestions", len(paginatedQuestions))
    print("all Questions", len(Question.query.all()))
    questions = [question.format() for question in questionsInCategory]

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(questionsInCategory),
      'current_category': category.type
    })


  '''
  @TO DO: 
  Create a POST endpoint to get questions to play the quiz. 
  '''
  def check_if_question_used(question, previous):
    used = False
    for ques in previous:
      if (ques == question.id):
        used = True
    return used
  def get_list_questions_choose_from(category):
    if (category['id'] == 0):
        questions = Question.query.all()
    else:
      questions = Question.query.filter_by(category=category['id']).all()
    return questions
  @app.route('/quizzes', methods=['POST'])
  def get_random_questions():
    body = request.get_json()
    print(body)
    previous_question = body.get('previous_questions', None)    
    category = body.get('quiz_category', None)    
    print("previous_question")
    print(previous_question)      
    if ((category is None) or (previous_question is None)):
      abort(400)
    questions_choose_from=get_list_questions_choose_from(category)
    random_question = questions_choose_from[random.randrange(0, len(questions_choose_from), 1)]
    while (check_if_question_used(random_question, previous_question)):
      random_question = questions_choose_from[random.randrange(0, len(questions_choose_from), 1)]

    return jsonify({
      'success': True,
      'question': random_question.format()
    })


  '''
  @TO DO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  return app

    