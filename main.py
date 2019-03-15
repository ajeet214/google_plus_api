from flask import Flask, jsonify, request
from modules.googleplusactivity_db import ActivitySearch
from modules.people_search_db import PeopleSearch
from modules.googlePlus_profiles_db import ProfileFetch
from modules.googlePlus_profile_post import ProfilePost
from raven.contrib.flask import Sentry

app = Flask(__name__)
sentry = Sentry(app)

# @app.route('/api/v1/profile_id/<string:p_id>')
# def profile(p_id):
#     obj1 = Googleprofile()
#     result = obj1.googleprofile(p_id)
#     return jsonify({'data': result})


@app.route('/api/v1/profile')
def profile():
    query = request.args.get('id')
    obj1 = ProfileFetch()
    result = obj1.db_check(query)
    return jsonify(result)


# @app.route('/api/v1/activity/<string:activity>/<int:count>')
@app.route('/api/v1/search/activity')
def activity():
    query = request.args.get('q')
    # limit = request.args.get('limit')
    obj2 = ActivitySearch()
    result = obj2.db_check(query)
    return jsonify(result)


# @app.route('/api/v1/search/<string:q>')
@app.route('/api/v1/search/profile')
def users():
    query = request.args.get('q')
    obj3 = PeopleSearch()
    result = obj3.db_check(query)
    return jsonify(result)


@app.route('/api/v1/profile/post')
def profile_posts():
    query = request.args.get('id')
    # limit = request.args.get('limit')
    obj2 = ProfilePost()
    result = obj2.post_fetcher(query)
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5006)




