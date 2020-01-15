from django.db import models
from django.contrib.auth.models import(BaseUserManager, AbstractBaseUser, PermissionsMixin)
class MyUserManager(BaseUserManager):
    def create_user(self, email, user_type, department,username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            user_type=user_type,
            department=department,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, user_type, username, password=None):
        user = self.create_user(
            email,
            user_type=user_type,
            department=None,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES_CHOICES = (
        (1, 'SuperAdmin'),
        (2, 'Admin'),
        (3, 'Employee'),
    )
    DEPARTMENTS = (
        (1, 'Human Resource'),
        (2, 'Inventory' ),
        (3, 'Finance'),
        (4, 'Marketing'),
        (5, 'Information Technology'),
    )
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=200)
    employee_id = models.IntegerField(blank=True, null=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES_CHOICES)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    department = models.PositiveSmallIntegerField(choices=DEPARTMENTS, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_type']
    objects = MyUserManager()
    def __str__(self):
        return self.username
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin
    def save_image(self):
        self.save()
    def delete_image(self):
        self.delete()
class Profile(models.Model):
    image = models.ImageField(upload_to='photos/')
    first_name =  models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    def save_profile(self):
        self.save()
    def __str__(self):
        return self.first_name
class Updates(models.Model):
    title =  models.CharField(max_length=50)
    update = models.TextField()
    time_stamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class Comments(models.Model):
    comment = models.CharField(max_length=100,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    update = models.ForeignKey(Updates,on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    @classmethod
    def get_comments(cls,id):
        comments = cls.objects.filter(update__id=id)
        return comments
    def save_comment(self):
        self.save()
    def __str__(self):
      return self.comment







