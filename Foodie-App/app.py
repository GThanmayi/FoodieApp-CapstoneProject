from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory “database”
restaurants = {}
dishes = {}
users = {}
orders = {}
ratings = {}
feedbacks = []

restaurant_counter = 1
dish_counter = 1
user_counter = 1
order_counter = 1
rating_counter = 1

# --- Restaurant APIs ---

@app.route("/api/v1/restaurants", methods=["POST"])
def register_restaurant():
    global restaurant_counter
    data = request.get_json()
    # simple conflict check
    for r in restaurants.values():
        if r["name"] == data.get("name"):
            return jsonify({"error": "Restaurant already exists"}), 409
    restaurant_id = restaurant_counter
    data["id"] = restaurant_id
    data["enabled"] = True
    restaurants[restaurant_id] = data
    restaurant_counter += 1
    return jsonify(data), 201

@app.route("/api/v1/restaurants/<int:restaurant_id>", methods=["PUT"])
def update_restaurant(restaurant_id):
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    data = request.get_json()
    restaurants[restaurant_id].update(data)
    return jsonify(restaurants[restaurant_id]), 200

@app.route("/api/v1/restaurants/<int:restaurant_id>/disable", methods=["PUT"])
def disable_restaurant(restaurant_id):
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    restaurants[restaurant_id]["enabled"] = False
    return jsonify({"message": "Restaurant disabled"}), 200

@app.route("/api/v1/restaurants/<int:restaurant_id>", methods=["GET"])
def get_restaurant(restaurant_id):
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurants[restaurant_id]), 200

# --- Dish APIs ---

@app.route("/api/v1/restaurants/<int:restaurant_id>/dishes", methods=["POST"])
def add_dish(restaurant_id):
    global dish_counter
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    data = request.get_json()
    dish_id = dish_counter
    data.update({"id": dish_id, "restaurant": restaurant_id, "enabled": True})
    dishes[dish_id] = data
    dish_counter += 1
    return jsonify(data), 201

@app.route("/api/v1/dishes/<int:dish_id>", methods=["PUT"])
def update_dish(dish_id):
    if dish_id not in dishes:
        return jsonify({"error": "Dish not found"}), 404
    data = request.get_json()
    dishes[dish_id].update(data)
    return jsonify(dishes[dish_id]), 200

@app.route("/api/v1/dishes/<int:dish_id>/status", methods=["PUT"])
def toggle_dish(dish_id):
    if dish_id not in dishes:
        return jsonify({"error": "Dish not found"}), 404
    data = request.get_json()
    dishes[dish_id]["enabled"] = data.get("enabled", dishes[dish_id]["enabled"])
    return jsonify({"message": "Dish status updated"}), 200

@app.route("/api/v1/dishes/<int:dish_id>", methods=["DELETE"])
def delete_dish(dish_id):
    if dish_id not in dishes:
        return jsonify({"error": "Dish not found"}), 404
    dishes.pop(dish_id)
    return jsonify({"message": "Dish deleted"}), 200

# --- Admin APIs ---

@app.route("/api/v1/admin/restaurants/<int:restaurant_id>/approve", methods=["PUT"])
def admin_approve_restaurant(restaurant_id):
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    restaurants[restaurant_id]["approved"] = True
    return jsonify({"message": "Restaurant approved"}), 200

@app.route("/api/v1/admin/restaurants/<int:restaurant_id>/disable", methods=["PUT"])
def admin_disable_restaurant(restaurant_id):
    if restaurant_id not in restaurants:
        return jsonify({"error": "Restaurant not found"}), 404
    restaurants[restaurant_id]["enabled"] = False
    return jsonify({"message": "Restaurant disabled"}), 200

@app.route("/api/v1/admin/feedback", methods=["GET"])
def admin_feedback():
    return jsonify(feedbacks), 200

@app.route("/api/v1/admin/orders", methods=["GET"])
def admin_orders():
    return jsonify(list(orders.values())), 200

# --- User / Customer APIs ---

@app.route("/api/v1/users/register", methods=["POST"])
def register_user():
    global user_counter
    data = request.get_json()
    for u in users.values():
        if u["email"] == data.get("email"):
            return jsonify({"error": "User already exists"}), 409
    user_id = user_counter
    data["id"] = user_id
    users[user_id] = data
    user_counter += 1
    return jsonify(data), 201

@app.route("/api/v1/restaurants/search", methods=["GET"])
def search_restaurants():
    name = request.args.get("name", "").lower()
    location = request.args.get("location", "").lower()
    dish_name = request.args.get("dish", "").lower()
    rating = request.args.get("rating")
    result = []
    for r in restaurants.values():
        if name in r.get("name","").lower() and location in r.get("location","").lower():
            result.append(r)
    return jsonify(result), 200

@app.route("/api/v1/orders", methods=["POST"])
def place_order():
    global order_counter
    data = request.get_json()
    oid = order_counter
    data["id"] = oid
    orders[oid] = data
    order_counter += 1
    return jsonify(data), 201

@app.route("/api/v1/ratings", methods=["POST"])
def give_rating():
    global rating_counter
    data = request.get_json()
    rid = rating_counter
    data["id"] = rid
    ratings[rid] = data
    rating_counter += 1
    return jsonify(data), 201

# --- Order Module APIs ---

@app.route("/api/v1/restaurants/<int:restaurant_id>/orders", methods=["GET"])
def orders_by_restaurant(restaurant_id):
    result = [o for o in orders.values() if o.get("restaurant_id") == restaurant_id]
    return jsonify(result), 200

@app.route("/api/v1/users/<int:user_id>/orders", methods=["GET"])
def orders_by_user(user_id):
    result = [o for o in orders.values() if o.get("user_id") == user_id]
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)
