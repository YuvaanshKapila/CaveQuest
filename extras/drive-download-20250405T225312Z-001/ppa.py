from flask import Flask, render_template, request

app = Flask(__name__)

# 🌍 Enhanced Food Guide with rich data per dish
food_guide = {
    "Italian": {
        "pasta": [
            {
                "name": "Campfire Pasta Primavera",
                "tags": ["vegetarian", "easy"],
                "instructions": "Boil pasta, sauté veggies, and mix together.",
                "image": "https://www.rei.com/dam/up_2017-07-a07b4543-edit.jpg",
                "equipment": ["Pot", "Stove", "Strainer"]
            },
            {
                "name": "One-Pot Spaghetti Bolognese",
                "tags": ["hearty"],
                "instructions": "Brown beef, add sauce and spaghetti, simmer until cooked.",
                "image": "https://img.taste.com.au/Nd3a144g/taste/2016/11/one-pot-spaghetti-bolognaise-92051-1.jpeg",
                "equipment": ["Pot", "Ladle"]
            }
        ],
        "bread": [
            {
                "name": "Garlic Bread on Skillet",
                "tags": ["vegetarian", "quick"],
                "instructions": "Toast bread with garlic butter in a pan.",
                "image": "https://www.plainchicken.com/wp-content/uploads/2020/03/garlic%2Bparmesan%2Bskillet%2Bbread%2B%25281%2529%2Bcopy.jpg",
                "equipment": ["Skillet", "Spatula"]
            },
            {
                "name": "Tomato Bruschetta",
                "tags": ["fresh", "starter"],
                "instructions": "Top toasted bread with diced tomatoes, garlic, and olive oil.",
                "image": "https://emilybites.com/wp-content/uploads/2023/11/Tomato-and-Goat-Cheese-Bruschetta-5b.jpg",
                "equipment": ["Knife", "Pan"]
            }
        ],
        "cheese": [
            {
                "name": "Grilled Cheese Sandwiches",
                "tags": ["quick", "kid-friendly"],
                "instructions": "Grill cheese between buttered bread slices over campfire.",
                "image": "https://www.jocooks.com/wp-content/uploads/2024/01/grilled-cheese-1-9-500x500.jpg",
                "equipment": ["Pan", "Spatula"]
            },
            {
                "name": "Cheesy Campfire Potatoes",
                "tags": ["hearty"],
                "instructions": "Wrap potatoes and cheese in foil and grill over fire.",
                "image": "https://hips.hearstapps.com/hmg-prod/images/campfire-potatoes-secondary-64da9afecc4c0.jpg",
                "equipment": ["Foil", "Tongs"]
            }
        ]
    },
    "Mexican": {
        "beans": [
            {
                "name": "Bean Burritos",
                "tags": ["vegetarian", "protein-rich"],
                "instructions": "Fill tortillas with beans and cheese, wrap and heat.",
                "image": "https://media.istockphoto.com/id/689572418/photo/nice-vegetarian-burrito-over-black-table-on-wooden-board.jpg?s=612x612&w=0&k=20&c=IPNP4q9nCctZ_rBKJEckfCO6bQXv99JrwyfQka6xqIg=",
                "equipment": ["Foil", "Grill"]
            },
            {
                "name": "Campfire Chili",
                "tags": ["hearty"],
                "instructions": "Simmer beans and tomatoes with spices in a pot.",
                "image": "https://2nerdsinatruck.com/wp-content/uploads/2024/07/Campfire-Chili-5-scaled.jpg",
                "equipment": ["Pot", "Spoon"]
            }
        ],
        "tortilla": [
            {
                "name": "Quesadillas",
                "tags": ["quick", "kid-friendly"],
                "instructions": "Fill tortillas with cheese, fold and grill until golden.",
                "image": "https://appetizing-cactus-7139e93734.media.strapiapp.com/Quesadillas_Con_Carne_d9b2d0cab8.jpeg",
                "equipment": ["Pan", "Spatula"]
            },
            {
                "name": "Taco Wraps",
                "tags": ["easy"],
                "instructions": "Wrap cooked meat and veggies in tortillas.",
                "image": "https://successrice.com/wp-content/uploads/2020/07/Mexican-Taco-Wraps-OH-016-16x9-3.jpg",
                "equipment": ["Foil", "Knife"]
            }
        ],
        "corn": [
            {
                "name": "Grilled Corn",
                "tags": ["simple", "classic"],
                "instructions": "Grill whole corn with husk or foil until golden.",
                "image": "https://hips.hearstapps.com/hmg-prod/images/shot-2-0129-1522854796.png?crop=1xw:1xh;center,top&resize=1200:*",
                "equipment": ["Grill", "Tongs"]
            },
            {
                "name": "Corn Salsa with Chips",
                "tags": ["fresh", "starter"],
                "instructions": "Mix corn, onion, and lime juice. Serve with chips.",
                "image": "http://allrecipes.com/thmb/wHl8GLsI5ca_Uc6YELY067hJqho=/0x512/filters:no_upscale():max_bytes(150000):strip_icc()/187625-Easy-Corn-Salsa-ddmfs-183-4x3-2e340910922348849f49f084aef08427.jpg",
                "equipment": ["Bowl", "Spoon"]
            }
        ]
    },
    "Indian": {
        "rice": [
            {
                "name": "Jeera Rice",
                "tags": ["vegetarian", "simple"],
                "instructions": "Cook rice with cumin seeds in a pot.",
                "image": "https://myfoodstory.com/wp-content/uploads/2018/07/Perfect-Jeera-Rice-Indian-Cumin-Rice-4-500x500.jpg",
                "equipment": ["Pot", "Spoon"]
            },
            {
                "name": "One-Pot Vegetable Pulao",
                "tags": ["vegetarian", "hearty"],
                "instructions": "Mix rice with vegetables and spices in one pot.",
                "image": "https://hedgecombers.com/wp-content/uploads/2017/02/One-Pot-Campervan-Egg-Fried-Rice-9860.jpg",
                "equipment": ["Pot", "Knife"]
            }
        ],
        "lentils": [
            {
                "name": "Dal Tadka",
                "tags": ["vegetarian", "protein-rich"],
                "instructions": "Cook lentils, temper spices and mix in.",
                "image": "https://bakinghermann.com/wp-content/uploads/2024/11/Dal-Tadka-12.jpg",
                "equipment": ["Pot", "Pan"]
            },
            {
                "name": "Lentil Soup",
                "tags": ["warm", "nourishing"],
                "instructions": "Simmer lentils with garlic, onion and cumin.",
                "image": "https://images.101cookbooks.com/red-lentil-soup-recipe-23-v.jpg?w=1200&auto=format",
                "equipment": ["Pot", "Ladle"]
            }
        ],
        "spices": [
            {
                "name": "Spicy Grilled Paneer",
                "tags": ["vegetarian", "grilled"],
                "instructions": "Marinate paneer in spices and grill on skewers.",
                "image": "https://www.funfoodfrolic.com/wp-content/uploads/2023/09/Grilled-Paneer.jpg",
                "equipment": ["Skewers", "Grill"]
            },
            {
                "name": "Campfire Masala Potatoes",
                "tags": ["spicy"],
                "instructions": "Toss boiled potatoes with spices and sauté.",
                "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRiYvUoPpsz089P2n2O1xezr2BB3cfFYxiqPA&s",
                "equipment": ["Pan", "Spoon"]
            }
        ]
    },
    "American": {
        "potatoes": [
            {
                "name": "Loaded Campfire Potatoes",
                "tags": ["hearty"],
                "instructions": "Stuff foil-wrapped potatoes with cheese and bacon, grill.",
                "image": "https://girlcarnivore.com/wp-content/uploads/2023/07/Campfire-Baked-Potatoes-3359.jpg",
                "equipment": ["Foil", "Grill"]
            },
            {
                "name": "Hash Browns",
                "tags": ["breakfast", "quick"],
                "instructions": "Grate and fry potatoes in skillet with oil.",
                "image": "https://www.simplyrecipes.com/thmb/3OdzP8sGeKWZbVCxZnSgo6-ENvQ=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/__opt__aboutcom__coeus__resources__content_migration__simply_recipes__uploads__2018__03__Crispy-Hash-Browns-METHOD-08-81651f95bb2642458ac93f7dce56ad0b.jpg",
                "equipment": ["Skillet", "Spatula"]
            }
        ],
        "eggs": [
            {
                "name": "Scrambled Eggs",
                "tags": ["quick", "classic"],
                "instructions": "Whisk and scramble eggs in buttered pan.",
                "image": "https://www.budgetbytes.com/wp-content/uploads/2024/09/Scrambled-Eggs-Close.jpg",
                "equipment": ["Pan", "Whisk"]
            },
            {
                "name": "Egg Burrito",
                "tags": ["protein-rich", "wrap"],
                "instructions": "Wrap cooked eggs and cheese in a tortilla.",
                "image": "https://www.culinaryhill.com/wp-content/uploads/2022/06/Egg-Burrito-Culinary-Hill-1200x800-1-500x375.jpg",
                "equipment": ["Pan", "Foil"]
            }
        ],
        "bread": [
            {
                "name": "PB&J Sandwich",
                "tags": ["kid-friendly", "no-cook"],
                "instructions": "Spread peanut butter and jelly on bread slices.",
                "image": "https://simplyunbeetable.com/wp-content/uploads/2021/02/Decadent-Grilled-And-Stuffed-PBJ.jpg",
                "equipment": ["Knife"]
            },
            {
                "name": "Campfire Grilled Cheese",
                "tags": ["classic", "comfort food"],
                "instructions": "Grill cheese-filled bread slices until crispy.",
                "image": "https://www.freshoffthegrid.com/wp-content/uploads/cooking-apple-bacon-grilled-cheese-in-cast-iron126.jpg",
                "equipment": ["Pan", "Spatula"]
            }
        ]
    }
}

