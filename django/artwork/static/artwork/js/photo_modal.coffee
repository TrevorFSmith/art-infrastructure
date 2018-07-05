class @PhotoModal extends React.Component

  dom          = {}
  dom.i        = React.createFactory "i"
  dom.div      = React.createFactory "div"
  dom.label    = React.createFactory "label"
  dom.input    = React.createFactory "input"
  dom.textarea = React.createFactory "textarea"

  displayName: "Edit/New Photo Modal Dialog"

  constructor: (props, context) ->
    super(props, context)
    if not _.isEmpty(@props.photo)
      @state =
        id: @props.photo.id
        title: @props.photo.title
        image: @props.photo.image
        caption: @props.photo.caption
        description: @props.photo.description
    else
      this.state =
        title: ""
        image: ""
        caption: ""
        description: ""

  resetForm: ->
    if not @state.id
      $("[data-object='photo-new'] input[type=file]").attr('type', '').attr('type', 'file')
      @setState
        title: ""
        image: ""
        caption: ""
        description: ""

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

  savePhoto: =>

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)
    formData   = new FormData()
    formData.append("id", @state.id)
    formData.append("title", @state.title)
    formData.append("image", @state.image)
    formData.append("caption", @state.caption)
    formData.append("description", @state.description)
    scope = this
    adapter.uploadData @action(), csrf_token, formData, ( (data) =>
      # request ok
      $('html').trigger('update-photos', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: =>
    $("[data-object='photo-#{@domNode()}']").modal("hide")

  handleChange: (event) =>
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  handleFileChange: (event) =>
    @setState
      "#{$(event.target).prop('name')}": event.target.files[0]

  title: ->
    if @state.id
      "Edit Photo"
    else
      "Add New Photo"

  componentDidMount: ->
    $('html').on "edit-photo-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='photo-#{@domNode()}']").modal("show")

  componentWillUnmount: ->
    $("[data-object='photo-#{@domNode()}']").remove()

  render: ->
    dom.div className: "ui modal", 'data-object': "photo-#{@domNode()}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        @title()

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Title"
            dom.input value: @state.title, onChange: @handleChange.bind(this), name: 'title'

          dom.div className: "field",
            dom.label null, "Image"
            dom.input type: "file", onChange: @handleFileChange.bind(this), name: 'image'

          dom.div className: "field",
            dom.label null, "Caption"
            dom.input value: @state.caption, onChange: @handleChange.bind(this), name: 'caption'

          dom.div className: "field",
            dom.label null, "Description"
            dom.textarea value: @state.description, rows: 3, onChange: @handleChange.bind(this), name: 'description'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @savePhoto.bind(this)}, "Save"
