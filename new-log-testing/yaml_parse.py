import yaml
from dataclasses import dataclass
from pprint import pprint as print
from yaml.loader import SafeLoader


# value is either a pattern to match on field (type) or an operator to be applied on child nodes
@dataclass
class Node:
    def __init__(
        self,
        value,
        hostname=None,
        strictness=None,
        left=None,
        right=None,
        objective=None,
        label=None,
    ) -> None:
        self.label = label
        self.value = value
        self.objective = objective
        self.left = left
        self.right = right
        self.strictness = strictness
        self.hostname = hostname

    @classmethod
    def from_yaml(cls, loader: SafeLoader, node):
        data = loader.construct_mapping(node)
        return cls(**data)

    def __repr__(self) -> str:
        return f"""Node(left:{self.left}, label: {self.label}, value: {self.value}, right:{self.right})"""


def evaluate(node: Node, csv_line: dict):
    result = 0
    # first check hostame condition and return early if not correct?
    
    if node.label == "input":
        result = __eval__input(node, csv_line["stdin"])
    elif node.label == "output":
        result = __eval__output(node, csv_line["output"])
    elif node.label == "compound" and (node.left and node.right):
        if node.value == "OR":
            result = evaluate(node.left, csv_line) or evaluate(node.right, csv_line)
        elif node.value == "AND":
            result = evaluate(node.left, csv_line) and evaluate(node.right, csv_line)
        else:
            result = -1
    else:
        result = -1
    return result

def load(path: str):
    with open(path, "r") as f:
        yaml.SafeLoader.add_constructor("!Node", Node.from_yaml)
        data = yaml.load(f.read(), yaml.SafeLoader)
    return data
def __eval__input(node: Node, input: str):
    return int(all(x in input for x in node.value.split(" ")))

def __eval__output(node: Node, output: str):
    return int(node.value in output)

if __name__ == "__main__":
    with open("proto_milestones_dev.yml", "r") as f:
        yaml.SafeLoader.add_constructor("!Node", Node.from_yaml)
        data = yaml.load(f.read(), yaml.SafeLoader)
        print(data, width=40)
        print(data[0], width=20)
        print(data[1], width=20)
