from flask import Flask, send_from_directory
from flask_restful import Api
from resources.rule import RuleResource, CombineRulesResource, EvaluateRuleResource, GetRulesResource
from database import Session
from flask_cors import CORS
import webbrowser

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)  # Enable CORS for all routes

api = Api(app)
session = Session()

# Define API endpoints
api.add_resource(GetRulesResource, '/get_rules')
api.add_resource(RuleResource, '/create_rule')
api.add_resource(CombineRulesResource, '/combine_rules')
api.add_resource(EvaluateRuleResource, '/evaluate_rule')

# Serve index.html when the root URL is accessed
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Open the browser manually
    webbrowser.open('http://127.0.0.1:5000/')  # Open the browser without a timer
    app.run(debug=True)
