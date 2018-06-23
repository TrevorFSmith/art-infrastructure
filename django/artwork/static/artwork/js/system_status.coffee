do ->

  dom = {}

  dom.i      = React.createFactory "i"
  dom.p      = React.createFactory "p"
  dom.h3     = React.createFactory "h3"
  dom.h2     = React.createFactory "h2"
  dom.div    = React.createFactory "div"
  dom.span   = React.createFactory "span"
  dom.button = React.createFactory "button"
  dom.table  = React.createFactory "table"
  dom.tbody  = React.createFactory "tbody"
  dom.tr     = React.createFactory "tr"
  dom.td     = React.createFactory "td"


  "use strict"


  class InstallationUnit extends React.Component

    displayName: "Installation Unit"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    render: ->
        @props.installation.equipment.map (equipment, i) =>
          class_device = if equipment.device_info.status then "device-active" else "device-inactive"
          icon_device  = if equipment.device_info.status then "check" else "minus"
          dom.tr null,
            if i == 0
              dom.td {rowspan: @props.installation.equipment.length}, 
                @props.installation.name
            dom.td {className: "#{class_device}"},
              dom.i {className: "ui icon circle #{icon_device}"}, ""
              equipment.name
            dom.td null,
             "#{equipment.device_info.type}"
            dom.td null,
             "#{equipment.device_info.name}"


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

      setInterval(=>
        @promiseSystemStatus().then (results) => 
          @setState
            collection: results
      , 30000)

    promiseSystemStatus: ->
      new Promise (resolve) -> 
        url = $("#root").data("url")
        adapter = new Adapter(url)
        adapter.loadData (data) ->
          resolve(data)

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
        dom.table {className: "ui celled structured table"},
          dom.tbody null,
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