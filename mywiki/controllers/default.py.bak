def index():
    """ this controller returns a dictionary rendered by the view
    it lists all wiki pages
    >>> index().has_key('pages')
    True
    """
    if auth.user!=None:
        redirect(URL('afterlogin'))
    else:
        redirect("http://127.0.0.1:8000/mywiki/default/user/login")
    msg="WELCOME!"
    return dict(msg=msg)

@auth.requires_login()
def afterlogin():
    redirect(URL('showall'))
    msg="WELCOME!"
    return dict(msg=msg)

@auth.requires_login()
def create():
    """creates a new empty wiki page"""
    form = SQLFORM(db.page)
    if form.process().accepted:
            response.flash="Recipe Uploaded"
    return dict(form=form)

@auth.requires_login()
def show():
    """shows a wiki page"""
    this_page = db.page(request.args(0,cast=int)) or redirect(URL('index'))
    if this_page.created_by==auth.user.id:
        a=1
    else:
        a=2
    db.post.page_id.default = this_page.id
    form = SQLFORM(db.post).process() if auth.user else None
    pagecomments = db(db.post.page_id==this_page.id).select()
    flag = False
    results = db(db.likes.Username==auth.user.id)(db.likes.Dish==this_page.id).select()
    for result in results:
        flag = True
    return dict(page=this_page, comments=pagecomments, form=form,ps=a,flag=flag)

@auth.requires_login()
def showall():
    if len(request.args):
        page=int(request.args[0])
    else: 
        page=0
    items_per_page=5
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    pages = db(db.page.id>0).select(limitby=limitby)
    return dict(pages=pages,page=page,items_per_page=items_per_page)

@auth.requires_login()
def showmy():
    if len(request.args):
        page=int(request.args[0])
    else: 
        page=0
    items_per_page=5
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    pages = db(db.page.created_by==auth.user.id).select(limitby=limitby)
    return dict(pages=pages,page=page,items_per_page=items_per_page)

@auth.requires_login()
def inc_likes():
    nlikes = request.args(1)
    ndish = request.args(0)
    rows=db(db.page.id==ndish).select()
    for row in rows:
        k=row.likes
    else:
        db.likes.insert(Username=auth.user.id, Dish=ndish)
        k=k+1
        db(db.page.id==ndish).update(likes=k)
    return DIV('Likes:', k)

@auth.requires_login()
def dec_likes():
    nlikes = request.args(1)
    ndish = request.args(0)
    rows=db(db.page.id==ndish).select()
    for row in rows:
        k=row.likes
    else:
        db(db.likes.Username==auth.user.id)(db.likes.Dish==ndish).delete()
        k=k-1
        db(db.page.id==ndish).update(likes=k)
    return DIV('Likes:', k)


@auth.requires_login()
def edit():
    """edit an existing wiki page"""
    this_page = db.page(request.args(0,cast=int)) or redirect(URL('index'))
    form = SQLFORM(db.page, this_page)
    if form.process().accepted:
        response.flash="Recipe Updated"
    return dict(form=form)
def user():
    return dict(form=auth())

def download():
    """allows downloading of documents"""
    return response.download(request, db)
def search():
    """an ajax wiki search page"""
    return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
        _onkeyup="ajax('callback', ['keyword'], 'target');")),
        target_div=DIV(_id='target'))
def callback():
    """an ajax callback that returns a <ul> of links to wiki pages"""
    query = db.page.recipe_name.contains(request.vars.keyword)
    pages = db(query).select(orderby=db.page.recipe_name)
    links = [A(p.recipe_name, _href=URL('show',args=p.id)) for p in pages]
    return UL(*links)
