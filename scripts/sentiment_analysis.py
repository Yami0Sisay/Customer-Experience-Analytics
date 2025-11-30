"""
Sentiment and Thematic Analysis
Task 2: Sentiment + Keyword/Theme Extraction
"""

import os
import sys
import pandas as pd


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_PATHS


from transformers import pipeline


class SentimentAnalyzer:
    """
    Uses DistilBERT (distilbert-base-uncased-finetuned-sst-2-english)
    to compute sentiment for each review.

    - Raw model output: POSITIVE / NEGATIVE + confidence score
    - Its is converted to:
        * sentiment_label_bert: positive / neutral / negative (3 classes)
        * sentiment_score_bert: signed score in [-1, 1]
    """

    def __init__(self, batch_size: int = 64):
        print("Loading DistilBERT sentiment model...")
        self.pipe = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        self.batch_size = batch_size

    def _map_to_3class(self, label: str, score: float):
        """
        Converts POSITIVE/NEGATIVE + score into:
        - 3-class label: positive / neutral / negative
        - signed score in [-1, 1]
        """
        label_up = label.upper()
        # Makes negative scores negative
        signed_score = score if label_up.startswith("POS") else -score

        # Thresholds can be tuned;
        if signed_score >= 0.3:
            final_label = "positive"
        elif signed_score <= -0.3:
            final_label = "negative"
        else:
            final_label = "neutral"

        return final_label, signed_score

    def add_sentiment(self, df: pd.DataFrame) -> pd.DataFrame:
        # Trys to figure out the text column name robustly
        text_col = "review"
        if text_col not in df.columns:
            for cand in ["review_text", "content", "text"]:
                if cand in df.columns:
                    text_col = cand
                    break

        if text_col not in df.columns:
            raise ValueError(
                "Could not find a review text column. "
                "Expected one of: 'review', 'review_text', 'content', 'text'."
            )

        texts = df[text_col].fillna("").astype(str).tolist()

        all_raw_labels = []
        all_raw_scores = []
        all_final_labels = []
        all_signed_scores = []

        print(f"Running DistilBERT sentiment on {len(texts)} reviews...")
        for start in range(0, len(texts), self.batch_size):
            batch = texts[start:start + self.batch_size]
            results = self.pipe(batch)

            for res in results:
                raw_label = res["label"]
                raw_score = float(res["score"])

                final_label, signed_score = self._map_to_3class(raw_label, raw_score)

                all_raw_labels.append(raw_label)
                all_raw_scores.append(raw_score)
                all_final_labels.append(final_label)
                all_signed_scores.append(signed_score)

        df = df.copy()
        df["sentiment_raw_label_bert"] = all_raw_labels      # POSITIVE / NEGATIVE
        df["sentiment_raw_score_bert"] = all_raw_scores      # 0–1 confidence
        df["sentiment_label_bert"] = all_final_labels        # positive / neutral / negative
        df["sentiment_score_bert"] = all_signed_scores       # -1 to 1

        return df



class ThemeAssigner:
    def __init__(self):
        # We'll define theme rules and/or TF-IDF here later
        pass

    def add_themes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Placeholder: will add themes column(s) based on review text.
        """
        return df


def main():
    print("=== Task 2: Sentiment and Thematic Analysis ===")

    # 1. Load processed reviews from Task 1
    input_path = DATA_PATHS['processed_reviews']
    print(f"Loading processed reviews from: {input_path}")
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} reviews")

    # 2. Run sentiment analysis (placeholder)
    sentiment_analyzer = SentimentAnalyzer()
    df = sentiment_analyzer.add_sentiment(df)

    # 3. Run theme assignment (placeholder)
    theme_assigner = ThemeAssigner()
    df = theme_assigner.add_themes(df)

    # 4. Save output for Task 2
    output_path = DATA_PATHS['sentiment_reviews']
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved sentiment + themes data to: {output_path}")

    return df


if __name__ == "__main__":
    main()
