def cleanHeaderName(name):
  e = name.split('-')
  if (len(e) > 1):
    e[1] = e[1].title()
  return "".join(e)

class UserInfo:
  def __init__(self, request):
    headers = dict(request.headers)
    headers = dict(filter(lambda val: val[0].startswith('X-Replit-User-'), headers.items()))
    for name in headers:
      setattr(self, cleanHeaderName(name.split('X-Replit-User-')[1].lower()), headers.get(name))
      if name in ["X-Replit-User-Teams", "X-Replit-User-Roles"]:
        setattr(self, cleanHeaderName(name.split('X-Replit-User-')[1].lower()), headers.get(name).split(','))

    self.loggedIn = headers.get('X-Replit-User-Id')!=None

def getUserInfo(request):
  return UserInfo(request)

if __name__ == '__main__':
  from flask import Flask, request
  
  app = Flask(__name__)
  
  @app.route('/')
  def index():
    user = getUserInfo(request)
    return f'''
Hello <strong>{ user.name }</strong>! Here's some info about you:<ul>
  <li>Username: { user.name }</li>
  <li>User ID: { user.id }</li>
  <li>Bio: { user.bio or "You haven't set a bio!" }</li>
  <li>URL: <a href="{ user.url }">{ user.url }</a></li>
  <li>Profile Picture: <br><a href="{ user.profileImage }"><img src="{ user.profileImage }" alt="Your profile picture" width="128px" height="128px"/></a></li>
  <li>Roles ({ len(user.roles) }): { ", ".join(user.roles) }</li>
  <li>Teams ({ len(user.teams) }): { ", ".join(user.teams) }</li>
</ul>
    '''
    
  
  app.run(host='0.0.0.0', port=8080)
    