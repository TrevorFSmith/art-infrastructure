do ->

  dom = {}

  dom.i      = React.createFactory "i"
  dom.p      = React.createFactory "p"
  dom.h3     = React.createFactory "h3"
  dom.h2     = React.createFactory "h2"
  dom.div    = React.createFactory "div"
  dom.span   = React.createFactory "span"
  dom.button = React.createFactory "button"
  dom.select = React.createFactory "select"
  dom.option = React.createFactory "option"


  "use strict"


  class CrestonUnitHeader extends React.Component

    displayName: "Creston Header"

    constructor: (props) ->
      super(props)

    render: ->
      dom.div {className: "extra content"},
        dom.h3 {className: "left floated"},
          dom.i {className: "ui icon check circle"}, ""
          dom.span null, @props.data.creston.name


  class CrestonUnitBody extends React.Component

    displayName: "Creston Body"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editCreston: (data) ->
      $('html').trigger("edit-creston-dialog-#{data.creston.id}", data)

    removeCreston: (creston_id) ->

      if confirm "Are you sure?"

        url        = $("#root").data("url")
        csrf_token = $("#root").data("csrf_token")

        $("[data-object ='creston-#{creston_id}']").toggleClass("loading")

        adapter  = new Adapter(url)
        postData =
          id: creston_id

        scope = this
        adapter.delete csrf_token, postData, ( (data, status) ->
          # request ok
          $('html').trigger('creston-deleted', data)
        ), ( (data, status) ->
          # request failed
        ), () ->
          # request finished
          $("[data-object='creston-#{creston_id}']").toggleClass("loading")


    render: ->
      scope = this
      dom.div {className: "content"},

        dom.h3 null, "Host: #{@props.data.creston.host} | Port: #{@props.data.creston.port}"
        React.createElement(CrestonSelectCommand, {creston: @props.data.creston})
        dom.h3 null, "Actions:"
        dom.div {className: "ui buttons mini"},
          dom.button
            className: "ui button"
            onClick: @editCreston.bind(this, @props.data)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"

          dom.div {className: "or"}

          dom.button
            className: "ui button negative"
            onClick: @removeCreston.bind(this, @props.data.creston.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"

        React.createElement(CrestonModal, {creston: @props.data.creston})


  class CrestonUnit extends React.Component

    displayName: "Creston Unit"

    constructor: (props) ->
      super(props)

    render: ->
        dom.div {className: "ui card"},
          React.createElement(CrestonUnitHeader, {data: @props})
          React.createElement(CrestonUnitBody, {data: @props})


  class CrestonNoRecords extends React.Component

    displayName: "Creston no records"

    constructor: (props) ->
      super(props)

    render: ->
      if @props.output
        dom.h3 null, "No records found."
      else
        dom.h3 null, ""


  class CrestonOptionCommand extends React.Component

      displayName: "Creston option command"

      constructor: (props) ->
        super(props)

      render: ->
        if @props.command
          dom.option null, @props.command.command
        else
          dom.option null, ""


  class CrestonSelectCommand extends React.Component

    displayName: "Creston select command"

    constructor: (props) ->
      super(props)
      @state =
        commands: @props.creston.commands
        select_command: @props.creston.commands[0]

    selectCommand: (creston_id) ->
      command = $("[data-object ='command-#{creston_id}'] option:selected").val()
      command = $.grep(@state.commands, (e) -> e.command == command)
      @setState
        select_command: command[0]

    sendCommand: (creston_id) ->
      url        = $("#root").data("command-url")
      csrf_token = $("#root").data("csrf_token")
      command    = @state.select_command.command

      $("[data-object='command-#{creston_id}-#{command}']").toggleClass("loading")

      adapter  = new Adapter(url)
      postData =
        id: creston_id
        command: command

      props = @props
      adapter.pushData "PUT", csrf_token, postData, ( (data) ->
        # request ok
        $('html').trigger('show-dialog', {message: data.details})
      ), ( (data, status) ->
        # request failed
        $('html').trigger('show-dialog', {message: data.responseJSON.details})
      ), () ->
        # request finished
        $("[data-object='command-#{creston_id}-#{command}']").toggleClass("loading")

    render: ->
      dom.div null, "",
        dom.select
          className: "ui dropdown margin-right"
          "data-object": "command-#{@props.creston.id}"
          onChange: @selectCommand.bind(this, @props.creston.id)
          , "",
            @props.creston.commands.map (cmd) ->
              React.createElement(CrestonOptionCommand, {command: cmd})
        dom.p null, @state.select_command.title
        dom.div
          className: "button ui mini"
          "data-object": "command-#{@props.creston.id}-#{@state.select_command.command}"
          onClick: this.sendCommand.bind(this, @props.creston.id)
        , "",
          dom.i {className: "cog icon"}, ""
          "Send command"


  class CrestonPagination extends React.Component

    displayName: "Creston pagination"

    constructor: (props) ->
      super(props)

    clickNextPage: ->
      $('html').trigger("creston-next-page")

    clickPrevPage: ->
      $('html').trigger("creston-prev-page")

    render: ->
      if @props.pages
        dom.div {className: "ui center aligned segment"},
          if @props.prev
            dom.button {className: "ui button margin-right", onClick: @clickPrevPage.bind(this)}, "Prev"
          dom.span {className: "margin-right"}, "Page #{@props.page} of #{@props.pages}"
          if @props.next
            dom.button {className: "ui button", onClick: @clickNextPage.bind(this)}, "Next"
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
        next_page: @props.next
        prev_page: @props.prev

    buildCrestons: ->
      @state.collection.map (creston) =>
        React.createElement(CrestonUnit, {creston: creston})

    loadCrestons: (url) ->
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

      $('html').on 'update-crestons', (event, data) =>
        if @state.next_page
          $('html').trigger("creston-current-page")
        else
          index          = _.findIndex @state.collection, {id: data.id}
          new_collection = @state.collection
          count          = @state.count

          if index >= 0
            new_collection[index] = data
          else
            if not @state.count or (@state.count % 9) == 0
              $('html').trigger("creston-current-page")
            else
              count += 1
              new_collection.push(data)

          @setState
            collection: new_collection
            no_records: false
            count: count

      $('html').on 'creston-deleted', (event, data) =>
        count = @state.count - 1
        if @state.next_page
          $('html').trigger("creston-current-page")
        else if @state.prev_page and (count % 9) == 0
          $('html').trigger("creston-prev-page")
        else
          filtered_crestons = _.filter @state.collection, (creston) =>
            creston.id != data.id

          @setState
            collection: filtered_crestons
            no_records: if filtered_crestons.length > 0 then false else true
            count: count

      $('html').on 'creston-next-page', (event, data) =>
        @loadCrestons(@state.next_page)

      $('html').on 'creston-prev-page', (event, data) =>
        @loadCrestons(@state.prev_page)

      $('html').on 'creston-current-page', (event, data) =>
        @loadCrestons(@getUrlCurrentPage())

    newCreston: ->
      $('html').trigger("edit-creston-dialog-new")

    render: ->
      dom.div null,
        dom.h2 className: "ui dividing header",
          "Lighting::Crestons"
          dom.button
            className: "button ui mini right floated positive"
            onClick: @newCreston.bind(this)
          , "",
            dom.i {className: "plus icon"}, ""
            "New Creston"
        dom.div {className: "ui three cards"},
          @buildCrestons()
        React.createElement(CrestonNoRecords, {output: @state.no_records})
        React.createElement(CrestonPagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / 9), 
          next: @state.next_page, prev: @state.prev_page})
        React.createElement(CrestonModal, {creston: {}})


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
