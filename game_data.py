import json
import os
from datetime import datetime

class GameData:
    def __init__(self):
        self.data_file = "game_data.json"
        self.default_data = {
            "high_scores": [],
            "total_play_time": 0,
            "total_kills": 0,
            "powerups_collected": {
                "MULTI_SHOT": 0,
                "SPEED_BOOST": 0,
                "SHIELD": 0
            },
            "last_played": None,
            "settings": {
                "sound_volume": 0.3,
                "difficulty": "normal"
            }
        }
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return self.default_data.copy()
        return self.default_data.copy()

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_high_score(self, score, level):
        self.data["high_scores"].append({
            "score": score,
            "level": level,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # Keep only top 10 scores
        self.data["high_scores"] = sorted(
            self.data["high_scores"],
            key=lambda x: x["score"],
            reverse=True
        )[:10]
        self.save_data()

    def update_stats(self, play_time, kills, powerup_type=None):
        self.data["total_play_time"] += play_time
        self.data["total_kills"] += kills
        if powerup_type:
            self.data["powerups_collected"][powerup_type] += 1
        self.data["last_played"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_data()

    def get_high_scores(self):
        return self.data["high_scores"]

    def get_stats(self):
        return {
            "total_play_time": self.data["total_play_time"],
            "total_kills": self.data["total_kills"],
            "powerups_collected": self.data["powerups_collected"],
            "last_played": self.data["last_played"]
        }

    def update_settings(self, settings):
        self.data["settings"].update(settings)
        self.save_data()

    def get_settings(self):
        return self.data["settings"] 