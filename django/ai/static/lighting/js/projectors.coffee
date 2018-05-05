do ->

  "use strict"

  class ProjectorControll extends React.Component

    displayName: "Projector Controll Block"

    constructor: (props) ->
      super(props)

    componentDidMount: ->
      $("div.projector-#{this.props.obj.id}").dropdown()

    sendCommand: (event) ->
      cmd = $(event.target).data('cmd')
      id = $(event.target).data('id')
      alert("Sending cmd #{cmd} to projector with ID #{id}");

    render: ->
      React.createElement("div", {className: "projector-#{this.props.obj.id} ui icon top left pointing dropdown button"},
      React.createElement("i", {className: "wrench icon"}),
      React.createElement("div", {className: "menu"},
        React.createElement("div", {className: "header"}, "Projector Details"),
        React.createElement("div", {
          className: "item",
          "data-cmd": "poweroff",
          "data-id": this.props.obj.id,
          onClick: this.sendCommand,
          }, "Power Off"),
        React.createElement("div", {
          className: "item",
          "data-cmd": "poweron",
          "data-id": this.props.obj.id,
          onClick: this.sendCommand,
          }, "Power On"),
        React.createElement("div", {
          className: "item",
          "data-cmd": "delete",
          "data-id": this.props.obj.id,
          onClick: this.sendCommand,
          }, "Delete"),
        React.createElement("div", {className: "ui divider"}),
        React.createElement("div", {className: "item"}, "Edit"),
        )
      )

  class ProjectorUnitHeader extends React.Component

    displayName: "Projector Header"

    constructor: (props) ->
      super(props)

    render: ->
      React.createElement("div", {
        className: "extra content"
      }, React.createElement("h3", {
        className: "left floated"
      }, React.createElement("i", {className: "ui icon check circle"}),
        React.createElement('span', null, this.props.obj.name)), React.createElement("span", {
        className: "right floated"
      }, React.createElement(ProjectorControll, {obj: this.props.obj}))
      )


  class ProjectorUnitBody extends React.Component

    displayName: "Projector Body"

    constructor: (props) ->
      super(props)

    render: ->
      React.createElement("div", {
        className: "content"
      }, React.createElement("p", {
      }, "Host: #{this.props.obj.pjlink_host} | Port: #{this.props.obj.pjlink_port}")
      )


  class ProjectorUnit extends React.Component

    displayName: "Projector Unit"

    constructor: (props) ->
      super(props)

    render: ->
      React.createElement("div", {
        className: "ui card"
      }, React.createElement(ProjectorUnitHeader, {
        obj: this.props.obj
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
      # console.log("composer mounted")

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
          if data.length > 0
            ReactDOM.render(React.createElement(Composer, {
              collection: data
            }), document.getElementById("root"))
          else
            $("#root").html($("[data-object='no-records']").html())
        , (data, status) =>
          $("#root").html("#{$("[data-object='error']").html()} #{data.statusText}")

  # page etrypoint
  $(document).ready ->
    page = new Visualizer()
    page.visualize()
