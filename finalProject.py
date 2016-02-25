from flask import Flask, redirect, render_template, request, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from workoutDatabaseSetup import Base, BodyPart, WorkoutMovement

engine = create_engine('sqlite:///workoutmovement.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route("/")
@app.route("/workout/")
def indexCategory():
	categories = session.query(BodyPart).all()
	return render_template('indexWorkout.html', categories= categories, url_font= "https://fonts.googleapis.com/css?family=Open+Sans")

@app.route("/workout/newcate/", methods=['POST', 'GET'])
def addCategory():
	if request.method == 'POST':
		newCate = BodyPart(name= request.form['cate_name'], description= request.form['description'])
		session.add(newCate)
		session.commit()
		return redirect(url_for('indexCategory'))
	else:
		return render_template('createNewCate.html')

@app.route("/workout/<int:category_id>/editcate/", methods=['POST', 'GET'])
def editCategory(category_id):
	target = session.query(BodyPart).filter_by(id= category_id).one()
	if request.method == 'POST':
		if request.form['edit_name']:
			target.name = request.form['edit_name']
		if request.form['edit_descri']:
			target.description = request.form['edit_descri']
		session.add(target)
		session.commit()
		return redirect(url_for('indexCategory'))
	else:
		return render_template('editCate.html', i= target, category_id= category_id)

@app.route("/workout/<int:category_id>/deletecate/", methods=['POST', 'GET'])
def deleteCategory(category_id):
	target = session.query(BodyPart).filter_by(id=category_id).one()
	if request.method == 'POST':
		session.delete(target)
		session.commit()
		return redirect(url_for('indexCategory'))
	else:
		return render_template('deleteCate.html', i=target, category_id= category_id)

@app.route("/workout/<int:category_id>/movementlist/")
def indexMovement(category_id):
	category = session.query(BodyPart).filter_by(id=category_id).one()
	movement = session.query(WorkoutMovement).filter_by(bodypart_id= category.id)
	return render_template('indexMovement.html', category=category, movement=movement)

@app.route("/workout/<int:category_id>/newmove/", methods=['POST', 'GET'])
def addMovement(category_id):
	cate = session.query(BodyPart).filter_by(id=category_id).one()
	if request.method == 'POST':
		newMove = WorkoutMovement(name= request.form['move_name'], personal_record= request.form['move_pr'], bodypart_id= cate.id)
		session.add(newMove)
		session.commit()
		return redirect(url_for('indexMovement', category_id= cate.id))
	else:
		return render_template('createMovement.html', i= cate)

@app.route("/workout/<int:category_id>/<int:movement_id>/edit/", methods=['POST', 'GET'])
def editMovement(category_id, movement_id):
	target = session.query(WorkoutMovement).filter_by(id=movement_id).one()
	if request.method == 'POST':
		if request.form['edit_name']:
			target.name = request.form['edit_name']
			session.add(target)
			session.commit()
		return redirect(url_for('indexMovement', category_id= category_id)) 
	else:
		return render_template('editMovement.html', i=target, category_id= category_id)

@app.route("/workout/<int:category_id>/<int:movement_id>/delete/", methods=['POST', 'GET'])
def deleteMovement(category_id, movement_id):
	cate = session.query(BodyPart).filter_by(id= category_id).one()
	target = session.query(WorkoutMovement).filter_by(id= movement_id).one()
	if request.method == 'POST':
		session.delete(target)
		session.commit()
		return redirect(url_for('indexMovement', category_id= category_id))
	else:
		return render_template('deleteMovement.html', i= target, cate= cate)


if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0', port=8080)