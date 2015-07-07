from flask.ext.security import UserMixin, RoleMixin
from VocabFinder import db

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    """Basic Role class"""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(UserMixin, db.Model):
    """Basic User class"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    sets = db.relationship('VocabSet', backref=db.backref('user'))

    @classmethod
    def get(self_class, id):
        """Return user instance of id, return None if not exist"""
        try:
            return self_class(id)
        except UserNotFoundError:
            return None

    def __repr__(self):
        return '<User %r>' % (self.email)

class VocabSet(db.Model):
    """The vocab set for a particular source"""
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(500))
    text = db.Column(db.Text)
    difficulty = db.Column(db.String(30))
    num_words = db.Column(db.Integer)
    public = db.Column(db.Boolean())
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<VocabSet %r>' % (self.source)
