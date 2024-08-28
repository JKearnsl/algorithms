from src.config import InIConfig
from src.models.sort import BaseSortModel
from src.models.sort import MenuItem


class TreeNode:
    def __init__(self, key=None):
        self.key = key
        self.left = None
        self.right = None

    def __str__(self):
        return f"TreeNode({self.key})"

    def insert(self, key):
        if self.key is None:
            self.key = key
            return

        if key < self.key:
            if self.left is None:
                self.left = TreeNode(key)
            else:
                self.left.insert(key)
        elif key > self.key:
            if self.right is None:
                self.right = TreeNode(key)
            else:
                self.right.insert(key)
        else:
            print(f"Key {key} already exists")

    def traversal(self) -> list[int]:
        result = []
        if self.left is not None:
            result.extend(self.left.traversal())
        result.append(self.key)
        if self.right is not None:
            result.extend(self.right.traversal())
        return result


class TreeSortModel(BaseSortModel):
    id: MenuItem = MenuItem.TREE
    title: str = 'Сортировка Деревом'
    complexity: str = 'O(nlog(n))'

    def __init__(self, config: InIConfig, theme):

        self.config = config
        self.theme = theme

        # список наблюдателей
        self._mObservers = []

    def sort(self) -> None:
        array = self.input_list.copy()
        tree = TreeNode()
        for el in array:
            tree.insert(el)
        self.output_list = tree.traversal()