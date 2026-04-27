import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

RAW_CSV = 'CLEAN- PCOS SURVEY SPREADSHEET.csv'
MODEL_PATH = 'model.pkl'

COLUMN_MAP = {
    'Age (in Years)': 'age',
    'Weight (in Kg)': 'weight',
    'Height (in Cm / Feet)': 'height',
    'Can you tell us your blood group ?': 'blood_group',
    'After how many months do you get your periods?\n(select 1- if every month/regular)': 'menstrual_interval',
    'Have you gained weight recently?': 'weight_gain',
    'Do you have excessive body/facial hair growth ?': 'hair_growth',
    'Are you noticing skin darkening recently?': 'skin_darkening',
    'Do have hair loss/hair thinning/baldness ?': 'hair_loss',
    'Do you have pimples/acne on your face/jawline ?': 'acne',
    'Do you eat fast food regularly ?': 'fast_food',
    'Do you exercise on a regular basis ?': 'exercise',
    'Have you been diagnosed with PCOS/PCOD?': 'pcos',
    'Do you experience mood swings ?': 'mood_swings',
    'Are your periods regular ?': 'periods_regular',
    'How long does your period last ? (in Days)\nexample- 1,2,3,4.....': 'period_length'
}

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


def load_dataset():
    raw = pd.read_csv(RAW_CSV)
    raw = raw.rename(columns=COLUMN_MAP)
    raw = raw[list(COLUMN_MAP.values())]
    raw = raw.dropna()
    raw = raw.astype({
        'age': int,
        'weight': float,
        'height': float,
        'blood_group': int,
        'menstrual_interval': int,
        'weight_gain': int,
        'hair_growth': int,
        'skin_darkening': int,
        'hair_loss': int,
        'acne': int,
        'fast_food': int,
        'exercise': int,
        'mood_swings': int,
        'periods_regular': int,
        'period_length': int,
        'pcos': int,
    })
    return raw


def train():
    df = load_dataset()
    X = df[FEATURE_COLUMNS]
    y = df['pcos']

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(max_iter=500, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    score = pipeline.score(X_test, y_test)
    print(f'Training complete. Test accuracy: {score:.4f}')
    joblib.dump(pipeline, MODEL_PATH)
    print(f'Model saved to {MODEL_PATH}')


if __name__ == '__main__':
    train()
