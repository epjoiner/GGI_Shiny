### This is code that I got from LLMs (so far just Anthropic Claude) 

from treelib import Tree

class IDGenerator:
    def __init__(self):
        self.counter = 0
    
    def generate(self, params=None):
        self.counter += 1
        if params:
            return f"{hash(params)}_{self.counter}"
        return f"node_{self.counter}"

def build_tree(tree, parent_id, id_gen, depth, max_depth, params=None, children_generator=None):
    if depth >= max_depth:
        return
    
    node_id = id_gen.generate(params)
    tree.create_node(
        tag=f"Node {node_id}", 
        identifier=node_id, 
        parent=parent_id, 
        data=params
    )
    
    # If no children generator is provided, use a default that creates no children
    if children_generator is None:
        return
    
    # Generate children based on the provided generator function
    for child_params in children_generator(depth, params):
        build_tree(
            tree, node_id, id_gen, 
            depth + 1, max_depth, 
            params=child_params, 
            children_generator=children_generator
        )

def main():
    # Example of a children generator that creates 3-5 children at each level
    def dynamic_children_generator(depth, parent_params):
        import random
        # Number of children varies between 3 and 5
        num_children = random.randint(3, 5)
        return [
            (depth, f'child_{i}') 
            for i in range(num_children)
        ]
    
    # Another example of a fixed children generator
    def fixed_children_generator(depth, parent_params):
        return [
            (depth, 'science'),
            (depth, 'math'),
            (depth, 'literature')
        ]
    
    # Create and build trees
    tree1 = Tree()
    tree2 = Tree()
    
    id_gen1 = IDGenerator()
    id_gen2 = IDGenerator()
    
    # Build a tree with random number of children
    build_tree(
        tree1, None, id_gen1, 0, 3, 
        children_generator=dynamic_children_generator
    )
    
    # Build a tree with fixed children
    build_tree(
        tree2, None, id_gen2, 0, 3, 
        children_generator=fixed_children_generator
    )
    
    print("Tree with Random Number of Children:")
    tree1.show()
    
    print("\nTree with Fixed Children:")
    tree2.show()

if __name__ == "__main__":
    main()