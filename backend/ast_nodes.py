class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        """
        Initialize a Node.
        
        :param node_type: 'operator' or 'operand'
        :param left: Left child Node
        :param right: Right child Node (for operators)
        :param value: Value for operand nodes
        """
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        if self.type == "operator":
            return f"({self.left} {self.value} {self.right})"
        else:
            return f"{self.value}"
