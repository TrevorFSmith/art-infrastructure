2class @EquipmentTypeModal extends React.Component

  dom       = {}
  dom.i     = React.createFactory "i"
  dom.div   = React.createFactory "div"
  dom.label = React.createFactory "label"
  dom.input = React.createFactory "input"

  displayName: "Edit/New Equipment Type Modal Dialog"

  constructor: (props, context) ->
    super(props, context);
    if @props.equipment_type
      @state =
        id: @props.equipment_type.id
        name: @props.equipment_type.name
        provider: @props.equipment_type.provider
        url: @props.equipment_type.url
        notes: @props.equipment_type.notes
    else
      @state =
        name: ""
        provider: ""
        url: ""
        notes: ""

  resetForm: ->
    if not @state.id
      @setState
        name: ""
        provider: ""
        url: ""
        notes: ""

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

  saveEquipmentType: =>

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    scope = this
    adapter.pushData @action(), csrf_token, @state, ( (data) =>
      # request ok
      $('html').trigger('update-equipment-types', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: =>
    $("[data-object='equipment-type-#{@domNode()}']").modal("hide")

  handleChange: (event) =>
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  title: ->
    if @state.id
      "Edit Equipment Type"
    else
      "Add New Equipment Type"

  componentDidMount: ->
    $('html').on "edit-equipment-type-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='equipment-type-#{@domNode()}']").modal("show")

  componentWillUnmount: ->
    $("[data-object='equipment-type-#{@domNode()}']").remove()

  render: ->
    dom.div className: "ui modal", 'data-object': "equipment-type-#{@domNode()}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        @title()

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Name"
            dom.input value: @state.name, onChange: @handleChange.bind(this), name: 'name'

          dom.div className: "field",
            dom.label null, "Provider"
            dom.input value: @state.provider, onChange: @handleChange.bind(this), name: 'provider'

          dom.div className: "field",
            dom.label null, "URL"
            dom.input value: @state.url, onChange: @handleChange.bind(this), name: 'url'

          dom.div className: "field",
            dom.label null, "Notes"
            dom.input value: @state.notes, onChange: @handleChange.bind(this), name: 'notes'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveEquipmentType.bind(this)}, "Save"
