from bottle import route, run, HTTPError, HTTPResponse, Bottle, request
import os
import random
import sentry_sdk
from sentry_sdk.integrations.bottle import BottleIntegration
from sayings import *

# app = Bottle()

def generate_message():
    return "Сегодня уже не вчера, ещё не завтра"

def generate_random_message():
  return str(random.choice(beginnings) + random.choice(subjects) + random.choice(verbs) + random.choice(actions) + random.choice(ends))


@route("/")
def index():
#     html = """
# <!doctype html>
# <html lang="en">
#   <head>
#     <title>Генератор утверждений</title>
#   </head>
#   <body>
#     <div class="container">
#       <h1>Коллеги, добрый день!</h1>
#       <p>{}</p>
#       <p class="small">Чтобы обновить это заявление, обновите страницу</p>
#     </div>
#   </body>
# </html>
# """.format(
#         generate_message()
#     )
    return {
      "message": generate_message()
    }


@route("/api/generate/")
def render_random_message():
    return {
      "message": generate_random_message()
    }


@route("/api/generate/<num:int>")
def render_random_messages(num):
  if num < 21:
    messages_obj = {"message": []}
    for i in range(num):
      messages_obj["message"].append(generate_random_message())
    return messages_obj
  else:
    return "ERROR: Максимальное количество сообщений 20"


@route("/api/roll/<some_id:int>")
def example_api_response(some_id):
    return {"requested_id": some_id, "random_number": random.randrange(some_id)}


@route("/fail")
def fail_route():
  raise RuntimeError("There is an error!")
  return HTTPResponse(status=500, body="Fail page")


@route("/success")
def success_route():
  html = """
<!doctype html>
<html lang="en">
  <head>
    <title>Генератор утверждений</title>
  </head>
  <body>
    <div class="container">
      <h1>Коллеги, добрый день!</h1>
      <p>{}</p>
      <p class="small">Чтобы обновить это заявление, обновите страницу</p>
    </div>
  </body>
</html>
""".format(
        generate_random_message()
    )
  return HTTPResponse(status=200, body=html)


if os.environ.get("APP_LOCATION") == "heroku":
  sentry_sdk.init(
    dsn="https://<key>@o471662.ingest.sentry.io/<project>", # Для интерграции с sentry введите свои данные
    integrations=[BottleIntegration()]
  )
  run(
      host="0.0.0.0",
      port=int(os.environ.get("PORT", 5000)),
      server="gunicorn",
      workers=3,
  )
else:
    run(host="127.0.0.1", port=8000, debug=True)
