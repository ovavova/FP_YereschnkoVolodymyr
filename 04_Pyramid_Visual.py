import uuid
import networkx as nx
import matplotlib.pyplot as plt
import heapq


class Node:
  def __init__(self, key, color="skyblue"):
    self.left = None
    self.right = None
    self.val = key
    self.color = color # Додатковий аргумент для зберігання кольору вузла
    self.id = str(uuid.uuid4()) # Унікальний ідентифікатор для кожного вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1):
  if node is not None:
    graph.add_node(node.id, color=node.color, label=node.val) # Використання id та збереження значення вузла
    if node.left:
      graph.add_edge(node.id, node.left.id)
      l = x - 1 / 2 ** layer
      pos[node.left.id] = (l, y - 1)
      l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
    if node.right:
      graph.add_edge(node.id, node.right.id)
      r = x + 1 / 2 ** layer
      pos[node.right.id] = (r, y - 1)
      r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
  return graph


def draw_tree(tree_root):
  tree = nx.DiGraph()
  pos = {tree_root.id: (0, 0)}
  tree = add_edges(tree, tree_root, pos)

  colors = [node[1]['color'] for node in tree.nodes(data=True)]
  labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)} # Використовуйте значення вузла для міток

  plt.figure(figsize=(8, 5))
  nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
  plt.show()

def heap_to_tree(heap):
  """Будує бінарне дерево з купи."""
  if not heap:
      return None

  nodes = [Node(v) for v in heap]

  for i in range(len(nodes)):
      li = 2 * i + 1
      ri = 2 * i + 2
      if li < len(nodes):
          nodes[i].left = nodes[li]
      if ri < len(nodes):
          nodes[i].right = nodes[ri]

  return nodes[0]

# збираємо купу - максимальну чи мінімальну
def make_heap(data, heap_type="min"):
    """
    data: list[int] (або list[float])
    heap_type: "min" або "max"
    Повертає список у форматі купи.
    """
    h = data[:]  # копія

    if heap_type == "min":
        heapq.heapify(h)
        return h

    if heap_type == "max":
        # heapq — це min-heap, тому робимо max-heap через зміну знаку
        h = [-x for x in h]
        heapq.heapify(h)
        return [-x for x in h]

    raise ValueError("heap_type має бути 'min' або 'max'")


# Функція, що МАЛЮЄ купу
def draw_heap(heap):
    """
    heap: list — вже готова купа у вигляді масиву.
    """
    root = heap_to_tree(heap)
    if root is None:
        print("Купа порожня — нема що малювати.")
        return
    draw_tree(root)

if __name__ == "__main__":
    data = [24, 31, 25, 10, 0, 13, 55, 7, 89, 3, 6]

    heap_min = make_heap(data, "min")
    draw_heap(heap_min)

    # Якщо треба max-heap:
    # heap_max = make_heap(data, "max")
    # draw_heap(heap_max)