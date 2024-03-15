#!/usr/bin/env python3
# Infinite Craft Recipe Search
version = "1.0.0"

import os
import json
import shutil
import requests

def main():
    print("\n".join([
        "------------------------------------------------------------",
        " > [Update Recipe Tree]",
        "------------------------------------------------------------",
        " Infinite Craft Recipe Search v" + version,
        " Made for https://neal.fun/infinite-craft",
        " Repo: github.com/onnowhere/optimized-infinite-craft-solver",
        " Main recipe DB: github.com/vantezzen/infinite-craft-solver",
        " This updates the optimal recipe tree file for all recipes.",
        "------------------------------------------------------------\n",
    ]))

    curr_dir = "."
    recipes_url = "https://icscdn.vantezzen.io/recipes.json"
    recipes_path = os.path.join(curr_dir, "recipes.json")
    recipes = {}

    try:
        r = requests.get(recipes_url, stream = True, verify = True)
        with open(recipes_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    except Exception as e:
        print(f"Failed to obtain recipes dynamically from {recipes_url}. Falling back to local copy.")
        print(e)

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

    print(f"Loaded {len(recipes['recipes'])} recipes")

    # Remap recipes
    remapped_recipes = {}
    items = recipes["items"]
    for recipe in recipes["recipes"]:
        first = items[recipe[0]]
        second = items[recipe[1]]
        result = items[recipe[2]]

        if first.lower() == result.lower() or second.lower() == result.lower():
            continue

        if first not in remapped_recipes:
            remapped_recipes[first] = {}

        if second not in remapped_recipes[first]:
            remapped_recipes[first][second] = result

    recipes_weighted = {}
    checked_recipes = {}
    found_words = ["Water", "Fire", "Wind", "Earth"]
    new_found_words = set()

    # Create initial weighted recipes
    for word in found_words:
        recipes_weighted[word] = [0, None]

    # Scan for recipes
    recipe_count = 0
    last_found_words = []
    last_new_found_words = []

    while True:
        # Check all possible recipe combinations within found words
        print(f"Current found words: {len(found_words)}")
        total_recipes = 0
        for values in remapped_recipes.values():
            total_recipes += len(values)
        print(f"Current remaining recipes: {total_recipes}")
        for first in found_words:
            if first not in remapped_recipes:
                continue

            if first in last_found_words:
                found = False
                for second in last_new_found_words:
                    if second in remapped_recipes[first]:
                        found = True
                        break
                if not found:
                    continue

            delete_keys = []
            for second, result in remapped_recipes[first].items():
                # Skip if second is not yet found
                if second not in found_words:
                    continue

                # Skip if recipe already checked
                if second in checked_recipes.get(first, []) or first in checked_recipes.get(second, []):
                    delete_keys.append(second)
                    continue

                # Update checked recipes
                if first not in checked_recipes:
                    checked_recipes[first] = set()
                checked_recipes[first].add(second)
                recipe_count += 1

                delete_keys.append(second)

                # Find maximum steps
                steps = 1 + max(recipes_weighted[first][0], recipes_weighted[second][0])
                recipe = [first, second]
                
                # If result already found, skip if new recipe has equal or more weight
                if result in recipes_weighted and steps >= recipes_weighted[result][0]:
                    continue

                # Update recipe
                recipes_weighted[result] = [steps, recipe]
                if result not in found_words:
                    new_found_words.add(result)

            # Delete recipe if checked
            for second in delete_keys:
                del remapped_recipes[first][second]
            if len(remapped_recipes[first]) == 0:
                del remapped_recipes[first]

        # Finished, no new recipes found
        if len(new_found_words) == 0:
            break

        # Update found words for next cycle
        last_found_words = list(found_words)
        last_new_found_words = list(new_found_words)
        found_words += list(new_found_words)
        new_found_words = set()

    print(f"Finished scanning: {recipe_count} recipes tested")

    total_recipes = 0
    for values in recipes_weighted.values():
        total_recipes += len(values)
    print(f"Final recipes weighted: {total_recipes}")

    with open("recipe_tree.json", "w+", encoding="utf8") as f:
        json.dump(recipes_weighted, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
