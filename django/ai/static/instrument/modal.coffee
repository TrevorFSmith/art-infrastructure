class @EditProjectorModal extends React.Component

  dom     = {}
  dom.i = React.createFactory "i"
  dom.div = React.createFactory "div"
  dom.label = React.createFactory "label"
  dom.input = React.createFactory "input"

  displayName: "Edit Projector Modal Dialog"


  constructor: (props, context) ->
    super(props, context);
    @state =
      name: @props.projector.name


  saveProjector: ->
    console.log(@props)


  closeDialog: ->
    $("[data-object='projector-#{@props.projector.id}']").modal("hide")


  handleChange: (event) ->
    value = $(event.target).prop('value')
    field = $(event.target).prop('name')

    console.log(value)
    console.log($(event).prop("name"))

    # @state.setState
    #   name: "fooooo"


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
            dom.input className: "", value: @state.name, onChange: @handleChange.bind(this), name: 'name'

          dom.div className: "field",
            dom.label null, "Host"
            dom.input className: "", value: @props.projector.pjlink_host, name: 'pjlink_host'

          dom.div className: "field",
            dom.label null, "Port"
            dom.input className: "", value: @props.projector.pjlink_port, name: 'pjlink_port'

          dom.div className: "field",
            dom.label null, "Password"
            dom.input className: "", value: @props.projector.pjlink_password, name: 'pjlink_password'

      dom.div className: "actions",
        dom.div {className: "ui button", onClick: @closeDialog.bind(this)}, "Cancel"
        dom.div {className: "ui button positive", onClick: @saveProjector.bind(this)}, "Save"
