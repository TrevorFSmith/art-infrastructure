'use strict'

var base = base || {}
base.ui = base.ui || {}
base.api = base.api || {}

base.siteName = 'Art Infrastructure' 

base.api.version = '0_1'
base.api.baseURL = '/api/' + base.api.version + '/'

base.api.User = class extends k.DataModel {
	get url(){
		if(typeof this.get('id') === 'undefined'){
			return base.api.baseURL + 'user'
		}
		return base.api.baseURL + 'user' + '/' + this.get('id')
	}
}

base.api.CurrentUser = class extends k.DataModel {
	get url(){
		return base.api.baseURL + 'current-user'
	}
}

base.api.initCurrentUser = function(){
	if(localStorage.user){
		try  {
			base.currentUser = new base.api.User(JSON.parse(localStorage.user))
		} catch (e) {
			base.currentUser = new base.api.User()
		}
	} else {
		base.currentUser = new base.api.User()
	}
	base.currentUser.addListener(() => {
		localStorage.user = JSON.stringify(base.currentUser.data);
	}, 'reset')

	// Ask the server for the authed user info
	new base.api.CurrentUser().fetch().then(currentUser => {
		base.currentUser._new = false
		base.currentUser.reset(currentUser.data)
	}).catch((...params) => {
		base.currentUser._new = false
		base.currentUser.reset({})
	})
}
document.addEventListener('DOMContentLoaded', base.api.initCurrentUser)

/*
TopNavComponent renders the top navigation links as well as login/out links.
*/
base.ui.TopNavComponent = class extends k.Component {
	constructor(dataObject=null, options={}){
		super(dataObject, options)
		this.el.addClass('top-nav-component')
		this.nav = k.el.nav().appendTo(this.el)
		this.siteName = k.el.a(
			{ href: '/' },
			k.el.h1(base.siteName)
		).appendTo(this.nav)

		this.rightLinks = k.el.ul({ class: 'right-links'}).appendTo(this.nav)

		if(base.currentUser.isNew){
			base.currentUser.addListener(this.updateLinks.bind(this), 'reset', true)
		} else {
			this.updateLinks()
		}

	}
	updateLinks(){
		if(base.currentUser.get('staff') === true) {
			this._addStaffLinks()
		}
		if(base.currentUser.get('id') !== null){
			this._addAuthedLinks()
		} else {
			this._addUnauthedLinks()
		}
	}
	_addAuthedLinks(){
		this.addLink('/admin/logout/', 'logout', 'logout-nav')
	}
	_addUnauthedLinks(){
		this.addLink('/admin/login/', 'login', 'login-nav')
	}
	_addStaffLinks(){
		this.addLink('/admin/', 'admin', 'admin-nav')
	}
	addLink(href, anchorText, className) {
		this.rightLinks.append(k.el.li(k.el.a({ 'href': href, 'class': className }, anchorText )))
	}
}