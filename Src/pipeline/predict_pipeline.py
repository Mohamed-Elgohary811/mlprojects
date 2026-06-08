"""Minimal prediction pipeline stub used for local development and testing.

This provides `CustomData` and `PredictPipeline` so `app.py` can import
and run without the real trained model. Replace with your real pipeline
or restore the original file when available.
"""
import pandas as pd
import numpy as np


class CustomData:
    def __init__(
        self,
        gender=None,
        race_ethnicity=None,
        parental_level_of_education=None,
        lunch=None,
        test_preparation_course=None,
        reading_score=0,
        writing_score=0,
    ):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        data = {
            "gender": [self.gender],
            "race_ethnicity": [self.race_ethnicity],
            "parental_level_of_education": [self.parental_level_of_education],
            "lunch": [self.lunch],
            "test_preparation_course": [self.test_preparation_course],
            "reading_score": [self.reading_score],
            "writing_score": [self.writing_score],
        }
        return pd.DataFrame(data)


class PredictPipeline:
    def __init__(self):
        # In the real pipeline you'd load models/encoders here.
        pass

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Return a simple dummy prediction: mean of reading and writing scores.

        This keeps the web UI functional until the real model is restored.
        """
        # Ensure numeric
        df = df.copy()
        df["reading_score"] = pd.to_numeric(df.get("reading_score", 0), errors="coerce").fillna(0)
        df["writing_score"] = pd.to_numeric(df.get("writing_score", 0), errors="coerce").fillna(0)

        preds = (df["reading_score"] + df["writing_score"]) / 2.0
        return preds.to_numpy()
