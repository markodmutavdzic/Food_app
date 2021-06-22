import datetime

from flask_script import Manager

from clearbit_info import additional_data
from recipes import app, User, db

manager = Manager(app)


@manager.command
def update_users_clearbit():
    users_to_update = User.query.filter_by(user_location="Clear").all()

    for user in users_to_update:
        user_data = additional_data(user.email)
        user.user_location = user_data['user_location']
        user.user_title = user_data['user_title']
        user.company_name = user_data['company_name']
        user.company_sector = user_data['company_sector']
    db.session.commit()
    db.session.close()


if __name__ == "__main__":
    manager.run()
