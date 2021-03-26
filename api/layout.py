from app import ma


class ProfileSchema(ma.Schema):
    """Utility class for serializing profiles data."""

    class Meta:
        """Fields for serializing."""
        fields = ("id", "name", "grades", "group")


profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)


class GradeSchema(ma.Schema):
    """Utility class for serializing grades data."""

    class Meta:
        """Fields for serializing."""
        fields = ("id", "object_id", "user_id", "grade_id", "timestamp")


grade_schema = GradeSchema()
grades_schema = GradeSchema(many=True)


class AdminSchema(ma.Schema):
    """Utility class for serializing admins data."""

    class Meta:
        """Fields for serializing."""
        fields = ("id", "name", "groups")


admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)


class ObjectSchema(ma.Schema):
    """Utility class for serializing objects data."""

    class Meta:
        """Fields for serializing."""
        fields = ("id", "name")


object_schema = ObjectSchema()
objects_schema = ObjectSchema(many=True)
