from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SECRET_KEY'] = 'eventmgmt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  #admin/user

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    available_tickets = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    tickets = db.Column(db.Integer, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']         
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  
            if user.role.value == 'admin':
                login_user(user)
                return "Ok",200
            
            else:
                login_user(user)
                return "ok",200
                
        else:
            return "Invalid username or password", 401  
        
    return "ok",200


@app.route("/admin/events",methods=["GET"])
def viewEvents():
    event_list = Event.query.all()
    return jsonify([event.to_dict() for event in event_list])


@app.route("/admin/events", methods=["POST"])
def postEvent():
    data=request.json
    event = Event(
        name=data['name'], 
        date=data['date'],
        location=data['location'], 
        available_tickets=data['available_tickets']
    )
    db.session.add(event)
    db.session.commit()
    return "Event added", 201


@app.route("/admin/events/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    data = request.json
    event = Event.query.get(event_id)
    if not event:
        return "Event not found", 404
    event.name = data.get('name', event.name)
    event.date = data.get('date', event.date)
    event.location = data.get('location', event.location)
    event.available_tickets = data.get('available_tickets', event.available_tickets)
    db.session.commit()
    return "Event updated", 200

@app.route("/admin/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return "Event not found", 404
    db.session.delete(event)
    db.session.commit()
    return "Event deleted", 200

@app.route("/events", methods=["GET"])
def view_events():
    events = Event.query.filter(Event.available_tickets > 0).all()
    return jsonify([event.to_dict() for event in events])

@app.route("/events/<int:event_id>/book", methods=["POST"])
def book_event(event_id):
    event = Event.query.get(event_id)
    if not event or event.available_tickets <= 0:
        return "Event not available", 400

    tickets = int(request.json.get('tickets', 1))
    if tickets > event.available_tickets:
        return "Not enough tickets", 400

    booking = Booking(user_id=current_user.id, event_id=event.id, tickets=tickets)
    event.available_tickets -= tickets
    db.session.add(booking)
    db.session.commit()
    return "Booking successful", 200


@app.route('/events/<int:event_id>/cancel', methods=['DELETE'])
def cancel_booking(event_id):
    booking = Booking.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    if not booking:
        return "Booking not found", 404

    event = Event.query.get(event_id)
    event.available_tickets += booking.tickets
    db.session.delete(booking)
    db.session.commit()
    return "Booking cancelled", 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  

        User.query.delete()
        Event.query.delete()
        Booking.query.delete()
        db.session.commit()
        new_user1 = User(id=1, username="userhu", password="xyzabc", role="user")
        db.session.add(new_user1)

        new_user2 = User(id=2, username="adminhu", password="bnv678", role="admin")
        db.session.add(new_user2)

        db.session.commit()
    app.run(debug=True)