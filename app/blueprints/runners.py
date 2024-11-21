from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

runners = Blueprint('runners', __name__)

@runners.route('/runner', methods=['GET', 'POST'])
def runner():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new runner
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Insert the new runner into the database
        cursor.execute('INSERT INTO runners (first_name, last_name) VALUES (%s, %s)', (first_name, last_name))
        db.commit()

        flash('New runner added successfully!', 'success')
        return redirect(url_for('runners.runner'))

    # Handle GET request to display all runners
    cursor.execute('SELECT * FROM runners')
    all_runners = cursor.fetchall()
    return render_template('runners.html', all_runners=all_runners)

@runners.route('/update_runner/<int:runner_id>', methods=['GET', 'POST'])
def update_runner(runner_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the runner's details
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        cursor.execute('UPDATE runners SET first_name = %s, last_name = %s WHERE runner_id = %s', (first_name, last_name, runner_id))
        db.commit()

        flash('Runner updated successfully!', 'success')
        return redirect(url_for('runners.runner'))

    # GET method: fetch runner's current data for pre-populating the form
    cursor.execute('SELECT * FROM runners WHERE runner_id = %s', (runner_id,))
    current_runner = cursor.fetchone()
    return render_template('update_runners.html', current_runner=current_runner)

@runners.route('/delete_runner/<int:runner_id>', methods=['POST'])
def delete_runner(runner_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the runner
    cursor.execute('DELETE FROM runners WHERE runner_id = %s', (runner_id,))
    db.commit()

    flash('Runner deleted successfully!', 'danger')
    return redirect(url_for('runners.runner'))

