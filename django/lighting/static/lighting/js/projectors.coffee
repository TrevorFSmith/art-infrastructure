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


  class ProjectorUnitHeader extends React.Component

    displayName: "Projector Header"

    constructor: (props) ->
      super(props)

    render: ->
      dom.div {className: "extra content"},
        dom.h3 {className: "left floated"},
          dom.i {className: "ui icon check circle"}, ""
          dom.span null, @props.data.projector.name


  class ProjectorUnitBody extends React.Component

    displayName: "Projector Body"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editProjector: (data) ->
      $('html').trigger("edit-projector-dialog-#{data.projector.id}", data)

    sendCommand: (cmd) ->

      url        = $("#root").data("command-url")
      csrf_token = $("#root").data("csrf_token")
      projector_id = @props.data.projector.id

      $("[data-object='command-#{projector_id}-#{cmd}']").toggleClass("loading")

      adapter  = new Adapter(url)
      postData =
        id: projector_id
        command: cmd

      props = @props
      adapter.pushData "PUT", csrf_token, postData, ( (data) ->
        # request ok
        $('html').trigger('show-dialog', {message: data.details})
      ), ( (data, status) ->
        # request failed
        $('html').trigger('show-dialog', {message: data.responseJSON.details})
      ), () ->
        # request finished
        $("[data-object='command-#{projector_id}-#{cmd}']").toggleClass("loading")


    removeProjector: (projector_id) ->

      if confirm "Are you sure?"

        url        = $("#root").data("url")
        csrf_token = $("#root").data("csrf_token")

        $("[data-object ='projector-#{projector_id}']").toggleClass("loading")

        adapter  = new Adapter(url)
        postData =
          id: projector_id

        scope = this
        adapter.delete csrf_token, postData, ( (data, status) ->
          # request ok
          $('html').trigger('projector-deleted', data)
        ), ( (data, status) ->
          # request failed
        ), () ->
          # request finished
          $("[data-object='projector-#{projector_id}']").toggleClass("loading")


    render: ->
      scope = this
      dom.div {className: "content"},

        dom.h3 null, "Host: #{@props.data.projector.pjlink_host} | Port: #{@props.data.projector.pjlink_port}"

        @props.data.projector.commands.map (cmd) ->
          dom.div
            className: "button ui mini"
            "data-object": "command-#{scope.props.data.projector.id}-#{cmd.command}"
            onClick: scope.sendCommand.bind(scope, cmd.command)
          , "",
            dom.i {className: "cog icon"}, ""
            cmd.title

        dom.h3 null, ""

        dom.div {className: "ui buttons mini"},
          dom.button
            className: "ui button"
            onClick: @editProjector.bind(this, @props.data)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"

          dom.div {className: "or"}

          dom.button
            className: "ui button negative"
            onClick: @removeProjector.bind(this, @props.data.projector.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"

        React.createElement(ProjectorModal, {projector: @props.data.projector})


  class ProjectorUnit extends React.Component

    displayName: "Projector Unit"

    constructor: (props) ->
      super(props)

    render: ->
        dom.div {className: "ui card"},
          React.createElement(ProjectorUnitHeader, {data: @props})
          React.createElement(ProjectorUnitBody, {data: @props})


  class ProjectorNoRecords extends React.Component

    displayName: "Projector no records"

    constructor: (props) ->
      super(props)

    render: ->
      if @props.output
        dom.h3 {className: ""}, "No records found."
      else
        dom.h3 {className: ""}, ""


  class ProjectorPagination extends React.Component

    displayName: "Projector pagination"

    constructor: (props) ->
      super(props)

    clickNextPage: ->
      $('html').trigger("projector-next-page")

    clickPrevPage: ->
      $('html').trigger("projector-prev-page")

    render: ->
      dom.div {className: "ui center aligned segment"},
        if @props.prev
          dom.button {className: "ui button margin-right", onClick: @clickPrevPage.bind(this)}, "Prev"
        dom.span {className: "margin-right"}, "#{@props.page}(#{@props.pages})"
        if @props.next
          dom.button {className: "ui button", onClick: @clickNextPage.bind(this)}, "Next"


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
        next_page: @props.next
        prev_page: @props.prev

    buildProjectors: ->
      @state.collection.map (projector) =>
        React.createElement(ProjectorUnit, {projector: projector})

    loadProjectors: (url) ->
      @adapter = new Adapter(url)
      @adapter.loadData (data) =>
        if data.results.length > 0
          @setState
            collection: data.results
            count: data.count
            current_page: @getCurrentPage(data.next, data.previous)
            next_page: data.next
            prev_page: data.previous

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
      $('html').on 'update-projectors', (event, data) =>
        if @state.next_page
          $('html').trigger("projector-current-page")
        else
          index          = _.findIndex @state.collection, {id: data.id}
          new_collection = @state.collection
          count          = @state.count

          if index >= 0
            new_collection[index] = data
          else
            count += 1
            if (@state.count % 9) == 0
              $('html').trigger("projector-current-page")
              return
            new_collection.push(data)

          @setState
            collection: new_collection
            no_records: false
            count: count


      $('html').on 'projector-deleted', (event, data) =>
        count = @state.count - 1
        if @state.next_page
          $('html').trigger("projector-current-page")
        else if @state.prev_page and (count % 9) == 0
          $('html').trigger("projector-prev-page")
        else
          filtered_projectors = _.filter @state.collection, (projector) =>
            projector.id != data.id

          @setState
            collection: filtered_projectors
            no_records: if filtered_projectors.length > 0 then false else true
            count: count

      $('html').on 'projector-next-page', (event, data) =>
        @loadProjectors(@state.next_page)

      $('html').on 'projector-prev-page', (event, data) =>
        @loadProjectors(@state.prev_page)

      $('html').on 'projector-current-page', (event, data) =>
        @loadProjectors(@getUrlCurrentPage())

    newProjector: ->
      $('html').trigger("edit-projector-dialog-new")

    render: ->
      dom.div null,
        dom.h2 className: "ui dividing header",
          "Lighting::Projectors"
          dom.button
            className: "button ui mini right floated positive"
            onClick: @newProjector.bind(this)
          , "",
            dom.i {className: "plus icon"}, ""
            "New Projector"
        dom.div {className: "ui three cards"},
          @buildProjectors()
        React.createElement(ProjectorNoRecords, {output: @state.no_records})
        React.createElement(ProjectorPagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / 9), 
          next: @state.next_page, prev: @state.prev_page})
        React.createElement(ProjectorModal, {projector: {}})


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
            next: data.next,
            prev: data.previous,
          }), document.getElementById("root"))
        else
          ReactDOM.render(React.createElement(Composer, {}), document.getElementById("root"))
      , (data, status) =>
        $("#root").html("#{$("[data-object='error']").html()} #{data.statusText}")


  # page etrypoint
  $(document).ready ->
    page = new Visualizer()
    page.visualize()


  $('html').on 'show-dialog', (event, scope) =>
    dialog = $("[data-object='simple-dialog']")
    dialog.find(".content").html(scope.message)
    dialog.modal("show")


  $('html').on 'click', "[data-action='close-dialog']", (event) =>
    $("[data-object='simple-dialog']").modal("hide")
