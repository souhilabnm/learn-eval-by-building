# Failure Mode Taxonomy

This document outlines the failure modes observed for the Recipe Chatbot in the bulk run of 2026-10-26 (18 traces, 17 with open-coding notes). Each failure mode includes a title, a concise definition, and illustrative examples quoted from the traces. DRAFT: to be reviewed and renamed by the author.

## Failure Mode 1: Asks Instead of Answers

*   **Definition**: Bot replies with a question (usually "Any allergies or foods to avoid?") and gives no recipe, even when the request is already clear enough to cook from.
*   **Illustrative Examples**:
    1.  *User Query (trace 4)*: "something easy for dinner, kids are hungry and i have like 20 min"
        *Bot Response*: "Any allergies or foods to avoid?"
    2.  *User Query (trace 18)*: "how do i make that creamy soup thing with potatoes"
        *Bot Response*: "Any allergies or foods to avoid?"

## Failure Mode 2: Hard-to-Follow Recipe

*   **Definition**: Bot gives a recipe, but chef-style ingredient wording, long intros or US-only units make it hard for a home cook to use.
*   **Illustrative Examples**:
    1.  *User Query (trace 13)*: "gluten free pancakes?"
        *Bot Response*: Lists "1 cup gluten-free 1-to-1 baking flour (make sure it contains xanthan gum)" and gives the pan temperature only as "about 350°F", with no °C.
    2.  *User Query (trace 20)*: "no meat today, family dinner"
        *Bot Response*: Opens with "Since you're looking for a meatless family dinner, I'm assuming a comforting, crowd-pleasing pasta bake fits the bill!", then lists "1 teaspoon dried Italian seasoning" and "1 lb (16 oz) ziti or penne pasta" and a "9x13-inch baking dish", with no metric amounts.

## Failure Mode 3: Dish Idea Without a Recipe

*   **Definition**: Bot names a dish idea but gives no title, ingredients or steps.
*   **Illustrative Examples**:
    1.  *User Query (trace 23)*: "i have a tomato, cheese and bread. thoughts?"
        *Bot Response*: "You have the makings of a classic, comforting grilled cheese and tomato sandwich. Any allergies or foods to avoid before we get started?"
