""" Завдання 5. Візуалізація обходу бінарного дерева

Використовуючи код із завдання 4 для побудови бінарного дерева, необхідно створити програму на Python, яка візуалізує обходи дерева: у глибину та в ширину.

Вона повинна відображати кожен крок у вузлах з різними кольорами, використовуючи 16-систему RGB (приклад #1296F0). Кольори вузлів мають змінюватися від темних до світлих відтінків, залежно від послідовності обходу. Кожен вузол при його відвідуванні має отримувати унікальний колір, який візуально відображає порядок обходу. """


from collections import deque

import networkx as nx
import matplotlib.pyplot as plt

from Task04_Pyramid_Visual import Node, add_edges, heap_to_tree  # імпорт з попередньої 


def hex_to_rgb(h: str):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(rgb):
    r, g, b = rgb
    return f"#{r:02X}{g:02X}{b:02X}"


def gradient_colors(n: int, start_hex="#0B1A33", end_hex="#BFE6FF"):
    if n <= 0:
        return []
    if n == 1:
        return [start_hex]

    s = hex_to_rgb(start_hex)
    e = hex_to_rgb(end_hex)

    out = []
    for i in range(n):
        t = i / (n - 1)
        r = round(s[0] + (e[0] - s[0]) * t)
        g = round(s[1] + (e[1] - s[1]) * t)
        b = round(s[2] + (e[2] - s[2]) * t)
        out.append(rgb_to_hex((r, g, b)))
    return out


def iter_dfs_preorder(root):
    if root is None:
        return
    stack = [root]
    while stack:
        node = stack.pop()
        yield node
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)


def iter_bfs(root):
    if root is None:
        return
    q = deque([root])
    while q:
        node = q.popleft()
        yield node
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)


def draw_tree_step(root, ax, title=""):
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(tree, root, pos)

    colors = [n[1]["color"] for n in tree.nodes(data=True)]
    labels = {n[0]: n[1]["label"] for n in tree.nodes(data=True)}

    ax.clear()
    ax.set_title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors, ax=ax)


def visualize_traversal(
    root,
    traversal="dfs",          # "dfs" або "bfs"
    delay=0.8,                # пауза між кроками
    unvisited="#D3D3D3",      # колір невідвіданих
    start="#0B1A33",          # темний старт
    end="#BFE6FF",            # світлий фініш
):
    if root is None:
        print("Дерево порожнє.")
        return

    # скидаємо кольори
    def collect_all_nodes_bfs(r):
        return list(iter_bfs(r))

    all_nodes = collect_all_nodes_bfs(root)
    for n in all_nodes:
        n.color = unvisited

    if traversal.lower() == "dfs":
        order = list(iter_dfs_preorder(root))
        prefix = "DFS (глибина, preorder)"
    else:
        order = list(iter_bfs(root))
        prefix = "BFS (ширина)"

    colors = gradient_colors(len(order), start, end)

    plt.ion()
    fig, ax = plt.subplots(figsize=(9, 5))

    draw_tree_step(root, ax, f"{prefix}: старт")
    fig.canvas.draw()
    plt.pause(0.001)

    for i, (node, col) in enumerate(zip(order, colors), start=1):
        node.color = col
        draw_tree_step(root, ax, f"{prefix}: крок {i}/{len(order)}")
        fig.canvas.draw()
        plt.pause(delay)

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    heap = [24, 31, 25, 10, 0, 13, 55, 7]
    root = heap_to_tree(heap)

    visualize_traversal(root, traversal="dfs", delay=0.8)
    visualize_traversal(root, traversal="bfs", delay=0.8)
