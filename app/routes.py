from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from . import app, db  # Change this line
from .models import TestRide, Service, User, Feedback  # Change this line

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('signup'))

@app.route('/home')
@login_required
def home():
    user_email = current_user.email if current_user.is_authenticated else None
    print(f"User Email: {user_email}")  # Add this line for debugging
    return render_template('home.html', user=current_user)

@app.route('/aboutus')
@login_required
def aboutus():
    return render_template('aboutus.html')

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        rating = int(request.form['rating'])

        new_feedback = Feedback(user=current_user,feedback_text=feedback_text,
            rating=rating)
        
        try:
            db.session.add(new_feedback)
            db.session.commit()
            flash('Feedback submitted successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting feedback: {str(e)}', 'error')

    return render_template('feedback.html', user=current_user)

    return render_template('feedback.html')

@app.route('/e_bikes')
@login_required
def e_bikes():
    return render_template('e_bikes.html')

@app.route('/test_ride', methods=['GET', 'POST'])
@login_required
def test_ride():
    if request.method == 'POST':
        # Get form data
        bike_model = request.form['bike']
        preferred_date = request.form['date']
        preferred_time = request.form['time']
        additional_comments = request.form['message']

        # Create a new TestRide instance
        new_test_ride = TestRide(
            user=current_user,
            bike_model=bike_model,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            additional_comments=additional_comments
        )

        # Add the test ride to the database
        try:
            db.session.add(new_test_ride)
            db.session.commit()
            flash('Test ride booked successfully!', 'success')
            return redirect(url_for('user_bookings'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error booking test ride: {str(e)}', 'error')

    return render_template('test_ride.html', user=current_user)

@app.route('/service', methods=['GET', 'POST'])
@login_required
def service():
    if request.method == 'POST':
        # Get form data
        bike_model = request.form['bike']
        service_type = request.form['service']
        scheduled_date = request.form['date']
        scheduled_time = request.form['time']
        additional_complaints = request.form['message']

        # Create a new Service instance
        new_service = Service(
            user=current_user,
            bike_model=bike_model,
            service_type=service_type,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            additional_complaints=additional_complaints
        )

        # Add the service to the database
        try:
            db.session.add(new_service)
            db.session.commit()
            flash('Service booked successfully!', 'success')
            return redirect(url_for('user_bookings'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error booking service: {str(e)}', 'error')

    return render_template('service.html', user=current_user)



@app.route('/user_bookings')
@login_required
def user_bookings():
    # Retrieve the test rides and service bookings for the current user
    test_rides = TestRide.query.filter_by(user_id=current_user.id).all()
    services = Service.query.filter_by(user_id=current_user.id).all()

    return render_template('user_bookings.html', test_rides=test_rides, services=services)

@app.route('/jetterclassic')
@login_required
def jetterclassic():
    return render_template('jetterclassic.html')

@app.route('/jettersports')
@login_required
def jettersports():
    return render_template('jettersports.html')

@app.route('/turnerex')
@login_required
def turnerex():
    return render_template('turner.html')

@app.route('/olas1pro')
@login_required
def olas1pro():
    return render_template('olas1pro.html')

@app.route('/dexpress')
@login_required
def dexpress():
    return render_template('dexpress.html')

@app.route('/zooba')
@login_required
def zooba():
    return render_template('zooba.html')

@app.route('/elyx')
@login_required
def elyx():
    return render_template('elyx.html')

@app.route('/tvs')
@login_required
def tvs():
    return render_template('tvs.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form['uname']
        email = request.form['uemail']
        password = request.form['upassword']
        phone = request.form['uphone']
        
        # Validate other form fields as needed
        if not name or not email or not password or not phone:
            flash('All fields are required.', 'error')
            return redirect(url_for('signup'))


        # Check if the username is already taken
        if User.query.filter_by(email=email).first():
            flash('Email is already taken. Choose another one.')
            return redirect(url_for('signup'))

        # Create a new user
        new_user = User(name=name,
                        email=email,
                        password=password,
                        phone=phone)
            

        # Add the user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'error')
            app.logger.error(f'Error creating account: {str(e)}')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database by username or email
        user = User.query.filter_by(email=email).first()

        if user:
            # Check if the provided password is correct
            if user.password == password:
                # Use Flask-Login's login_user function to log in the user
                login_user(user)
                flash('Login successful!')

                # Redirect to the "home" after a successful login
                return redirect(url_for('home'))
            else:
                flash('Login unsuccessful. Please check your username and password.')
        else:
            flash('User not found. Please check your username (or email).')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
     # Check if the user is authenticated before logging out
    if current_user.is_authenticated:
        # Use Flask-Login's logout_user function to log out the user
        logout_user()
        flash('Logout successful!', 'info')
    else:
        flash('You are not logged in.', 'warning')

    return redirect(url_for('login'))






