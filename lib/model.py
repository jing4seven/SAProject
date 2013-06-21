from django.db.models.fields import PositiveIntegerField, BigIntegerField

class PositiveBigIntegerField(PositiveIntegerField):
    """Represents MySQL's unsigned BIGINT data type (works with MySQL only!)"""
    empty_strings_allowed = False

    def get_internal_type(self):
        return "PositiveBigIntegerField"

    def db_type(self):
        # This is how MySQL defines 64 bit unsigned integer data types
        return "bigint UNSIGNED"


class PositiveBigIntegerAutoField(BigIntegerField):
    """Represents MySQL's unsigned BIGINT AUTO data type (works with MySQL only!)"""
    empty_strings_allowed = False

    def get_internal_type(self):
        return "PositiveBigIntegerAutoField"

    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return 'bigint UNSIGNED AUTO_INCREMENT'
        return super(BigAutoField, self).db_type(connection)