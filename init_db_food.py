import sqlite3, requests, re
from array import *


connection = sqlite3.connect('init_db_food.db')

with open('food_schema.sql') as f:
    connection.executescript(f.read())

c = connection.cursor()

# returns IDs from API into our database
def getID(request):
    pattern = re.compile(r"(\bid:)([0-9]+)")
    setID = array('i')
    for (id, data) in re.findall(pattern, request) :
        setID.append(int(data))

    return setID

# returns dish names from API into our database
def getDishName(request):
    pattern = re.compile(r"(\btitle:)([A-Za-z ]+)")
    setDishName = ""
    for (title, data) in re.findall(pattern, request) :
        setDishName += data.strip() + " | "

    setDishName = setDishName.split(" | ")
    del setDishName[-1]

    return setDishName

# returns images of food from API into our database
def getDishImage(request):
    pattern = re.compile(r"(\bimage:)([A-Za-z:/.0-9\-]+)")
    setDishImage = ""
    for (image, data) in re.findall(pattern, request) :
        setDishImage += data + " | "

    setDishImage = setDishImage.split(" | ")
    del setDishImage[-1]

    return setDishImage

# populates italian dishes into database
def populateItalian(request): 
    i = 0
    while i < len(getID(request)):
        c.execute("INSERT OR IGNORE INTO food VALUES (?, ?, ?, ?, ?, ?, ?)",
              (getID(request)[i], getDishName(request)[i], getDishImage(request)[i], "E", "E", "E", 4))
        i = i + 1

# populates American dishes into database
def populateAmerican(request): 
    i = 0
    while i < len(getID(request)):
        c.execute("INSERT OR IGNORE INTO food VALUES (?, ?, ?, ?, ?, ?, ?)",
              (getID(request)[i], getDishName(request)[i], getDishImage(request)[i], "E", "E", "E", 1))
        i = i + 1

# populates Chinese dishes into database
def populateChinese(request): 
    i = 0
    while i < len(getID(request)):
        c.execute("INSERT OR IGNORE INTO food VALUES (?, ?, ?, ?, ?, ?, ?)",
              (getID(request)[i], getDishName(request)[i], getDishImage(request)[i], "E", "E", "E", 3))
        i = i + 1

# populates British dishes into database
def populateBritish(request): 
    i = 0
    while i < len(getID(request)):
        c.execute("INSERT OR IGNORE INTO food VALUES (?, ?, ?, ?, ?, ?, ?)",
              (getID(request)[i], getDishName(request)[i], getDishImage(request)[i], "E", "E", "E", 2))
        i = i + 1



#Get Italian dishes from API
response = "{results:[{id:487873,title:Pasta Salad,image:https://spoonacular.com/recipeImages/487873-312x231.jpg,imageType:jpg},{id:1028851,title:Pasta Pomodoro,image:https://spoonacular.com/recipeImages/1028851-312x231.jpg,imageType:jpg}],offset:0,number:10,totalResults:1593},{id:491489,title:Pasta Fagioli,image:https://spoonacular.com/recipeImages/491489-312x231.jpg,imageType:jpg},{results:[{id:510455,title:Zucchini Pepperoni Pizza,readyInMinutes:45,servings:1,sourceUrl:http://www.slenderkitchen.com/zucchini-pepperoni-pizza/,image:Zucchini-Pepperoni-Pizza-510455.jpg},},{id:621337,title:Healthy Pizza with a Cauliflower Crust,readyInMinutes:50,servings:2,sourceUrl:http://www.eatingbirdfood.com/2012/09/healthy-pizza-with-a-cauliflower-crust/,image:Healthy-Pizza-with-a-Cauliflower-Crust-621337.jpg},"
populateItalian(response)

