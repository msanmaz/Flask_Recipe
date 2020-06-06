import requests
import json
from flask import Flask, jsonify, request, render_template, redirect, url_for, make_response
from flask_cors import CORS



app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})



def getSearchURL(q,url):
    try:
        import urlparse
        from urllib import urlencode
    except:  # For Python 3
        import urllib.parse as urlparse
        from urllib.parse import urlencode

    params = {'ingredients': q, 'apiKey': '9d90cc9dd21c45edb7f2f725d0554fd8'}

    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urlencode(query)

    return urlparse.urlunparse(url_parts)





@app.route('/' , methods=['GET', 'POST'])
def SearchRecipe():
    if request.method == 'POST':
        url = "https://api.spoonacular.com/recipes/findByIngredients?"
        # url = "https://gist.githubusercontent.com/msanmaz/b11e042f76d2d7f7c54a57b5c857bbbf/raw/29a1fa7747967cea79d1db7bce657a73a3944947/gistfile1.txt"
        query = request.form['ing_name']
        r = requests.get(getSearchURL(query,url))
        data = r.json()
        return render_template('index.html', response = data) if data != [] else render_template(
            'index.html', response='')
    return render_template('index.html')



def getRecipeURL(query,url):
    try:
        import urlparse
        from urllib import urlencode
    except:  # For Python 3
        import urllib.parse as urlparse
        from urllib.parse import urlencode

    params = {'ids': query, 'apiKey': '9d90cc9dd21c45edb7f2f725d0554fd8'}

    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urlencode(query)

    return urlparse.urlunparse(url_parts)

@app.route('/recipe/<recipe_id>', methods=['GET'])
def recipe(recipe_id):
    query =recipe_id
    url = "https://api.spoonacular.com/recipes/informationBulk?ids="+recipe_id+"&includeNutrition=true"
    r = requests.get(getRecipeURL(query,url))
    data = r.json()
    print(data)
    make_response(render_template("recipelist.html", recipe_id=json.dumps(data)),200)