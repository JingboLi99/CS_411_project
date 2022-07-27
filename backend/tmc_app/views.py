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
        'isError':False
    }
    return render(request, 'login.html', context)
def login_auth_view(request):
    currUserName = request.GET['user']
    currUserPsw = request.GET['psw']
    
    if len(Users.objects.filter(username__exact = currUserName)) != 0 and len(Users.objects.filter(psw = currUserPsw)) != 0:
        
        context = {
            'user': currUserName,
            'psw': currUserPsw
        }
        return render(request, 'profile.html', context)
    else:
        form = UserForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = UserForm()
        context = {
            'form': form,
            'isError':True
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
    
    query2 = "select name, image from (select cuisine, avg(difficulty) as avgd from recipes group by cuisine) a, recipes b where b.cuisine=a.cuisine and b.difficulty>a.avgd order by views limit 15"
    # print(query)
    cursor = connection.cursor()
    cursor.execute(queryOne)
    row = cursor.fetchall()
    for i in row:
        i = list(i)
    row = list(row)
    cursor.execute(query2)
    row2 = cursor.fetchall()
    for i in row2:
        i = list(i)
    row2 = list(row2)
    context = {
        'items': row,
        'items2': row2
    }
    return render(request, 'reccomendations.html', context)

def profile_view(request):
    user = request.GET['user'] if request.GET['user'] != None else ''
    psw =  request.GET['psw'] if request.GET['psw'] != None else 'psw'
    
    context = {
        'user': user,
        'psw': psw
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
    if cuisine_kw is not None:
        results = Recipes.objects.filter(cuisine__exact = cuisine_kw)
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
    curr_rcp_name = request.GET.get('curr_rcp')
    cursor = connection.cursor()
    query = "SELECT R.name, Y.url,Y.id, T.url FROM Yt_recipes Y RIGHT OUTER JOIN Recipes R ON Y.id = R.yt_id LEFT OUTER JOIN Text_Recipes T ON T.id = R.text_id WHERE R.name = '"+curr_rcp_name+"' ORDER BY R.name"
    cursor.execute(query)
    row = cursor.fetchall()
    if len(row) != 1:
        HTTPResponse("<h1>Did not return exactly one result</h1>")
    context = {
        'rcp_name': row[0][0],
        'yt_url': row[0][1],
        'yt_id': row[0][2],
        'txt_url': row[0][3],
        
    }
    return render(request, 'recipe.html', context)