do ->

  dom = {}

  dom.i      = React.createFactory "i"
  dom.p      = React.createFactory "p"
  dom.h3     = React.createFactory "h3"
  dom.div    = React.createFactory "div"
  dom.span   = React.createFactory "span"
  dom.button = React.createFactory "button"


  "use strict"


  class ProjectorUnitHeader extends React.Component

    displayName: "Projector Header"

    constructor: (props) ->
      super(props)

    render: ->
      dom.div {className: "extra content"},
        dom.h3 {className: "left floated"},
          dom.i {className: "ui icon check circle"}, ""
          dom.span null, @props.data.projector.name


  class ProjectorUnitBody extends React.Component

    displayName: "Projector Body"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editProjector: (data) ->
      $('html').trigger("edit-projector-dialog-#{data.projector.id}", data)

    sendCommand: (cmd) ->

      url        = $("#root").data("url")
      csrf_token = $("#root").data("csrf_token")
      projector_id = @props.data.projector.id

      $("[data-object='command-#{projector_id}-#{cmd}']").toggleClass("loading")

      adapter  = new Adapter(url)
      postData =
        id: projector_id
        command: cmd

      props = @props
      adapter.pushData csrf_token, postData, ( (data, status) ->
        # request ok
      ), ( (data, status) ->
        # request failed
        $('html').trigger('show-dialog', {message: data.responseJSON.details})
      ), () ->
        # request finished
        $("[data-object='command-#{projector_id}-#{cmd}']").toggleClass("loading")


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
      scope = this
      dom.div {className: "content"},

        dom.h3 null, "Host: #{@props.data.projector.pjlink_host} | Port: #{@props.data.projector.pjlink_port}"

        @props.data.projector.commands.map (cmd) ->
          dom.div
            className: "button ui mini"
            "data-object": "command-#{scope.props.data.projector.id}-#{cmd.command}"
            onClick: scope.sendCommand.bind(scope, cmd.command)
          , "",
            dom.i {className: "cog icon"}, ""
            cmd.title

        dom.h3 null, "Last activity:"

        dom.div {className: "ui buttons mini"},
          dom.button
            className: "ui button"
            onClick: @editProjector.bind(this, @props.data)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"

          dom.div {className: "or"}

          dom.button
            className: "ui button negative"
            onClick: @removeProjector.bind(this, @props.data.projector.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"




  class ProjectorUnit extends React.Component

    displayName: "Projector Unit"

    constructor: (props) ->
      super(props)

    render: ->
      dom.div {className: "ui card"},
        React.createElement(ProjectorUnitHeader, {data: @props})
        React.createElement(ProjectorUnitBody, {data: @props})
        React.createElement(EditProjectorModal, {projector: @props.projector})


  class Composer extends React.Component

    displayName: "Page Composer"

    constructor: (props) ->
      super(props)
      @state = @state || {}
      @state.projectors = @buildProjectors();

    buildProjectors: ->
      @props.collection.map (projector) =>
        React.createElement(ProjectorUnit, {projector: projector})

    componentDidMount: ->
      $('html').on 'projector-deleted', (event) =>
        # TODO: implement delete

    render: ->
      dom.div {className: "ui two cards"},
        @state.projectors


  class Visualizer

    constructor: () ->
      @placeholder = $("#root")
      @adapter     = new Adapter(@placeholder.data("url"))

    visualize: () =>

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


  $('html').on 'click', "[data-action='close-dialog']", (event) =>
    $("[data-object='simple-dialog']").modal("hide")
