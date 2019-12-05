from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
# Create your views here.


class GreetingView(View):
    gettint ='hello world'

    def test1(self,request):
        msg =request.GET.get('msg')
        print(msg)

        return render(request,'demo1.html',{
            'msg':self.gettint



        })