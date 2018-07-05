class @ArtistGroupModal extends React.Component

  dom          = {}
  dom.i        = React.createFactory "i"
  dom.div      = React.createFactory "div"
  dom.label    = React.createFactory "label"
  dom.input    = React.createFactory "input"
  dom.select   = React.createFactory "select"
  dom.option   = React.createFactory "option"

  displayName: "Edit/New Artist Group Modal Dialog"

  constructor: (props, context) ->
    super(props, context)
    if not _.isEmpty(@props.artist_group)
      @state =
        id: @props.artist_group.id
        name: @props.artist_group.name
        artists: @props.artist_group.artists
        url: @props.artist_group.url
        all_artists: []
    else
      @state =
        name: ""
        artists: []
        url: ""
        all_artists: []

    @promiseArtists().then (results) => 
      @setState
        all_artists: results

  resetForm: ->
    if not @state.id
      $("[data-object='artist-group-new'] option:selected").prop('selected', false)
      @setState
        name: ""
        artists: []
        url: ""

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

  promiseArtists: ->
    new Promise (resolve) -> 
      url = $("#root").data("url-artists")
      adapter = new Adapter(url)
      adapter.loadData (data) ->
        resolve(data)

  buildArtists: (artists, selected_artists) ->
    options = []
    if artists.length > 0
      artists.map (artist) ->
        if _.includes(selected_artists, artist.id)
          options.push(dom.option {selected: true, value: artist.id}, artist.name)
        else
          options.push(dom.option value: artist.id, artist.name)
    options

  saveArtistGroup: =>

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    data = {
      id: @state.id
      name: @state.name
      artists: if @state.artists then @state.artists else []
      url: @state.url
    }
    scope = this
    adapter.pushData @action(), csrf_token, data, ( (data) =>
      # request ok
      $('html').trigger('update-artist-groups', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: =>
    $("[data-object='artist-group-#{@domNode()}']").modal("hide")

  handleChange: (event) =>
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  title: ->
    if @state.id
      "Edit Artist Group"
    else
      "Add New Artist Group"

  componentDidMount: ->
    $('html').on "edit-artist-group-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='artist-group-#{@domNode()}']").modal("show")

  componentWillUnmount: ->
    $("[data-object='artist=group-#{@domNode()}']").remove()

  render: ->
    dom.div className: "ui modal", 'data-object': "artist-group-#{@domNode()}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        @title()

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Name"
            dom.input value: @state.name, onChange: @handleChange.bind(this), name: 'name'

          dom.div className: "field",
            dom.label null, "Artists"
            dom.select placeholder: "Artists", multiple: "multiple", onChange: @handleChange.bind(this), name: 'artists',
              @buildArtists(@state.all_artists, @state.artists)

          dom.div className: "field",
            dom.label null, "URL"
            dom.input value: @state.url, onChange: @handleChange.bind(this), name: 'url'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveArtistGroup.bind(this)}, "Save"
