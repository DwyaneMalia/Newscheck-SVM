# NewsCheck — Fake News Article Classifier

An AI and Machine Learning group project for **1833 CST 9/L**.

A small Flask website that classifies full English news articles with your
Colab-trained TF-IDF + Linear SVM pipeline. No JavaScript, database, or account
is needed.

## Run locally

Install Python 3.13, then open a terminal in this folder:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python app.py
```

Open http://127.0.0.1:5000 in your browser. Paste an article and select
**Analyze article**. Select **Clear** to reset the page. Press Ctrl+C in the
terminal to stop the server. This command runs a local development server.

## Code to review

- `app.py`: loads the model once, checks the input, and renders the prediction.
- `templates/index.html`: the form, result, and model information.
- `static/style.css`: layout, colors, and mobile styling.

The form submits to `/` using POST. The Python route calls
`model.predict([article])`; 0 maps to Fake and 1 maps to Real. The saved pipeline
already includes TF-IDF, so the website passes the original text directly to it.
The browser escapes article text when displaying it. Blank input and articles
longer than 50,000 characters are rejected. Articles are not saved by the app.

## Included model files

- `fake_news_svm.joblib`: your original model, copied without retraining.
- `metrics.json`: your original Colab evaluation, displayed on the page.
- `requirements.txt`: your model's package versions plus Flask.

The supplied metrics report **99.01% accuracy on 7,674 held-out articles**. This
website does not independently reproduce that evaluation because the held-out
articles are not included. It classifies text patterns, not factual truth; new
articles may perform differently. Removing normalized duplicates during training
does not remove all related stories or source-specific patterns.

The model was trained with Python 3.13.18. Use Python 3.13 and the pinned library
versions for your own setup. Only load the joblib model you trained and trust.
No confidence percentage is shown because LinearSVC scores are not calibrated
probabilities.

## Verification performed

Local checks passed using Python 3.12.14 with the exact model library versions
listed above: model loading, direct-model versus web prediction agreement for
two sample articles, missing/blank input, length limits, HTML escaping, reset,
and original model file integrity. Dependency checks also passed. Browser checks
confirmed article submission and Clear. The Python 3.13 setup instructions above
were not independently tested in a fresh Python 3.13 environment.
