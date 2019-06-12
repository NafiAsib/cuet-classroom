from flask import render_template, url_for, flash, redirect, request, abort
from classroom import app, db, bcrypt
from classroom.forms import RegistrationForm, LoginForm, PostForm
from classroom.models import User, Ct
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Successfully created account for {form.username.data}! Your are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Log in unsuccessfull!! Please check email and password', 'danger')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        ct = Ct(course=form.course.data, date=form.date.data, time=form.time.data, syllabus=form.syllabus.data, poster=current_user)
        db.session.add(ct)
        db.session.commit()
        flash('Successfully created post!', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form, legend='Add CT')

@app.route('/ct')
def ct():
    posts = Ct.query.all()
    return render_template('ct.html', posts=posts)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Ct.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Ct.query.get_or_404(post_id)
    if post.poster != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.course = form.course.data
        post.date = form.date.data
        post.time = form.time.data
        post.syllabus = form.syllabus.data
        db.session.commit()
        flash("CT schedule has been updated!", 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.course.data = post.course
        form.date.data = post.date
        form.time.data = post.time
        form.syllabus.data = post.syllabus
    return render_template('create_post.html', form=form, legend='Update CT')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Ct.query.get_or_404(post_id)
    if post.poster != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("CT schedule has been deleted!", 'success')
    return redirect(url_for('ct'))