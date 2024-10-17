from flask import Flask
from flask_restful import Api
from resources.rule import RuleResource, CombineRulesResource, EvaluateRuleResource,GetRulesResource
from database import Session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

api = Api(app)
session = Session()

# Define API endpoints
api.add_resource(GetRulesResource, '/get_rules')
api.add_resource(RuleResource, '/create_rule')
api.add_resource(CombineRulesResource, '/combine_rules')
api.add_resource(EvaluateRuleResource, '/evaluate_rule')

if __name__ == '__main__':
    app.run(debug=True)
