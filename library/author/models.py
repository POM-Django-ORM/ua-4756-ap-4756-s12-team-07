from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)

    def __str__(self):
        return (
            f"'id': {self.id}, "
            f"'name': '{self.name}', "
            f"'surname': '{self.surname}', "
            f"'patronymic': '{self.patronymic}'"
        )

    def __repr__(self):
        return f"Author(id={self.id})"

    @staticmethod
    def get_by_id(author_id):
        try:
            return Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(author_id):
        try:
            author = Author.objects.get(id=author_id)
            author.delete()
            return True
        except Author.DoesNotExist:
            return False

    @staticmethod
    def create(name, surname, patronymic):
        try:
            if (
                len(name) > 20
                or len(surname) > 20
                or len(patronymic) > 20
            ):
                return None

            author = Author(
                name=name,
                surname=surname,
                patronymic=patronymic,
            )
            author.save()
            return author

        except (TypeError, ValueError):
            return None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "patronymic": self.patronymic,
        }

    def update(
        self,
        name=None,
        surname=None,
        patronymic=None,
    ):
        if name is not None:
            if len(name) > 20:
                return None
            self.name = name

        if surname is not None:
            if len(surname) > 20:
                return None
            self.surname = surname

        if patronymic is not None:
            if len(patronymic) > 20:
                return None
            self.patronymic = patronymic

        self.save()

    @staticmethod
    def get_all():
        return Author.objects.all()