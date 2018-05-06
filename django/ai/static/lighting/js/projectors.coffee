do ->

  "use strict"

  class ProjectorCommand extends React.Component

    displayName: "Projector Control Block"

    constructor: (props) ->
      super(props)

    sendCommand: (event) ->
      data       = event.target.dataset
      url        = $("#root").data("url")
      csrf_token = $("#root").data("csrf_token")

      $("[data-object ='projector-#{data.projector_id}']").toggleClass("loading")

      adapter  = new Adapter(url)
      postData =
        id: data.projector_id
        command: data.command

      adapter.pushData csrf_token, postData, ( (data, status) ->
        # request ok
        # console.log(data, status)
      ), ( (data, status) ->
        # request failed
        alert(data.responseJSON.details)
      ), () ->
        # request finished
        $("[data-object='projector-#{data.projector_id}']").toggleClass("loading")

    render: ->
      React.createElement("div", {
        className: "item",
        "data-command": @props.command.command,
        "data-projector_id": @props.projector.id,
        onClick: @sendCommand,
        }, React.createElement("i", {className: "cog icon"}), @props.command.title)


  class ProjectorControl extends React.Component

    displayName: "Projector Control Block"

    constructor: (props) ->
      super(props)
      @state = @state || {}
      @state.commands = @buildCommands();

    buildCommands: ->
      @props.data.projector.commands.map((command) =>
        React.createElement(ProjectorCommand, {
          command: command,
          projector: @props.data.projector,
        })
      )

    componentDidMount: ->
      $("[data-object='projector-#{@props.data.projector.id}']").dropdown()

    removeProjector: (event) ->

      data       = event.target.dataset
      url        = $("#root").data("url")
      csrf_token = $("#root").data("csrf_token")

      $("[data-object ='projector-#{data.projector_id}']").toggleClass("loading")

      adapter  = new Adapter(url)
      postData =
        id: data.projector_id

      adapter.delete csrf_token, postData, ( (data, status) ->
        # request ok
        # console.log(data, status)
      ), ( (data, status) ->
        # request failed
        alert(data.responseJSON.details)
      ), () ->
        # request finished
        $("[data-object='projector-#{data.projector_id}']").toggleClass("loading")

    render: ->
      React.createElement("div", {
        "data-object": "projector-#{@props.data.projector.id}",
        className: "ui icon top left pointing dropdown button"
        },
      React.createElement("i", {className: "wrench icon"}),
      React.createElement("div", {className: "menu"},
        React.createElement("div", {className: "header"}, "Projector Details"), @state.commands,
        React.createElement("div", {className: "ui divider"}),
        React.createElement("div", {className: "item"}, React.createElement("i", {className: "pencil icon"}), "Edit"),
        React.createElement("div", {
          className: "item"
          onClick: @removeProjector
          "data-projector_id": @props.data.projector.id
          }, React.createElement("i", {className: "trash icon"}), "Delete"),
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
        React.createElement('span', null, @props.projector.name)), React.createElement("span", {
        className: "right floated"
      }, React.createElement(ProjectorControl, {
        data: @props,
        }))
      )


  class ProjectorUnitBody extends React.Component

    displayName: "Projector Body"

    constructor: (props) ->
      super(props)

    render: ->
      React.createElement("div", {
        className: "content"
      }, React.createElement("p", {
      }, "Host: #{@props.projector.pjlink_host} | Port: #{@props.projector.pjlink_port}")
      )


  class ProjectorUnit extends React.Component

    displayName: "Projector Unit"

    constructor: (props) ->
      super(props)

    render: ->
      React.createElement("div", {
        className: "ui card"
      }, React.createElement(ProjectorUnitHeader, {
        projector: @props.projector,
      }), React.createElement(ProjectorUnitBody, {
        projector: @props.projector,
      }))


  class Composer extends React.Component

    displayName: "Page Composer"

    constructor: (props) ->
      super(props)
      @state = @state || {}
      @state.projectors = @buildProjectors();

    buildProjectors: ->
      scope = this
      @props.collection.map((projector) =>
        React.createElement(ProjectorUnit, {
          projector: projector,
        })
      )

    render: ->
      React.createElement("div", {
        className: "ui four cards"
      }, @state.projectors)


  class Visualizer

    constructor: () ->
      @placeholder = $("#root")
      @adapter     = new Adapter(@placeholder.data("url"))

    visualize: () =>

      scope = this
      if @placeholder.length

        @adapter.loadData (data) =>
          if data.length > 0
            ReactDOM.render(React.createElement(Composer, {
              collection: data,
            }), document.getElementById("root"))
          else
            $("#root").html($("[data-object='no-records']").html())
        , (data, status) =>
          $("#root").html("#{$("[data-object='error']").html()} #{data.statusText}")

  # page etrypoint
  $(document).ready ->
    page = new Visualizer()
    page.visualize()