# 🧺 Get all unique ingredients from the food_guide
all_ingredients = sorted({ingredient for cuisine in food_guide.values() for ingredient in cuisine})

@app.route("/", methods=["GET", "POST"])
def index():
    meals = {}
    selected_ingredients = []
    selected_cuisine = ""

    if request.method == "POST":
        selected_ingredients = request.form.getlist("ingredients")
        selected_cuisine = request.form.get("cuisine")

        if selected_cuisine and selected_ingredients:
            for ing in selected_ingredients:
                if ing in food_guide[selected_cuisine]:
                    meals[ing] = food_guide[selected_cuisine][ing]

    return render_template("index.html",
                           ingredients=all_ingredients,
                           cuisines=food_guide.keys(),
                           selected_ingredients=selected_ingredients,
                           selected_cuisine=selected_cuisine,
                           meals=meals)

@app.route("/dish/<cuisine>/<ingredient>/<dish_name>")
def dish_detail(cuisine, ingredient, dish_name):
    dish = None
    try:
        for item in food_guide[cuisine][ingredient]:
            if item["name"] == dish_name:
                dish = item
                break
    except KeyError:
        pass

    if dish:
        return render_template("dish.html", dish=dish, cuisine=cuisine)
    else:
        return "Dish not found", 404

if __name__ == "__main__":
    app.run(debug=True)
