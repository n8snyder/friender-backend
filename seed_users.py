import random
import io
import os
import requests
import pdb

from app import db
from models import User, Picture

NUM_USERS = 25

MAX_PICTURES = 3


def add_picture(user_id):
    res = requests.get("https://loremflickr.com/320/240")
    picture = io.BytesIO(res.content)
    picture.filename = res.url
    Picture.create(picture, user_id)


cat_ipsum = """
Loved it, hated it, loved it, hated it make muffins. Make it to the carpet before i vomit mmmmmm. You have cat to be kitten me right meow eat half my food and ask for more i hate cucumber pls dont throw it at me. Scratch me there, elevator butt purr when give birth or decide to want nothing to do with my owner today rub butt on table kitten is playing with dead mouse yet i love cats i am one wake up scratch humans leg for food then purr then i have a and relax. Eat prawns daintily with a claw then lick paws clean wash down prawns with a lap of carnation milk then retire to the warmest spot on the couch to claw at the fabric before taking a catnap get video posted to internet for chasing red dot. Love you, then bite you meow for sniff other cat's butt and hang jaw half open thereafter, so scratch leg; meow for can opener to feed me for lick butt get suspicious of own shadow then go play with toilette paper and purr for no reason. Attack the dog then pretend like nothing happened cat gets stuck in tree firefighters try to get cat down firefighters get stuck in tree cat eats firefighters' slippers yet adventure always intently sniff hand intently sniff hand, yet hiss and stare at nothing then run suddenly away cat snacks. Proudly present butt to human jump on human and sleep on her all night long be long in the bed, purr in the morning and then give a bite to every human around for not waking up request food, purr loud scratch the walls, the floor, the windows, the humans grab pompom in mouth and put in water dish yet jump on fridge swat turds around the house. Iâ€™m so hungry iâ€™m so hungry but ew not for that somehow manage to catch a bird but have no idea what to do next, so play with it until it dies of shock but my slave human didn't give me any food so i pooped on the floor i shredded your linens for you at four in the morning wake up owner meeeeeeooww scratch at legs and beg for food then cry and yowl until they wake up at two pm jump on window and sleep while observing the bootyful cat next door that u really like but who already has a boyfriend end up making babies with her and let her move in spread kitty litter all over house. Toy mouse squeak roll over. Being gorgeous with belly side up. Roll on the floor purring your whiskers off. Ask to be pet then attack owners hand mouse, and nyan nyan goes the cat, scraaaaape scraaaape goes the walls when the cat murders them with its claws be superior so play riveting piece on synthesizer keyboard and side-eyes your "jerk" other hand while being petted and hate dog. If human is on laptop sit on the keyboard crusty butthole weigh eight pounds but take up a full-size bed but lasers are tiny mice, so swat turds around the house paw at beetle and eat it before it gets away shed everywhere shed everywhere stretching attack your ankles chase the red dot, hairball run catnip eat the grass sniff. Weigh eight pounds but take up a full-size bed. Human is washing you why halp oh the horror flee scratch hiss bite this human feeds me, i should be a god yet lick butt, for stare at wall turn and meow stare at wall some more meow again continue staring so missing until dinner time. Meow in empty rooms sleeps on my head lick the curtain just to be annoying leave hair on owner's clothes or wake up wander around the house making large amounts of noise jump on top of your human's bed and fall asleep again. Catch mouse and gave it as a present find empty spot in cupboard and sleep all day lick left leg for ninety minutes, still dirty run around the house at 4 in the morning and try to hold own back foot to clean it but foot reflexively kicks you in face, go into a rage and bite own foot, hard, cough furball. I love cats i am one wake up scratch humans leg for food then purr then i have a and relax hack up furballs or twitch tail in permanent irritation but stretch, or attack feet, so lick master's hand at first then bite because im moody i vomit in the bed in the middle of the night. Refuse to come home when humans are going to bed; stay out all night then yowl like i am dying at 4am. Love you, then bite you bleghbleghvomit my furball really tie the room together and lick butt, but demand to have some of whatever the human is cooking, then sniff the offering and walk away munch, munch, chomp, chomp but lick human with sandpaper tongue.
"""
cat_ipsum = cat_ipsum.replace("â€™", "'").strip().split(".")
cat_ipsum = [f"{sentence.strip()}." for sentence in cat_ipsum if sentence]
zip_codes = [
    "94601",
    "94602",
    "94603",
    "94608",
    "94622",
    "94701",
    "94707",
    "94709",
    "94720",
]
first_names = [
    "Philip",
    "Gavriel",
    "Jessa",
    "Hurley",
    "Paxon",
    "Waleed",
    "Kathy",
    "Malik",
    "Lynn",
    "Lizbeth",
    "Zaeem",
    "Amen",
    "Edith",
    "Jaclynn",
    "Xena",
    "Damario",
    "Ragnar",
    "Aman",
    "Sky",
    "Krystian",
]
last_names = [
    "Trotter",
    "Batista",
    "Gober",
    "Skeen",
    "Tarantino",
    "Landreth",
    "Keel",
    "Sisco",
    "Moorer",
    "Huckaby",
    "Fink",
    "Edison",
    "Aceves",
    "Hollins",
    "Blackburn",
    "Cobbs",
    "Eden",
    "Oberg",
    "Barnett",
    "Weller",
]

for i in range(NUM_USERS):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    zip_code = random.choice(zip_codes)
    hobbies = ""
    for i in range(random.randint(0, 4)):
        hobbies += f"{random.choice(cat_ipsum)} "
    interests = ""
    for i in range(random.randint(0, 4)):
        interests += f"{random.choice(cat_ipsum)} "
    email = f"{name.replace(' ', '')}{random.randint(1, 1000)}@mail.com"
    password = "password"
    user = User.register(
        email=email,
        password=password,
        name=name,
        zip_code=zip_code,
        hobbies=hobbies,
        interests=interests,
    )
    db.session.add(user)
    db.session.commit()

    for i in range(random.randint(1, MAX_PICTURES + 1)):
        add_picture(user.id)
