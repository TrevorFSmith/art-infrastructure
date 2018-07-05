class @DocumentModal extends React.Component

  dom          = {}
  dom.i        = React.createFactory "i"
  dom.div      = React.createFactory "div"
  dom.label    = React.createFactory "label"
  dom.input    = React.createFactory "input"
  dom.textarea = React.createFactory "textarea"

  displayName: "Edit/New Document Modal Dialog"

  constructor: (props, context) ->
    super(props, context)
    if not _.isEmpty(@props.document)
      @state =
        id: @props.document.id
        title: @props.document.title
        doc: @props.document.doc
    else
      this.state =
        title: ""
        doc: ""

  resetForm: ->
    if not @state.id
      $("[data-object='document-new'] input[type=file]").attr('type', '').attr('type', 'file')
      @setState
        title: ""
        doc: ""

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

  saveDocument: =>

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)
    formData   = new FormData()
    formData.append("id", @state.id)
    formData.append("title", @state.title)
    formData.append("doc", @state.doc)
    scope = this
    adapter.uploadData @action(), csrf_token, formData, ( (data) =>
      # request ok
      $('html').trigger('update-documents', data)
      scope.resetForm()
    ), ( (data) ->
      # request failed
      messages = _.map data.responseJSON.details, (value, key) =>
        "#{key} #{value}"
      $('html').trigger('show-dialog', {message: messages.join(" ")})
    )

  closeDialog: =>
    $("[data-object='document-#{@domNode()}']").modal("hide")

  handleChange: (event) =>
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  handleFileChange: (event) =>
    @setState
      "#{$(event.target).prop('name')}": event.target.files[0]

  title: ->
    if @state.id
      "Edit Document"
    else
      "Add New Document"

  componentDidMount: ->
    $('html').on "edit-document-dialog-#{@domNode()}", (event, scope) =>
      $("[data-object='document-#{@domNode()}']").modal("show")

  componentWillUnmount: ->
    $("[data-object='document-#{@domNode()}']").remove()

  render: ->
    dom.div className: "ui modal", 'data-object': "document-#{@domNode()}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        @title()

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Title"
            dom.input value: @state.title, onChange: @handleChange.bind(this), name: 'title'

          dom.div className: "field",
            dom.label null, "Document"
            dom.input type: "file", onChange: @handleFileChange.bind(this), name: 'doc'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveDocument.bind(this)}, "Save"
