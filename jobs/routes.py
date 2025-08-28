from flask import Blueprint, render_template, request, session, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename

jobs_bp = Blueprint('jobs', __name__)

# Configurations
UPLOAD_FOLDER = 'static/resumes'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
jobs_list = []
applications = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@jobs_bp.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if session.get('role') != 'Employer':
        flash("Access denied. Only Employers can post jobs.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if not title or not description:
            flash("Please fill all fields")
            return render_template('post_job.html')

        job = {
            'title': title,
            'description': description,
            'posted_by': session.get('email')
        }
        jobs_list.append(job)

        flash("Job posted successfully!")
        return redirect(url_for('jobs.post_job'))

    return render_template('post_job.html')


@jobs_bp.route('/jobs')
def view_jobs():
    if session.get('role') != 'Job Seeker':
        flash("Access denied. Only Job Seekers can view jobs.")
        return redirect(url_for('auth.login'))

    return render_template('jobs.html', jobs=jobs_list)


@jobs_bp.route('/apply/<string:title>', methods=['GET', 'POST'])
def apply_job(title):
    if session.get('role') != 'Iam a Job Seeker':
        flash("Only Job Seekers can apply for jobs.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        resume = request.files.get('resume')
        if resume and allowed_file(resume.filename):
            filename = secure_filename(f"{title}_{session.get('email')}_{resume.filename}")
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            resume.save(save_path)

            applications.append({
                'job_title': title,
                'applicant': session.get('email'),
                'resume_filename': filename
            })

            flash("Application submitted successfully!")
            return redirect(url_for('jobs.view_jobs'))
        else:
            flash("Invalid or missing resume file. Only PDF/DOC/DOCX allowed.")

    return render_template('apply_job.html', job={'title': title})


@jobs_bp.route('/applications')
def view_applications():
    if session.get('role') != 'Employer':
        flash("Access denied. Only Employers can view applications.")
        return redirect(url_for('auth.login'))

    return render_template('dashboard_employer.html', applications=applications)


@jobs_bp.route('/resumes/<filename>')
def download_resume(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
