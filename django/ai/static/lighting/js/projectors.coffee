do ->

  "use strict"

  class ProjectorCommand extends React.Component

    displayName: "Projector Control Block"

    constructor: (props) ->
      super(props)

    sendCommand: (event) ->
      cmd = $(event.target).data('cmd')
      id = $(event.target).data('id')
      alert("Sending cmd #{cmd} to projector with ID #{id}");

    render: ->
      React.createElement("div", {
        className: "item",
        "data-cmd": this.props.command.command,
        "data-id": this.props.projector.id,
        onClick: this.sendCommand,
        }, this.props.command.title)


  class ProjectorControll extends React.Component

    displayName: "Projector Controll Block"

    constructor: (props) ->
      super(props)
      this.state = this.state || {}
      this.state.commands = this.buildCommands();

    buildCommands: ->
      this.props.projector.commands.map((command) =>
        React.createElement(ProjectorCommand, {
          command: command,
          projector: this.props.projector
        })
      )

    componentDidMount: ->
      $("div.projector-#{this.props.projector.id}").dropdown()

    render: ->
      React.createElement("div", {className: "projector-#{this.props.projector.id} ui icon top left pointing dropdown button"},
      React.createElement("i", {className: "wrench icon"}),
      React.createElement("div", {className: "menu"},
        React.createElement("div", {className: "header"}, "Projector Details"), this.state.commands,
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
        React.createElement('span', null, this.props.projector.name)), React.createElement("span", {
        className: "right floated"
      }, React.createElement(ProjectorControll, {projector: this.props.projector}))
      )


  class ProjectorUnitBody extends React.Component

    displayName: "Projector Body"

    constructor: (props) ->
      super(props)

    render: ->
      React.createElement("div", {
        className: "content"
      }, React.createElement("p", {
      }, "Host: #{this.props.projector.pjlink_host} | Port: #{this.props.projector.pjlink_port}")
      )


  class ProjectorUnit extends React.Component

    displayName: "Projector Unit"

    constructor: (props) ->
      super(props)

    render: ->
      React.createElement("div", {
        className: "ui card"
      }, React.createElement(ProjectorUnitHeader, {
        projector: this.props.projector
      }), React.createElement(ProjectorUnitBody, {
        projector: this.props.projector
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
          projector: projector
        })
      )

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
