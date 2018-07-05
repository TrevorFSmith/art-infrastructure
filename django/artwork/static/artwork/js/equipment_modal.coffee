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
        device_type: @props.equipment.device_type
        device_id: @props.equipment.device_id
        all_types: []
        all_photos: []
        all_device_types: []
        all_devices: []
        all_device_bacnet_lights: []
        all_device_projectors: []
        all_device_crestons: []
        all_device_iboots: []
    else
      this.state =
        name: ""
        type: ""
        photos: ""
        notes: ""
        device_type: ""
        device_id: ""
        all_types: []
        all_photos: []
        all_devices: []
        all_device_types: []
        all_device_bacnet_lights: []
        all_device_projectors: []
        all_device_crestons: []
        all_device_iboots: []

    @promiseObjects("url-types").then (results) =>
      @setState
        all_types: results

    @promiseObjects("url-photos").then (results) =>
      @setState
        all_photos: results

    @promiseObjects("url-device-types").then (results) =>
      @setState
        all_device_types: results

    @promiseObjects("url-device-bacnet-lights").then (results) =>
      @setState
        all_device_bacnet_lights: results
      @setDevices('BACNetLight', results)

    @promiseObjects("url-device-projectors").then (results) =>
      @setState
        all_device_projectors: results
      @setDevices('Projector', results)

    @promiseObjects("url-device-crestons").then (results) =>
      @setState
        all_device_crestons: results
      @setDevices('Creston', results)

    @promiseObjects("url-device-iboots").then (results) =>
      @setState
        all_device_iboots: results
      @setDevices('IBoot', results)

  resetForm: ->
    if not @state.id
      $("[data-object='equipment-new'] option:selected").prop('selected', false)
      @setState
        name: ""
        type: ""
        photos: ""
        notes: ""
        device_type: ""
        device_id: ""
        all_devices: []

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

  promiseObjects: (url) ->
    new Promise (resolve) -> 
      url = $("#root").data(url)
      adapter = new Adapter(url)
      adapter.loadData (data) ->
        resolve(data)

  buildObjects: (objects, selected_object) ->
    options = []
    if objects and objects.length > 0
      objects.map (object) ->
        if selected_object == object.id
          options.push(dom.option {selected: true, value: object.id}, object.name)
        else
          options.push(dom.option value: object.id, object.name)
    options

  buildPhotos: (photos, selected_photos) ->
    options = []
    if photos and photos.length > 0
      photos.map (photo) ->
        if _.includes(selected_photos, photo.id)
          options.push(dom.option {selected: true, value: photo.id}, photo.title)
        else
          options.push(dom.option value: photo.id, photo.title)
    options

  setDevices: (type, devices) =>
    if (@state.all_devices.length == 0) and (@state.device_type)
      @state.all_device_types.map (device_type) =>
        if (device_type.name == type) and (device_type.id == @state.device_type)
          @setState
            all_devices: devices

  saveEquipment: =>

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    device_id = ""
    if @state.device_id
      device_id = @state.device_id
    else if @state.device_type
      device_id = @state.all_devices[0].id

    data = {
      id: @state.id
      name: @state.name
      equipment_type: if @state.type then @state.type else @state.all_types[0].id
      photos: if @state.photos then @state.photos else []
      notes: @state.notes
      device_type: @state.device_type
      device_id: device_id
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

  handleChangeDeviceType: (event) =>
    device_type_id = $(event.target).val()
    devices = []
    @state.all_device_types.map (device_type) =>
      if device_type.id == +device_type_id
        switch(device_type.name)
          when "BACNetLight" then devices = @state.all_device_bacnet_lights
          when "Projector" then devices = @state.all_device_projectors
          when "Creston" then devices = @state.all_device_crestons
          when "IBoot" then devices = @state.all_device_iboots

    $("[data-object='equipment-new'] [name='device_id'] option:selected").prop('selected', false)
    @setState
      device_type: device_type_id
      device_id: ""
      all_devices: devices

  handleClickDeviceType: (event) =>
    option = $(event.target).find('option')[0]
    $(option).attr('hidden', true)

  handleResetDeviceType: (event) =>
    option = $(event.target).find('option')[0]
    $(option).attr('hidden', false)

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
              @buildObjects(@state.all_types, @state.type)

          dom.div className: "field",
            dom.label null, "Device types"
            dom.select {
              onChange: @handleChangeDeviceType.bind(this),
              onFocus: @handleClickDeviceType.bind(this),
              onBlur: @handleResetDeviceType.bind(this),
              name: 'device_type'},
              dom.option null, "Select device type..."
              @buildObjects(@state.all_device_types, @state.device_type)

          dom.div className: "field",
            dom.label null, "Devices"
            dom.select onChange: @handleChange.bind(this), name: 'device_id',
              @buildObjects(@state.all_devices, @state.device_id)

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
