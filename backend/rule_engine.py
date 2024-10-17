# backend/rule_engine.py
import re
from ast_nodes import Node  # Ensure Node class is defined in ast_nodes.py

class RuleEngine:
    def __init__(self):
        self.rules = []

    def create_rule(self, rule_string):
        tokens = self.tokenize(rule_string)  
        ast_root = self.parse_expression(tokens)
        self.rules.append(ast_root)
        return ast_root

    def tokenize(self, rule_string):
        token_specification = [
            ('AND', r'AND'),
            ('OR', r'OR'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('OP', r'<=|>=|!=|==|=|<|>'),
            ('VALUE', r"'[^']*'|\d+"),
            ('IDENT', r'\w+'),
            ('SKIP', r'\s+'),
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join(f'(?P<{kind}>{regex})' for kind, regex in token_specification)
        tokens = []
        for mo in re.finditer(tok_regex, rule_string):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'VALUE':
                value = value.strip("'")  # Remove surrounding quotes from string values
            if kind not in ['SKIP', 'MISMATCH']:
                tokens.append((kind, value))
        
        return tokens

    def parse_expression(self, tokens):
        self.tokens = tokens
        self.pos = 0
        return self.logical_or()

    def match(self, expected_kind):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_kind:
            token = self.tokens[self.pos]
            self.pos += 1  # Move to the next token
            return token
        raise SyntaxError(f"Expected {expected_kind} but found {self.tokens[self.pos][0] if self.pos < len(self.tokens) else 'EOF'}")
    def logical_or(self):
        node = self.logical_and()  # Parse first AND expression
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'OR':
            op = self.match('OR')
            right = self.logical_and()  # Parse the next AND expression
            node = Node('operator', left=node, right=right, value='OR')
        return node

    def logical_and(self):
        node = self.condition()  # Start with a condition
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'AND':
            op = self.match('AND')
            right = self.condition()  # Get the next condition
            node = Node('operator', left=node, right=right, value='AND')
        return node

    def condition(self):
        # Check for parentheses but don't require them
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'LPAREN':
            self.match('LPAREN')
            node = self.logical_or()
            self.match('RPAREN')
            return node

        # Otherwise, match a condition without parentheses
        ident = self.match('IDENT')
        if ident is None:
            raise SyntaxError("Expected IDENT")

        op = self.match('OP')
        if op is None:
            raise SyntaxError("Expected OP")

        value = self.match('VALUE')
        if value is None:
            raise SyntaxError("Expected VALUE")

        return Node('operand', value=(ident[1], op[1], value[1]))



    def combine_rules(self, rules, operator='AND'):
        """
        Combines multiple rules into a single AST node.

        :param rules: A list of rule strings.
        :param operator: The operator to combine the rules ('AND' or 'OR').
        :return: The combined AST root node.
        """
        ast_roots = [self.create_rule(rule) for rule in rules]
        if not ast_roots:
            return None
        combined = ast_roots[0]
        for ast_root in ast_roots[1:]:
            combined = Node('operator', left=combined, right=ast_root, value=operator)
        return combined

    def safe_eval(self, data_value, op, value):
        """
        Safely evaluates a comparison between a data value and a rule value.

        :param data_value: The actual value from the data.
        :param op: The comparison operator.
        :param value: The value to compare against.
        :return: True if the comparison holds, otherwise False.
        """
        # Convert the value to the appropriate type (int or float)
        try:
            value = int(value)  # Try to convert to int
        except ValueError:
            # If it fails, it might be a string; you can handle this case as needed
            pass

        if op == '==':
            return data_value == value
        elif op == '!=':
            return data_value != value
        elif op == '<':
            return data_value < value
        elif op == '<=':
            return data_value <= value
        elif op == '>':
            return data_value > value
        elif op == '>=':
            return data_value >= value
        return False

    def evaluate_rule(self, ast_root, data):
        if not isinstance(ast_root, Node):
            raise TypeError(f"Expected a Node object, got {type(ast_root)}")
            
        if ast_root.type == 'operator':
            left = self.evaluate_rule(ast_root.left, data)
            right = self.evaluate_rule(ast_root.right, data)
            if ast_root.value == 'AND':
                return left and right
            elif ast_root.value == 'OR':
                return left or right
        elif ast_root.type == 'operand':
            field, op, value = ast_root.value
            data_value = data.get(field)
            if data_value is None:
                return False
            return self.safe_eval(data_value, op, value)
        return False
