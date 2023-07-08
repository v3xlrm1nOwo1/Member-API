from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DEBUG'] = True

# Database configration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Members.db'
db = SQLAlchemy(app)

# Created Database
class Members(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), unique=True)
	email = db.Column(db.String(100), unique=True)
	level = db.Column(db.String(100))

	def __repr__(self):
		return f'<name: {self.name}>'


# Get all Members
@app.route('/member', methods=['GET'])
def get_members():
	members = Members.query.order_by(Members.id).all()

	members_list = []

	for member in members:
		members_list.append({f'{member.id} - Member': {'ID': member.id, 'Name': member.name, 'Email': member.email, 'Level': member.level}})

	return jsonify({'Members': members_list})


# Get Member by ID
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
	member = Members.query.filter(Members.id==member_id).first()

	if member:
		return jsonify({'Member': {'ID': member.id, 'Name': member.name, 'Email': member.email, 'Level': member.level}})
	else:
		return jsonify({'Message': 'Not Find Member.'})


# Add new Member
@app.route('/member', methods=['POST'])
def add_member():
	if request.get_json():
		new_member_data = request.get_json()

		name = new_member_data['name']
		email = new_member_data['email']
		level = new_member_data['level']

		if Members.query.filter(Members.name==name).first():
			return jsonify({'Message': 'The name is already exists.'})

		elif Members.query.filter(Members.email==email).first():
			return jsonify({'Message': 'The email is already exists.'})

		else:
			new_member = Members(name=name, email=email, level=level)

		try:
			db.session.add(new_member)
			db.session.commit()

			new_member_data = Members.query.filter(Members.name==name).first()

			return jsonify({'Member': {'ID': new_member_data.id, 'Name': new_member_data.name, 'Email': new_member_data.email, 'Level': new_member_data.level}})

		except:
			return jsonify({'Message': 'There was an issue on your add member.'})

	else:
		return jsonify({'Message': 'Not Find "json data".'})


# Update a Member by ID
@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
	member = Members.query.filter(Members.id==member_id).first()
	if member:
		if request.get_json():
			update_member_data = request.get_json()

			name = update_member_data['name']
			email = update_member_data['email']
			level = update_member_data['level']

			if Members.query.filter(Members.name==name, Members.id!=member.id).first():
				return jsonify({'Message': 'The name is already exists.'})

			elif Members.query.filter(Members.email==email, Members.id!=member.id).first():
				return jsonify({'Message': 'The email is already exists.'})

			else:
				member.name = name
				member.email = email
				member.level = level
				
			try:
				db.session.commit()
				update_member_data = Members.query.filter(Members.name==name).first()
				return jsonify({'Member': {'ID': update_member_data.id, 'Name': update_member_data.name, 'Email': update_member_data.email, 'Level': update_member_data.level}})

			except:
				return jsonify({'Message': 'There was an issue on your update member.'})
		else:
			return jsonify({'Message': 'Not Find "json data".'})
	else:
		return jsonify({'Message': 'Not Find Member.'})


# Delete Member by ID 
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
	member = Members.query.filter(Members.id==member_id).first()
	if member:
		try:
			db.session.delete(member)
			db.session.commit()
			return jsonify({'Message': 'Delteting member successfully!.'})
		except:
			return jsonify({'Message': 'There was an problem delteting member.'})

	else:
		return jsonify({'Message': 'Not Find Member.'})


if __name__ == '__main__':
	app.run()
