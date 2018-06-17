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


  class IBootUnit extends React.Component

    displayName: "iBoot Body"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editIBoot: (data) ->
      $('html').trigger("edit-iboot-dialog-#{data.iboot.id}", data)

    sendCommand: (cmd) ->

      url        = $("#root").data("command-url")
      csrf_token = $("#root").data("csrf_token")
      iboot_id = @props.iboot.id

      $("[data-object='command-#{iboot_id}-#{cmd}']").toggleClass("loading")

      adapter  = new Adapter(url)
      postData =
        id: iboot_id
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
        $("[data-object='command-#{iboot_id}-#{cmd}']").toggleClass("loading")

    removeIBoot: (iboot_id) ->

      if confirm "Are you sure?"

        url        = $("#root").data("url")
        csrf_token = $("#root").data("csrf_token")

        $("[data-object ='iboot-#{iboot_id}']").toggleClass("loading")

        adapter  = new Adapter(url)
        postData =
          id: iboot_id

        scope = this
        adapter.delete csrf_token, postData, ( (data, status) ->
          # request ok
          $('html').trigger('iboot-deleted', data)
        ), ( (data, status) ->
          # request failed
        ), () ->
          # request finished
          $("[data-object='iboot-#{iboot_id}']").toggleClass("loading")


    render: ->
      scope = this
      dom.div {className: "ui card"},
        dom.div {className: "extra content"},
          dom.h3 {className: "left floated"},
            dom.i {className: "ui icon check circle"}, ""
            dom.span null, @props.iboot.name

        dom.div {className: "content"},
          dom.h3 null, 
            dom.p null, "Host: #{@props.iboot.host} | Port: #{@props.iboot.port}"
            dom.p null, "Mac: #{@props.iboot.mac_address}"

          @props.iboot.commands.map (cmd) ->
            dom.div
              className: "button ui mini"
              "data-object": "command-#{scope.props.iboot.id}-#{cmd.command}"
              onClick: scope.sendCommand.bind(scope, cmd.command)
            , "",
              dom.i {className: "cog icon"}, ""
              cmd.title

        dom.div {className: "ui buttons mini attached bottom"},
          dom.button
            className: "ui button"
            onClick: @editIBoot.bind(this, @props)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"
          dom.div {className: "or"}
          dom.button
            className: "ui button negative"
            onClick: @removeIBoot.bind(this, @props.iboot.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"

        React.createElement(IBootModal, {iboot: @props.iboot})


  class IBootNoRecords extends React.Component

    displayName: "iBoot no records"

    constructor: (props) ->
      super(props)

    render: ->
      if @props.output
        dom.h3 null, "No records found."
      else
        dom.h3 null, ""


  class IBootPagination extends React.Component

    displayName: "iBoot pagination"

    constructor: (props) ->
      super(props)

    clickNextPage: ->
      $('html').trigger("iboot-next-page")

    clickPrevPage: ->
      $('html').trigger("iboot-prev-page")

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
        next_page: @props.next_page
        prev_page: @props.prev_page
        page_size: @props.page_size

    buildIBoots: ->
      @state.collection.map (iboot) =>
        React.createElement(IBootUnit, {iboot: iboot, key: iboot.id})

    loadIBoots: (url) ->
      @adapter = new Adapter(url)
      @adapter.loadData (data) =>
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
      $('html').on 'update-iboots', (event, data) =>
        if @state.next_page
          $('html').trigger("iboot-current-page")
        else
          index          = _.findIndex @state.collection, {id: data.id}
          new_collection = @state.collection
          count          = @state.count

          if index >= 0
            new_collection[index] = data
          else
            if not @state.count or (@state.count % @state.page_size) == 0
              $('html').trigger("iboot-current-page")
            else
              count += 1
              new_collection.push(data)

          @setState
            collection: new_collection
            no_records: false
            count: count


      $('html').on 'iboot-deleted', (event, data) =>
        count = @state.count - 1
        if @state.next_page
          $('html').trigger("iboot-current-page")
        else if @state.prev_page and (count % @state.page_size) == 0
          $('html').trigger("iboot-prev-page")
        else
          filtered_iboots = _.filter @state.collection, (iboot) =>
            iboot.id != data.id

          @setState
            collection: filtered_iboots
            no_records: if filtered_iboots.length > 0 then false else true
            count: count

      $('html').on 'iboot-next-page', (event, data) =>
        @loadIBoots(@state.next_page)

      $('html').on 'iboot-prev-page', (event, data) =>
        @loadIBoots(@state.prev_page)

      $('html').on 'iboot-current-page', (event, data) =>
        @loadIBoots(@getUrlCurrentPage())

    newIBoot: ->
      $('html').trigger("edit-iboot-dialog-new")

    render: ->
      dom.div null,
        dom.h2 className: "ui dividing header",
          "iBoot::iBoots"
          dom.button
            className: "button ui mini right floated positive"
            onClick: @newIBoot.bind(this)
          , "",
            dom.i {className: "plus icon"}, ""
            "New iBoot"
        dom.div {className: "ui three cards"},
          @buildIBoots()
        React.createElement(IBootNoRecords, {output: @state.no_records})
        React.createElement(IBootPagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / @state.page_size),
          next: @state.next_page, prev: @state.prev_page})
        React.createElement(IBootModal, {iboot: {}})


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


  $('html').on 'show-dialog', (event, scope) =>
    dialog = $("[data-object='simple-dialog']")
    dialog.find(".content").html(scope.message)
    dialog.modal("show")


  $('html').on 'click', "[data-action='close-dialog']", (event) =>
    $("[data-object='simple-dialog']").modal("hide")
