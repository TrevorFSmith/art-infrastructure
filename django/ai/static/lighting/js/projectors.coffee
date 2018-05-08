do ->

  dom = {}

  dom.i    = React.createFactory "i"
  dom.p    = React.createFactory "p"
  dom.h3   = React.createFactory "h3"
  dom.div  = React.createFactory "div"
  dom.span = React.createFactory "span"


  "use strict"

  class ProjectorCommand extends React.Component

    displayName: "Projector Control Block"

    constructor: (props) ->
      super(props)

    sendCommand: (cmd) ->

      url        = $("#root").data("url")
      csrf_token = $("#root").data("csrf_token")
      projector_id = @props.data.projector.id

      $("[data-object ='projector-#{projector_id}']").toggleClass("loading")

      adapter  = new Adapter(url)
      postData =
        id: @props.data.projector.id
        command: cmd

      props = @props
      adapter.pushData csrf_token, postData, ( (data, status) ->
        # request ok
        # console.log(data, status)
      ), ( (data, status) ->
        # request failed
        $('html').trigger('show-dialog', {message: data.responseJSON.details})
      ), () ->
        # request finished
        $("[data-object ='projector-#{projector_id}']").toggleClass("loading")

    render: ->
      dom.div
        className: "item",
        "data-command": @props.command.command,
        onClick: @sendCommand.bind(this, @props.command.command),
      ,
        dom.i {className: "cog icon"}
        @props.command.title


  class ProjectorControl extends React.Component

    displayName: "Projector Control Block"

    constructor: (props) ->
      super(props)
      @state = @state || {}
      @state.commands = @buildCommands()

    buildCommands: ->
      @props.data.projector.commands.map (command) =>
        React.createElement ProjectorCommand, {
          command: command,
          data: @props.data,
        }

    componentDidMount: ->
      $("[data-object='projector-#{@props.data.projector.id}']").dropdown()

    editProjector: (data) ->
      console.log(this)
      console.log(data)
      $('html').trigger('edit-projector-dialog', {message: "Test"})


    removeProjector: (projector_id) ->

      url        = $("#root").data("url")
      csrf_token = $("#root").data("csrf_token")

      $("[data-object ='projector-#{projector_id}']").toggleClass("loading")

      adapter  = new Adapter(url)
      postData =
        id: projector_id

      scope = this
      adapter.delete csrf_token, postData, ( (data, status) ->
        # request ok
      ), ( (data, status) ->
        # request failed
      ), () ->
        # request finished
        $('html').trigger('projector-deleted', scope)
        $("[data-object='projector-#{projector_id}']").toggleClass("loading")

    render: ->
      dom.div
        className: "ui icon top left pointing dropdown button"
        "data-object": "projector-#{@props.data.projector.id}"
      ,
        dom.i {className: "wrench icon"}
      ,
      dom.div {className: "menu"},
        dom.div {className: "header"}, "Projector Details"
        @state.commands
        dom.div {className: "ui divider"}

        dom.div
          className: "item"
          onClick: @editProjector.bind(this, @props.data)
        , "",
          dom.i {className: "pencil icon"}, ""
          "Edit"

        dom.div
          className: "item"
          onClick: @removeProjector.bind(this, @props.data.projector.id)
          "data-projector_id": @props.data.projector.id
        , "",
          dom.i {className: "trash icon"}, ""
          "Delete"


  class ProjectorUnitHeader extends React.Component

    displayName: "Projector Header"

    constructor: (props) ->
      super(props)

    render: ->
      dom.div {className: "extra content"},
        dom.h3 {className: "left floated"},
          dom.i {className: "ui icon check circle"}, ""
          dom.span null, @props.data.projector.name
        dom.span {className: "right floated"},
          React.createElement(ProjectorControl, {data: @props.data})


  class ProjectorUnitBody extends React.Component

    displayName: "Projector Body"

    constructor: (props) ->
      super(props)

    render: ->
      dom.div {className: "content"},
        if @props.data.projector.error
          dom.div {className: "ui red label"}, "Projector error"
        dom.p null, "Host: #{@props.data.projector.pjlink_host} | Port: #{@props.data.projector.pjlink_port}"


  class ProjectorUnit extends React.Component

    displayName: "Projector Unit"

    constructor: (props) ->
      super(props)

    render: ->
      dom.div {className: "ui card"},
        React.createElement(ProjectorUnitHeader, {data: @props})
        React.createElement(ProjectorUnitBody, {data: @props})


  class Composer extends React.Component

    displayName: "Page Composer"

    constructor: (props) ->
      super(props)
      @state = @state || {}
      @state.projectors = @buildProjectors();

    buildProjectors: ->
      scope = this
      @props.collection.map (projector) =>
        React.createElement(ProjectorUnit, {projector: projector})

    componentDidMount: ->
      $('html').on 'projector-deleted', (event, scope) =>
        page = new Visualizer()
        page.visualize()

    render: ->
      dom.div {className: "ui two cards"},
        @state.projectors


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


  $('html').on 'show-dialog', (event, scope) =>
    dialog = $("[data-object='simple-dialog']")
    dialog.find(".content").html(scope.message)
    dialog.modal("show")


  $('html').on 'edit-projector-dialog', (event, scope) =>
    dialog = $("[data-object='edit-dialog']")
    # dialog.find(".content").html(scope.message)
    dialog.modal("show")


  $('html').on 'click', "[data-action='close-dialog']", (event) =>
    $("[data-object='simple-dialog'], [data-object='edit-dialog']").modal("hide")
