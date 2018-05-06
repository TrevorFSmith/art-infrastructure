class @SimpleModal extends React.Component

  displayName: "OK Modal Dialog"

  constructor: (url, onClick) ->
    @url = url
    @onClick = onClick


  constructor: (props) ->
    super(props)

  action: ->
    if @onClick
      @onClick()
    else
      console.log("foo")

  componentDidMount: ->
    $("[data-object='projector-#{@props.data.projector.id}']").dropdown()

  render: ->
    React.createElement("div", {className: "ui modal"},
      React.createElement("div", {className: "header"}, "Text"),
      React.createElement("div", {className: "content"}, "Message Details")
      React.createElement("div", {className: "actions"}, React.createElement("div", {
        className: "ui button"
        onClick: @action,
        }, "OK"))
    )


  # <div class="ui modal" data-object="simple-modal">
  #   <div class="header">
  #     {{title}}
  #   </div>
  #   <div class="content">
  #     {{content}}
  #   </div>
  #   <div class="actions">
  #     <div class="ui button">OK</div>
  #   </div>
  # </div>
