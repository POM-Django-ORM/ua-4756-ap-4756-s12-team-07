from django.db import IntegrityError, models


class CustomUser(models.Model):
    first_name = models.CharField(max_length=20, blank=True)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"'id': {self.id}, "
            f"'first_name': '{self.first_name}', "
            f"'middle_name': '{self.middle_name}', "
            f"'last_name': '{self.last_name}', "
            f"'email': '{self.email}', "
            f"'created_at': {int(self.created_at.timestamp())}, "
            f"'updated_at': {int(self.updated_at.timestamp())}, "
            f"'role': {self.role}, "
            f"'is_active': {self.is_active}"
        )

    def __repr__(self):
        return f"CustomUser(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return True
        except CustomUser.DoesNotExist:
            return False

    @staticmethod
    def create(
        email,
        password,
        first_name,
        middle_name,
        last_name,
    ):
        try:
            if (
                len(first_name) > 20
                or len(middle_name) > 20
                or len(last_name) > 20
                or "@" not in email
            ):
                return None

            if CustomUser.objects.filter(email=email).exists():
                return None

            user = CustomUser(
                email=email,
                password=password,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
            )
            user.save()
            return user

        except (TypeError, ValueError, IntegrityError):
            return None

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": int(self.created_at.timestamp()),
            "updated_at": int(self.updated_at.timestamp()),
            "role": self.role,
            "is_active": self.is_active,
        }

    def update(
        self,
        first_name=None,
        middle_name=None,
        last_name=None,
        password=None,
        role=None,
        is_active=None,
    ):
        if first_name is not None:
            self.first_name = first_name

        if middle_name is not None:
            self.middle_name = middle_name

        if last_name is not None:
            self.last_name = last_name

        if password is not None:
            self.password = password

        if role is not None:
            self.role = role

        if is_active is not None:
            self.is_active = is_active

        self.save()

    @staticmethod
    def get_all():
        return CustomUser.objects.all()

    def get_role_name(self):
        roles = {
            0: "visitor",
            1: "admin",
        }
        return roles.get(self.role)