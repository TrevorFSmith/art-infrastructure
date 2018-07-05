class @InstallationSiteModal extends React.Component

  dom          = {}
  dom.i        = React.createFactory "i"
  dom.div      = React.createFactory "div"
  dom.label    = React.createFactory "label"
  dom.input    = React.createFactory "input"
  dom.textarea = React.createFactory "textarea"
  dom.select   = React.createFactory "select"
  dom.option   = React.createFactory "option"

  displayName: "Edit/New Installation Site Modal Dialog"

  constructor: (props, context) ->
    super(props, context)
    if not _.isEmpty(@props.installation_site)
      this.state =
        id: @props.installation_site.id
        name: @props.installation_site.name
        location: @props.installation_site.location
        photos: @props.installation_site.photos
        equipment: @props.installation_site.equipment
        notes: @props.installation_site.notes
        all_photos: []
        all_equipment: []
    else
      this.state =
        name: ""
        location: ""
        photos: ""
        equipment: ""
        notes: ""
        all_photos: []
        all_equipment: []

    @promiseObjects("url-photos").then (results) =>
      @setState
        all_photos: results

    @promiseObjects("url-equipment").then (results) =>
      @setState
        all_equipment: results

  resetForm: =>
    if not @state.id
      $("[data-object='installation-site-new'] option:selected").prop('selected', false)
      @setState
        name: ""
        location: ""
        photos: ""
        equipment: ""
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

  promiseObjects: (url) ->
    new Promise (resolve) -> 
      url = $("#root").data(url)
      adapter = new Adapter(url)
      adapter.loadData (data) ->
        resolve(data)

  buildPhotos: (photos, selected_photos) ->
    options = []
    if photos.length > 0
      photos.map (photo) ->
        if _.includes(selected_photos, photo.id)
          options.push(dom.option {selected: true, value: photo.id}, photo.title)
        else
          options.push(dom.option value: photo.id, photo.title)
    options

  buildEquipment: (equipment, selected_equipment) ->
    options = []
    if equipment.length > 0
      equipment.map (e) ->
        if _.includes(selected_equipment, e.id)
          options.push(dom.option {selected: true, value: e.id}, e.name)
        else
          options.push(dom.option value: e.id, e.name)
    options

  saveInstallationSite: =>

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    data = {
      id: @state.id
      name: @state.name
      location: @state.location
      photos: if @state.photos then @state.photos else []
      equipment: if @state.equipment then @state.equipment else []
      notes: @state.notes
    }
    scope = this
    adapter.pushData @action(), csrf_token, data, ( (data) =>
      # request ok
      $('html').trigger('update-installation-sites', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: =>
    $("[data-object='installation-site-#{@domNode()}']").modal("hide")

  handleChange: (event) =>
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  title: ->
    if @state.id
      "Edit Installation Site"
    else
      "Add New Installation Site"

  componentDidMount: ->
    $('html').on "edit-installation-site-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='installation-site-#{@domNode()}']").modal("show")

  componentWillUnmount: ->
    $("[data-object='installation-site-#{@domNode()}']").remove()

  render: ->
    dom.div className: "ui modal", 'data-object': "installation-site-#{@domNode()}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        @title()

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Name"
            dom.input value: @state.name, onChange: @handleChange.bind(this), name: 'name'

          dom.div className: "field",
            dom.label null, "Location"
            dom.input value: @state.location, onChange: @handleChange.bind(this), name: 'location'

          dom.div className: "field",
            dom.label null, "Photos"
            dom.select placeholder: "Photos", multiple: "multiple", onChange: @handleChange.bind(this), name: 'photos',
              @buildPhotos(@state.all_photos, @state.photos)

          dom.div className: "field",
            dom.label null, "Equipment"
            dom.select placeholder: "Equipment", multiple: "multiple", onChange: @handleChange.bind(this), name: 'equipment',
              @buildEquipment(@state.all_equipment, @state.equipment)

          dom.div className: "field",
            dom.label null, "Notes"
            dom.textarea value: @state.notes, rows: 3, onChange: @handleChange.bind(this), name: 'notes'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveInstallationSite.bind(this)}, "Save"
