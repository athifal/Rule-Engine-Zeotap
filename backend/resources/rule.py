from flask_restful import Resource, reqparse
from rule_engine import RuleEngine
from ast_nodes import print_ast
from io import StringIO
import sys

rule_engine = RuleEngine()


class RuleResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rule_string', type=str, required=True, help="Rule string cannot be blank!")
        args = parser.parse_args()
        
        # Create the rule and get the AST as a Node object
        rule = rule_engine.create_rule(args['rule_string'])
        
        # Prepare the tree-like string output
        output = StringIO()
        sys.stdout = output
        
        print_ast(rule)  # Print the AST to capture it in output
        
        # Reset redirect
        sys.stdout = sys.__stdout__
        
        # Get printed output for tree representation
        ast_tree = output.getvalue()
        
        # Return the response with 'ast_tree' instead of 'ast'
        return {
            'ast_tree': ast_tree.strip(),  # Ensure to strip any leading/trailing whitespace
            'message': 'Rule created successfully'
        }, 201
class CombineRulesResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rules', type=list, location='json', required=True, help="Rules list cannot be blank!")
        args = parser.parse_args()
        combined_ast = rule_engine.combine_rules(args['rules'])
        return {'combined_ast': str(combined_ast)}, 201

class EvaluateRuleResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rule', type=str, required=True, help="Rule cannot be blank!")  # Use 'rule', not 'ast'
        parser.add_argument('data', type=dict, required=True, help="Data cannot be blank!")
        args = parser.parse_args()

        # Step 1: Create the rule (AST) from the rule string
        ast_root = rule_engine.create_rule(args['rule'])

        # Step 2: Call the evaluate_rule function with parsed arguments
        result = rule_engine.evaluate_rule(ast_root, args['data'])
        
        return {'result': result}, 200

    