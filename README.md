# Group chatting application
In this POC we can chat in group

This POC uses channels library to enable websocket <br>
  
# Prerequisites
You will need the following programmes properly installed on your computer.<br>
Python 3.7+

# Installation and Running

clone the repository
```
git clone https://github.com/Ritesh1200/Django_Group_chatting.git
cd Django_Group_chatting
```
create a vertual environment
```
python -m venv .venv
.venv/bin/activate.bat
```
install required packages
```
pip install -r requirements.txt
```
running
```
python manage.py runserver
```

# Testing:
Create or enter room : http://localhost:8000/chat/ <br>
Chatting : http://localhost:8000/chat/roomname/username   <br>