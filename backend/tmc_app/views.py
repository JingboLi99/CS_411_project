from pickle import TRUE
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from urllib3 import HTTPResponse
#--Models--
from .models import Skills
from .models import Cuisines
from .models import Recipes
from .models import Users
#--Forms--
from .forms import UserForm

# Create your views here.
def login_view(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = UserForm()
    context = {
        'form': form,
        'isError':False,
        'noUser': False
    }
    return render(request, 'login.html', context)
def login_auth_view(request):
    currUserName = request.GET['user']
    currUserPsw = request.GET['psw']
    
    if len(Users.objects.filter(username__exact = currUserName)) != 0 and len(Users.objects.filter(psw = currUserPsw)) != 0:
        #put current user into sessions:
        request.session['curr_user'] = currUserName
        return profile_view(request)
    else:
        form = UserForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = UserForm()
        context = {
            'form': form,
            'isError':True,
            'noUser': False
        }
        return render(request, 'login.html', context)
    
def categories_view(request):
    skills = Skills.objects.all()
    cuisines = Cuisines.objects.all()
    
    skill_tags = []
    skill_descs = []
    for s in skills:
        skill_tags.append(s.tag)
        skill_descs.append(s.dscrp)
        
    c_tags = []
    c_descs = []
    
    for c in cuisines:
        c_tags.append(c.name)
        c_descs.append(c.dscrp)
    
    context = {
        's_tags': skill_tags,
        'c_tags': c_tags,
        'skills': zip(skill_tags, skill_descs),
        'cuisines': zip(c_tags, c_descs)
    }
    return render(request, 'categories.html', context)

def recs_view(request):
    
    uSkill = request.GET['sk_tag']
    uCuisine = request.GET['c_tag'] #string is broken up by get
    print(uCuisine)
    uDf = request.GET['d_tag']
    uOrder = request.GET['o_tag'] #0 by lowest, 1 by highest
    queryOne = ''
    if uOrder:
        queryOne += "((SELECT name, image, views FROM Recipes R Natural Join Recipe_has_skills RS WHERE skill = '" + uSkill + "' AND difficulty = " + uDf + ") UNION " + "(SELECT name, image, views FROM Recipes R Natural Join Recipe_has_skills RS WHERE cuisine = '" + uCuisine + "' AND difficulty = " + uDf + ")) ORDER BY views DESC"
    else:
        queryOne += "((SELECT name, image, views FROM Recipes R Natural Join Recipe_has_skills RS WHERE skill = '" + uSkill + "' AND difficulty = " + uDf + ") UNION " + "(SELECT name, image, views FROM Recipes R Natural Join Recipe_has_skills RS WHERE cuisine = '" + uCuisine + "' AND difficulty = " + uDf + ")) ORDER BY views"
    
    # print(query)
    cursor = connection.cursor()
    cursor.execute(queryOne)
    row = cursor.fetchall()
    for i in row:
        i = list(i)
    row = list(row)
    rec_list = []
    if 'curr_user' in request.session:
        currUser = request.session['curr_user']
        sp_query = "CALL Result('"+currUser+"')"
        cursor.execute(sp_query)
        sp_row = cursor.fetchall()
        for item in sp_row:
            rec_list.append([item[0], item[4]])
            
    context = {
        'items': row,
        'rec': rec_list
    }
    return render(request, 'reccomendations.html', context)

def profile_view(request):
    if 'curr_user' in request.session:
        currUser = request.session['curr_user']
        todo_list = []
        comp_list = []
        rec_list = []
        empty_todo = True
        empty_comp = True
        cursor = connection.cursor()
        # query = "SELECT R.name, Y.id, T.url, UR.is_todo FROM Recipes as R INNER JOIN User_recipes UR ON UR.recipe = R.name LEFT OUTER JOIN Yt_recipes Y ON Y.id = R.yt_id LEFT OUTER JOIN Text_Recipes T ON T.id = R.text_id WHERE UR.user = '"+ currUser+"'"
        query = "SELECT R.name, R.image, UR.is_todo FROM Recipes R inner join User_recipes UR ON R.name = UR.recipe WHERE UR.user = '"+ currUser+"'"
        cursor.execute(query)
        row = cursor.fetchall()
        for item in row:
            if item[2]:
                todo_list.append([item[0], item[1]])
                empty_todo = False
            else:
                comp_list.append([item[0], item[1]])
                empty_comp = False
        sp_query = "CALL Result('"+currUser+"')"
        cursor.execute(sp_query)
        sp_row = cursor.fetchall()
        for item in sp_row:
            print('name: ', item[0], 'image: ', item[4])
            rec_list.append([item[0], item[4]])
        context = {
            'noAcc' : False,
            'user': currUser,
            'todo': todo_list,
            'completed': comp_list,
            'empty_todo': empty_todo,
            'empty_comp': empty_comp,
            'rec': rec_list
        }
    else:
        currUser = 'User'
        context = {
            'noAcc': True,
            'user': currUser,
            'todo': None,
            'completed': None,
            'empty_todo': empty_todo,
            'empty_comp': empty_comp
        }
    return render(request, 'profile.html', context)

def search_result_view(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        queries = search.split(' ')
        results = Recipes.objects
        for query in queries:
            query.strip()
            results = results.filter(name__icontains = query)
        res_names = results.values_list('name', flat = True).order_by('name')
        res_imgs = results.values_list('image', flat = True).order_by('name')
        # print(res_names)
        context = {
            'query': search,
            'results': zip(res_names, res_imgs)
        }
        return render(request, 'searchresult.html', context)
    

def choose_category_view(request):
    skill_kw = request.GET.get('skill_kw', None)
    cuisine_kw = request.GET.get('cuisine_kw', None)
    ##Note: why are the exact same strings not equating????
    if cuisine_kw is not None:
        results = Recipes.objects.filter(cuisine__exact = cuisine_kw)
        print(len(results))
        res_names = results.values_list('name', flat = True).order_by('name')
        res_imgs = results.values_list('image', flat = True).order_by('name')
        # print(res_names)
        context = {
            'query': cuisine_kw,
            'results': zip(res_names, res_imgs)
        }
        return render(request, 'searchresult.html', context)
    elif skill_kw is not None:
        query = ''
        query += ("select name, image from Recipes natural join Recipe_has_skills where skill = '" +skill_kw+"'")
        print(query)
        cursor = connection.cursor()
        cursor.execute(query)
        row = cursor.fetchall() 
        
        name = []
        img = []
        for r in row:
            name.append(r[0])
            img.append(r[1])
        context = {
            'query': skill_kw,
            'results': zip(name, img)
        }
        return render(request, 'searchresult.html', context)
    else:
        return categories_view(request)
def update_del_user_view(request):
    context = {
        'hasUpdated': False,
        'hasDeleted': False,
        'isError': False
    }
    return render(request, 'updateuser.html', context)

def update_user_auth_view(request):
    currUserName = request.GET['user']
    currUserPsw = request.GET['oldpsw']
    newUserPsw = request.GET['newpsw']
    toDelete = request.GET.get('toDel', False)
    if len(Users.objects.filter(username__exact = currUserName)) != 0 and len(Users.objects.filter(psw = currUserPsw)) != 0: #this is wrong way to authenticate a user
        if toDelete:
            # query = "Create Trigger newpsw Before Insert on Users For Each Row BEGIN Set @username = NEW.username Set @level = NEW.skill_level Set New.username = upper(username) If level >5 then Set New.skill_level = 5 End if If level <0 then Set New.skill_levle = 0 End if End;"
            # cursor= connection.cursor()
            # cursor.execute(query)
            Users.objects.filter(username__exact = currUserName).delete()
            context = {
                'hasUpdated': False,
                'hasDeleted': True,
                'isError': False,
            }
        else:    
            Users.objects.filter(username__exact = currUserName).update(psw = newUserPsw)
            context = {
                'hasUpdated': True,
                'hasDeleted': False,
                'isError': False,
            }
        
    else:
        context = {
            'isError':True,
            'hasUpdated': False,
            'hasDeleted': False,
            
        }
    return render(request, 'updateuser.html', context)

def recipe_view(request):
    if 'curr_recipe' in request.session:
        curr_rcp_name = request.session['curr_recipe']
        del request.session['curr_recipe']
    else:
        curr_rcp_name = request.GET.get('curr_rcp')
    print(">>>>>>", curr_rcp_name)
    cursor = connection.cursor()
    query = "SELECT R.name, Y.url,Y.id, T.url FROM Yt_recipes Y RIGHT OUTER JOIN Recipes R ON Y.id = R.yt_id LEFT OUTER JOIN Text_Recipes T ON T.id = R.text_id WHERE R.name = '"+curr_rcp_name+"' ORDER BY R.name"
    cursor.execute(query)
    row = cursor.fetchall()
    if len(row) != 1:
        return HTTPResponse("<h1>Did not return exactly one result</h1>")
    
    #check if recipe is saved, completed, or neither:
    is_saved = False
    is_completed = False
    rcp_name = row[0][0]
    if 'curr_user' in request.session:
        user = request.session['curr_user']
        query2 = "SELECT is_todo FROM User_recipes WHERE user = '"+ user +"' AND recipe = '"+ rcp_name +"'"
        cursor.execute(query2)
        rcpRow = cursor.fetchall()
        if len(rcpRow) != 0 and rcpRow[0][0] == 1: #if recipe is saved
            is_saved = True
        elif len(rcpRow) != 0 and rcpRow[0][0] == 0:
            is_completed = True
    print(is_saved," , ", is_completed)
    context = {
        'rcp_name': rcp_name,
        'yt_url': row[0][1],
        'yt_id': row[0][2],
        'txt_url': row[0][3],
        'is_saved': is_saved,
        'is_completed': is_completed
    }
    return render(request, 'recipe.html', context)

def save_recipes_view(request):
    
    if 'curr_user' in request.session:
        is_saved = request.GET["is_saved"]
        is_comp = request.GET["is_comp"]
        add_todo = request.GET.get("add_todo_rcp", None)
        add_comp = request.GET.get("add_comp_rcp", None)
        print("Results are: ", is_saved, is_comp, "Name: >>>>" , add_todo, add_comp)
        # if add_comp != "Beef Brisket Hot Pot hahahahahah":
        #     return HttpResponse("Something went wrong")
        currUser = request.session['curr_user']
        if add_todo is not None: #clicked the save button
            if is_saved == '1': #if it is already saved, make it not saved
                cursor = connection.cursor()
                query = "DELETE FROM User_recipes WHERE user ='"+ currUser +"' AND recipe = '"+add_todo+"'"
                cursor.execute(query)
            else: #if it is not saved, make it saved
                if is_comp == '1': # if currently comp, make it not comp
                    cursor = connection.cursor()
                    query = "UPDATE User_recipes SET is_todo = 1 WHERE user ='"+ currUser +"' AND recipe = '"+add_todo+"'"
                    cursor.execute(query)
                else:#if it is neither comp nor saved, add it to User_recipes
                    cursor = connection.cursor()
                    query = "INSERT INTO User_recipes VALUES ('"+currUser+"', '"+add_todo+"', 1)"
                    cursor.execute(query)
            request.session['curr_recipe'] = add_todo
        elif add_comp is not None:#clicked the completed button
            if is_comp == '1': #if it is already completed, make it not completed
                cursor = connection.cursor()
                query = "DELETE FROM User_recipes WHERE user ='"+ currUser +"' AND recipe = '"+add_comp+"'"
                cursor.execute(query)
            else: #if it is not completed, make it completed
                if is_saved == '1': # if currently saved, make it not saved
                    cursor = connection.cursor()
                    query = "UPDATE User_recipes SET is_todo = 0 WHERE user ='"+ currUser +"' AND recipe = '"+add_comp+"'"
                    cursor.execute(query)
                else:#if it is neither comp nor saved, add it to User_recipes
                    cursor = connection.cursor()
                    query = "INSERT INTO User_recipes VALUES ('"+currUser+"', '"+add_comp+"', 0)"
                    cursor.execute(query)
            request.session['curr_recipe'] = add_comp
        else:
            return HTTPResponse("Something went terribly wrong")
        return recipe_view(request)
    else:
        form = UserForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = UserForm()
        context = {
            'form': form,
            'isError': False,
            'noUser': True
        }
        return render(request, 'login.html', context)
