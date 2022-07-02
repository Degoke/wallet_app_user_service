from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        if not first_name:
            raise ValueError("Users must have a firstname")
        
        if not last_name:
            raise ValueError("Users must have a lastname")

        if not password:
            raise ValueError("Users must have a password")
        
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )

        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email,
            password,
            first_name,
            last_name,
        )
        user.is_staff = True
        user.admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staff(self, email, password, first_name, last_name):
        user = self.create_user(
            email,
            password,
            first_name,
            last_name,
        )
        user.is_staff = True
        user.admin = True
        user.is_superuser = False
        user.save(using=self._db)
        return user