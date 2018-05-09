class @EditProjectorModal extends React.Component

  dom     = {}
  dom.i = React.createFactory "i"
  dom.div = React.createFactory "div"
  dom.label = React.createFactory "label"
  dom.input = React.createFactory "input"

  displayName: "Edit Projector Modal Dialog"


  constructor: (props, context) ->
    super(props, context);
    this.state =
      id: @props.projector.id
      name: @props.projector.name
      pjlink_host: @props.projector.pjlink_host
      pjlink_port: @props.projector.pjlink_port
      pjlink_password: @props.projector.pjlink_password


  saveProjector: ->

    url        = $("#root").data("url")
    csrf_token = $("#root").data("csrf_token")
    adapter    = new Adapter(url)

    adapter.pushData csrf_token, @state, ( (data, status) ->
      # request ok
      # noop
    ), ( (data, status) ->
      # request failed
      $('html').trigger('show-dialog', {message: data.responseJSON.details})
    )

  closeDialog: ->
    $("[data-object='projector-#{@props.projector.id}']").modal("hide")

  handleChange: (field, event) ->
    @setState
      "#{$(event.target).prop('name')}": $(event.target).val()

  componentDidMount: ->
    $('html').on "edit-projector-dialog-#{@props.projector.id}", (event, scope) =>
      $("[data-object='projector-#{@props.projector.id}']").modal("show")

  render: ->
    dom.div className: "ui modal", 'data-object': "projector-#{@props.projector.id}",

      dom.div className: "header",
        dom.i className: "pencil icon"
        "Edit Projector"

      dom.div className: "content",
        dom.div className: "ui form",

          dom.div className: "field",
            dom.label null, "Name"
            dom.input value: @state.name, onChange: @handleChange.bind(this, 'name'), name: 'name'

          dom.div className: "field",
            dom.label null, "Host"
            dom.input value: @state.pjlink_host, onChange: @handleChange.bind(this, 'name'), name: 'pjlink_host'

          dom.div className: "field",
            dom.label null, "Port"
            dom.input value: @state.pjlink_port, onChange: @handleChange.bind(this, 'name'), name: 'pjlink_port'

          dom.div className: "field",
            dom.label null, "Password"
            dom.input value: @state.pjlink_password, onChange: @handleChange.bind(this, 'name'), name: 'pjlink_password'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveProjector.bind(this)}, "Save"
