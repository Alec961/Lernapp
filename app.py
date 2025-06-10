from flask import Flask, render_template, request, redirect
from datetime import date
import json
import os

print(">>> Starte Flask-App...")

app = Flask(__name__)

DATA_FILE = "lernfortschritt.json"  # JSON file to store entries


# 1. Class to represent a learning entry
class LearningEntry:
    def __init__(self, topic, description, duration_minutes, learning_date=None):
        self.topic = topic
        self.description = description
        self.duration_minutes = duration_minutes
        self.learning_date = learning_date or date.today()

    def to_dict(self):
        return {
            "topic": self.topic,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "learning_date": self.learning_date.isoformat()
        }

    @staticmethod
    def from_dict(data):
        return LearningEntry(
            topic=data["topic"],
            description=data["description"],
            duration_minutes=data["duration_minutes"],
            learning_date=date.fromisoformat(data["learning_date"])
        )


# 2. Load existing entries
def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return [LearningEntry.from_dict(d) for d in data]


# 3. Save entries
def save_entries(entries):
    with open(DATA_FILE, "w") as f:
        json.dump([e.to_dict() for e in entries], f, indent=2)


# 4. Route: index page
@app.route("/", methods=["GET", "POST"])
def index():
    entries = load_entries()

    if request.method == "POST":
        topic = request.form["topic"]
        description = request.form["description"]
        duration = int(request.form["duration"])
        new_entry = LearningEntry(topic, description, duration)
        entries.append(new_entry)
        save_entries(entries)
        return redirect("/")

    return render_template("index.html", entries=entries)


# 5. Start Flask
if __name__ == "__main__":
    print(">>> Starte Webserver...")
    port = int(os.environ.get("PORT", 5000))  # use Render's dynamic port or 5000 for local
    app.run(debug=True, host="0.0.0.0", port=port)
