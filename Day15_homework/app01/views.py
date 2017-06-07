from django.shortcuts import render,HttpResponse,redirect
from app01 import models
import json
# Create your views here.
def admin(request):

    #return render(request,'index.html',{'hosts',host_query})
    return render(request,'index.html')

def table_area(request):
    if request.method=='GET':
        host_query=models.host.objects.all()
        host_list=[]
        for host in host_query:
            temp={'id':host.id,
                  'hostname':host.hostname,
                  'ip':host.ip,
                  'port':host.port,
                  'status':host.status}
            host_list.append(temp)
        data=json.dumps(host_list)
        return HttpResponse(data)
    if request.method=='POST':
        if request.POST['action_type']=='add':
            data_dic={
                'hostname':request.POST['hostname'],
                'ip':request.POST['ip'],
                'port':request.POST['port'],
                'status':request.POST['status']
            }
            models.host.objects.create(**data_dic)
        if request.POST['action_type']=='batch_save':
            data_list=json.loads(request.POST['data_list'])
            for host_item in data_list:
                models.host.objects.filter(id=int(host_item['row_id'])).update(hostname=host_item['hostname'],
                                                                               ip=host_item['ip'],
                                                                               port=host_item['port'],
                                                                               status=host_item['status'])
        if request.POST['action_type']=='delete':
            data_list=json.loads(request.POST['data_list'])
            for host_id in data_list:
                models.host.objects.filter(id=int(host_id)).delete()
        host_query=models.host.objects.all()
        host_list=[]
        for host in host_query:
            temp={'id':host.id,
                  'hostname':host.hostname,
                  'ip':host.ip,
                  'port':host.port,
                  'status':host.status}
            host_list.append(temp)
        data=json.dumps(host_list)
        return HttpResponse(data)

def edit_row(request):
    host_query=models.host.objects.all()
    return render(request,'edit_row.html',{'hosts':host_query})

def db_inital(request):
    sample_user={
        "username":'eric',
        "password":'eric123'
    }
    models.userinfo.objects.create(**sample_user)

def submit(request):
    if request.method=="POST":
        data_dic=request.POST
        ret2=models.userinfo.objects.filter(username=data_dic['account'],password=data_dic['password']).first()
        if ret2:
            print(data_dic)
            #return HttpResponse("login success")
            return redirect("/app01/admin/")
        else:
            failed_msg="用户名或密码有误！"
            #return redirect("/app01/login/")
            return render(request,'login.html',{'login_result':failed_msg})
def login(request):
    ret=models.userinfo.objects.all()
    if ret.__len__()==0:
        db_inital(request)
    # if request.method=="POST":
    #     data_dic=request.POST
    #     ret2=models.userinfo.objects.filter(username=data_dic['account'],password=data_dic['password']).first()
    #     if ret2:
    #         print(data_dic)
    #         print("login success")
    #     else:
    #         print("login failed!")
    # if ret2:
    #     print("login success")
    # else:
    #     print("login failed!")
    return render(request,'login.html')
