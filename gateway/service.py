from asyncio.windows_events import NULL
import datetime
from fileinput import filename
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy
import uuid
import json
import base64
from gateway.dependencies.news import NewsService
from gateway.dependencies.file import FileService
from gateway.dependencies.user import UserService

from gateway.dependencies.session import SessionProvider

class User:
    def __init__(self, name, password):
        self.username = name
        self.password = password
    
    #print
    def __str__(self):
        return 'User: {}, Password: {}'.format(self.username, self.password)


class Service:
    name = "gateway_service"

    user_rpc=RpcProxy('user_service')
    file_rpc=RpcProxy('file_service')
    news_rpc=RpcProxy('news_service')
    session_provider = SessionProvider()

    
    @http('POST', '/login')
    def login(self, request):
        session_id = request.cookies.get("SESSID")
        if session_id:
            session_data = self.session_provider.get_session(session_id)
            #get username
            username = session_data.get("username")
            return Response(f"You are already logged in as {username}")
        else:
            #check if username and password is exist in the body
            username = request.get_json()['username']
            password = request.get_json()['password']
            exist,user= self.user_rpc.login(username, password)
            #check if user exists
            if exist:
                user_data = {
                    'username': username
                }
                session_id = self.session_provider.set_session(user_data)
                response = Response(f"Welcome {username}")
                response.set_cookie('SESSID', session_id)
                return response
            else:
                return Response("Please check your username and password!")


    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            response = Response(self.session_provider.delete_session(cookies['SESSID']))
            response.set_cookie('SESSID', '', expires=0)
            return response
        else:
            response = Response('You need to Login First')
            return response

    @http('POST', '/register')
    def register(self, request):
        username = request.get_json()['username']
        password = request.get_json()['password']
        success,username= self.user_rpc.register(username, password)
        if(success):
            user_data={
                'username': username,
            }
            session_id = self.session_provider.set_session(user_data)
            response = Response("Register Success!, Welcome {}".format(username))
            response.set_cookie('SESSID', session_id)
            return response
        else:
            return Response("Register Failed, Username already exist!")


    #NEWS API

    @http('POST', '/news')
    def post_news(self, request):
        session_id = request.cookies.get("SESSID")
        if session_id:
            #check if key = title, content, author, date is in request
            session_data = self.session_provider.get_session(session_id)
            needed_keys=['title','content']
            for key in needed_keys:
                if key not in request.get_json().keys():
                    response=Response("Missing {}".format(key))
                    response.status_code=400
                    return response
            #get data from request
            
            user_id=self.user_rpc.get_user_id(session_data.get("username"))
            title=request.get_json()['title']
            content=request.get_json()['content']
            todaydate=str(datetime.datetime.now())
            # print(f"{user_id} {title} {content} {date}")
            file_id="NULL"
            if 'files' in request.get_json().keys():
                needed_files_keys=['file_name','b64_file']
                # print(request.get_json()['files'].keys())
                for key in needed_files_keys:
                    if key not in request.get_json()['files'].keys():
                        response=Response("Missing {}".format(key))
                        response.status_code=400
                        return response
                #get data from request
                file_name=request.get_json()['files']['file_name']
                file_type=file_name.split('.')[-1]
                file_name=file_name.split('.')[0]
                today = str(datetime.datetime.now())
                # todaydate=today!!!!!!!!!!!!!!!!!!!!!!!!
                #remove miliseconds
                today=today.split('.')[0]
                today=today.replace(':','')
                file_path = 'file/{}{}.{}'.format(file_name, today,file_type)
                # file_path='file/{}'.format(file_name)
                with open(f"file/{file_name}", "wb") as fh:
                    fh.write(base64.decodebytes(request.get_json()['files']['b64_file'].encode("ascii")))
                self.file_rpc.upload_file(file_name,file_path)
                print("test")
                file_id=self.file_rpc.get_file_id(file_name,file_path)
                print(file_id)
            
            self.news_rpc.add_news(user_id,title,content,todaydate,file_id)
            response={
                'status':'success',
                'message':'News added successfully',
                'data':{
                    'title':title,
                    'content':content,
                    'date':todaydate,
                    'files':file_id
                    }
            }
            return Response(json.dumps(response))
        else:
            return Response("You need to Login First")
    
    #edit news
    @http('PUT', '/news/<news_id>')
    def edit_news(self, request, news_id):
        session_id = request.cookies.get("SESSID")
        if session_id:
            #check if that news belong to user
            session_data = self.session_provider.get_session(session_id)
            user_id=self.user_rpc.get_user_id(session_data.get("username"))
            if not self.news_rpc.check_news_belong_to_user(news_id,user_id):
                response=Response("You don't have permission to edit this news")
                #unauthorized
                response.status_code=401
                return response

            new_title=NULL
            new_content=NULL

            if 'title' in request.get_json().keys():
                new_title=request.get_json()['title']
            if 'content' in request.get_json().keys():
                new_content=request.get_json()['content']
            
            if new_title==NULL and new_content==NULL:
                print("no change")
                response=Response("No data to update")
                response.status_code=400
                return response

            today=str(datetime.datetime.now())
            self.news_rpc.edit_news(news_id,new_title,new_content,today)
            

            response={
                'status':'success',
                'message':'News edited successfully'
            }
            return Response(json.dumps(response))
        else:
            return Response("You need to Login First")

    #delete news
    @http('DELETE', '/news/<news_id>')
    def delete_news(self, request, news_id):
        session_id = request.cookies.get("SESSID")
        if session_id:
            #check if that news belong to user
            session_data = self.session_provider.get_session(session_id)
            user_id=self.user_rpc.get_user_id(session_data.get("username"))
            if not self.news_rpc.check_news_belong_to_user(news_id,user_id):
                response=Response("You don't have permission to delete this news")
                #unauthorized
                response.status_code=401
                return response
            self.news_rpc.delete_news(news_id)
            response={
                'status':'success',
                'message':'News deleted successfully'
            }
            return Response(json.dumps(response))
        else:
            return Response("You need to Login First")

    #get news
    @http('GET', '/news')
    def get_news(self, request):
        data=self.news_rpc.get_news()
        response={
            'status':'success',
            'message':'News fetched successfully',
            'data':data
        }
        return Response(json.dumps(response))

    #get news by id
    @http('GET', '/news/<news_id>')
    def get_news_by_id(self, request, news_id):
        data=self.news_rpc.get_news_by_id(news_id)
        print(data)
        if data is None:
            response=Response("News not found")
            response.status_code=404
            return response
        response={
            'status':'success',
            'message':'News fetched successfully',
            'data':data
        }
        return Response(json.dumps(response))

    #download file by id
    @http('GET', '/file/<file_id>')
    def download_file(self, request, file_id):
        success,file_path,filename=self.file_rpc.download_file(file_id)
        if(success):
            response = Response(open(file_path, 'rb').read())
            #get file type
            file_type=filename.split('.')[-1]
            if(file_type=='jpg' or file_type=='png' or file_type=='jpeg' or file_type=='gif'):
                if file_type=='jpg':
                    file_type='jpeg'
                response.headers['Content-Type'] = 'image/{}'.format(file_type)
            else:
                response.headers['Content-Type'] = 'application/{}'.format(file_type)
            #replace spaces with underscore
            filename=filename.replace(' ','_')
            response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
            return response
        else:
            return Response(file_path)


        

            

            
            

            


            
    
    
    

