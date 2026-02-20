*** Settings ***
Library           RequestsLibrary
Library           Collections
Library           String

Suite Setup       Create Session    foodie    ${BASE_URL}

*** Variables ***
${BASE_URL}       http://127.0.0.1:5000/api/v1


*** Test Cases ***

# ==============================
# Restaurant Module
# ==============================

Register Restaurant
    ${rand}=    Generate Random String    5
    ${name}=    Set Variable    FastFood_${rand}

    ${body}=    Create Dictionary
    ...    name=${name}
    ...    category=FastFood
    ...    location=Hyderabad
    ...    images=@{EMPTY}
    ...    contact=9999999999

    ${resp}=    POST On Session    foodie    /restaurants    json=${body}    expected_status=201

    ${REST_ID}=    Set Variable    ${resp.json()['id']}
    Set Suite Variable    ${REST_ID}
    Set Suite Variable    ${REST_NAME}    ${name}


Update Restaurant
    ${body}=    Create Dictionary    location=Vijayawada
    PUT On Session    foodie    /restaurants/${REST_ID}    json=${body}    expected_status=200


View Restaurant Profile
    GET On Session    foodie    /restaurants/${REST_ID}    expected_status=200


# ==============================
#  Dish Module
# ==============================

Add Dish
    ${body}=    Create Dictionary
    ...    name=Biryani
    ...    type=Non-Veg
    ...    price=250
    ...    available_time=Lunch
    ...    image=

    ${resp}=    POST On Session    foodie    /restaurants/${REST_ID}/dishes    json=${body}    expected_status=201

    ${DISH_ID}=    Set Variable    ${resp.json()['id']}
    Set Suite Variable    ${DISH_ID}


Update Dish
    ${body}=    Create Dictionary    price=300
    PUT On Session    foodie    /dishes/${DISH_ID}    json=${body}    expected_status=200


# ==============================
#  User Module
# ==============================

Register User
    ${rand}=    Generate Random String    5
    ${email}=    Set Variable    user_${rand}@test.com

    ${body}=    Create Dictionary
    ...    name=Bob
    ...    email=${email}
    ...    password=pass123

    ${resp}=    POST On Session    foodie    /users/register    json=${body}    expected_status=201

    ${USER_ID}=    Set Variable    ${resp.json()['id']}
    Set Suite Variable    ${USER_ID}


Search Restaurants
    ${params}=    Create Dictionary    name=${REST_NAME}    location=Vijayawada
    GET On Session    foodie    /restaurants/search    params=${params}    expected_status=200


# ==============================
# Order Module
# ==============================

Place Order
    ${item}=    Create Dictionary    dish_id=${DISH_ID}    qty=1
    @{items}=   Create List    ${item}

    ${body}=    Create Dictionary
    ...    user_id=${USER_ID}
    ...    restaurant_id=${REST_ID}
    ...    dishes=${items}

    ${resp}=    POST On Session    foodie    /orders    json=${body}    expected_status=201

    ${ORDER_ID}=    Set Variable    ${resp.json()['id']}
    Set Suite Variable    ${ORDER_ID}


Give Rating
    ${body}=    Create Dictionary
    ...    order_id=${ORDER_ID}
    ...    rating=5
    ...    comment=Excellent

    POST On Session    foodie    /ratings    json=${body}    expected_status=201


# ==============================
#  View Orders
# ==============================

View Orders By Restaurant
    GET On Session    foodie    /restaurants/${REST_ID}/orders    expected_status=200


View Orders By User
    GET On Session    foodie    /users/${USER_ID}/orders    expected_status=200