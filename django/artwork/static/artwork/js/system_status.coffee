do ->

  dom = {}

  dom.i      = React.createFactory "i"
  dom.p      = React.createFactory "p"
  dom.h3     = React.createFactory "h3"
  dom.h2     = React.createFactory "h2"
  dom.div    = React.createFactory "div"
  dom.span   = React.createFactory "span"
  dom.button = React.createFactory "button"


  "use strict"


  class InstallationUnit extends React.Component

    displayName: "Installation Unit"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    handleActiveChange: (event) =>
      if $(event.target).hasClass("device-inactive")
        $(event.target).removeClass("device-inactive").addClass("device-active")
        $(event.target).find('i').removeClass("minus").addClass("check")
      else
        $(event.target).removeClass("device-active").addClass("device-inactive")
        $(event.target).find('i').removeClass("check").addClass("minus")

    render: ->
      dom.div {className: "ui card"},
        dom.div {className: "extra content"},
          dom.h3 {className: "left floated"},
            dom.i {className: "ui icon check circle"}, ""
            dom.span null, @props.installation.name

        dom.div {className: "content"},
          dom.h3 {className: "center aligned"}, "Location: #{@props.installation.location_name}"
          dom.div {className: "ui cards centered"},
            @props.installation.equipment.map (equipment) =>
              dom.div {className: "ui card"},
                dom.div {className: "extra content device-inactive", onClick: @handleActiveChange.bind(this)},
                  dom.h3 {className: "left floated"},
                    dom.i {className: "ui icon minus circle"}, ""
                    dom.span null, equipment.name
                dom.div {className: "content"},
                  dom.div null, "Device type: #{equipment.device_type_name}"
                  dom.div null, "Device name: #{equipment.device_name}"

  class InstallationNoRecords extends React.Component

    displayName: "Installation no records"

    constructor: (props) ->
      super(props)

    render: ->
      if @props.output
        dom.h3 null, "No records found."
      else
        dom.h3 null, ""


  class InstallationPagination extends React.Component

    displayName: "Installation pagination"

    constructor: (props) ->
      super(props)

    clickNextPage: ->
      $('html').trigger("installation-next-page")

    clickPrevPage: ->
      $('html').trigger("installation-prev-page")

    render: ->
      if @props.pages
        dom.div {className: "ui center aligned segment"},
          if @props.prev
            dom.button {className: "ui button margin-right", onClick: @clickPrevPage}, "Prev"
          dom.span {className: "margin-right"}, "Page #{@props.page} of #{@props.pages}"
          if @props.next
            dom.button {className: "ui button", onClick: @clickNextPage}, "Next"
      else
        dom.div null, ""


  class Composer extends React.Component

    displayName: "Page Composer"

    constructor: (props) ->
      super(props)
      collection = @props.collection || []
      @state =
        collection: collection
        no_records: if collection.length > 0 then false else true

    buildInstallations: ->
      @state.collection.map (installation) =>
        React.createElement(InstallationUnit, {installation: installation, key: installation.id})

    componentDidMount: ->

    newInstallation: ->
      $('html').trigger("edit-installation-dialog-new")

    render: ->
      dom.div null,
        dom.h2 className: "ui dividing header",
          "System Status"
        dom.div {className: "ui one cards"},
          @buildInstallations()
        React.createElement(InstallationNoRecords, {output: @state.no_records})
        React.createElement(InstallationPagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / @state.page_size),
          next: @state.next_page, prev: @state.prev_page})


  class Visualizer

    constructor: () ->
      @placeholder = $("#root")
      @adapter     = new Adapter(@placeholder.data("url"))

    visualize: () =>

      if @placeholder.length
        @render()

    render: ->
      @adapter.loadData (data) =>
        if data.length > 0
          ReactDOM.render(React.createElement(Composer, {
            collection: data,
          }), document.getElementById("root"))
        else
          ReactDOM.render(React.createElement(Composer, {}), document.getElementById("root"))
      , (data, status) =>
        $("#root").html("#{$("[data-object='error']").html()} #{data.statusText}")


  # page etrypoint
  $(document).ready ->
    page = new Visualizer()
    page.visualize()