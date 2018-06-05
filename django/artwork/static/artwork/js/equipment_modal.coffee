class @EquipmentModal extends React.Component

  dom          = {}
  dom.i        = React.createFactory "i"
  dom.div      = React.createFactory "div"
  dom.label    = React.createFactory "label"
  dom.input    = React.createFactory "input"
  dom.textarea = React.createFactory "textarea"
  dom.select   = React.createFactory "select"
  dom.option   = React.createFactory "option"

  displayName: "Edit/New Equipment Modal Dialog"

  constructor: (props, context) ->
    super(props, context)
    if not _.isEmpty(@props.equipment)
      this.state =
        id: @props.equipment.id
        name: @props.equipment.name
        type: @props.equipment.equipment_type
        photos: @props.equipment.photos
        notes: @props.equipment.notes
        all_types: []
        all_photos: []
    else
      this.state =
        name: ""
        type: ""
        photos: ""
        notes: ""
        all_types: []
        all_photos: []

    @promiseTypes().then (results) => 
      @setState
        all_types: results

    @promisePhotos().then (results) => 
      @setState
        all_photos: results

  resetForm: ->
    if not @state.id
      $("[data-object='equipment-new'] option:selected").prop('selected', false)
      @setState
        name: ""
        type: ""
        photos: ""
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

  promiseTypes: ->
    new Promise (resolve) -> 
      url = $("#root").data("url-types")
      adapter = new Adapter(url)
      adapter.loadData (data) ->
        resolve(data)

  promisePhotos: ->
    new Promise (resolve) -> 
      url = $("#root").data("url-photos")
      adapter = new Adapter(url)
      adapter.loadData (data) ->
        resolve(data)

  buildTypes: (types, selected_type) ->
    options = []
    if types.length > 0
      types.map (type) ->
        if selected_type == type.id
          options.push(dom.option {selected: true, value: type.id}, type.name)
        else
          options.push(dom.option value: type.id, type.name)
    options

  buildPhotos: (photos, selected_photos) ->
    options = []
    if photos.length > 0
      photos.map (photo) ->
        if _.includes(selected_photos, photo.id)
          options.push(dom.option {selected: true, value: photo.id}, photo.title)
        else
          options.push(dom.option value: photo.id, photo.title)
    options

  saveEquipment: =>

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    data = {
      id: @state.id
      name: @state.name
      equipment_type: if @state.type then @state.type else @state.all_types[0].id
      photos: if @state.photos then @state.photos else []
      notes: @state.notes
    }
    scope = this
    adapter.pushData @action(), csrf_token, data, ( (data) =>
      # request ok
      $('html').trigger('update-equipments', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: =>
    $("[data-object='equipment-#{@domNode()}']").modal("hide")

  handleChange: (event) =>
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  title: ->
    if @state.id
      "Edit Equipment"
    else
      "Add New Equipment"

  componentDidMount: ->
    $('html').on "edit-equipment-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='equipment-#{@domNode()}']").modal("show")

  componentWillUnmount: ->
    $("[data-object='equipment-#{@domNode()}']").remove()

  render: ->
    dom.div className: "ui modal", 'data-object': "equipment-#{@domNode()}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        @title()

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Name"
            dom.input value: @state.name, onChange: @handleChange.bind(this), name: 'name'

          dom.div className: "field",
            dom.label null, "Types"
            dom.select onChange: @handleChange.bind(this), name: 'type',
              @buildTypes(@state.all_types, @state.type)

          dom.div className: "field",
            dom.label null, "Photos"
            dom.select multiple: "multiple", onChange: @handleChange.bind(this), name: 'photos',
              @buildPhotos(@state.all_photos, @state.photos)

          dom.div className: "field",
            dom.label null, "Notes"
            dom.textarea value: @state.notes, rows: 3, onChange: @handleChange.bind(this), name: 'notes'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveEquipment.bind(this)}, "Save"
