# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
POST '/questions'
POST '/questions/search'
POST '/categories/<int:id>/questions'
POST '/quizzes'
DELETE '/questions/<int:question_id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions' or 'questions?page=number'
- Fetches all questions paginated with 10 questions per response
- Request Arguments: None
- Returns: An object that has 2 objects, categories & questions. The response is paginated with 10 questions per response. The categories object has key:value pairs of id & category_string. The questions object has an array of objects. Each object in that array has key:value pairs of Id and Id_Number, answer and answer_String, category & category_Number, difficulty & difficulty_Number.

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ], 
  "success": true, 
  "total_questions": 17
}


POST '/questions'
- Adds a question to DB
- Request Arguments: requires 4 arguments; question:String, answer:String,difficulty:String, category:String
{"question": "testQ3", "answer": "testA3", "difficulty": "3", "category": "3"}
- Returns: An object keys created,questions,success &total_questions. The key created has value containing the id of the created question. The key questions has value containing of an array of object containging all wuestions available paginated by 10. The key success has value containing of success state of request. Finally, The key total_questions has value containing size of questions available as a whole in DB.

{
  "created": 28, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 18
}


POST '/questions/search'
- Search questions using the provided keyword
- Request Arguments: requires 1 arguments; a json object with key search:String & value searchKeyword:String
{"search": "bo"}
- Returns: An object containing keys current_category, questions, success & total_questions. The key current_category always has value null. The key questions has value of an array of object containing the found questions matching the search keyword (if any). The key success has value containing of success state of request. The key total_questions has value of number of questions returned in the response

{
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}


POST '/categories/<int:id>/questions'
- Fetches question of specified categories given the categories id in the reqquest path
- Request Arguments: None
- Returns: An object containing keys current_category, questions, success & total_questions. The key current_category has category that we sent its Id in the request (<int:id>/). The key questions has value of an array of object containing the found questions that belong to the precified category (if any). The key success has value containing of success state of request. The key total_questions has value of number of questions returned in the response

{
    "current_category": "Art",
    "questions": [
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "testA3",
            "category": 2,
            "difficulty": 1,
            "id": 26,
            "question": "testQ2"
        }
    ],
    "success": true,
    "total_questions": 2
}


POST '/quizzes'
- Provides a new random question that is not includded in the list of previous_question provided
- Request Arguments: takes a json object with 2 pairs of key value. The first key is previous_questions that has an array containing the Ids of all previous questions played. The second key quiz_category has an object containg 2 pairs of key value; key type has the category of questions, key id has the id of category.
{"previous_questions": [21,3], "quiz_category": {"type": "Science", "id": "1"}}

- Returns: An object containing with 2 pairs of key values. It has 2 keys; question, success. The key question has value of an object containing the next random questions to be displayed. The key success has value containing of success state of request. 
{
  "question": {
    "answer": "Blood", 
    "category": 1, 
    "difficulty": 4, 
    "id": 22, 
    "question": "Hematology is a branch of medicine involving the study of what?"
  }, 
  "success": true
}



DELETE '/questions/<int:question_id>'
- Delete question with the provided ID


{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ], 
  "success": true, 
  "total_questions": 17
}


```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```