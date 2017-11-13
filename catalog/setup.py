#!/usr/bin/env python3
# -*- coding: latin-1 -*-

import random
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Category, Item

print("Creating database. Please wait..")

# Create db folder if not existing
path = '/vagrant/catalog/db'
if not os.path.exists(path):
    try:
        os.makedirs(path)
    # Guard against race condition
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

engine = create_engine('sqlite:////vagrant/catalog/db/item_catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User = User(name="Alan Elliott", email="alanelliott@example.com",
            picture='https://uinames.com/api/photos/male/32.jpg')
session.add(User)
session.commit()

# Categories
categories = [
    "Armor",
    "Clothes",
    "Containers",
    "Jewelry",
    "Potions",
    "Weapons",
    "Artifacts",
    "Books",
    "Surprise",
    "Starter"
]

# Create categories
for c in categories:
    categ = Category(name=c)
    session.add(categ)
    session.commit()

# Items
items = [
    "Longevity Canopic Jar",
    "Genesis Key",
    "Light's Mantle",
    "Longevity Ring",
    "Pestilence Goblet",
    "Skull of Truth",
    "Tablet of the Titans",
    "Tiara of Resurrection",
    "Statue of Spite",
    "Stone of the Elements",
    "Blinding Fruit",
    "Paramount Instrument",
    "Paragon Robes",
    "Temptation Cylinder",
    "Virility Fruit",
    "Amulet of Malice",
    "Ark of Scorching",
    "Door of Time",
    "Ark of Futures",
    "Jar of Heroism",
    "Absorbing Band",
    "Dread Cup",
    "Infernal Mask",
    "Restoration Mirror",
    "Hallowed Lamp",
    "Monolith of Binding",
    "Crown of Invocation",
    "Statue of Dreams",
    "Fruit of Lightning",
    "Robes of Binding",
    "Paradise Shard",
    "Teleporting Jar",
    "Mirage Stone",
    "Philosopher's Ark",
    "Fortitude Sword",
    "Statuette of Spells",
    "Ark of Sanctification",
    "Shield of Specters",
    "Runes of Demons",
    "Hide of Light",
    "Guardian's Lamp",
    "Dementia Ring",
    "Hellish Monolith",
    "Divine Boots",
    "Hero's Gem",
    "Grail of Evils",
    "Gauntlet of Shadows",
    "Tome of Lightness",
    "Circlet of Destruction",
    "Inscriptions of Death"
]

# Descriptions
descriptions = [
    "It induces sleep, induces visions, and amplifies one's special talents.",
    "It enhances reaction time.",
    "It induces honesty, induces wakefulness, aids certain skin problems,\
     and enhances the sense of touch.",
    "It enhances strength and enhances the sense of touch.",
    "It wards off ill fortune, aids certain heart conditions, and induces\
     transformation.",
    "It aids certain lung ailments, aids certain skin problems, and wards off\
     nightmares.",
    "It attracts good fortune and enhances reaction time.",
    "It wards off nightmares.",
    "It attracts good fortune.",
    "It induces transformation."
]

# Create items
for i in items:
    it = Item(name=i,
              description=descriptions[random.randint(0, len(descriptions)-1)],
              category=categories[random.randint(0, len(categories)-1)])
    session.add(it)
    session.commit()

print("Added dummy items!")
