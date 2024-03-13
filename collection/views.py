from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token 
import sms, json, re, datetime, random
from .models import *
from .forms import LoginForm

def main(request):
    all_cats = Categories.objects.values('cat_name')
    template = loader.get_template('index.html')
    if request.session.has_key('username'):
        uname = request.session['username']
        all_areas = Areas.objects.values('location')
        context = {
        'uname':uname,
        'all_cats':all_cats,
        'all_areas':all_areas,
        'us_type':request.session['user_type'],
    }
        template2 = loader.get_template('auth-index.html')
        return HttpResponse(template2.render(context, request))    
    elif request.session.has_key('uname-err'):
        context = {
            'all_cats':all_cats,
            'uname':request.session['uname-err'],
            'upass':request.session['upass-err'],
            'msg':request.session['msg']
        }
        del request.session['uname-err']
        del request.session['upass-err']
        del request.session['msg']
    else:
        context = {'all_cats':all_cats}

    return HttpResponse(template.render(context, request))


def getCategoryData(request):
    req_data = json.loads(request.body.decode("utf-8"))
    qcat_name = req_data['querycat_name'] #Get data from POST request
        #Do something with the data from the POST request
        #If sending data back to the view, create the data dictionary
    cat_details = Categories.objects.get(cat_name = qcat_name)
    catid = cat_details.cat_id
    catdesc = cat_details.cat_desc
    return JsonResponse({'catid':catid, 'catdesc':catdesc})

'''def qsToArray(query_set, col):
    #val = []
    for row in query_set:
        val = row[col]
    return val'''

def qsToList(query_set, col):
    val = []
    for row in query_set:
        val.append(row[col])
    return val

def getNumOfSubscribers(request):
    req_data = json.loads(request.body.decode("utf-8"))
    cat = req_data['cat_name']
    zip = req_data['zip_code']
    all_areas = Areas.objects.all()
    SubCount = "0"
    try:
        for area in all_areas:
            curr_zipcodes = area.zip_codes
            curr_zipcodes = curr_zipcodes.replace(" ","")
            zipcodes = re.split(',', curr_zipcodes)
            for zipcode in zipcodes:
                if zip == zipcode:
                    areaID = area.area_id
        if areaID is not None:        
            if ServiceLists.objects.filter(category = cat, area = areaID).exists():
                listID = ServiceLists.objects.get(category = cat, area = areaID)
                list_ID = listID.list_id
                SubCount =  Subscriptions.objects.filter(service_list = list_ID).count()
    except(TypeError, ValueError, OverflowError, NameError):
        listID = None
        areaID = None
    return JsonResponse({'subs':SubCount}) 


def signInMain(request):
    usrname = request.POST.get('u_id')
    passwd = request.POST.get('u_pass')

    if Users.objects.filter(user_id = usrname, password = passwd).exists():
        user = Users.objects.get(user_id = usrname, password = passwd)
        if user.is_active:
            request.session['username'] = usrname
            request.session['user_type'] = user.type_of_user
        else:
            return redirect("/collection/activate-act/")
    else:
        request.session['uname-err'] = usrname
        request.session['upass-err'] = passwd
        request.session['msg'] = 'Username and/or password is incorrect'

    return redirect("/")


def signInLogin(request):
    usrname = request.POST.get('u-id')
    passwd = request.POST.get('u-pass')

    if Users.objects.filter(user_id = usrname, password = passwd).exists():
        user = Users.objects.get(user_id = usrname, password = passwd)
        if user.is_active:
            request.session['username'] = usrname
            request.session['user_type'] = user.type_of_user
            return redirect("/collection/dashboard/")
        else:
            return redirect("/collection/activate-act/")
    else:
        request.session['uname-err'] = usrname
        request.session['upass-err'] = passwd
        request.session['msg'] = 'Username and/or password is incorrect'
    
    return redirect("/collection/userlogin/")

def signinGuestLogin(request):
    gemail = request.POST.get('g_id')
    gid = gemail.split('@')
    gpasswd = request.POST.get('g_pass')

    if Guests.objects.filter(guest_email = gemail, guest_password = gpasswd).exists():
        guest = Guests.objects.get(guest_email = gemail, guest_password = gpasswd)
        request.session['username'] = gid[0]
        request.session['user_type'] = 'guest'
        request.session['guest_id'] = guest.id

    return redirect("/")



