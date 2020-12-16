import os
import unittest
import sys

sys.path.insert(1, '/home/toshka/PycharmProjects/EPAM linux/EPAM/')
from instance.config import Config
from app.app import app, db


class TestCase(unittest.TestCase):

    def setUp(self):
        basedir = Config()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir.basedir, 'test.db')
        self.app = app.test_client()

        from main import main
        from models.dep import dep
        from api.views import api
        from models.empl import emp

        self.app.register_blueprint(main)
        self.app.register_blueprint(emp)
        self.app.register_blueprint(dep)
        self.app.register_blueprint(api)
        print(self.app.get('/'))

    def views_add_department(self, name):
        return self.app.post('/api/department', json=dict(
            name=name
        ), follow_redirects=True)

    def views_update_department(self, id, name):
        return self.app.put('/api/department/' + str(id), data=dict(
            name=name
        ), follow_redirects=True)

    def views_get_department(self, id):
        return self.app.get('/api/department/' + str(id))

    def views_get_departments(self):
        return self.app.get('/api/department')

    def views_delete_department(self, id):
        return self.app.delete('/api/department/' + str(id))

    def test_views_department(self):
        rv = self.views_add_department('first_dep')
        assert b'Department has been added!' in rv.data
        rv = self.views_add_department('first_dep')
        assert b'Department with this name already exists.' in rv.data
        rv = self.views_add_department('1')
        assert b'Field must be between 2 and 100 characters long.' in rv.data
        self.views_add_department('second_dep')
        rv = self.views_get_departments()
        assert (b'first_dep' and b'second_dep') in rv.data
        rv = self.views_get_department(1)
        assert b'first_dep' in rv.data
        self.views_delete_department(1)
        self.views_delete_department(2)
        rv = self.views_get_departments()
        assert b'first_dep' not in rv.data

    def views_add_employee(self, name, date_of_birth, salary, dep_id):
        return self.app.post('/api/employee', data=dict(
            name=name,
            date_of_birth=date_of_birth,
            salary=salary,
            dep=dep_id
        ), follow_redirects=True)

    def views_update_employee(self, id, name, date_of_birth, salary, dep_id):
        return self.app.put('/api/employee/' + str(id), data=dict(
            name=name,
            date_of_birth=date_of_birth,
            salary=salary,
            dep=dep_id
        ), follow_redirects=True)

    def views_get_employee(self, id):
        return self.app.get('/api/employee/' + str(id))

    def views_get_employess(self):
        return self.app.get('/api/employee')

    def views_delete_employee(self, id):
        return self.app.delete('/api/employee/' + str(id))

    def test_views_employee(self):
        rv = self.views_add_employee('Anton', '11/11/11', 100, 1)
        assert b'Employee has been added!' in rv.data


if __name__ == '__main__':
    unittest.main()
