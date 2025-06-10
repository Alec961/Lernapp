from flask import Flask

print(">>> Starte Flask-Test...")

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hallo von deiner App!"

if __name__ == "__main__":
    print(">>> Starte Webserver...")
    app.run(debug=True)

DATA_FILE = "lernfortschritt.json"  # JSON file to store entries


# 1. Class to represent a learning entry
class LearningEntry:
    def __init__(self, topic, description, duration_minutes, learning_date=None):
        self.topic = topic
        self.description = description
        self.duration_minutes = duration_minutes
        self.learning_date = learning_date or date.today()

    def to_dict(self):
        # Converts object to dictionary for saving
        return {
            "topic": self.topic,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "learning_date": self.learning_date.isoformat()
        }

    @staticmethod
    def from_dict(data):
        # Converts dictionary back into a LearningEntry object
        return LearningEntry(
            topic=data["topic"],
            description=data["description"],
            duration_minutes=data["duration_minutes"],
            learning_date=date.fromisoformat(data["learning_date"])
        )


# 2. Load existing entries from JSON file
def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return [LearningEntry.from_dict(d) for d in data]


# 3. Save all entries to JSON file
def save_entries(entries):
    with open(DATA_FILE, "w") as f:
        json.dump([e.to_dict() for e in entries], f, indent=2)


# 4. Route: "/" (main page)
@app.route("/", methods=["GET", "POST"])
def index():
    entries = load_entries()

    if request.method == "POST":
        # Get form data submitted by user
        topic = request.form["topic"]
        description = request.form["description"]
        duration = int(request.form["duration"])

        # Create and save new entry
        new_entry = LearningEntry(topic, description, duration)
        entries.append(new_entry)
        save_entries(entries)

        return redirect("/")  # Prevent double form submission

    # Show the page with current entries
    return render_template("index.html", entries=entries)


# 5. Start the Flask app
if __name__ == "__main__":
    # "debug=True" reloads the app when you make changes
    # "host='0.0.0.0'" lets you test on your iPhone over Wi-Fi
    app.run(debug=True, host="0.0.0.0")
