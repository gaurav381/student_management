# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import student_management

from student_managementapp.EmailBackEnd import EmailBackEnd
from django.core.mail import send_mail
from student_management import settings
import requests
import json
import random



def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')



def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                #Send Mail
    
                subject='Re:signup Successfully'
                msg="Hello [Admin],\nThank you. We are delighted to have you with us.\nWe hope you find in our business what you are looking for.\nSomeone from our customer care team will get in touch within 24 hours.\nstudent_management Pvt Ltd \n +91 9876512597 |student@int.com \n\n Respectfully,\n@student_management"
                #msg="Hello User, \nYour account has been created successfully! \nEnjoy our services. \n Thanks & Regards, \nBatchProject - TOPS Technologoies Pvt Ltd \n +91 9998506434 | sanketchauhanios@gmail.com"
                from_email=settings.EMAIL_HOST_USER
                #to_email=['gk.vekariya000@gmail.com']
                to_email=[request.POST['email']]
                send_mail(subject,msg,from_email,to_email)
                return redirect('admin_home')
                
            elif user_type == '2':
                # return HttpResponse("Staff Login")
                 #Send Mail
    
                subject='Re:signup Successfully'
                msg="Hello [Staff],\nThank you. We are delighted to have you with us.\nWe hope you find in our business what you are looking for.\nSomeone from our customer care team will get in touch within 24 hours.\nstudent_management Pvt Ltd \n +91 9876512597 |student@int.com \n\n Respectfully,\n@student_management"
                #msg="Hello User, \nYour account has been created successfully! \nEnjoy our services. \n Thanks & Regards, \nBatchProject - TOPS Technologoies Pvt Ltd \n +91 9998506434 | sanketchauhanios@gmail.com"
                from_email=settings.EMAIL_HOST_USER
                #to_email=['gk.vekariya000@gmail.com']
                to_email=[request.POST['email']]
                send_mail(subject,msg,from_email,to_email)
                return redirect('staff_home')
                
            elif user_type == '3':
                # return HttpResponse("Student Login")
                 #Send Mail
                fnm=request.POST['email']
                print(fnm)
                subject='Re:signup Successfully'
                msg="Hello{{fnm}},\nThank you. We are delighted to have you with us.\nWe hope you find in our business what you are looking for.\nSomeone from our customer care team will get in touch within 24 hours.\nstudent_management Pvt Ltd \n +91 9876512597 |student@int.com \n\n Respectfully,\n@student_management"
                #msg="Hello User, \nYour account has been created successfully! \nEnjoy our services. \n Thanks & Regards, \nBatchProject - TOPS Technologoies Pvt Ltd \n +91 9998506434 | sanketchauhanios@gmail.com"
                from_email=settings.EMAIL_HOST_USER
                #to_email=['gk.vekariya000@gmail.com']
                to_email=[request.POST['email']]
                send_mail(subject,msg,from_email,to_email)

                 # SMS Sending after Login!
                # mention url
                url = "https://www.fast2sms.com/dev/bulk"

                otp=random.randint(1111,9999)
                # create a dictionary
                my_data = {
                    # Your default Sender ID
                    'sender_id': 'FSTSMS', 
                    
                    # Put your message here!
                    'message': f'Hello User, \nYour account has been logged in successfully. \nYour one time password is {otp}', 
                    
                    'language': 'english',
                    'route': 'p',
                    
                    # You can send sms to multiple numbers
                    # separated by comma.
                    #'numbers': '7359333245,8347344100,9409702277,6353630122'    
                    'numbers': '9081540689'   
                }
                
                # create a dictionary
                headers = {
                    'authorization': 'OVA7MfELxlaKrNSbuvIzopCsWQgqc4BPU2Y5dnwH9e6jJ3mRyZuMLpREYsfiGBVrXocFWNthyK1IPxgb',
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Cache-Control': "no-cache"
                }

                # make a post request
                response = requests.request("POST",
                                            url,
                                            data = my_data,
                                            headers = headers)
                #load json data from source
                returned_msg = json.loads(response.text)
                
                # print the send message
                print(returned_msg['message'])

                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


