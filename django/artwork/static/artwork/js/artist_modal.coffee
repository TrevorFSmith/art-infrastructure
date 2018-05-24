class @ArtistModal extends React.Component

  dom          = {}
  dom.i        = React.createFactory "i"
  dom.div      = React.createFactory "div"
  dom.label    = React.createFactory "label"
  dom.input    = React.createFactory "input"
  dom.textarea = React.createFactory "textarea"

  displayName: "Edit/New Artist Modal Dialog"

  constructor: (props, context) ->
    super(props, context);
    if @props.artist
      this.state =
        id: @props.artist.id
        name: @props.artist.name
        email: @props.artist.email
        phone: @props.artist.phone
        url: @props.artist.url
        notes: @props.artist.notes
    else
      this.state =
        name: ""
        email: ""
        phone: ""
        url: ""
        notes: ""

  resetForm: =>
    if not @state.id
      @setState
        name: ""
        email: ""
        phone: ""
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

  saveArtist: ->

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    scope = this
    adapter.pushData @action(), csrf_token, @state, ( (data) =>
      # request ok
      $('html').trigger('update-artists', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: ->
    $("[data-object='artist-#{@domNode()}']").modal("hide")

  handleChange: (event) ->
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  title: ->
    if @state.id
      "Edit Artist"
    else
      "Add New Artist"

  componentWillReceiveProps: (nextProps) ->
    if(@props.artist.id != nextProps.artist.id)
      @setState
        id: nextProps.artist.id
        name: nextProps.artist.name
        email: nextProps.artist.email
        phone: nextProps.artist.phone
        url: nextProps.artist.url
        notes: nextProps.artist.notes

      $('html').on "edit-artist-dialog-#{nextProps.artist.id}", (event, scope) =>
        $("[data-object='artist-#{nextProps.artist.id}']").modal("show")

  componentDidMount: ->
    $('html').on "edit-artist-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='artist-#{@domNode()}']").modal("show")

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
            dom.label null, "URL"
            dom.input value: @state.url, onChange: @handleChange.bind(this), name: 'url'

          dom.div className: "field",
            dom.label null, "Notes"
            dom.textarea value: @state.notes, rows: 3, onChange: @handleChange.bind(this), name: 'notes'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveArtist.bind(this)}, "Save"
