class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # Ensure this attribute exists
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        """Convert the Node to a dictionary representation."""
        return {
            'type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None,
        }
    def __repr__(self):
        return f"{self.type}: {self.value}"

  
def print_ast(node, prefix="", is_last=True):
    """Recursively print the AST in a tree-like format with correct indentation."""
    if node is not None:
        # Determine the correct connector (├── for middle items, └── for the last item)
        connector = "└── " if is_last else "├── "

        # Check if the node is an operator or operand
        if node.type == "operator":
            print(prefix + connector + str(node.value))  # Print the operator (AND, OR)
            # Adjust prefix for next level
            new_prefix = prefix + ("    " if is_last else "│   ")
        elif node.type == "operand":
            # Format and print the operand in "field operator value" format
            field, op, value = node.value
            print(prefix + connector + f"{field} {op} {repr(value)}")  # Print field, operator, value
            new_prefix = prefix + ("    " if is_last else "│   ")
        
        # Recursively print the children, adjusting for the last child
        if node.left or node.right:  # If there are children
            if node.left:
                print_ast(node.left, new_prefix, is_last=(node.right is None))  # Left child
            if node.right:
                print_ast(node.right, new_prefix, is_last=True)  # Right child
