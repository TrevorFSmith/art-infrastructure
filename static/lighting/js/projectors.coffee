do ->

  "use strict"

  class ProjectorUnitHeader extends React.Component

    displayName: "Projector Header"

    constructor: (props) ->
      super(props)

    render: ->
      React.createElement("div", {
        className: "extra content"
      }, React.createElement("span", {
        className: "left floated"
      }, "left"), React.createElement("span", {
        className: "right floated"
      }, "right")
      )


  class ProjectorUnitBody extends React.Component

    displayName: "Projector Body"

    constructor: (props) ->
      super(props)

    render: ->
      React.createElement("div", {
        className: "content"
      }, React.createElement("p", {
        # no props
      }, this.props.obj.name)
      )


  class ProjectorUnit extends React.Component

    displayName: "Projector Unit"

    constructor: (props) ->
      super(props)

    render: ->
      React.createElement("div", {
        className: "ui card"
      }, React.createElement(ProjectorUnitHeader, {
        # no props
      }), React.createElement(ProjectorUnitBody, {
        obj: this.props.obj
      }))


  class Composer extends React.Component

    displayName: "Page Composer"

    constructor: (props) ->
      super(props)
      this.state = this.state || {}
      this.state.projectors = this.buildProjectors();

    buildProjectors: ->
      this.props.collection.map((projector) =>
        React.createElement(ProjectorUnit, {
          obj: projector
        })
      )

    componentDidMount: ->
      console.log("composer mounted")

    render: ->
      React.createElement("div", {
        className: "ui four cards"
      }, this.state.projectors)


  class Visualizer

    constructor: () ->
      @placeholder = $("#root")
      @url         = @placeholder.data("url")
      @adapter     = new Adapter(this.url)

    visualize: () =>

      if this.placeholder.length

        this.adapter.loadData (data) =>
          ReactDOM.render(React.createElement(Composer, {
            collection: data
          }), document.getElementById("root"))
        , (data, status) =>
          $("#root").html($("[data-object='error']").html())
          console.log(data)
          console.log(status)

  # page etrypoint
  $(document).ready ->
    page = new Visualizer()
    page.visualize()
