(function () {

  'use strict';

  var base = base || {}
  base.ui = base.ui || {}
  base.api = base.api || {}

  base.siteName = 'Art Infrastructure'

  base.api.initCurrentUser = function(){

	  // if(localStorage.user){
		//   try  {
		// 	  base.currentUser = new base.api.User(JSON.parse(localStorage.user))
		//   } catch (e) {
		// 	  base.currentUser = new base.api.User()
		//   }
	  // } else {
		//   base.currentUser = new base.api.User()
	  // }
	  // base.currentUser.addListener(() => {
		//   localStorage.user = JSON.stringify(base.currentUser.data);
	  // }, 'reset')

	  // Ask the server for the authed user info
	  // new base.api.CurrentUser().fetch().then(currentUser => {
		//   base.currentUser._new = false
		//   base.currentUser.reset(currentUser.data)
	  // }).catch((...params) => {
		//   base.currentUser._new = false
		//   base.currentUser.reset({})
	  // })
  }

  document.addEventListener('DOMContentLoaded', base.api.initCurrentUser)

  base.getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  base.getCSRFToken = function(){ return base.getCookie('csrftoken') }

}());

$(function(){
  $('.ui.dropdown').dropdown();
});