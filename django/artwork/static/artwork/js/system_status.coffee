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

    render: ->
      date_time = @props.installation.created.substr(0, 10) + " " +
                  @props.installation.created.substr(11, 8)

      dom.div {className: "ui card"},
        dom.div {className: "extra content"},
          dom.h3 {className: "left floated"},
            dom.i {className: "ui icon check circle"}, ""
            dom.span null, @props.installation.name

        dom.div {className: "content"},
          dom.div null, "Status"


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
        count: @props.count
        current_page: @getCurrentPage(@props.next, @props.prev)
        next_page: @props.next_page
        prev_page: @props.prev_page
        page_size: @props.page_size

    buildInstallations: ->
      @state.collection.map (installation) =>
        React.createElement(InstallationUnit, {installation: installation, key: installation.id})

    loadInstallations: (url) ->
      adapter = new Adapter(url)
      adapter.loadData (data) =>
        if data.results.length > 0
          @setState
            collection: data.results
            count: data.count
            current_page: @getCurrentPage(data.next, data.previous)
            next_page: data.next
            prev_page: data.previous
            page_size: data.page_size

    getCurrentPage: (next_page, prev_page) ->
      if next_page
        return next_page.substr(next_page.length - 1) - 1
      if prev_page
        if prev_page.indexOf("?page=") != -1
          return +prev_page.substr(prev_page.length - 1) + 1
        else
          return 2
      return 1

    getUrlCurrentPage: ->
      return $('#root').data('url') + "?page=" + @state.current_page

    componentDidMount: ->

      $('html').on 'installation-next-page', (event, data) =>
        @loadInstallations(@state.next_page)

      $('html').on 'installation-prev-page', (event, data) =>
        @loadInstallations(@state.prev_page)

      $('html').on 'installation-current-page', (event, data) =>
        @loadInstallations(@getUrlCurrentPage())

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
        if data.results.length > 0
          ReactDOM.render(React.createElement(Composer, {
            collection: data.results,
            count: data.count,
            next_page: data.next,
            prev_page: data.previous,
            page_size: data.page_size,
          }), document.getElementById("root"))
        else
          ReactDOM.render(React.createElement(Composer, {}), document.getElementById("root"))
      , (data, status) =>
        $("#root").html("#{$("[data-object='error']").html()} #{data.statusText}")


  # page etrypoint
  $(document).ready ->
    page = new Visualizer()
    page.visualize()