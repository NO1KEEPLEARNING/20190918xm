from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
from django.core.paginator import Paginator
# Create your views here.


class GreetingView(View):
    gettint ='hello world'
    def __init__(self):
        self.msg = 'msg'

    def test1(self,request):
        print('msg111111',self.msg)
        mssg =request.GET.get('mssg')
        print(mssg)
        self.msg=mssg
        print('mssg',self.msg)

        return render(request, 'demo2.html', {
            'msg':self.gettint



        })
greeting =GreetingView()