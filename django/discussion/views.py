from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.shortcuts import redirect
from django.urls import reverse

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from . import consumers

from googleapiclient import discovery
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2

from home.authhelper import loginFLOW
from datetime import datetime

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "iitg-speech-lab",
    "private_key_id": "2f757184a13945f894a474a1f7f0ed15547d0781",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCnGJ6a0ncoPF0w\nilyrOHSMNuRM7XK620f3/euPvayvIxC/Yad9CHUbieQiwnIJTknJv5T5aXZ2Brq8\nxr0tkxkjNnhzn8VYS2QjrWkgVHP80WNs/S4kpZp7E4G+kgzCVxi5Mu0Qd1onyiL9\nvY4X5I9PrP06foAl18FPDRSxKi7mBJf4enQcp6fvSASDbAKMoOlU4u1NVMbi50Nx\nUqJC0Hq1TogyKgFgDbSOSEdFjRHk53+G5Ved4QlTIEJCws6NHcLaek6YPyz80vp3\nB61+u4IvDsGEcITbkq1ayKwhCNlTG4A5ksxETOKAOC55njRjrVtjinxXXjqkrioG\n+CxIatGrAgMBAAECggEAAK/nuxBBgC9bXL886VFWnVr+bliNn7oWHi1zoggwJRo6\nT+cpZqi5vo6/Gut8x5AEWqmIhcwKuiqF6w/QKFdSA6SOMz+FcrsAoursIz9lqLT9\nuS2DWpA5xebLIkr8dXIhPmW4ttgezUoWAcAdTPjaJAQ8mFh702wDNf2CR8Y6IiUB\n/OECTrCGI6ED+5xvE8JevRE8HLksOv5crwKBoEa/yb65uDmVnFgHfISS3TkdRmpW\nFAHpPZ/1zsbgU3v4cXSQJsj5xuEk/vv5tamuvJtfyJ9MdEd2WDjN1zw2fpl/Fhgy\nC9/hED02Lu/lmLRNoU9IyUFSNAWVToWR6waobmAZ8QKBgQDaSvjCJfd0jDbd6nHX\nmuLIYU5vwEqWDO8lZljH8JBX9DDvXEzqKdRQS6kqdYu3hsKpIlJzDvqShVemfAda\ntdXNQXrqt8pPH4IVZVYj4raAIT4nXqGJDl4Mnayk/eM6YVhJQMIr/yW5EPfssHjz\nxZ0avYn2I0YBfMupn4JB12FZEQKBgQDD9bPc/uw1JDnj+9i9/xdsDbpQ8e8pjbA7\nIwSlzs6PhjVg1oZUjIhlKleBshqG/DKeBZfhrKGo7HsX3yXpOZcs1iVT3a50TW6h\n+CX/H3nzVXRjdEFUcWX2qwKjGagOeNtNtAR0dkluovHbkxiWAHXNMnyG0+HEN6zj\nlAi3lwCe+wKBgFSBr5mhjxGccmUorJe2C1NdcDsM6xL5wN7upzIH7ClQjF0tk00X\nkmzfTYb1aHhNADDv65FFXDW6zzrRSxuPx0wlrEsPiY9l+DsGNvm/e71QoTomhUyE\ntl4V8E8TRpNEOiRpoIHdzaG+cuw7SSe9+drvQ2h5MVHEGSf6azfIBJSxAoGBALrt\nQmnpcwEuUVq8/wAeugUFA1n7rxyAYD/JI8HXCQu4BmsduH4moGWAgoDhmJRzNwWu\naDeKKZuuGa2n284idab7kBf0O1oOEx7GS9iV+gq41ZGZcEhQ8+bdMmLLMpi7iNcS\nhb1iqKG1JelC5A0S20ymgEtNCuvWAEIHEFmw3ZLJAoGAVfK3ovsR3e0PptoJ27WS\neoFm1Fh2iXovrtOE23EONuakCy9aLmc9QfBq3TG+OJdKZXD+pe4xtRVvtipnbryU\nAzYz9k4p3cJHnnQwtHDakeaXvQXO960uM1C3VHn+XAVNd8tO3sUNyenpZzJPwcX2\no4Lsy7nKljoEGxCgS2I94mI=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ggn1f@iitg-speech-lab.iam.gserviceaccount.com",
    "client_id": "110868864917664596078",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ggn1f%40iitg-speech-lab.iam.gserviceaccount.com"
})
# firebase_admin.initialize_app(cred)
db = firestore.client()


# Calender
flags = tools.argparser.parse_args([])
FLOW = OAuth2WebServerFlow(
    client_id='378262545952-1r36bf3nd2bjad3641sprit3020rcpem.apps.googleusercontent.com',
    client_secret='vMX5C3nvgZ2OKkr1b0aXcZex',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='IITG-Speech-Lab'
    )
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
    credentials = tools.run_flow(FLOW, storage, flags)

