class @BACNetLightModal extends React.Component

  dom       = {}
  dom.i     = React.createFactory "i"
  dom.div   = React.createFactory "div"
  dom.label = React.createFactory "label"
  dom.input = React.createFactory "input"

  displayName: "Edit/New BACNet Light Modal Dialog"

  constructor: (props, context) ->
    super(props, context);
    if @props.bacnet_light
      @state =
        id: @props.bacnet_light.id
        name: @props.bacnet_light.name
        device_id: @props.bacnet_light.device_id
        property_id: @props.bacnet_light.property_id
    else
      @state =
        name: ""
        device_id: ""
        property_id: ""

  resetForm: =>
    if not @state.id
      @setState
        name: ""
        device_id: ""
        property_id: ""

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

  saveBacNetLight: ->

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    scope = this
    adapter.pushData @action(), csrf_token, @state, ( (data) =>
      # request ok
      $('html').trigger('update-bacnet-lights', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: ->
    $("[data-object='bacnet-light-#{@domNode()}']").modal("hide")

  handleChange: (event) ->
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  title: ->
    if @state.id
      "Edit BACNet Light"
    else
      "Add New BACNet Light"

  componentDidMount: ->
    $('html').on "edit-bacnet-light-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='bacnet-light-#{@domNode()}']").modal("show")

  render: ->
    dom.div className: "ui modal", 'data-object': "bacnet-light-#{@domNode()}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        @title()

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Name"
            dom.input value: @state.name, onChange: @handleChange.bind(this), name: 'name'

          dom.div className: "field",
            dom.label null, "Device ID"
            dom.input value: @state.device_id, onChange: @handleChange.bind(this), name: 'device_id'

          dom.div className: "field",
            dom.label null, "Property ID"
            dom.input value: @state.property_id, onChange: @handleChange.bind(this), name: 'property_id'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveBacNetLight.bind(this)}, "Save"
