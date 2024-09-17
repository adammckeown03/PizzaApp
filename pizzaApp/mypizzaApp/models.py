from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        # create and save a user with the given email and password.
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # create a regular user (not staff or superuser)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
    # create a superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField('Email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Crust(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Sauce(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Cheese(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Topping(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    crust = models.ForeignKey('Crust', on_delete=models.CASCADE)
    sauce = models.ForeignKey('Sauce', on_delete=models.CASCADE)
    cheese = models.ForeignKey('Cheese', on_delete=models.CASCADE)
    toppings = models.ManyToManyField('Topping')

    def __str__(self):
        return f"{self.size} Pizza with {self.crust}, {self.sauce}, {self.cheese}, and toppings: {', '.join(str(t) for t in self.toppings.all())}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=2)
    cvv = models.CharField(max_length=3)
    order_datetime = models.DateTimeField(auto_now_add=True)

    def order_time(self):
        return self.order_datetime.strftime("%H:%M")

    def __str__(self):
        return f"Order for {self.name} - {self.address} ({self.order_datetime.strftime('%Y-%m-%d %H:%M')})"