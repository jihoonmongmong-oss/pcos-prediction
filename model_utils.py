import pandas as pd
import joblib
from config import MODEL_PATH

FEATURE_COLUMNS = [
    'age',
    'weight',
    'height',
    'blood_group',
    'menstrual_interval',
    'weight_gain',
    'hair_growth',
    'skin_darkening',
    'hair_loss',
    'acne',
    'fast_food',
    'exercise',
    'mood_swings',
    'periods_regular',
    'period_length'
]


def load_model():
    return joblib.load(MODEL_PATH)


def build_features(data):
    row = {
        'age': int(data['age']),
        'weight': float(data['weight']),
        'height': float(data['height']),
        'blood_group': int(data['blood_group']),
        'menstrual_interval': int(data['menstrual_interval']),
        'weight_gain': int(data['weight_gain']),
        'hair_growth': int(data['hair_growth']),
        'skin_darkening': int(data['skin_darkening']),
        'hair_loss': int(data['hair_loss']),
        'acne': int(data['acne']),
        'fast_food': int(data['fast_food']),
        'exercise': int(data['exercise']),
        'mood_swings': int(data['mood_swings']),
        'periods_regular': int(data['periods_regular']),
        'period_length': int(data['period_length'])
    }
    return pd.DataFrame([row], columns=FEATURE_COLUMNS)


def predict(data):
    model = load_model()
    features = build_features(data)
    proba = model.predict_proba(features)[0][1]
    label = int(proba >= 0.5)
    return label, float(proba)
