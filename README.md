# Infinite Craft Recipe Search
Find the most optimal way to craft an item in Infinite Craft and generate a visual graph in seconds

# Requirements
For recipe graph display to work:
- Install Graphviz: https://graphviz.org/download/
- `Graphviz/bin` folder must be added to `PATH` in Environment Variables in Windows

# Install
For Windows, you can directly download the recipes and executables from the Release page: https://github.com/onnowhere/infinite-craft-recipe-search/releases/latest

Alternatively, you can clone and install from source with Python 3.
```
git clone https://github.com/onnowhere/infinite-craft-recipe-search
cd infinite-craft-recipe-search
pip install -r requirements.txt
```

# Usage
- [OPTIONAL] If you would like newer recipes, run `update_recipe_tree.py`
    - This will update the optimal tree of all recipes from `recipes.json` into `recipe_tree.json`
    - Recipes are automatically pulled from: `https://icscdn.vantezzen.io/recipes.json`
- Run `search_recipes.py` to search for the optimal recipe path to a phrase
    - To view a visual recipe graph, put `!` before your search.
    - Ex.: `!anagram`
- Run `search_recipe_options.py` to search for all possible top level recipes for a phrase
    - To do a partial phrase search, put `!` before your search.
    - Ex.: `!alpha`

# Special thanks
- Thanks to Neal Agarwal for creating Infinite Craft: https://neal.fun/infinite-craft/
- Thanks to @vantezzen for the recipe database: https://github.com/vantezzen/infinite-craft-solver/tree/main
