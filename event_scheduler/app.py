from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)

# ---------------- DATABASE MODELS ----------------

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    description = db.Column(db.String(200))

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(50))

class Allocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))

# ---------------- ROUTES ----------------

@app.route('/')
def index():
    return render_template('index.html')

# -------- EVENTS --------
@app.route('/events')
def events():
    return render_template('events.html', events=Event.query.all())

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        event = Event(
            title=request.form['title'],
            start_time=datetime.fromisoformat(request.form['start']),
            end_time=datetime.fromisoformat(request.form['end']),
            description=request.form['desc']
        )
        db.session.add(event)
        db.session.commit()
        return redirect('/events')
    return render_template('add_event.html')

# -------- RESOURCES --------
@app.route('/resources')
def resources():
    return render_template('resources.html', resources=Resource.query.all())

@app.route('/add_resource', methods=['GET', 'POST'])
def add_resource():
    if request.method == 'POST':
        resource = Resource(
            name=request.form['name'],
            type=request.form['type']
        )
        db.session.add(resource)
        db.session.commit()
        return redirect('/resources')
    return render_template('add_resource.html')

# -------- ALLOCATION + CONFLICT CHECK --------
@app.route('/allocate', methods=['GET', 'POST'])
def allocate():
    if request.method == 'POST':
        event_id = int(request.form['event'])
        resource_id = int(request.form['resource'])

        event = Event.query.get(event_id)

        # Conflict check
        existing_allocations = Allocation.query.filter_by(resource_id=resource_id).all()
        for a in existing_allocations:
            e = Event.query.get(a.event_id)
            if not (event.end_time <= e.start_time or event.start_time >= e.end_time):
                flash("❌ Conflict: Resource already allocated for this time slot!")
                return redirect('/allocate')

        # Save allocation
        db.session.add(Allocation(event_id=event_id, resource_id=resource_id))
        db.session.commit()
        flash("✅ Resource allocated successfully!")

        return redirect('/allocate')

    # GET request – show allocations
    allocations = []
    for a in Allocation.query.all():
        allocations.append({
            'event': Event.query.get(a.event_id).title,
            'resource': Resource.query.get(a.resource_id).name,
            'type': Resource.query.get(a.resource_id).type
        })

    return render_template(
        'allocate.html',
        events=Event.query.all(),
        resources=Resource.query.all(),
        allocations=allocations
    )


# -------- REPORT --------
@app.route('/report', methods=['GET', 'POST'])
def report():
    data = []
    start_date = None
    end_date = None

    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end'], '%Y-%m-%d')

        # include full end day
        end_date = end_date.replace(hour=23, minute=59, second=59)

    for r in Resource.query.all():
        total_hours = 0
        upcoming = []

        for a in Allocation.query.filter_by(resource_id=r.id).all():
            e = Event.query.get(a.event_id)

            # Apply date filter ONLY if user selected dates
            if start_date and end_date:
                if e.end_time < start_date or e.start_time > end_date:
                    continue

            duration = (e.end_time - e.start_time).total_seconds() / 3600
            total_hours += duration

            if e.start_time > datetime.now():
                upcoming.append(e.title)

        data.append({
            'name': r.name,
            'type': r.type,
            'hours': round(total_hours, 2),
            'upcoming': upcoming
        })

    return render_template(
        'report.html',
        data=data,
        start=start_date,
        end=end_date
    )


# -------- EDIT EVENT --------
@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    event = Event.query.get(id)
    if request.method == 'POST':
        event.title = request.form['title']
        event.start_time = datetime.fromisoformat(request.form['start'])
        event.end_time = datetime.fromisoformat(request.form['end'])
        event.description = request.form['desc']
        db.session.commit()
        return redirect('/events')
    return render_template('edit_event.html', event=event)

# -------- DELETE EVENT --------
@app.route('/delete_event/<int:id>')
def delete_event(id):
    Event.query.filter_by(id=id).delete()
    Allocation.query.filter_by(event_id=id).delete()
    db.session.commit()
    return redirect('/events')


# -------- EDIT RESOURCE --------
@app.route('/edit_resource/<int:id>', methods=['GET', 'POST'])
def edit_resource(id):
    resource = Resource.query.get(id)
    if request.method == 'POST':
        resource.name = request.form['name']
        resource.type = request.form['type']
        db.session.commit()
        return redirect('/resources')
    return render_template('edit_resource.html', resource=resource)

# -------- DELETE RESOURCE --------
@app.route('/delete_resource/<int:id>')
def delete_resource(id):
    Allocation.query.filter_by(resource_id=id).delete()
    Resource.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/resources')

@app.route('/allocations')
def allocations():
    data = []
    for a in Allocation.query.all():
        data.append({
            'event': Event.query.get(a.event_id).title,
            'resource': Resource.query.get(a.resource_id).name
        })
    return render_template('allocations.html', data=data)



# ---------------- MAIN ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # DATABASE CREATION
    app.run(debug=True)
