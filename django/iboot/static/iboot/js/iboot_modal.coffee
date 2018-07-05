class @IBootModal extends React.Component

  dom       = {}
  dom.i     = React.createFactory "i"
  dom.div   = React.createFactory "div"
  dom.label = React.createFactory "label"
  dom.input = React.createFactory "input"

  displayName: "Edit/New iBoot Modal Dialog"

  constructor: (props, context) ->
    super(props, context)
    if not _.isEmpty(@props.iboot)
      this.state =
        id: @props.iboot.id
        name: @props.iboot.name
        mac_address: @props.iboot.mac_address
        host: @props.iboot.host
        port: @props.iboot.port
    else
      this.state =
        name: ""
        mac_address: ""
        host: ""
        port: ""

  resetForm: =>
    if not @state.id
      @setState
        name: ""
        mac_address: ""
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

  saveIBoot: ->

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    scope = this
    adapter.pushData @action(), csrf_token, @state, ( (data) =>
      # request ok
      $('html').trigger('update-iboots', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: ->
    $("[data-object='iboot-#{@domNode()}']").modal("hide")

  handleChange: (event) ->
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  title: ->
    if @state.id
      "Edit iBoot"
    else
      "Add New iBoot"

  componentDidMount: ->
    $('html').on "edit-iboot-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='iboot-#{@domNode()}']").modal("show")

  componentWillUnmount: ->
    $("[data-object='iboot-#{@domNode()}']").remove()

  render: ->
    dom.div className: "ui modal", 'data-object': "iboot-#{@domNode()}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        @title()

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Name"
            dom.input value: @state.name, onChange: @handleChange.bind(this), name: 'name'

          dom.div className: "field",
            dom.label null, "Mac address"
            dom.input value: @state.mac_address, onChange: @handleChange.bind(this), name: 'mac_address'

          dom.div className: "field",
            dom.label null, "Host"
            dom.input value: @state.host, onChange: @handleChange.bind(this), name: 'host'

          dom.div className: "field",
            dom.label null, "Port"
            dom.input value: @state.port, onChange: @handleChange.bind(this), name: 'port'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveIBoot.bind(this)}, "Save"
