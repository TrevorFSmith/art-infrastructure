'use strict'

var front = front || {}
front.ui = front.ui || {}

front.ui.IndexPageComponent = class extends k.Component {
	constructor(dataObject=null, options={}){
		super(dataObject, options)

		this.topNav = new base.ui.TopNavComponent()
		this.el.appendChild(this.topNav.el)
	}
}