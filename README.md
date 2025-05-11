🚀 2D Space Shooter Game

A fast-paced, retro-inspired space shooter built with Python and Pygame. Destroy waves of enemies, collect power-ups, and survive as long as you can!

📖 Table of Contents

Gameplay Features

Project Structure

Requirements

Running the Game

Controls

Data Tracking

License

Credits
🎮 Gameplay Features

Procedurally generated sprites and sound effects

Multiple enemy types and increasing difficulty

Power-ups: Shield, Speed Boost, Multi-Shot

Scoring and high score tracking

Game stats tracking (kills, playtime, power-ups collected)

Polished Game Over screen with stats and high score list
📦 Project Structure
.
├── main.py              # Game loop and logic
├── create_sprites.py    # Sprite generation for ships, enemies, bullets
├── create_sounds.py     # Procedural sound generation
├── game_data.py         # GameData class for handling state and JSON
├── game_data.json       # Stores high scores, settings, and stats
├── run_game.sh          # Shell script to run the game
└── README.md            # You're reading it!

🧪 Requirements

Python 3.8+

Pygame (tested with version 2.1+)

Install dependencies using pip:
pip install pygame

🚀 Running the Game

Use the shell script or run the main file directly:
# Option 1: With shell script (Linux/macOS)
bash run_game.sh

# Option 2: Directly in Python
python main.py
🛠️ Controls

Arrow Keys / WASD – Move your ship

Spacebar – Shoot

P – Pause

ESC – Quit

📈 Data Tracking

Game statistics are saved in game_data.json, including:

High scores (top 10)

Total kills and play time

Power-ups collected

Game settings (sound volume, difficulty)

📜 License

This project is open-source for educational and non-commercial use. Feel free to modify and share!

👨‍💻 Credits

Code & Design: Arshak

Sound & Graphics: Generated procedurally via Python