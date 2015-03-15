import os
import logging
import wsgiref.handlers
import google.appengine.api
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from util.sessions import Session
from google.appengine.ext import db
from google.appengine.ext import django
from sets import Set
from google.appengine.api import search 
import datetime






  
# A Model for a User
class User(db.Model):
  account = db.StringProperty()
  password = db.StringProperty()
  name = db.StringProperty()
  
class MapCat(db.Model):
    
    ATTRIBUTE_1='attribute_1'
    ATTRIBUTE_2='attribute_2'
    ATTRIBUTE_3='attribute_3'
    ATTRIBUTE_4='attribute_4'
    ATTRIBUTE_5='attribute_5'
    ATTRIBUTE_6='attribute_6'
    ATTRIBUTE_7='attribute_7'
    ATTRIBUTE_8='attribute_8'
    ATTRIBUTE_9='attribute_9'
    ATTRIBUTE_10='attribute_10'
    Category = db.StringProperty()
    Attribute_1 = db.StringProperty()
    Attribute_2 = db.StringProperty()
    Attribute_3 = db.StringProperty()
    Attribute_4 = db.StringProperty()
    Attribute_5 = db.StringProperty()
    Attribute_6 = db.StringProperty()  
    Attribute_7 = db.StringProperty()
    Attribute_8 = db.StringProperty()
    Attribute_9 = db.StringProperty()
    Attribute_10 = db.StringProperty()
  
class MapAtt(db.Model):
  Category = db.StringProperty()
  Attribute = db.StringProperty()    
  Type_1 = db.StringProperty()
  Type_2 = db.StringProperty()
  Type_3 = db.StringProperty()
  Type_4 = db.StringProperty()
  Type_5 = db.StringProperty()
  Type_6 = db.StringProperty()  
  Type_7 = db.StringProperty()
  Type_8 = db.StringProperty()
  Type_9 = db.StringProperty()
  Type_10 = db.StringProperty()  
  
class Temp(db.Model):
  temp_1= db.StringProperty()
  temp_2= db.StringProperty()
  
temp = {}
# A helper to do the rendering and to add the necessary
# variables for the _base.htm template
def doRender(handler, tname = 'index.htm', values = { }):
  temp = os.path.join(
      os.path.dirname(__file__),
      'templates/' + tname)
  if not os.path.isfile(temp):
    return False

  # Make a copy of the dictionary and add the path and session
  newval = dict(values)
  newval['path'] = handler.request.path
  handler.session = Session()
  if 'username' in handler.session:
     newval['username'] = handler.session['username']

  outstr = template.render(temp, newval)
  handler.response.out.write(unicode (outstr))
  return True

class LoginHandler(webapp.RequestHandler):

  def get(self):
    doRender(self, 'loginscreen.htm')

  def post(self):
    self.session = Session()
    acct = self.request.get('account')
    pw = self.request.get('password')
    logging.info('Checking account='+acct+' pw='+pw)

    self.session.delete_item('username')

    if pw == '' or acct == '':
      doRender(
          self,
          'loginscreen.htm',
          {'error' : 'Please specify Account and Password'} )
      return

    que = db.Query(User)
    que = que.filter('account =',acct)
    que = que.filter('password = ',pw)

    results = que.fetch(limit=1)

    if len(results) > 0 :
      self.session['username'] = acct
      doRender(self,'index.htm',{ } )
    else:
      doRender(
          self,
          'loginscreen.htm',
          {'error' : 'Incorrect password'} )

class ApplyHandler(webapp.RequestHandler):

  def get(self):
    doRender(self, 'applyscreen.htm')

  def post(self):
    self.session = Session()
    name = self.request.get('name')
    acct = self.request.get('account')
    pw = self.request.get('password')
    logging.info('Adding account='+acct)

    if pw == '' or acct == '' or name == '':
      doRender(
          self,
          'applyscreen.htm',
           {'error' : 'Please fill in all fields'} )
      return

    # Check if the user already exists
    que = db.Query(User).filter('account =',acct)
    results = que.fetch(limit=1)

    if len(results) > 0 :
      doRender(
          self,
          'applyscreen.htm',
          {'error' : 'Account Already Exists'} )
      return

    # Create the User object and log the user in
    newuser = User(name=name, account=acct, password=pw);
    newuser.put();
    self.session['username'] = acct
    doRender(self,'index.htm',{ })

