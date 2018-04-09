'use strict'

var front = front || {}
front.ui = front.ui || {}

front.ui.IndexPageComponent = class extends k.Component {
	constructor(dataObject=null, options={}){
		super(dataObject, options)
		this.el.addClass('front-index-page-component')

		this.topNav = new base.ui.TopNavComponent()
		this.el.appendChild(this.topNav.el)

		this.topRow = k.el.div({ class: 'row' }).appendTo(this.el)
		this.topCol = k.el.div({ class: 'col-12' }).appendTo(this.topRow)

		this.welcomeEl = k.el.p(`Welcome to the art infrastructure control site.`).appendTo(this.topCol)

		this.linksRow = k.el.div({ class: 'row links-row' }).appendTo(this.el)
		this.linksCol = k.el.div({ class: 'col-12' }).appendTo(this.linksRow)

		this.linksCol.appendChild(k.el.h2(k.el.a({ href: '/heartbeat/' }, 'Heartbeats')))
		this.linksCol.appendChild(k.el.p('Periodic updates from the art'))

		this.linksCol.appendChild(k.el.h2(k.el.a({ href: '/lighting/' }, 'Lighting')))
		this.linksCol.appendChild(k.el.p('Projectors, creston, and bacnet controls'))
	}
}