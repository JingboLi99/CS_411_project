# Generated by Django 4.0.6 on 2022-07-25 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tmc_app', '0004_authgroup_authgrouppermissions_authpermission_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AuthGroup',
        ),
        migrations.DeleteModel(
            name='AuthGroupPermissions',
        ),
        migrations.DeleteModel(
            name='AuthPermission',
        ),
        migrations.DeleteModel(
            name='AuthUser',
        ),
        migrations.DeleteModel(
            name='AuthUserGroups',
        ),
        migrations.DeleteModel(
            name='AuthUserUserPermissions',
        ),
        migrations.DeleteModel(
            name='Cuisines',
        ),
        migrations.DeleteModel(
            name='DjangoAdminLog',
        ),
        migrations.DeleteModel(
            name='DjangoContentType',
        ),
        migrations.DeleteModel(
            name='DjangoMigrations',
        ),
        migrations.DeleteModel(
            name='DjangoSession',
        ),
        migrations.RemoveField(
            model_name='recipehasskills',
            name='name',
        ),
        migrations.RemoveField(
            model_name='recipes',
            name='yt_id',
        ),
        migrations.DeleteModel(
            name='Skills',
        ),
        migrations.DeleteModel(
            name='TextRecipes',
        ),
        migrations.DeleteModel(
            name='TmcAppRecipeHasSkills',
        ),
        migrations.DeleteModel(
            name='TmcAppRecipes',
        ),
        migrations.DeleteModel(
            name='TmcAppSkills',
        ),
        migrations.DeleteModel(
            name='TmcAppYtRecipes',
        ),
        migrations.DeleteModel(
            name='YtRecipes',
        ),
        migrations.DeleteModel(
            name='RecipeHasSkills',
        ),
        migrations.DeleteModel(
            name='Recipes',
        ),
    ]
