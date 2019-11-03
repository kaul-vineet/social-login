from django.shortcuts import render
from django.http import HttpResponse
from simple_salesforce import Salesforce
import simplejson as json

from .models import Greeting

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

@csrf_protect
def create_post(request):
    if request.method == 'POST':
        fname = request.POST.get('FirstName')
        lname = request.POST.get('LastName')
        email = request.POST.get('EmailID')
        socialid = request.POST.get('SocialID')
        response_data = {}

        sf = Salesforce(username='viyer@sp17.demo', password='IndianSummer', organizationId='00D460000001FBb')

        result = sf.query("SELECT Id FROM Contact WHERE Email = '" + email + "'")

        if result.get('totalSize') == 0:
            result = sf.Contact.create({'FirstName' : fname, 'Email' : email, 'LastName' : lname})
            if result.get('success') == 1:
                result = sf.SocialPersona.create({'Name' : socialid,'ParentId' : str(result.get('id')),'Provider' : 'Facebook'})
                print(json.dumps(result))

        return HttpResponse(
            json.dumps(result),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