httpObject = httplib2.Http()
httpObject = credentials.authorize(httpObject)
service = discovery.build('calendar', 'v3', http=httpObject)


def course_group(request, CourseID, CourseGroupID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    # context['CourseGroupID_json'] = mark_safe(json.dumps(CourseGroupID))
    # context['CourseID_json'] = mark_safe(json.dumps(CourseID))
    context['CourseGroupID_json'] = CourseGroupID
    context['CourseID_json'] = CourseID
    # return render(request, 'discussion/group.html', {
    #     'CourseGroupID_json' : mark_safe(json.dumps(CourseGroupID)),
    #     'CourseID_json' : mark_safe(json.dumps(CourseID)),
    # })
    return render(request, 'discussion/group.html', context)

def group(request, CourseID, AssignmentID, GroupID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    context['GroupID_json'] = mark_safe(json.dumps(GroupID))
    context['CourseID_json'] = mark_safe(json.dumps(CourseID))
    context['AssignmentID_json'] = mark_safe(json.dumps(AssignmentID))
    # return render(request, 'discussion/group.html', {
    #     'GroupID_json' : mark_safe(json.dumps(GroupID)),
    #     'CourseID_json' : mark_safe(json.dumps(CourseID)),
    #     'AssignmentID_json' : mark_safe(json.dumps(AssignmentID)),
    # })
    return render(request, 'discussion/group.html', context)

def notice_board(request,CourseID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    user_ref = db.collection(u'Users').document(username).get()
    user_dict = user_ref.to_dict()
    Designation = user_dict['Designation']

    # CourseID = self.scope['url_route']['kwargs']['CourseID']
    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'Notices')
    # #
    all_notice=[]
    docs = list(doc_ref.get())
    for i in range(len(docs)):
        id = docs[i].id
        doc = docs[i]
        doc = doc.to_dict()
        temp={
            'NoticeHead' : doc['NoticeHead'],
            'NoticeBody': doc['NoticeBody'],
            'Author': doc['Author'],
            'NoticeTime': doc['NoticeTime'],
        }
        all_notice.append(temp)

    context['all_notice'] = all_notice
    context['title'] = CourseID
    context['Designation'] = Designation
    # context={
    #     "all_notice":all_notice,
    #     "title":CourseID
    # }
    return render(request,'discussion/notice.html',context)

def add_notice(request,CourseID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    NoticeHead = request.POST['NoticeHead']
    if NoticeHead=="":
        NoticeHead="Notice"
    NoticeBody = request.POST['NoticeBody']
    print(NoticeHead)
    print(NoticeBody)
    doc_ref = db.collection(u'Courses').document(CourseID).collection(u'Notices').add({'Author' : username,'NoticeHead' : NoticeHead, 'NoticeBody' : NoticeBody, 'NoticeTime':firestore.SERVER_TIMESTAMP})
    return redirect('/discussion/courses/'+CourseID+'/noticeboard')

def view_calendar(request, CourseID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == CourseID:
                CalendarID = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        context['CourseID'] = CourseID
        context['CalendarID'] = CalendarID
        # return render(request, 'discussion/calendar.html', {'CourseID': CourseID, 'CalendarID': CalendarID})
        return render(request, 'discussion/calendar.html', context)


def add_event(request, CourseID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == CourseID:
                CalendarID = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    if request.method == 'POST':
        Summary = request.POST['Summary']
        Location = request.POST['Location']
        Description = request.POST['Description']
        StartDate = request.POST['Start']
        EndDate = request.POST['End']

        event = {
            'summary': Summary,
            'location': Location,
            'description': Description,
            'start': {
                'dateTime': StartDate+'T00:00:00+0530',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': EndDate+'T23:59:59+0530',
                'timeZone': 'America/Los_Angeles',
            },
            'visibility': 'public',
        }

        event = service.events().insert(calendarId=CalendarID, body=event).execute()
        return redirect('/discussion/courses/'+CourseID+'/events')

    elif request.method == 'GET':
        events_result = service.events().list(calendarId=CalendarID, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        context['events'] = events
        context['CourseID'] = CourseID
        context['CalendarID'] = CalendarID

        dateToday = datetime.today().strftime('%Y-%m-%d')
        context['dateToday'] = dateToday
        return render(request, 'discussion/add_event.html', context)

def delete_event(request, CourseID, EventID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == CourseID:
                CalendarID = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    service.events().delete(calendarId=CalendarID, eventId=EventID).execute()
    return redirect('/discussion/courses/'+CourseID+'/events')

def create_calendar(request, CourseID):
    context = {}
    context = loginFLOW(request, context)
    if context['username'] == '':
        return HttpResponseRedirect(reverse('home:home'))

    username = context['username']

    calendar = {
    'summary': CourseID,
    'timeZone': 'America/Los_Angeles'
    }

    created_calendar = service.calendars().insert(body=calendar).execute()
    print(created_calendar['id'])
    return redirect('/discussion/courses/'+CourseID+'/;')
