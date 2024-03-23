#!/usr/bin/env python3
# Infinite Craft Recipe Search
version = "1.0.0"

import os
import json

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
        " > [Search Recipe Options]",
        "------------------------------------------------------------",
        " Infinite Craft Recipe Search v" + version,
        " Made for https://neal.fun/infinite-craft",
        " Repo: github.com/onnowhere/optimized-infinite-craft-solver",
        " Main recipe DB: github.com/vantezzen/infinite-craft-solver",
        " This finds and lists all known recipes for a given phrase.",
        " - To do a partial phrase search, put ! before your search.",
        "------------------------------------------------------------\n",
    ]))
    curr_dir = "."
    recipes_path = os.path.join(curr_dir, "recipes.json")
    recipes = {}

    # Read recipes
    open(recipes_path, "a+", encoding="utf8")
    with open(recipes_path, "r", encoding="utf8") as f:
        data = f.read()
        if data == "":
            recipes = {}
        else:
            recipes = json.loads(data)

    # Normalize items
    key_case_mapping = {item.lower():item for item in recipes["items"]}
    recipes["items"] = [key_case_mapping[item.lower()] for item in recipes["items"]]

    print(f"Loaded {len(recipes['recipes'])} recipes\n")

    # Remap recipes
    remapped_recipes = {}
    items = recipes["items"]
    for recipe in recipes["recipes"]:
        first = items[recipe[0]]
        second = items[recipe[1]]
        result = items[recipe[2]]

        if first.lower() == result.lower() or second.lower() == result.lower():
            continue

        if result not in remapped_recipes:
            remapped_recipes[result] = []

        entry = [first, second]
        entry2 = [second, first]
        if entry not in remapped_recipes[result] and entry2 not in remapped_recipes[result]:
            entry.sort(key=lambda x: x[0])
            remapped_recipes[result].append(entry)

    while True:
        print("Put ! before your search to search for a partial phrase")
        query = input("Search: ").lower()

        if query.strip() == "":
            print("[ERROR] Please provide a valid query")
            continue

        exact = True
        if query.startswith("!"):
            query = query[1:]
            exact = False

        found = False
        results = []
        for key in remapped_recipes.keys():
            if (not exact and query in key.lower()) or (exact and query == key.lower()):
                found = True
                values = remapped_recipes[key]
                values.sort(key=lambda x: x[0])

                values = [f"- {x[0]}, {x[1]}" for x in values]
                values = "\n".join(values)
                results.append(f"[ {key} ]\n{values}\n")

        if found:
            print("\n".join(results))
        else:
            print("[ERROR] Recipe not found")

        print("=====================\n")

if __name__ == "__main__":
    main()
