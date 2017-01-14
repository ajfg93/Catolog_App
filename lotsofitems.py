# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Item, Category, Base

engine = create_engine('sqlite:///catelog_app.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

#create User 
user1 = User(name = "TIANQING", email = "myemail@yahoo.com")
session.add(user1)
session.commit()

user2 = User(name = "YUTING", email = "youremail@outlook.com")
session.add(user2)
session.commit()

#create categories

Soccer = Category(name = "Soccer")
session.add(Soccer)
session.commit()

BasketBall = Category(name = "BasketBall")
session.add(BasketBall)
session.commit()

BaseBall = Category(name = "BaseBall")
session.add(BaseBall)
session.commit()

Frisbee = Category(name = "Frisbee")
session.add(Frisbee)
session.commit()

Snowboarding = Category(name = "Snowboarding")
session.add(Snowboarding)
session.commit()

Rock_Climbing = Category(name = "Rock Climbing")
session.add(Rock_Climbing)
session.commit()

Foosball = Category(name = "Foosball")
session.add(Foosball)
session.commit()

Skating = Category(name = "Skating")
session.add(Skating)
session.commit()

Hockey = Category(name = "Hockey")
session.add(Hockey)
session.commit()

#add items 
Stick = Item(name = "Stick", description = "Success is the sum of small efforts, repeated day in and day out. ", user_id = 1, category_id = 9)
session.add(Stick)
session.commit()

Goggles = Item(name = "Goggles", description = "Goggles", user_id = 1, category_id = 5)
session.add(Goggles)
session.commit()

Snowboard = Item(name = "Snowboard", description = "A clear vision, backed by definite plans, gives you a tremendous feeling of confidence and personal power.", user_id = 1, category_id = 5)
session.add(Snowboard)
session.commit()

Two_shinguards = Item(name = "Two shinguards", description = "Two shinguards", user_id = 1, category_id = 1)
session.add(Two_shinguards)
session.commit()

Shinguards = Item(name = "Shinguards", description = "When you come slam bang up against trouble, it never looks half as bad if you face up to it.", user_id = 2, category_id = 1)
session.add(Shinguards)
session.commit()

Frisbee_Item = Item(name = "Frisbee", description = "If I should meet thee, after long years, how should I greet thee? With silence and tears.", user_id = 2, category_id = 4)
session.add(Frisbee_Item)
session.commit()

Bat = Item(name = "Bat", description = "Baidu, Alibaba, Tencent, would never be as great as Facebook, LinkedIn, Airbnb and Google.", user_id = 2, category_id = 2)
session.add(Bat)
session.commit()

Jersey = Item(name = "Jersey", description = "I shot an arrow into the air,It fell to earth, I knew not where.", user_id = 2, category_id = 1)
session.add(Jersey)
session.commit()

Soccer_Cleats = Item(name = "Soccer Cleats", description = "Soccer Cleats", user_id = 2, category_id = 1)
session.add(Soccer_Cleats)
session.commit()

print "added done!"

