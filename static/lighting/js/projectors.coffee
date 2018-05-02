do ->

  'use strict'

  class Composer extends React.Component

    displayName: 'Composer'

    render: ->
      React.createElement('div', null, "#{this.props.toWhat} mounted.")


  class Visualizer

    constructor: () ->
      @placeholder = $("#root")
      @url         = @placeholder.data('url')
      @adapter     = new Adapter(@placeholder.data('url'))

    visualize: () =>

      if this.placeholder.length

        this.adapter.loadData (data) =>
          ReactDOM.render(React.createElement(Composer, {
            toWhat: data
          }), document.getElementById('root'))
        , (data, status) =>
          $("#root").html($("[data-object='error']").html())
          console.log(data)
          console.log(status)


  $(document).ready ->
    page = new Visualizer()
    page.visualize()