def register(request):
    user_type = request.POST.get('user_type')
    n_mode = ("N/A", request.POST.get('n_mode')) [user_type == "subscriber"]
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    us_email = request.POST.get('us_email')
    us_phone = "+" + request.POST.get('us_phone')
    us_id = request.POST.get('us_id')
    us_pass = request.POST.get('us_pass')
    us_pass_2 = request.POST.get('us_pass_2')
    valid_userdata = True

    if us_pass != us_pass_2:
        valid_userdata = False
        request.session['err'] = 'Entered passwords do not match'
    elif Users.objects.filter(user_id = us_id).exists():
        valid_userdata = False
        request.session['err'] = 'This username is already taken. Please try a slight variant'

    if valid_userdata:
        user_rec = Users(us_id, user_type, fname, lname, us_email, us_phone, n_mode, us_pass, 0)
        user_rec.save()
        current_site = get_current_site(request)  
        mail_subject = 'ServiceGarage - Your account activation link'  
        message = render_to_string(
                'acc_active_email.html',
                {
                    'user': us_id,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(us_id)),
                    'token': account_activation_token.make_token(user_rec),
                }
            )
        stat = sendEmailNotifications([us_email], mail_subject, message)  
        return redirect("/collection/activate-act/")

    request.session['u_type'] = user_type
    request.session['nt_mode'] = n_mode
    request.session['f_name'] = fname
    request.session['l_name'] = lname
    request.session['u_email'] = us_email
    request.session['u_phone'] = us_phone
    request.session['u_id'] = us_id
    request.session['u_pass'] = us_pass
    request.session['u_pass_2'] = us_pass_2
    return redirect("/collection/signup/")

def registerGuest(request):
    req_data = json.loads(request.body.decode("utf-8"))
    g_email = req_data['gs_email']
    g_id = g_email.split('@')
    g_password = random.randint(100000, 100000000)
    guest_rec = Guests(guest_email=g_email, guest_password=g_password)
    guest_rec.save()
    subj = "ServiceGarage - Your One-time password"
    message = "Hello " + g_id[0] + ",\nHere is your one-time password for signing in to ServiceGarage:\n" + str(g_password)
    stat = sendEmailNotifications([g_email],subj,message)
    return JsonResponse({'result':g_email})

def currSite(request):
    curr_site = get_current_site(request)
    return JsonResponse({'curr_site':str(curr_site.domain)})

