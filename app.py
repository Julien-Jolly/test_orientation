from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Charger les questions depuis le fichier JSON
with open("questions.json", "r", encoding="utf-8") as file:
    questions_data = json.load(file)


@app.route("/", methods=["GET", "POST"])
def questionnaire():
    if request.method == "POST":
        # Récupérer le nom de l'utilisateur et les réponses
        user_name = request.form.get("user_name")
        answers = {key: request.form.get(key) for key in questions_data.keys()}

        # Créer un fichier JSON pour l'utilisateur
        filename = f"reponses_{user_name}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({"nom_utilisateur": user_name, "reponses": answers}, f, ensure_ascii=False, indent=4)

        return redirect(url_for("merci", user_name=user_name))

    return render_template("questionnaire.html", questions=questions_data)


@app.route("/merci/<user_name>")
def merci(user_name):
    return render_template("merci.html", user_name=user_name)


if __name__ == "__main__":
    app.run(debug=True)
