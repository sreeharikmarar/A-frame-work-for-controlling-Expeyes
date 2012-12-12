import web,sqlite3
from web import form 
from pylab import*
import eyes
import random

urls = (
  '/', 'home',
'/about','about',
'/first','first',
'/experiment','second',
'/third','third',
'/four','four',
'/five','five',
'/six','six',
'/seven','seven',
'/experiment1','experiment1',
'/experiment2','experiment2',
'/experiment3','experiment3',
'/experiment4','experiment4',
'/experiment5','experiment5',
'/experiment6','experiment6',
'/graph','graph',
'/signin','signin',
'/signup','signup',
'/login_success','login_success',
'/login_fail','login_fail',
'/reg_success','reg_success',
'/signout','signout',
'/contact','contact'
)



app = web.application(urls, globals(), True)

store = web.session.DiskStore('sessions')


if web.config.get('_session') is None:
        session = web.session.Session(app,store,initializer={'login': 0,'privilege': 0,'user':'anonymous','loggedin':False})
        web.config._session = session
else:
        session = web.config._session

render = web.template.render('templates/',globals={'context': session})




class home:
    def GET(self):
        return render.home()
class about:
    def GET(self):
        return render.about()

class first:

    def GET(self):
        return "Entered value goes here"        
        
    def POST(self):
        i = web.input()
        m = i.text3
        n = i.text4
        m = int(m)
        n = int(n)
        p = eyes.open() 
        if ((m == 0) and (n == 0)): 
            p.write_outputs(0)
        elif((m == 1) and ( n == 0)):
            p.write_outputs(1)
        elif((n == 1) and ( m == 0 )):
            p.write_outputs(2)
        elif((m ==1) and (n ==1)):
	    p.write_outputs(3)   
        else:
            p.write_outputs(0)
            
       
class second:

    def GET(self):
        return render.experiment()
	
class third:
    def GET(self):
        p = eyes.open()
        a = p.read_inputs() & 3
        return bin(a)

        
class four:
    def POST(self):
        i = web.input()
        n = i.text8
        n = int(n)
        p = eyes.open()
        p.set_sqr1(n)
       
class five:
    def GET(self):
        p = eyes.open()
        a = p.get_voltage(0)
        return a
        

class six:
    def GET(self):
        p=eyes.open()
        a = p.get_voltage(1)
        return a
        

class seven:
    def GET(self):
        p=eyes.open()
        a=p.get_voltage(2)
        return a
        

class experiment1:

    def GET(self):
        return render.experiment1()

class experiment2:
    def GET(self):  
        
        return render.experiment2()


class experiment3:
    def GET(self):
        return render.experiment3()


class experiment4:
    def GET(self):
        return render.experiment4()

class experiment5:
    def GET(self):
        p = eyes.open()
	a = p.capture(0, 200, 100)
	t, v = a 
        return render.experiment5(v)

class graph:
    def GET(self): 
        p = eyes.open()
	a = p.capture(0, 200, 100)
	t, v = a 
        return  render.graph(v)
        
class experiment6:
    def GET(self):
        return render.experiment6()

class signin:
    def GET(self):
        return render.signin()

    def POST(self):
        fi =  web.input()
        conn = sqlite3.connect('hari.db')
        curs = conn.cursor()
        check = curs.execute('''select * from reg_form where email=? and password=? ''',(fi.email, fi.pswd))
        count = check.fetchall()
	
        if len(count)!=0: 
            session.loggedin = True
            session.username = fi.email
	    
            raise web.redirect('/login_success')
        else:
            raise web.redirect('/login_fail')


class signup:
    def GET(self):
        return render.signup()
    def POST(self):
        fi =  web.input()
        conn = sqlite3.connect('hari.db')
        curs = conn.cursor()
        curs.execute('''insert into reg_form values(?,?,?,?,?,?,?,?)''',(fi.fname, fi.lname, fi.gender, fi.dd, fi.mm, fi.yyyy, fi.email, fi.pswd1))
        conn.commit()
        raise web.redirect('/reg_success')


class login_success:
    def GET(self):
        return render.login_success()
        

    def POST(self):
        raise web.redirect('/experiment1')


class login_fail:
    def GET(self):
        return render.login_fail()

    def POST(self):
        raise web.redirect('/signin')


class reg_success:
    def GET(self):
        return render.reg_success()
        
    def POST(self):

        raise web.redirect('/experiment1')

class signout:
    def GET(self):
        session.kill()
        return render.home()

class contact:
    def GET(self):
        return render.contact()

    
if __name__ == "__main__":
    #web.httpserver.runsimple(app.wsgifunc(), ("10.1.15.109",8080))
    web.httpserver.runsimple(app.wsgifunc(), ("127.0.0.1",8080))
    app.run()

