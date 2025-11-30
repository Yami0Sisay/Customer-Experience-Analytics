"""
Thematic Analysis Pipeline
Extract keywords, n-grams, TF-IDF, and assign themes (rule-based).
"""

import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


# Text Preprocessing

def clean_text(text: str) -> str:
    """Lowercase, remove special chars, normalize spaces."""
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Keyword Extraction

def extract_top_ngrams(texts, n=1, top_k=20):
    """
    Frequency-based n-grams using CountVectorizer.
    n=1 → unigrams, n=2 → bigrams, n=3 → trigrams.
    """
    vectorizer = CountVectorizer(ngram_range=(n, n), stop_words="english")
    X = vectorizer.fit_transform(texts)
    vocab = vectorizer.get_feature_names_out()
    counts = np.asarray(X.sum(axis=0)).flatten()
    df_counts = pd.DataFrame({"ngram": vocab, "count": counts})
    return df_counts.sort_values("count", ascending=False).head(top_k)


def extract_tfidf_keywords(texts, top_k=20):
    """
    TF-IDF scoring for unigrams.
    Higher TF-IDF = more informative word.
    """
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    X = vectorizer.fit_transform(texts)
    vocab = vectorizer.get_feature_names_out()
    scores = np.asarray(X.mean(axis=0)).flatten()
    df_tfidf = pd.DataFrame({"word": vocab, "tfidf": scores})
    return df_tfidf.sort_values("tfidf", ascending=False).head(top_k)


# Theme Assignment

def assign_theme(text: str) -> str:
    """
    Very simple rule-based theme assignment based on keywords.
    You can refine these rules in the notebook.
    """
    text = text.lower()

    rules = {
        "Account Access Issues": [
            "login", "log in", "password", "pin", "otp", "verify", "verification", "session"
        ],
        "Transaction Performance": [
            "slow", "delay", "delayed", "hang", "loading", "timeout", "transfer", "transaction"
        ],
        "Crashes & Bugs": [
            "crash", "crashes", "bug", "bugs", "freeze", "frozen", "stuck", "error", "fail", "problem"
        ],
        "User Interface & Experience": [
            "interface", "ui", "ux", "design", "layout", "user friendly", "navigation", "easy to use"
        ],
        "Feature Requests": [
            "add", "feature", "option", "doesn't have", "doesnt have", "missing", "please include"
        ],
        "Customer Support": [
            "support", "help", "service", "customer care", "agent"
        ],
    }

    for theme, keywords in rules.items():
        if any(k in text for k in keywords):
            return theme

    return "Other"


def run_thematic_analysis(df: pd.DataFrame, text_col: str = "review") -> pd.DataFrame:
    """
    Apply cleaning + rule-based theme assignment to a DataFrame.
    """
    if text_col not in df.columns:
        raise ValueError(f"Expected text column '{text_col}' in DataFrame.")

    df = df.copy()
    df["clean_text"] = df[text_col].apply(clean_text)
    df["theme"] = df["clean_text"].apply(assign_theme)
    return df
