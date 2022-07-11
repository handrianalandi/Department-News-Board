# Department News Board<hr />

a Department News Board service that able to :<br>
upload a news without attachment file (locally)(must logged in)<br>
upload a news with attachment file (locally)(must logged in)<br>
edit a news (locally)(must logged in)<br>
delete a news (locally)(must logged in)<br>
get all news (locally)(must logged in)<br>
get news by id(locally)(must logged in)<br>
download attachment file by id(locally)(must logged in)<br><br>
**You only need to run gateway.service to start all the services**<br><br>
this project also implement session, user must logged in in order to use some of the service<br><br>
please kindly look at the documentation about how the service works :https://documenter.getpostman.com/view/13165507/UzBiRV5B



## Post New News<br /> 
```POST```&nbsp;&nbsp;&nbsp;localhost:8000/news<br />  
> ### Response
**Post New News without file**<br />localhost:8000/news<br />``` Status Code: 200 OK```<br />
```
Request Body:
{
    "title":"title1",
    "content":"content1"
}
```


```
Response Body:
{
    "status": "success",
    "message": "News added successfully",
    "data": {
        "title": "title1",
        "content": "content1",
        "date": "2022-06-23 23:41:58.311565",
        "files": "NULL"
    }
}
``` 
**Post New News with file**<br />localhost:8000/news<br />``` Status Code: 200 OK```<br />
```
Request Body:
{
    "title":"title1withfile",
    "content":"content1withfile",
    "files":{
        "file_name":"testgambaranjeng.png",
        "b64_file":"<b64_file_string>"
```


```
Response Body:
{
    "status": "success",
    "message": "News added successfully",
    "data": {
        "title": "title1withfile",
        "content": "content1withfile",
        "date": "2022-06-23 23:42:49.139287",
        "files": 51
    }
}
``` 
<hr /> 

## login<br /> 
```POST```&nbsp;&nbsp;&nbsp;localhost:8000/login<br />  
> ### Response
**login**<br />localhost:8000/login<br />``` Status Code: 200 OK```<br />
```
Request Body:
{
    "username":"han1",
    "password":"han123"
}
```


```
Response Body:
Welcome han1
``` 
<hr /> 

## logout<br /> 
```POST```&nbsp;&nbsp;&nbsp;localhost:8000/logout<br />  
> ### Response
**logout**<br />localhost:8000/logout<br />``` Status Code: 200 OK```<br />

```
Response Body:
Successfully Logged out from han1
``` 
<hr /> 

## register<br /> 
```POST```&nbsp;&nbsp;&nbsp;localhost:8000/register<br />  
> ### Response
**register**<br />localhost:8000/register<br />``` Status Code: 200 OK```<br />
```
Request Body:
{
    "username":"han45",
    "password":"han123"
}
```


```
Response Body:
Register Success!, Welcome han45
``` 
<hr /> 

## edit news<br /> 
```PUT```&nbsp;&nbsp;&nbsp;localhost:8000/news<br />  
> ### Response
**edit news**<br />localhost:8000/news/24<br />``` Status Code: 200 OK```<br />
```
Request Body:
{
    "title":"titleupdate1",
    "content":"contentupdate1"
}
```


```
Response Body:
{
    "status": "success",
    "message": "News edited successfully"
}
``` 
**edit news update content**<br />localhost:8000/news/24<br />``` Status Code: 200 OK```<br />
```
Request Body:
{
    "content":"contentupdatekedua1"
}
```


```
Response Body:
{
    "status": "success",
    "message": "News edited successfully"
}
``` 
**edit news update title**<br />localhost:8000/news/24<br />``` Status Code: 200 OK```<br />
```
Request Body:
{
    "title":"titleupdatekedua1"
}
```


```
Response Body:
{
    "status": "success",
    "message": "News edited successfully"
}
``` 
**edit news no data to update**<br />localhost:8000/news/24<br />``` Status Code: 400 BAD REQUEST```<br />
```
Request Body:
{
    
}
```


```
Response Body:
No data to update
``` 
<hr /> 

## delete news<br /> 
```DELETE```&nbsp;&nbsp;&nbsp;localhost:8000/news<br />  
> ### Response
**delete news**<br />localhost:8000/news/24<br />``` Status Code: 200 OK```<br />

```
Response Body:
{
    "status": "success",
    "message": "News deleted successfully"
}
``` 
<hr /> 

## get news<br /> 
```GET```&nbsp;&nbsp;&nbsp;localhost:8000/news<br />  
> ### Response
**get news all**<br />localhost:8000/news<br />``` Status Code: 200 OK```<br />

```
Response Body:
{
    "status": "success",
    "message": "News fetched successfully",
    "data": [
        {
            "id": 25,
            "user_id": 2,
            "title": "title1",
            "content": "content1",
            "date": null,
            "file_id": 47
        },
        {
            "id": 26,
            "user_id": 2,
            "title": "title1",
            "content": "content1",
            "date": null,
            "file_id": 48
        },
        {
            "id": 27,
            "user_id": 2,
            "title": "title1",
            "content": "content1",
            "date": null,
            "file_id": 49
        },
        {
            "id": 28,
            "user_id": 2,
            "title": "title1",
            "content": "content1",
            "date": null,
            "file_id": 50
        },
        {
            "id": 29,
            "user_id": 2,
            "title": "title1",
            "content": "content1",
            "date": null,
            "file_id": null
        }
    ]
}
``` 
**get news by id (not found)**<br />localhost:8000/news/24<br />``` Status Code: 404 NOT FOUND```<br />

```
Response Body:
News not found
``` 
**get news by id**<br />localhost:8000/news/25<br />``` Status Code: 200 OK```<br />

```
Response Body:
{
    "status": "success",
    "message": "News fetched successfully",
    "data": {
        "id": 25,
        "user_id": 2,
        "title": "title1",
        "content": "content1",
        "date": null,
        "file_id": 47
    }
}
``` 
<hr /> 

## download file<br /> 
```GET```&nbsp;&nbsp;&nbsp;localhost:8000/file/1<br />  
> ### Response
```
file downloaded
```
<hr /> 


