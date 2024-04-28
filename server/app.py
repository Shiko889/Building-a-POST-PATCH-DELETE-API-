from flask import Flask, jsonify
from models import db, Game, Review, User
from faker import Faker
from random import randint, choice as rc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Faker for generating fake data
fake = Faker()

# Routes
@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():
    games_data = []
    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games_data.append(game_dict)

    return jsonify(games_data), 200

@app.route('/reviews')
def reviews():
    reviews_data = []
    for review in Review.query.all():
        review_dict = {
            "score": review.score,
            "comment": review.comment,
            "user_id": review.user_id,
            "game_id": review.game_id,
        }
        reviews_data.append(review_dict)

    return jsonify(reviews_data), 200

@app.route('/users')
def users():
    users_data = []
    for user in User.query.all():
        user_dict = {
            "name": user.name,
        }
        users_data.append(user_dict)

    return jsonify(users_data), 200

# Seed Data
with app.app_context():
    db.init_app(app)
    db.create_all()

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
    genres = [
        "Platformer", "Shooter", "Fighting", "Stealth", "Survival",
        "Rhythm", "Survival Horror", "Metroidvania", "Text-Based",
        "Visual Novel", "Tile-Matching", "Puzzle", "Action RPG", "MMORPG",
        "Tactical RPG", "JRPG", "Life Simulator", "Vehicle Simulator",
        "Tower Defense", "Turn-Based Strategy", "Racing", "Sports",
        "Party", "Trivia", "Sandbox"
    ]
    platforms = [
        "NES", "SNES", "Nintendo 64", "GameCube", "Wii", "Wii U",
        "Nintendo Switch", "GameBoy", "GameBoy Advance", "Nintendo DS",
        "Nintendo 3DS", "XBox", "XBox 360", "XBox One", "XBox Series X/S",
        "PlayStation", "PlayStation 2", "PlayStation 3", "PlayStation 4",
        "PlayStation 5", "PSP", "PS Vita", "Genesis", "DreamCast", "PC",
    ]
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

    db.session.commit()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
