class @InstallationModal extends React.Component

  dom          = {}
  dom.i        = React.createFactory "i"
  dom.div      = React.createFactory "div"
  dom.label    = React.createFactory "label"
  dom.input    = React.createFactory "input"
  dom.textarea = React.createFactory "textarea"
  dom.select   = React.createFactory "select"
  dom.option   = React.createFactory "option"

  displayName: "Edit/New Installation Modal Dialog"

  constructor: (props, context) ->
    super(props, context)
    if not _.isEmpty(@props.installation)
      this.state =
        id: @props.installation.id
        name: @props.installation.name
        groups: @props.installation.groups
        artists: @props.installation.artists
        users: @props.installation.user
        site: @props.installation.site
        photos: @props.installation.photos
        documents: @props.installation.documents
        notes: @props.installation.notes
        all_artist_groups: []
        all_artists: []
        all_users: []
        all_sites: []
        all_photos: []
        all_documents: []
    else
      this.state =
        name: ""
        groups: ""
        artists: ""
        users: ""
        site: ""
        photos: ""
        documents: ""
        notes: ""
        all_artist_groups: []
        all_artists: []
        all_users: []
        all_sites: []
        all_photos: []
        all_documents: []

    @promiseObjects("url-artist-groups").then (results) =>
      @setState
        all_artist_groups: results

    @promiseObjects("url-artists").then (results) =>
      @setState
        all_artists: results

    @promiseObjects("url-users").then (results) =>
      @setState
        all_users: results

    @promiseObjects("url-sites").then (results) =>
      @setState
        all_sites: results

    @promiseObjects("url-photos").then (results) =>
      @setState
        all_photos: results

    @promiseObjects("url-documents").then (results) =>
      @setState
        all_documents: results

  resetForm: =>
    if not @state.id
      $("[data-object='installation-new'] option:selected").prop('selected', false)
      @setState
        name: ""
        groups: ""
        artists: ""
        users: ""
        site: ""
        photos: ""
        documents: ""
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

  buildObjectsName: (objects, selected_objects, multiselect=true) ->
    options = []
    if objects.length > 0
      objects.map (object) ->
        if (multiselect and _.includes(selected_objects, object.id)) or (not multiselect and (selected_objects == object.id))
          options.push(dom.option {selected: true, value: object.id}, object.name)
        else
          options.push(dom.option value: object.id, object.name)
    options

  buildObjectsTitle: (objects, selected_objects, multiselect=true) ->
    options = []
    if objects.length > 0
      objects.map (object) ->
        if (multiselect and _.includes(selected_objects, object.id)) or (not multiselect and (selected_objects == object.id))
          options.push(dom.option {selected: true, value: object.id}, object.title)
        else
          options.push(dom.option value: object.id, object.title)
    options

  saveInstallation: =>

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    data = {
      id: @state.id
      name: @state.name
      groups: if @state.groups then @state.groups else []
      artists: if @state.artists then @state.artists else []
      user: if @state.users then @state.users else []
      site: if @state.site then @state.site else @state.all_sites[0].id
      photos: if @state.photos then @state.photos else []
      documents: if @state.documents then @state.documents else []
      notes: @state.notes
    }

    scope = this
    adapter.pushData @action(), csrf_token, data, ( (data) =>
      # request ok
      $('html').trigger('update-installations', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: =>
    $("[data-object='installation-#{@domNode()}']").modal("hide")

  handleChange: (event) =>
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  title: ->
    if @state.id
      "Edit Installation"
    else
      "Add New Installation"

  componentDidMount: ->
    $('html').on "edit-installation-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='installation-#{@domNode()}']").modal("show")

  componentWillUnmount: ->
    $("[data-object='installation-#{@domNode()}']").remove()

  render: ->
    dom.div className: "ui modal", 'data-object': "installation-#{@domNode()}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        @title()

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Name"
            dom.input value: @state.name, onChange: @handleChange.bind(this), name: 'name'

          dom.div className: "field",
            dom.label null, "Sites"
            dom.select onChange: @handleChange.bind(this), name: 'site',
              @buildObjectsName(@state.all_sites, @state.site, false)

          dom.div className: "field",
            dom.label null, "Artist groups"
            dom.select  multiple: "multiple", onChange: @handleChange.bind(this), name: 'groups',
              @buildObjectsName(@state.all_artist_groups, @state.groups)

          dom.div className: "field",
            dom.label null, "Artists"
            dom.select multiple: "multiple", onChange: @handleChange.bind(this), name: 'artists',
              @buildObjectsName(@state.all_artists, @state.artists)

          dom.div className: "field",
            dom.label null, "Users"
            dom.select multiple: "multiple", onChange: @handleChange.bind(this), name: 'users',
              @buildObjectsName(@state.all_users, @state.users)

          dom.div className: "field",
            dom.label null, "Photos"
            dom.select multiple: "multiple", onChange: @handleChange.bind(this), name: 'photos',
              @buildObjectsTitle(@state.all_photos, @state.photos)

          dom.div className: "field",
            dom.label null, "Documents"
            dom.select multiple: "multiple", onChange: @handleChange.bind(this), name: 'documents',
              @buildObjectsTitle(@state.all_documents, @state.documents)

          dom.div className: "field",
            dom.label null, "Notes"
            dom.textarea value: @state.notes, rows: 3, onChange: @handleChange.bind(this), name: 'notes'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveInstallation.bind(this)}, "Save"
