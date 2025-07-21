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

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return [LearningEntry.from_dict(d) for d in data]
    except (json.JSONDecodeError, ValueError):
        print(">>> Warnung: JSON-Datei leer oder beschädigt – starte mit leerer Liste.")
        return []


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

@app.route("/notizen", methods=["GET", "POST"])
def notizen():
    if request.method == "POST":
        note = request.form["note"]

        # ⬇️ Beispiel: Note speichern (in Textdatei, Liste, Datenbank o. Ä.)
        with open("notizen.txt", "a", encoding="utf-8") as f:
            f.write(f"{note}\n")

        return redirect("/notizen")  # Nach dem Speichern zurück zur Seite

    return render_template("notizen.html")


@app.route("/lernprogramme", methods=["GET", "POST"])
def lernprogramme():
    if request.method == "POST":
        data = request.form.get("input_name")  # Passe das an deine Form an
        print("POST-Daten von /lernprogramme:", data)
        # Optional: Daten speichern oder verarbeiten
        return redirect("/lernprogramme")

    return render_template("lernprogramme.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        data = request.form.get("input_name")  # Passe das an deine Form an
        print("POST-Daten von /dashboard:", data)
        # Optional: Daten speichern oder verarbeiten
        return redirect("/dashboard")

    return render_template("dashboard.html")

# 5. Start Flask
if __name__ == "__main__":
    print(">>> Starte Webserver...")
    port = int(os.environ.get("PORT", 5000))  # use Render's dynamic port or 5000 for local
    app.run(debug=True, host="0.0.0.0", port=port)
