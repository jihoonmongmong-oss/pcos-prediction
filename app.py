import os
from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_connection, init_db
from model_utils import predict
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

BLOOD_GROUPS = [
    (11, 'A+'),
    (12, 'A-'),
    (13, 'B+'),
    (14, 'B-'),
    (15, 'AB+'),
    (16, 'AB-')
]
BLOOD_GROUP_LABELS = {key: label for key, label in BLOOD_GROUPS}


def to_bool(value):
    return 1 if str(value) in ('1', 'True', 'true', 'yes', 'on') else 0


@app.context_processor
def inject_blood_group_labels():
    return dict(blood_group_labels=BLOOD_GROUP_LABELS)


def load_patient_data(form):
    return {
        'age': int(form['age']),
        'weight': float(form['weight']),
        'height': float(form['height']),
        'blood_group': int(form['blood_group']),
        'menstrual_interval': int(form['menstrual_interval']),
        'weight_gain': to_bool(form.get('weight_gain', 0)),
        'hair_growth': to_bool(form.get('hair_growth', 0)),
        'skin_darkening': to_bool(form.get('skin_darkening', 0)),
        'hair_loss': to_bool(form.get('hair_loss', 0)),
        'acne': to_bool(form.get('acne', 0)),
        'fast_food': to_bool(form.get('fast_food', 0)),
        'exercise': to_bool(form.get('exercise', 0)),
        'mood_swings': to_bool(form.get('mood_swings', 0)),
        'periods_regular': to_bool(form.get('periods_regular', 0)),
        'period_length': int(form['period_length'])
    }


def insert_patient(conn, patient_data):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO patients (
            age, weight, height, blood_group, menstrual_interval,
            weight_gain, hair_growth, skin_darkening, hair_loss, acne,
            fast_food, exercise, mood_swings, periods_regular, period_length
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        tuple(patient_data.values())
    )
    conn.commit()
    patient_id = cursor.lastrowid
    cursor.close()
    return patient_id


def insert_prediction(conn, patient_id, prediction, probability):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO predictions (patient_id, prediction, probability) VALUES (%s, %s, %s)",
        (patient_id, prediction, probability)
    )
    conn.commit()
    cursor.close()


_db_initialized = False


@app.before_request
def ensure_database_initialized():
    global _db_initialized
    if not _db_initialized:
        init_db()
        _db_initialized = True


@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT COUNT(*) AS total_patients FROM patients')
    total_patients = cursor.fetchone()['total_patients']
    cursor.execute('SELECT COUNT(*) AS total_predictions FROM predictions')
    total_predictions = cursor.fetchone()['total_predictions']
    cursor.execute('SELECT prediction, COUNT(*) AS count FROM predictions GROUP BY prediction')
    prediction_counts = cursor.fetchall()
    cursor.execute('SELECT p.*, pr.prediction, pr.probability, pr.created_at FROM patients p JOIN predictions pr ON p.id = pr.patient_id ORDER BY pr.created_at DESC LIMIT 5')
    recent_history = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        'index.html',
        blood_groups=BLOOD_GROUPS,
        total_patients=total_patients,
        total_predictions=total_predictions,
        prediction_counts=prediction_counts,
        recent_history=recent_history
    )


@app.route('/predict', methods=['POST'])
def predict_route():
    data = load_patient_data(request.form)
    prediction, probability = predict(data)
    try:
        conn = get_connection()
        patient_id = insert_patient(conn, data)
        insert_prediction(conn, patient_id, prediction, probability)
        conn.close()
        flash(f'Prediction complete: PCOS risk = {probability:.2f} ({"Positive" if prediction == 1 else "Negative"})', 'success')
    except Exception as err:
        flash(f'Database error: {err}', 'danger')
    return redirect(url_for('index'))


@app.route('/patients')
def patients():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM patients ORDER BY created_at DESC')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('patients.html', patients=rows)


@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        data = load_patient_data(request.form)
        try:
            conn = get_connection()
            insert_patient(conn, data)
            conn.close()
            flash('Patient record added successfully.', 'success')
            return redirect(url_for('patients'))
        except Exception as err:
            flash(f'Error adding patient: {err}', 'danger')

    return render_template('patient_form.html', blood_groups=BLOOD_GROUPS, action='Add', patient={})


@app.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM patients WHERE id = %s', (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        conn.close()
        flash('Patient record not found.', 'warning')
        return redirect(url_for('patients'))

    if request.method == 'POST':
        data = load_patient_data(request.form)
        cursor.execute(
            """
            UPDATE patients SET
                age=%s, weight=%s, height=%s, blood_group=%s, menstrual_interval=%s,
                weight_gain=%s, hair_growth=%s, skin_darkening=%s, hair_loss=%s, acne=%s,
                fast_food=%s, exercise=%s, mood_swings=%s, periods_regular=%s, period_length=%s
            WHERE id=%s
            """,
            (*tuple(data.values()), patient_id)
        )
        conn.commit()
        conn.close()
        flash('Patient record updated successfully.', 'success')
        return redirect(url_for('patients'))

    conn.close()
    return render_template('patient_form.html', blood_groups=BLOOD_GROUPS, action='Edit', patient=patient)


@app.route('/patients/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM patients WHERE id = %s', (patient_id,))
        conn.commit()
        conn.close()
        flash('Patient record deleted.', 'success')
    except Exception as err:
        flash(f'Unable to delete patient record: {err}', 'danger')
    return redirect(url_for('patients'))


@app.route('/history')
def history():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        'SELECT pr.id, pr.prediction, pr.probability, pr.created_at, p.age, p.blood_group, p.menstrual_interval FROM predictions pr JOIN patients p ON p.id = pr.patient_id ORDER BY pr.created_at DESC'
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('history.html', history=rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
