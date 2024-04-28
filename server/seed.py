from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, Game, Review, User

# Define genres and platforms
genres = [
    "Platformer",
    "Shooter",
    "Fighting",
    "Stealth",
    "Survival",
    "Rhythm",
    "Survival Horror",
    "Metroidvania",
    "Text-Based",
    "Visual Novel",
    "Tile-Matching",
    "Puzzle",
    "Action RPG",
    "MMORPG",
    "Tactical RPG",
    "JRPG",
    "Life Simulator",
    "Vehicle Simulator",
    "Tower Defense",
    "Turn-Based Strategy",
    "Racing",
    "Sports",
    "Party",
    "Trivia",
    "Sandbox"
]

platforms = [
    "NES",
    "SNES",
    "Nintendo 64",
    "GameCube",
    "Wii",
    "Wii U",
    "Nintendo Switch",
    "GameBoy",
    "GameBoy Advance",
    "Nintendo DS",
    "Nintendo 3DS",
    "XBox",
    "XBox 360",
    "XBox One",
    "XBox Series X/S",
    "PlayStation",
    "PlayStation 2",
    "PlayStation 3",
    "PlayStation 4",
    "PlayStation 5",
    "PSP",
    "PS Vita",
    "Genesis",
    "DreamCast",
    "PC",
]

# Initialize Faker for generating fake data
fake = Faker()

# Create instances of users, games, and reviews
with app.app_context():
    # Clear existing data from tables
    Review.query.delete()
    User.query.delete()
    Game.query.delete()

    # Add users to the database
    users = []
    for i in range(100):
        user = User(name=fake.name())
        users.append(user)

    db.session.add_all(users)

    # Add games to the database
    games = []
    for i in range(100):
        game = Game(
            title=fake.sentence(),
            genre=rc(genres),
            platform=rc(platforms),
            price=randint(5, 60)
        )
        games.append(game)

    db.session.add_all(games)

    # Add reviews to the database
    reviews = []
    for user in users:
        for i in range(randint(1, 10)):
            review = Review(
                score=randint(0, 10),
                comment=fake.sentence(),
                user=user,
                game=rc(games)
            )
            reviews.append(review)

    db.session.add_all(reviews)

    # Commit changes to the database
    db.session.commit()