def activate(request, uidb64, token):  
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(user_id=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("/collection/activated/")    
    else:
        return HttpResponse('Activation link is invalid!')

def signOut(request):
    if request.session.has_key('guest_id'):
        g_id = request.session['guest_id']
        guest = Guests.objects.get(id=g_id)
        guest.delete()
        del request.session['guest_id']
    del request.session['username']
    del request.session['user_type']
    return redirect("/")

def userlogin(request):
    template = loader.get_template('login.html')
    if request.session.has_key('uname-err'):
        context = {
            'uname':request.session['uname-err'],
            'upass':request.session['upass-err'],
            'msg':request.session['msg']
        }
        del request.session['uname-err']
        del request.session['upass-err']
        del request.session['msg']
    else:
        context = {
        'auth':'yes',
        }
    return HttpResponse(template.render(context,request))

def signup(request):
    template = loader.get_template('user-register.html')
    if request.session.has_key('err'):
        context = {
        'u_type':request.session['u_type'],
        'nt_mode':request.session['nt_mode'],
        'f_name':request.session['f_name'],
        'l_name':request.session['l_name'],
        'u_email':request.session['u_email'],
        'u_phone':request.session['u_phone'],
        'u_id':request.session['u_id'],
        'u_pass':request.session['u_pass'],
        'u_pass_2':request.session['u_pass_2'],
        'err':request.session['err']
        }
        del request.session['u_type']
        del request.session['nt_mode']
        del request.session['f_name']
        del request.session['l_name']
        del request.session['u_email']
        del request.session['u_phone']
        del request.session['u_id']
        del request.session['u_pass']
        del request.session['u_pass_2']
        del request.session['err']
    else:
        context = {
        'auth':'yes',
        }
    return HttpResponse(template.render(context,request))

def copyright(request):
    template = loader.get_template('copyright.html')
    return HttpResponse(template.render())

def privacy(request):
    template = loader.get_template('privacy.html')
    return HttpResponse(template.render())

def service(request):
    template = loader.get_template('TOS.html')
    return HttpResponse(template.render())

def actActivate(request):
    template = loader.get_template('confirm.html')
    return HttpResponse(template.render())

def activatedPage(request):
    template = loader.get_template('active.html')
    return HttpResponse(template.render())

def dashboard(request):
    template = loader.get_template('dashboard.html')

    if not request.session.has_key('username') or request.session['user_type'] == "guest":
        return redirect("/")
    elif request.session['user_type'] == "subscriber":
        userobj = Users.objects.get(user_id=request.session['username'])
        context = {
            'userobj':userobj
        }
    else:
        qrd_for_user = ""
        uname = request.session['username']
        userobj = Users.objects.get(user_id=uname)
        all_cats = Categories.objects.values('cat_name')
        all_areas = Areas.objects.values('location')
        if QRD.objects.filter(user=uname).exists():
            qrd_for_user = QRD.objects.filter(user=uname).values()    
        context = {
            'userobj':userobj,
            'all_cats':all_cats,
            'all_areas':all_areas,
            'qrds':qrd_for_user,
        }

    return HttpResponse(template.render(context,request))

def getListOfSubscribers(CatId, AreaId):
    q_list = ""
    subscribers = []
    subs = []
    if ServiceLists.objects.filter(category=CatId, area=AreaId).exists():
        list_num = ServiceLists.objects.get(category=CatId, area=AreaId)
        q_list = list_num.list_id
        if Subscriptions.objects.filter(service_list=q_list).exists():
            subscribers = Subscriptions.objects.filter(service_list=q_list).values_list('user',flat=True)
    return list(subscribers)

def getQrdHistory(request):
    req_data = json.loads(request.body.decode("utf-8"))
    user_name = req_data['usrname']
    qrd_ids = []
    if QRD.objects.filter(user=user_name).exists():
        qrd_for_user = QRD.objects.filter(user=user_name).values()    
        for x in qrd_for_user:
            qrd_ids.append(x['qrd_id'])
    return JsonResponse({'qrd_list':qrd_ids})
        

def getEmailsAndPhones(UserIds):
    emails = []
    phone_nos = []
    for x in UserIds:
        user_data = Users.objects.get(user_id=x)
        if user_data.notify_mode == "email":
           userdata = user_data.email
           emails.append(userdata)
        else:
            userdata = user_data.phone
            phone_nos.append(userdata)
    return [emails, phone_nos]

def sendEmailNotifications(Emails, subj, body):
    send_mail(
    	subject = subj,
    	message = body,
    	from_email=settings.EMAIL_HOST_USER,
    	recipient_list = Emails,
        fail_silently=True)
    return "success"

def sendSMSNotifications(PhoneNos, text):
    with sms.get_connection() as connection:
        sms.Message(
        text, '+18154019148', PhoneNos,
        connection=connection
        ).send(fail_silently=True)
    return "success"


def postQRD(request):
    req_data = json.loads(request.body.decode("utf-8"))
    
    category_name = req_data['q_cat']
    category_id = Categories.objects.get(cat_name = category_name)
    q_cat = category_id.cat_id
    area_name = req_data['q_area']
    area_num = Areas.objects.get(location = area_name)
    q_area = area_num.area_id
    
    q_id = nextQrdId() 
    q_user = req_data['q_user']
    q_budget = req_data['q_budget']
    q_timeline = req_data['q_timeline']
    q_desc = req_data['q_desc']
    q_subj = q_desc[0:60]
    qrdrec = QRD(q_id,q_user,q_cat,q_area,q_budget,q_timeline,q_desc,q_subj)
    qrdrec.save()

    if len(q_desc) > 120:
        q_body = q_desc[:120]
    else:
        q_body =q_desc

    subj = "You have a new quote request from " + q_user
    Notification_text = "Dear subscriber,\nYou have a new quote request from " + q_user + " \
\nProject Location: " + area_name + ", Project Category: " + category_name + ", \
Budget: " + q_budget + "$, Timeline: " + q_timeline + " days\nDescription:\n" + q_body + "\nLog in \
to your ServiceGarage account to view details:\nhttp://localhost:8000/collection/userlogin/"

    subs = getListOfSubscribers(q_cat, q_area)
    
    if subs:
        emails_phones = getEmailsAndPhones(subs)
        stat1 = sendEmailNotifications(emails_phones[0],subj,Notification_text)
        stat2 = sendSMSNotifications(emails_phones[1], Notification_text)
    return JsonResponse({'qrdId':q_id})   

def qrDetails(request, qrdId):
    template = loader.get_template('qr-details.html')
    qrdobj = QRD.objects.get(qrd_id=qrdId)
    context = {
        'qrdobj':qrdobj,
    }
    return HttpResponse(template.render(context,request))


def nextQrdId():
    last_qrd = QRD.objects.all().order_by('qrd_id').last()
    if not last_qrd:
        return 'qrd' + str(datetime.date.today().year) + str(datetime.date.today().month).zfill(2) + str(datetime.date.today().day).zfill(2) + '0000'
    qrdid = last_qrd.qrd_id
    qrd_num = int(qrdid[11:15])
    qrd_num = qrd_num + 1
    new_qrdid = 'qrd' + str(str(datetime.date.today().year)) + str(datetime.date.today().month).zfill(2) + str(datetime.date.today().day).zfill(2) + str(qrd_num).zfill(4)
    return new_qrdid

def testpage(request):
    template = loader.get_template('test.html')
    return HttpResponse(template.render())

def getSingleVal(request):
    user = Users.objects.get(user_id='ahmadd42')
    user_email = user.email
    return JsonResponse({'email':user_email})