#Get American dishes from API
response = "{results:[{id:690978,title:Healthy Salmon Quinoa Burgers,readyInMinutes:30,servings:5,sourceUrl:http://www.skinnytaste.com/2015/03/healthy-salmon-quinoa-burgers.html,image:healthy-salmon-quinoa-burgers-skinnytaste-690978.jpg},id:524656,title:Bacon Cheeseburgers with a Fried Egg + Maple Aioli,readyInMinutes:300,servings:4,sourceUrl:http://www.howsweeteats.com/2013/08/breakfast-burgers-with-maple-aioli/,image:Bacon-Cheeseburgers-with-a-Fried-Egg-+-Maple-Aioli-524656.jpg},{results:[{id:599089,title:Easy Slow Cooker Barbecued Ribs,readyInMinutes:405,servings:6,sourceUrl:http://leitesculinaria.com/84152/recipes-slow-cooker-barbecued-ribs.html,image:Easy-Slow-Cooker-Barbecued-Ribs-599089.jpg},{id:549619,title:BBQ Ribs That Anyone Can Make,readyInMinutes:130,servings:2,sourceUrl:http://www.ohsweetbasil.com/2013/05/bbq-ribs-recipe.html,image:BBQ-Ribs-That-Anyone-Can-Make-549619.jpg},{id:560225,title:Korean BBQ Ribs,readyInMinutes:30,servings:4,sourceUrl:http://www.jocooks.com/main-courses/pork-main-courses/korean-bbq-ribs/,image:Korean-BBQ-Ribs-560225.jpg},{id:471405,title:Oven-Baked BBQ Ribs,readyInMinutes:210,servings:8,sourceUrl:http://allrecipes.com/Recipe/Oven-Baked-BBQ-Ribs/Detail.aspx?src=rss,image:Oven-Baked-BBQ-Ribs-471405.jpg},{id:512973,title:Jim’s Country Style BBQ Ribs,readyInMinutes:180,servings:6,sourceUrl:http://www.fromvalerieskitchen.com/2013/09/jims-country-style-bbq-ribs/,image:Jims-Country-Style-BBQ-Ribs-512973.jpg},{id:617605,title:Slow Cooker BBQ Ribs,readyInMinutes:495,servings:6,sourceUrl:http://www.browneyedbaker.com/slow-cooker-bbq-ribs/,image:Slow-Cooker-BBQ-Ribs-617605.jpg},"
populateAmerican(response)

#Get Chinese dishes from API
response = "{results:[{id:525729,title:Crockpot Chicken and Dumplings,readyInMinutes:480,servings:4,sourceUrl:http://www.howsweeteats.com/2012/10/easy-crockpot-chicken-and-dumplings/,image:Crockpot-Chicken-and-Dumplings-525729.jpg},{id:1061416,title:Tofu and Kimchi Dumplings,readyInMinutes:110,servings:40,sourceUrl:https://healthynibblesandbits.com/tofu-and-kimchi-dumplings/,image:tofu-and-kimchi-dumplings-1061416.jpg},{id:329845,title:Beef Stew with Herbed Potato Dumplings,readyInMinutes:150,servings:6,sourceUrl:http://www.myrecipes.com/recipe/beef-stew-herbed-potato-dumplings-00420000006832/,image:beef-stew-with-herbed-potato-dumplings-329845.jpg},{id:157287,title:Steamed Dumplings With Shiitake Mushrooms in Sichuan Soup,readyInMinutes:10,servings:4,sourceUrl:http://www.seriouseats.com/recipes/2013/11/dinner-tonight-steamed-dumplings-shiitake-mushrooms-sichuan-soup-recipe.html,image:steamed-dumplings-with-shiitake-mushrooms-in-sichuan-soup-157287.jpg},{results:[{id:738588,title:Chow Mein,readyInMinutes:20,servings:4,sourceUrl:http://www.foodnetwork.com/recipes/ree-drummond/chow-mein.html,image:chow-mein-738588.jpeg},{id:631577,title:Skinny Chicken Chow Mein with Weight Watchers Points,readyInMinutes:30,servings:5,sourceUrl:http://www.skinnykitchen.com/recipes/skinny-chicken-chow-mein/,image:Skinny-Chicken-Chow-Mein-with-Weight-Watchers-Points-631577.jpg},{id:539999,title:Easy Shrimp Chow Mein,readyInMinutes:30,servings:2,sourceUrl:http://www.chinasichuanfood.com/easy-shrimp-chow-mein/,image:Easy-Shrimp-Chow-Mein-539999.jpg},"
populateChinese(response)

#Get British dishes from API
response = "{results:[{id:587123,title:Irish Beef Stew,readyInMinutes:45,servings:4,sourceUrl:http://www.laurenslatest.com/irish-beef-stew-mashed-potatoes/,image:Irish-Beef-Stew-587123.png},{id:714902,title:Irish Beef Stew,readyInMinutes:115,servings:6,sourceUrl:http://damndelicious.net/2015/03/09/irish-beef-stew/,image:irish-beef-stew-714902.jpg},{id:695061,title:Irish Lamb Stew,readyInMinutes:510,servings:8,sourceUrl:http://www.eatingwell.com/recipes/irish_lamb_stew.html,image:irish-lamb-stew-695061.jpg},{results:[{id:97886,title:Lamb Chop Lancashire Hot Pot,readyInMinutes:165,servings:4,sourceUrl:http://www.food.com/recipe/lamb-chop-lancashire-hot-pot-399122,image:lamb_chop_lancashire_hot_pot-97886.jpg},{id:205788,title:Sunday Supper: Lancashire Hotpot,readyInMinutes:120,servings:4,sourceUrl:http://www.seriouseats.com/recipes/2011/12/lancashire-hotpot-lamb-stew-recipe.html,image:Sunday-Supper--Lancashire-Hotpot-205788.jpg},"
populateBritish(response)

connection.commit()
connection.close()
