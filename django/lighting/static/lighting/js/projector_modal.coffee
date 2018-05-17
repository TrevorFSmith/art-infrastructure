class @ProjectorModal extends React.Component

  dom       = {}
  dom.i     = React.createFactory "i"
  dom.div   = React.createFactory "div"
  dom.label = React.createFactory "label"
  dom.input = React.createFactory "input"

  displayName: "Edit/New Projector Modal Dialog"

  constructor: (props, context) ->
    super(props, context);
    if @props.projector
      this.state =
        id: @props.projector.id
        name: @props.projector.name
        pjlink_host: @props.projector.pjlink_host
        pjlink_port: @props.projector.pjlink_port
        pjlink_password: @props.projector.pjlink_password
    else
      this.state =
        name: ""
        pjlink_host: ""
        pjlink_port: ""
        pjlink_password: ""

  resetForm: =>
    if not @state.id
      @setState
        name: ""
        pjlink_host: ""
        pjlink_port: ""
        pjlink_password: ""

  domNode: ->
    if @state.id
      @state.id
    else
      "new"

  action: ->
    if @state.id
      "PUT"
    else
      "POST"

  saveProjector: ->

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    scope = this
    adapter.pushData @action(), csrf_token, @state, ( (data) =>
      # request ok
      $('html').trigger('update-projectors', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: ->
    $("[data-object='projector-#{@domNode()}']").modal("hide")

  handleChange: (event) ->
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  title: ->
    if @state.id
      "Edit Projector"
    else
      "Add New Projector"

  componentDidMount: ->
    $('html').on "edit-projector-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='projector-#{@domNode()}']").modal("show")

  render: ->
    dom.div className: "ui modal", 'data-object': "projector-#{@domNode()}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        @title()

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Name"
            dom.input value: @state.name, onChange: @handleChange.bind(this), name: 'name'

          dom.div className: "field",
            dom.label null, "Host"
            dom.input value: @state.pjlink_host, onChange: @handleChange.bind(this), name: 'pjlink_host'

          dom.div className: "field",
            dom.label null, "Port"
            dom.input value: @state.pjlink_port, onChange: @handleChange.bind(this), name: 'pjlink_port'

          dom.div className: "field",
            dom.label null, "Password"
            dom.input value: @state.pjlink_password, onChange: @handleChange.bind(this), name: 'pjlink_password'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveProjector.bind(this)}, "Save"