class MapCatHandler(webapp.RequestHandler):
    def get(self):
  
      doRender(self, 'MapCat.htm')
    def post(self):
        self.session = Session()
        Category = self.request.get('Category')   
        Attribute_1 = self.request.get('Attribute_1')
        Attribute_2 = self.request.get('Attribute_2')
        Attribute_3 = self.request.get('Attribute_3')
        Attribute_4 = self.request.get('Attribute_4')
        Attribute_5 = self.request.get('Attribute_5')
        Attribute_6 = self.request.get('Attribute_6')
        Attribute_7 = self.request.get('Attribute_7')
        Attribute_8 = self.request.get('Attribute_8')
        Attribute_9 = self.request.get('Attribute_9')
        Attribute_10 = self.request.get('Attribute_10')
        newMapCat = MapCat(Category=Category, Attribute_1=Attribute_1, Attribute_2=Attribute_2,
                   Attribute_3=Attribute_3, Attribute_4=Attribute_4,Attribute_5=Attribute_5,
                    Attribute_6=Attribute_6,
                   Attribute_7=Attribute_7, Attribute_8=Attribute_8,Attribute_9=Attribute_9,
                    Attribute_10=Attribute_10);
        newMapCat.put()
        doRender(
        self, 
        'MapCat.htm', 
        {})

        
    
   

   

        
    

   

    # Create the User object and log the user in
 
    #self.response.out.write(att1)       
    
    #self.response.out.write(att1)
   
class MapProCatHandler(webapp.RequestHandler):
    
    def get(self):
       
     que=db.Query(MapCat)
     Category_list=que.fetch(limit=100)
         
     doRender(
              self,        
              'MapProCat.htm', {'Category_list':Category_list})
class MapProAttHandler(webapp.RequestHandler):
    
    def get(self):

     category=self.request.get('Category')
     

     que =db.Query(MapCat)
     
     que= que.filter('Category =',category)
     Category_list=que.fetch(limit=1)
     Att=[]
     
     for cat in Category_list:
         Att.insert(0, cat.Attribute_1)
         Att.insert(1, cat.Attribute_2)
         Att.insert(2, cat.Attribute_3)
         Att.insert(3, cat.Attribute_4)
         Att.insert(4, cat.Attribute_5)
         Att.insert(5, cat.Attribute_6)
         Att.insert(6, cat.Attribute_7)
         Att.insert(7, cat.Attribute_8)
         Att.insert(8, cat.Attribute_9)
         Att.insert(9, cat.Attribute_10)
         #db.GqlQuery()   
     doRender(
              self,        
              'MapProAtt.htm', {'Attributes':Att})
     #self.response.out.write(Att)
class MapProAttTabHandler(webapp.RequestHandler):
    
    def get(self):
       
     
     #Category_list=que.filter('Category=',MapAtt_1)
     category=self.request.get('Category')
    
      
     attribute=self.request.get('Attribute')
     myAtt=self.request.get('myAtt')
     #results= db.GqlQuery("SELECT * from MapCat where Category=:1",category) 
     
     
     que =db.Query(MapAtt)
     
     que= que.filter('Category =',category)
     que= que.filter('Attribute =',attribute)
     Category_list=que.fetch(limit=1)       
     doRender(
              self,        
              'MapProAttTab.htm', {'Category_list':Category_list,'myAtt':myAtt})          

    
class MapAtt1CatHandler(webapp.RequestHandler):
    
    def get(self):
       
     que=db.Query(MapCat)
     Category_list=que.fetch(limit=100)
         
     doRender(
              self,        
              'MapAtt1Cat.htm', {'Category_list':Category_list}) 
class MapAtt1AttHandler(webapp.RequestHandler):
    
    def get(self):
       
     
     #Category_list=que.filter('Category=',MapAtt_1)
     category=self.request.get('Category')
    
      
     attribute=self.request.get('Attribute')
     
     #results= db.GqlQuery("SELECT * from MapCat where Category=:1",category) 
     
     
     que =db.Query(MapCat)
     
     que= que.filter('Category =',category)
     Category_list=que.fetch(limit=1)       
     doRender(
              self,        
              'MapAtt1Att.htm', {'Category_list':Category_list})   
      
class MembersHandler(webapp.RequestHandler):

  def get(self):
    que = db.Query(MapCat)
    user_list = que.fetch(limit=100)
    doRender(
        self, 
        'memberscreen.htm', 
        {'user_list': user_list})

class LogoutHandler(webapp.RequestHandler):

  def get(self):
    self.session = Session()
    self.session.delete_item('username')
    doRender(self, 'index.htm')

class MapAttHandler(webapp.RequestHandler):
     def post(self):  
     
    
     
        Category = self.request.get('Category')
        Attribute = self.request.get('Attribute')                   
        Type_1 = self.request.get('Type_1')
        Type_2 = self.request.get('Type_2')
        Type_3 = self.request.get('Type_3')
        Type_4 = self.request.get('Type_4')
        Type_5 = self.request.get('Type_5')
        Type_6 = self.request.get('Type_6')
        Type_7 = self.request.get('Type_7')
        Type_8 = self.request.get('Type_8')
        Type_9 = self.request.get('Type_9')
        Type_10 = self.request.get('Type_10')
        newMapAtt = MapAtt(Category=Category,Attribute=Attribute,Type_1=Type_1, Type_2=Type_2,
                   Type_3=Type_3, Type_4=Type_4,Type_5=Type_5,
                    Type_6=Type_6,
                   Type_7=Type_7, Type_8=Type_8,Type_9=Type_9,
                    Type_10=Type_10);
        newMapAtt.put() 
        doRender(
        self, 
        'MapAtt2.htm', 
        {})       
