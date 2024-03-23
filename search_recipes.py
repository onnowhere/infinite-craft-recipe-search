#!/usr/bin/env python3
# Infinite Craft Recipe Search
version = "1.0.0"

import os
import json
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

def add_recipe_paths_recursive(recipe_tree, scanned, recipe, result):
    if result in scanned:
        return []

    scanned.add(result)

    if recipe is None:
        return []

    first = recipe[0]
    second = recipe[1]

    recipe_edges = []
    recipe_edges.append(f"{first} + {second} = {result}")

    if first in recipe_tree and first not in scanned:
        sub_recipe = recipe_tree[first][1]
        sub_recipe_edges = add_recipe_paths_recursive(recipe_tree, scanned, sub_recipe, first)
        for sub_recipe_edge in sub_recipe_edges:
            if sub_recipe_edge not in recipe_edges:
                recipe_edges.append(sub_recipe_edge)

    recipe_edges_2 = []
    if second in recipe_tree:
        sub_recipe = recipe_tree[second][1]
        sub_recipe_edges = add_recipe_paths_recursive(recipe_tree, scanned, sub_recipe, second)
        for sub_recipe_edge in sub_recipe_edges:
            if sub_recipe_edge not in recipe_edges and sub_recipe_edge not in recipe_edges_2:
                recipe_edges_2.append(sub_recipe_edge)

    recipe_edges = recipe_edges[0:1] + recipe_edges_2 + recipe_edges[1:]

    return recipe_edges

def add_recipe_edges_recursive(recipe_tree, scanned, recipe, result):
    if result in scanned:
        return []

    scanned.add(result)

    if recipe is None:
        return []

    first = recipe[0]
    second = recipe[1]

    recipe_edges = []
    recipe_edges.append((first, result))
    recipe_edges.append((second, result))
    recipe_edges = list(set(recipe_edges))

    if first in recipe_tree and first not in scanned:
        sub_recipe = recipe_tree[first][1]
        sub_recipe_edges = add_recipe_edges_recursive(recipe_tree, scanned, sub_recipe, first)
        for sub_recipe_edge in sub_recipe_edges:
            if sub_recipe_edge not in recipe_edges:
                recipe_edges.append(sub_recipe_edge)

    recipe_edges_2 = []
    if second in recipe_tree:
        sub_recipe = recipe_tree[second][1]
        sub_recipe_edges = add_recipe_edges_recursive(recipe_tree, scanned, sub_recipe, second)
        for sub_recipe_edge in sub_recipe_edges:
            if sub_recipe_edge not in recipe_edges and sub_recipe_edge not in recipe_edges_2:
                recipe_edges_2.append(sub_recipe_edge)

    recipe_edges = recipe_edges[0:1] + recipe_edges_2 + recipe_edges[1:]

    return recipe_edges

def main():
    print("\n".join([
        "------------------------------------------------------------",
        " > [Search Recipe]",
        "------------------------------------------------------------",
        " Infinite Craft Recipe Search v" + version,
        " Made for https://neal.fun/infinite-craft",
        " Repo: github.com/onnowhere/optimized-infinite-craft-solver",
        " Main recipe DB: github.com/vantezzen/infinite-craft-solver",
        " This generates the optimal recipe path for a given recipe.",
        " - To view a visual recipe graph, put ! before your search.",
        "------------------------------------------------------------\n",
    ]))

    curr_dir = "."
    recipe_tree_path = os.path.join(curr_dir, "recipe_tree.json")

    recipe_tree = {}
    open(recipe_tree_path, "a+", encoding="utf8")
    with open(recipe_tree_path, "r", encoding="utf8") as f:
        data = f.read()
        if data != "":
            recipe_tree = json.loads(data)

    while True:
        print("Put ! before your search to display a recipe graph visual")
        query = input("Search: ").lower()

        if query.strip() == "":
            print("[ERROR] Please provide a valid query")
            continue

        show_graph = False
        if query.startswith("!"):
            show_graph = True
            query = query[1:]

        found = False
        for result, values in recipe_tree.items():
            if result.lower() == query:
                found = True

                #steps = values[0]
                recipe = values[1]
                recipe_path = add_recipe_paths_recursive(recipe_tree, set(), recipe, result)
                print(f"\n[ You will need {len(recipe_path)} recipes to make '{result}' ]\n")
                print("\n".join(recipe_path) + "\n")

                if show_graph:
                    try:
                        recipe_edges = add_recipe_edges_recursive(recipe_tree, set(), recipe, result)
                        #print(recipe_edges)

                        G = nx.DiGraph()
                        G.add_edges_from(recipe_edges)

                        # plot the graph
                        plt.figure(figsize=(16, 9))
                        pos = graphviz_layout(G, prog="dot", args='-Grankdir="LR"')
                        nx.draw_networkx_edges(G, pos=pos, width=0.25, edge_color=(0,0,0,0.5), connectionstyle='arc3, rad = 0.1', arrowsize=5)
                        nx.draw_networkx_labels(G, pos=pos, font_size=5, bbox=dict(fc="w", linewidth=0.1, boxstyle="round", pad=0.2))

                        plt.show() # pause before exiting
                    except Exception as e:
                        print("[ERROR] Graph display is not supported! Please ensure Graphviz is properly installed and added to your PATH in environment variables.")
                        raise e

        if not found:
            print("[ERROR] Recipe not found")

        print("=====================\n")

if __name__ == "__main__":
    main()
