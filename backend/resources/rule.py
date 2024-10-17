from flask_restful import Resource, reqparse
from rule_engine import RuleEngine
from ast_nodes import print_ast
from io import StringIO
import sys
from database import Session
from models import Rule


rule_engine = RuleEngine()


class RuleResource(Resource):
    def post(self):
        # Create a request parser to handle input arguments
        parser = reqparse.RequestParser()
        parser.add_argument('rule_name', type=str, required=True, help="Rule name cannot be blank!")
        parser.add_argument('rule_string', type=str, required=True, help="Rule string cannot be blank!")
        args = parser.parse_args()
        
        # Extract the rule name and rule string from the parsed arguments
        rule_name = args['rule_name']
        rule_string = args['rule_string']
        
        # Create the rule and get the AST as a Node object
        rule = rule_engine.create_rule(rule_string)
        
        # Prepare the tree-like string output
        output = StringIO()
        sys.stdout = output
        
        print_ast(rule)  # Print the AST to capture it in output
        
        # Reset redirect
        sys.stdout = sys.__stdout__
        
        # Get printed output for tree representation
        ast_tree = output.getvalue()
        # Save the rule to the database
        session = Session()  # Create a new session
        existing_rule = session.query(Rule).filter_by(name=rule_name).first()
        
        if existing_rule:
            session.close()  # Close the session
            # If the rule name already exists, return an error response
            return {
                'message': f"Rule with name '{rule_name}' already exists. Please choose a different name."
            }, 400  # 400 Bad Request
        new_rule = Rule(name=args['rule_name'], rule_string=args['rule_string'], ast=ast_tree)
        session.add(new_rule)  # Add the new rule to the session
        session.commit()  # Commit the session to save the rule
        session.close()  # Close the session
        
        # Return the response with 'ast_tree' and the rule name
        return {
            'rule_name': rule_name,
            'ast_tree': ast_tree.strip(),  # Ensure to strip any leading/trailing whitespace
            'message': 'Rule created successfully'
        }, 201
class CombineRulesResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('rule_names', type=str, required=True,location='json', help="Rule name cannot be blank!")
        parser.add_argument('rules', type=list, location='json', required=True, help="Rules list cannot be blank!")
        parser.add_argument('operators', type=list, location='json', required=True, help="Operator must be either 'AND' or 'OR'!")
        args = parser.parse_args()
        operator=args['operators']

        combined_ast = rule_engine.combine_rules(args['rules'], operator)
        combined_ast2 = rule_engine.create_rule(combined_ast)
        output = StringIO()
        sys.stdout = output
        
        print_ast(combined_ast2)  # Print the AST to capture it in output
        
        # Reset redirect
        sys.stdout = sys.__stdout__
        
        # Get printed output for tree representation
        ast_tree = output.getvalue()
        session = Session()
        existing_rule = session.query(Rule).filter_by(name=args['rule_names']).first()
        
        if existing_rule:
            session.close()  # Close the session
            # If the rule name already exists, return an error response
            return {
                'message': f"Rule with name '{args['rule_names']}' already exists. Please choose a different name."
            }, 400  # 400 Bad Request
        new_rule = Rule(name=args['rule_names'], rule_string=combined_ast, ast=ast_tree)
        session.add(new_rule)  # Add the new rule to the session
        session.commit()  # Commit the session to save the rule
        session.close()        
        return {'message': 'Rules combined  successfully','combined_ast':ast_tree }, 201

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
class GetRulesResource(Resource):
    def get(self):
        session = Session()
        rules = session.query(Rule).all()  # Fetch all rules from the database
        session.close()
        return [{'id': rule.id, 'name': rule.name, 'rule_string': rule.rule_string, 'ast': rule.ast} for rule in rules], 200
    