class MainHandler(webapp.RequestHandler):

  def get(self):
    if doRender(self,self.request.path) :
      return
    doRender(self,'index.htm')

class SearchHandler(webapp.RequestHandler):
    def post(self):
        search_text=self.request.get('search_text')
        index=search.Index(_INDEX_NAME)
        query=search_text
        query_string=search.Query(query_string=search_text,options=search.QueryOptions(returned_fields=COMPANY))
        results=index.search(query_string)
        searchlist=list()
        #self.response.out.write(results)
        count=0
        for result in results:
            searchlist.insert(count, result )
            count=count+1
        #self.response.out.write(searchlist)
        doRender(self,'Search.htm',{'results':searchlist})
        
class MapProHandler(webapp.RequestHandler):
    def post(self):
        category=self.request.get("Category")
        pid=self.request.get("pid")
        attribute_1=self.request.get("Attribute_1")
        attribute_2=self.request.get("Attribute_2")
        attribute_3=self.request.get("Attribute_3")
        attribute_4=self.request.get("Attribute_4")
        attribute_5=self.request.get("Attribute_5")
        attribute_6=self.request.get("Attribute_6")
        attribute_7=self.request.get("Attribute_7")
        attribute_8=self.request.get("Attribute_8")
        attribute_9=self.request.get("Attribute_9")
        attribute_10=self.request.get("Attribute_10")
        company=self.request.get('Company')
        _buildCoreProductFields(pid, category, attribute_1, attribute_2, attribute_3, attribute_4,
        attribute_5, attribute_6, attribute_7, attribute_8, attribute_9, attribute_10, company)
        doRender(self,'MapPro.htm',{})    
    

_INDEX_NAME = 'productsearch'
PID='pid'
UPDATED='updated'
CATEGORY='category'
COMPANY='company'
def _buildCoreProductFields( pid,  category_name, Attribute_1,Attribute_2,Attribute_3,
      Attribute_4,Attribute_5,Attribute_6,Attribute_7,Attribute_8,Attribute_9,Attribute_10,Company):
    
    """Construct a 'core' document field list for the fields common to all
    Products. The various categories (as defined in the file 'categories.py'),
    may add additional specialized fields; these will be appended to this
    core list. (see _buildProductFields)."""
    fields = [
              
              # The 'updated' field is always set to the current date.
              search.DateField(name=UPDATED,value=datetime.datetime.now().date()),
              search.TextField(name=MapCat.ATTRIBUTE_1, value=Attribute_1),
              search.TextField(name=MapCat.ATTRIBUTE_2, value=Attribute_2),
              search.TextField(name=MapCat.ATTRIBUTE_3, value=Attribute_3),
              search.TextField(name=MapCat.ATTRIBUTE_4, value=Attribute_4),
              search.TextField(name=MapCat.ATTRIBUTE_5, value=Attribute_5),
              search.TextField(name=MapCat.ATTRIBUTE_6, value=Attribute_6),
              search.TextField(name=MapCat.ATTRIBUTE_7, value=Attribute_7),
              search.TextField(name=MapCat.ATTRIBUTE_8, value=Attribute_8),
              search.TextField(name=MapCat.ATTRIBUTE_9, value=Attribute_9),
              search.TextField(name=MapCat.ATTRIBUTE_10, value=Attribute_10),
              search.TextField(name=COMPANY, value=Company),
              
              # strip the markup from the description value, which can
              # potentially come from user input.  We do this so that
              # we don't need to sanitize the description in the
              # templates, showing off the Search API's ability to mark up query
              # terms in generated snippets.  This is done only for
              # demonstration purposes; in an actual app,
              # it would be preferrable to use a library like Beautiful Soup
              # instead.
              # We'll let the templating library escape all other rendered
              # values for us, so this is the only field we do this for.
              
              search.TextField(name=CATEGORY, value=category_name),
              
              
             ]
    document=search.Document(doc_id=pid,fields=fields)
    search.Index(_INDEX_NAME).put(document)

def main():
  application = webapp.WSGIApplication([
     ('/login', LoginHandler),     
     ('/MapCat', MapCatHandler),     
     ('/MapAtt', MapAttHandler),
     ('/MapProCat', MapProCatHandler),
     ('/MapProAtt', MapProAttHandler),
     ('/MapProAttTab', MapProAttTabHandler),
     ('/MapAtt1Cat', MapAtt1CatHandler),
     ('/MapAtt1Att', MapAtt1AttHandler),
     ('/apply', ApplyHandler),
     ('/members', MembersHandler),
     ('/logout', LogoutHandler),
     ('/MapPro',MapProHandler),
     ('/search',SearchHandler),
     ('/.*', MainHandler)],
     debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
