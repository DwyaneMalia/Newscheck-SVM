import json
from pathlib import Path

import joblib
from flask import Flask, render_template, request


# Resolve files relative to this script, even when started from another folder.
BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
# Flask rejects requests over this byte limit before the route processes them.
app.config["MAX_CONTENT_LENGTH"] = 1_000_000
MIN_ARTICLE_LENGTH = 100

# Load the saved TF-IDF + SVM pipeline once when the app starts.
model = joblib.load(BASE_DIR / "fake_news_svm.joblib")
# Display the recorded Colab evaluation; the website does not retrain the model.
metrics = json.loads((BASE_DIR / "metrics.json").read_text())


@app.route("/", methods=["GET", "POST"])
def index():
    # GET opens an empty page; the Clear link also uses GET to reset these values.
    article = ""
    result = None
    error = None

    if request.method == "POST":
        article = request.form.get("article", "").strip()

        # Check input on the server as well as through the HTML form controls.
        if not article:
            error = "Paste an article before analyzing."
        elif len(article) < MIN_ARTICLE_LENGTH:
            error = f"Please paste at least {MIN_ARTICLE_LENGTH} characters so the model has enough article text to analyze."
        elif len(article) > 50_000:
            error = "Please use an article with 50,000 characters or fewer."
        else:
            # The pipeline handles TF-IDF. Pass a list containing one raw article
            # and read its first prediction using the labels assigned in Colab.
            prediction = int(model.predict([article])[0])
            result = {0: "Fake", 1: "Real"}[prediction]

    # Keep submitted text visible and send the result/error to the same page.
    return render_template(
        "index.html",
        article=article,
        result=result,
        error=error,
        min_article_length=MIN_ARTICLE_LENGTH,
        accuracy=f"{metrics['test_accuracy']:.2%}",
        training_count=f"{metrics['training_articles']:,}",
        test_count=f"{metrics['testing_articles']:,}",
        fake_precision=f"{metrics['classification_report']['Fake']['precision']:.2%}",
        fake_recall=f"{metrics['classification_report']['Fake']['recall']:.2%}",
        real_precision=f"{metrics['classification_report']['Real']['precision']:.2%}",
        real_recall=f"{metrics['classification_report']['Real']['recall']:.2%}",
        confusion_matrix=metrics["confusion_matrix"],
    )


@app.errorhandler(413)
def too_large(error):
    # Handle requests blocked by MAX_CONTENT_LENGTH with a readable message.
    return "This request is too large. Go back and paste a shorter article.", 413


if __name__ == "__main__":
    # Start a local development server only when this file is run directly.
    app.run(host="127.0.0.1", port=5000)
