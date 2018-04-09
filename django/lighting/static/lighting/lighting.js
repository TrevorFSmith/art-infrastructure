'use strict'

var lighting = lighting || {}
lighting.ui = lighting.ui || {}

lighting.ui.IndexPageComponent = class extends k.Component {
	constructor(dataObject=null, options={}){
		super(dataObject, options)
		this.el.addClass('lighting-index-page-component')

		this.topNav = new base.ui.TopNavComponent()
		this.el.appendChild(this.topNav.el)
	}
}

lighting.ui.CrestronPageComponent = class extends k.Component {
	constructor(dataObject=null, options={}){
		super(dataObject, options)
		this.el.addClass('crestron-page-component')

		this.topNav = new base.ui.TopNavComponent()
		this.el.appendChild(this.topNav.el)
	}
}