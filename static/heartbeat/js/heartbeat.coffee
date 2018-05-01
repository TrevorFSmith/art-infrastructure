do ->

  'use strict'

  class Page extends React.Component

    displayName: 'Page'

    render: ->
      React.createElement('div', null, "#{this.props.toWhat} mounted.")


  ReactDOM.render React.createElement(Page, { toWhat: 'React' }, null), document.getElementById('root')
