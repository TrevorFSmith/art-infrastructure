class @ArtistModal extends React.Component

  dom          = {}
  dom.i        = React.createFactory "i"
  dom.div      = React.createFactory "div"
  dom.label    = React.createFactory "label"
  dom.input    = React.createFactory "input"
  dom.textarea = React.createFactory "textarea"
  dom.select   = React.createFactory "select"
  dom.option   = React.createFactory "option"

  displayName: "Edit/New Artist Modal Dialog"

  constructor: (props, context) ->
    super(props, context);
    if @props.artist
      this.state =
        id: @props.artist.id
        name: @props.artist.name
        email: @props.artist.email
        phone: @props.artist.phone
        groups: @props.artist.artistgroup_set
        url: @props.artist.url
        notes: @props.artist.notes
        all_groups: []
    else
      this.state =
        name: ""
        email: ""
        phone: ""
        groups: ""
        url: ""
        notes: ""
        all_groups: []

    @promiseGroups().then (results) =>
      @setState
        all_groups: results

  resetForm: =>
    if not @state.id
      @setState
        name: ""
        email: ""
        phone: ""
        groups: ""
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

  promiseGroups: ->
    new Promise (resolve) -> 
      url = $("#root").data("url-groups")
      adapter = new Adapter(url)
      adapter.loadData (data) ->
        resolve(data.results)

  buildGroups: (groups, selected_groups) ->
    options = []
    if groups.length > 0
      groups.map (group) ->
        if _.includes(selected_groups, group.id)
          options.push(dom.option {selected: true, value: group.id}, group.name)
        else
          options.push(dom.option value: group.id, group.name)
    options

  saveArtist: =>

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    data = {
      id: @state.id
      name: @state.name
      email: @state.email
      phone: @state.phone
      artistgroup_set: if @state.groups then @state.groups else []
      url: @state.url
      notes: @state.notes
    }
    scope = this
    adapter.pushData @action(), csrf_token, data, ( (data) =>
      # request ok
      $('html').trigger('update-artists', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: =>
    $("[data-object='artist-#{@domNode()}']").modal("hide")

  handleChange: (event) =>
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  title: ->
    if @state.id
      "Edit Artist"
    else
      "Add New Artist"

  componentDidMount: ->
    $('html').on "edit-artist-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='artist-#{@domNode()}']").modal("show")

  componentWillUnmount: ->
    $("[data-object='artist-#{@domNode()}']").remove()

  render: ->
    dom.div className: "ui modal", 'data-object': "artist-#{@domNode()}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        @title()

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Name"
            dom.input value: @state.name, onChange: @handleChange.bind(this), name: 'name'

          dom.div className: "field",
            dom.label null, "Email"
            dom.input type: "email", value: @state.email, onChange: @handleChange.bind(this), name: 'email'

          dom.div className: "field",
            dom.label null, "Phone"
            dom.input value: @state.phone, onChange: @handleChange.bind(this), name: 'phone'

          dom.div className: "field",
            dom.label null, "Groups"
            dom.select placeholder: "Groups", multiple: "multiple", onChange: @handleChange.bind(this), name: 'groups',
              @buildGroups(@state.all_groups, @state.groups)

          dom.div className: "field",
            dom.label null, "URL"
            dom.input value: @state.url, onChange: @handleChange.bind(this), name: 'url'

          dom.div className: "field",
            dom.label null, "Notes"
            dom.textarea value: @state.notes, rows: 3, onChange: @handleChange.bind(this), name: 'notes'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveArtist.bind(this)}, "Save"
