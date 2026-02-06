"""
Core portfolio routes
"""
import os
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .medium_feed import fetch_medium_posts

core_bp = Blueprint('core', __name__,
                     template_folder='templates',
                     static_folder='static')

@core_bp.route('/')
def core_home():
    data = fetch_medium_posts()
    return render_template('index.html', data=data)

@core_bp.route('/home')
def core_home2():
    data = fetch_medium_posts()
    return render_template('index.html', data=data)

@core_bp.route('/community')
def community_redirect():
    return redirect(url_for('core.core_home'), code=302)

@core_bp.route('/favicon.ico')
def favicon():
    return redirect(url_for('core.static', filename='core/images/favicon.svg'), code=302)

@core_bp.route('/consultation', methods=['POST'])
def consultation_submit():
    name = (request.form.get('name') or '').strip()
    email = (request.form.get('email') or '').strip()
    topic = (request.form.get('topic') or '').strip()
    message = (request.form.get('message') or '').strip()
    if not name or not email or not message:
        return jsonify({'success': False, 'error': 'Please fill in name, email, and message.'}), 400
    try:
        to_email = os.getenv('CONTACT_EMAIL', 'pparth967@gmail.com')
        body = f"New consultation request from portfolio\n\nName: {name}\nEmail: {email}\nTopic: {topic}\n\nMessage:\n{message}"
        if os.getenv('SMTP_HOST'):
            import smtplib
            from email.mime.text import MIMEText
            msg = MIMEText(body)
            msg['Subject'] = f"Portfolio consultation: {topic or 'General'}"
            # From must be your SMTP account (e.g. Gmail) so it delivers; Reply-To = submitter so you can reply
            from_email = os.getenv('SMTP_FROM') or os.getenv('SMTP_USER') or to_email
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Reply-To'] = email
            with smtplib.SMTP(os.getenv('SMTP_HOST'), int(os.getenv('SMTP_PORT', 587))) as s:
                if os.getenv('SMTP_USE_TLS', '1') == '1':
                    s.starttls()
                if os.getenv('SMTP_USER'):
                    s.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASSWORD', ''))
                s.send_message(msg)
        else:
            log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'consultation_requests.log')
            with open(log_path, 'a') as f:
                f.write(f"\n---\n{body}\n")
    except Exception as e:
        return jsonify({'success': False, 'error': 'Could not send. Please email directly.'}), 500
    return jsonify({'success': True})