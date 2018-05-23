class @IBootModal extends React.Component

  dom       = {}
  dom.i     = React.createFactory "i"
  dom.div   = React.createFactory "div"
  dom.label = React.createFactory "label"
  dom.input = React.createFactory "input"

  displayName: "Edit/New iBoot Modal Dialog"

  constructor: (props, context) ->
    super(props, context);
    if @props.iboot
      this.state =
        id: @props.iboot.id
        name: @props.iboot.name
        mac_address: @props.iboot.mac_address
        ip: @props.iboot.ip
    else
      this.state =
        name: ""
        mac_address: ""
        ip: ""

  resetForm: =>
    if not @state.id
      @setState
        name: ""
        mac_address: ""
        ip: ""

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

  componentWillReceiveProps: (nextProps) ->
    if(@props.iboot.id != nextProps.iboot.id)
      @setState
        id: nextProps.iboot.id
        name: nextProps.iboot.name
        mac_address: nextProps.iboot.mac_address
        ip: nextProps.iboot.ip

      $('html').on "edit-iboot-dialog-#{nextProps.iboot.id}", (event, scope) =>
        $("[data-object='iboot-#{nextProps.iboot.id}']").modal("show")

  componentDidMount: ->
    $('html').on "edit-iboot-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='iboot-#{@domNode()}']").modal("show")

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
            dom.label null, "IP"
            dom.input value: @state.ip, onChange: @handleChange.bind(this), name: 'ip'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveIBoot.bind(this)}, "Save"
