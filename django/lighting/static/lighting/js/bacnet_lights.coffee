do ->

  dom = {}

  dom.i      = React.createFactory "i"
  dom.p      = React.createFactory "p"
  dom.h3     = React.createFactory "h3"
  dom.h2     = React.createFactory "h2"
  dom.div    = React.createFactory "div"
  dom.span   = React.createFactory "span"
  dom.button = React.createFactory "button"
  dom.input  = React.createFactory "input"


  "use strict"


  class BACNetLightUnit extends React.Component

    displayName: "BACNet Light Body"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editBACNetLight: (data) ->
      $('html').trigger("edit-bacnet-light-dialog-#{data.bacnet_light.id}", data)

    sendCommand: ->

      url             = $("#root").data("command-url")
      csrf_token      = $("#root").data("csrf_token")
      bacnet_light_id = @props.bacnet_light.id
      cmd             = $("[data-object='command-#{bacnet_light_id}']").val()

      $("[data-object='command-send-#{bacnet_light_id}']").toggleClass("loading")

      adapter  = new Adapter(url)
      postData =
        id: bacnet_light_id
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
        $("[data-object='command-send-#{bacnet_light_id}']").toggleClass("loading")
        $input_command = $("[data-object='command-#{bacnet_light_id}']")
        $input_command.val($input_command.placeholder)

    removeBACNetLight: (bacnet_light_id) ->

      if confirm "Are you sure?"

        url        = $("#root").data("url")
        csrf_token = $("#root").data("csrf_token")

        $("[data-object ='bacnet-light-#{bacnet_light_id}']").toggleClass("loading")

        adapter  = new Adapter(url)
        postData =
          id: bacnet_light_id

        scope = this
        adapter.delete csrf_token, postData, ( (data, status) ->
          # request ok
          $('html').trigger('bacnet-light-deleted', data)
        ), ( (data, status) ->
          # request failed
        ), () ->
          # request finished
          $("[data-object='bacnet-light-#{bacnet_light_id}']").toggleClass("loading")


    render: ->
      scope = this
      dom.div {className: "ui card"},
        dom.div {className: "extra content"},
          dom.h3 {className: "left floated"},
            dom.i {className: "ui icon check circle"}, ""
            dom.span null, @props.bacnet_light.name

        dom.div {className: "content"},
          dom.h3 null, "Device ID: #{@props.bacnet_light.device_id} | Property ID: #{@props.bacnet_light.property_id}"
          dom.p
            className: "ui input margin-right"
            , "",
              dom.input placeholder: "Enter command ...", "data-object": "command-#{scope.props.bacnet_light.id}"
          dom.div
            className: "button ui mini"
            "data-object": "command-send-#{scope.props.bacnet_light.id}"
            onClick: scope.sendCommand.bind(scope)
          , "",
            dom.i {className: "cog icon"}, ""
            "Send command"

        dom.div {className: "ui buttons mini attached bottom"},
          dom.button
            className: "ui button"
            onClick: @editBACNetLight.bind(this, @props)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"
          dom.div {className: "or"}
          dom.button
            className: "ui button negative"
            onClick: @removeBACNetLight.bind(this, @props.bacnet_light.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"

        React.createElement(BACNetLightModal, {bacnet_light: @props.bacnet_light})


  class BACNetLightNoRecords extends React.Component

    displayName: "BACNet Light no records"

    constructor: (props) ->
      super(props)

    render: ->
      if @props.output
        dom.h3 null, "No records found."
      else
        dom.h3 null, ""


  class BACNetLightPagination extends React.Component

    displayName: "BACNet light pagination"

    constructor: (props) ->
      super(props)

    clickNextPage: ->
      $('html').trigger("bacnet-light-next-page")

    clickPrevPage: ->
      $('html').trigger("bacnet-light-prev-page")

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

    buildBACNetLights: ->
      @state.collection.map (bacnet_light) =>
        React.createElement(BACNetLightUnit, {bacnet_light: bacnet_light, key: bacnet_light.id})

    loadBACNetLights: (url) ->
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

      $('html').on 'update-bacnet-lights', (event, data) =>
        if @state.next_page
          $('html').trigger("bacnet-light-current-page")
        else
          index          = _.findIndex @state.collection, {id: data.id}
          new_collection = @state.collection
          count          = @state.count

          if index >= 0
            new_collection[index] = data
          else
            if not @state.count or (@state.count % @state.page_size) == 0
              $('html').trigger("bacnet-light-current-page")
            else
              count += 1
              new_collection.push(data)

          @setState
            collection: new_collection
            no_records: false
            count: count

      $('html').on 'bacnet-light-deleted', (event, data) =>
        count = @state.count - 1
        if @state.next_page
          $('html').trigger("bacnet-light-current-page")
        else if @state.prev_page and (count % @state.page_size) == 0
          $('html').trigger("bacnet-light-prev-page")
        else
          filtered_bacnet_lights = _.filter @state.collection, (bacnet_light) =>
            bacnet_light.id != data.id

          @setState
            collection: filtered_bacnet_lights
            no_records: if filtered_bacnet_lights.length > 0 then false else true
            count: count

      $('html').on 'bacnet-light-next-page', (event, data) =>
        @loadBACNetLights(@state.next_page)

      $('html').on 'bacnet-light-prev-page', (event, data) =>
        @loadBACNetLights(@state.prev_page)

      $('html').on 'bacnet-light-current-page', (event, data) =>
        @loadBACNetLights(@getUrlCurrentPage())

    newBACNetLight: ->
      $('html').trigger("edit-bacnet-light-dialog-new")

    render: ->
      dom.div null,
        dom.h2 className: "ui dividing header",
          "Lighting::BACNet Service"
          dom.button
            className: "button ui mini right floated positive"
            onClick: @newBACNetLight.bind(this)
          , "",
            dom.i {className: "plus icon"}, ""
            "New BACNet Light"
        dom.div {className: "ui three cards"},
          @buildBACNetLights()
        React.createElement(BACNetLightNoRecords, {output: @state.no_records})
        React.createElement(BACNetLightPagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / @state.page_size),
          next: @state.next_page, prev: @state.prev_page})
        React.createElement(BACNetLightModal, {bacnet_light: {}})

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
