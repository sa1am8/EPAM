from app import ma


class EmployeeSchema(ma.Schema):
    """Utility class for serializing employees data."""

    class Meta:
        """Fields for serializing."""
        fields = ("id", "name", "date_of_birth", "salary", "department_id")


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


class DepartmentSchema(ma.Schema):
    """Utility class for serializing departments data."""

    class Meta:
        """Fields for serializing."""
        fields = ("id", "name")


department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)


class ProfileSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "role", "grades")


profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)


class GradeSchema(ma.Schema):
    class Meta:
        fields = ("id", "object_id", "user_id", "grade_id", "timestamp")


grade_schema = GradeSchema()
grades_schema = GradeSchema(many=True)

class ObjectSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
