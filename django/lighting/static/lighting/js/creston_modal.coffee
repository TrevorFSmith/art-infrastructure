class @CrestonModal extends React.Component

  dom       = {}
  dom.i     = React.createFactory "i"
  dom.div   = React.createFactory "div"
  dom.label = React.createFactory "label"
  dom.input = React.createFactory "input"

  displayName: "Edit/New Creston Modal Dialog"

  constructor: (props, context) ->
    super(props, context);
    if @props.creston
      this.state =
        id: @props.creston.id
        name: @props.creston.name
        host: @props.creston.host
        port: @props.creston.port
    else
      this.state =
        name: ""
        host: ""
        port: ""

  resetForm: =>
    if not @state.id
      @setState
        name: ""
        host: ""
        port: ""

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

  saveCreston: ->

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    scope = this
    adapter.pushData @action(), csrf_token, @state, ( (data) =>
      # request ok
      $('html').trigger('update-crestons', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: ->
    $("[data-object='creston-#{@domNode()}']").modal("hide")

  handleChange: (event) ->
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  title: ->
    if @state.id
      "Edit Creston"
    else
      "Add New Creston"

  componentWillReceiveProps: (nextProps) ->
    if(@props.creston.id != nextProps.creston.id)
      @setState
        id: nextProps.creston.id
        name: nextProps.creston.name
        host: nextProps.creston.host
        port: nextProps.creston.port

      $('html').on "edit-creston-dialog-#{nextProps.creston.id}", (event, scope) =>
        $("[data-object='creston-#{nextProps.creston.id}']").modal("show")

  componentDidMount: ->
    $('html').on "edit-creston-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='creston-#{@domNode()}']").modal("show")

  render: ->
    dom.div className: "ui modal", 'data-object': "creston-#{@domNode()}",

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
            dom.input value: @state.host, onChange: @handleChange.bind(this), name: 'host'

          dom.div className: "field",
            dom.label null, "Port"
            dom.input value: @state.port, onChange: @handleChange.bind(this), name: 'port'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveCreston.bind(this)}, "Save"
