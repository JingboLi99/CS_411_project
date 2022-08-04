# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CheckConstraint, Q


class Cuisines(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    dscrp = models.CharField(max_length=700, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuisines'


class RecipeHasSkills(models.Model):
    name = models.OneToOneField('Recipes', models.DO_NOTHING, db_column='name', primary_key=True)
    skill = models.ForeignKey('Skills', models.DO_NOTHING, db_column='skill')

    class Meta:
        managed = False
        db_table = 'recipe_has_skills'
        unique_together = (('name', 'skill'),)


class Recipes(models.Model):
    name = models.CharField(primary_key=True, max_length=67)
    yt = models.ForeignKey('YtRecipes', models.DO_NOTHING, blank=True, null=True)
    text = models.ForeignKey('TextRecipes', models.DO_NOTHING, blank=True, null=True)
    cuisine = models.CharField(max_length=16, blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    isvalid = models.IntegerField(db_column='isValid', blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipes'


class Skills(models.Model):
    tag = models.CharField(primary_key=True, max_length=14)
    dscrp = models.CharField(max_length=209, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'skills'


class TextRecipes(models.Model):
    url = models.CharField(max_length=300, blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'text_recipes'


class YtRecipes(models.Model):
    id = models.CharField(primary_key=True, max_length=11)
    name = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=44, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'yt_recipes'

class Users(models.Model):
    username = models.CharField(primary_key = True, max_length =50)
    psw = models.CharField(max_length = 50, null = False)
    email = models.CharField(max_length=200)
    skill_lvl = models.FloatField(null = True, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],)
    
    class Meta:
        managed = False
        db_table = 'Users'
        constraints = (
            # for checking in the DB
            CheckConstraint(
                check=Q(myfloat__gte=0.0) & Q(myfloat__lte=5.0),
                name='Users_skill_constraint'),
            )
class User_recipes(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, db_column='username', primary_key = True)
    recipe = models.ForeignKey('Recipes', models.DO_NOTHING, db_column='name')
    is_todo = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'User_Recipes'
        unique_together = (('user', 'recipe'),)


# from django.db import models


# class Cuisines(models.Model):
#     name = models.CharField(primary_key=True, max_length=30)
#     dscrp = models.CharField(max_length=700, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'cuisines'


# class RecipeHasSkills(models.Model):
#     name = models.OneToOneField('Recipes', models.DO_NOTHING, db_column='name', primary_key=True)
#     skill = models.ForeignKey('Skills', models.DO_NOTHING, db_column='skill')

#     class Meta:
#         managed = False
#         db_table = 'recipe_has_skills'
#         unique_together = (('name', 'skill'),)


# class Recipes(models.Model):
#     name = models.CharField(primary_key=True, max_length=67)
#     yt = models.ForeignKey('YtRecipes', models.DO_NOTHING, blank=True, null=True)
#     text = models.ForeignKey('TextRecipes', models.DO_NOTHING, blank=True, null=True)
#     cuisine = models.CharField(max_length=16, blank=True, null=True)
#     difficulty = models.IntegerField(blank=True, null=True)
#     views = models.IntegerField(blank=True, null=True)
#     isvalid = models.IntegerField(db_column='isValid', blank=True, null=True)  # Field name made lowercase.
#     image = models.CharField(max_length=200, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'recipes'


# class Skills(models.Model):
#     tag = models.CharField(primary_key=True, max_length=14)
#     dscrp = models.CharField(max_length=209, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'skills'


# class TextRecipes(models.Model):
#     url = models.CharField(max_length=300, blank=True, null=True)
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=225, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'text_recipes'


# class YtRecipes(models.Model):
#     id = models.CharField(primary_key=True, max_length=11)
#     name = models.CharField(max_length=50, blank=True, null=True)
#     url = models.CharField(max_length=44, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'yt_recipes'

# class Users(models.Model):
#     username = models.CharField(primary_key = True, max_length =50)
#     psw = models.CharField(max_length = 50, null = False)
#     email = models.CharField(max_length=200)
    
#     class Meta:
#         managed = False
#         db_table = 'Users'

# class User_recipes(models.Model):
#     user = models.OneToOneField('Users', models.DO_NOTHING, db_column='username', primary_key=True)
#     recipe = models.ForeignKey('Recipes', models.DO_NOTHING, db_column='name')
#     is_todo = models.BooleanField(default=False)

#     class Meta:
#         managed = False
#         db_table = 'User_Recipes'
#         unique_together = (('user', 'recipe'),)

