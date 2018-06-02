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


  class EquipmentTypeUnitHeader extends React.Component

    displayName: "Equipment Type Header"

    constructor: (props) ->
      super(props)

    render: ->
      dom.div {className: "extra content"},
        dom.h3 {className: "left floated"},
          dom.i {className: "ui icon check circle"}, ""
          dom.span null, @props.data.equipment_type.name


  class EquipmentTypeUnitBody extends React.Component

    displayName: "Equipment Type Body"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editEquipmentType: (data) =>
      $('html').trigger("edit-equipment-type-dialog-#{data.equipment_type.id}", data)

    sendCommand: (cmd) =>

      url        = $("#root").data("command-url")
      csrf_token = $("#root").data("csrf_token")
      equipment_type_id = @props.data.equipment_type.id

      $("[data-object='command-#{equipment_type_id}-#{cmd}']").toggleClass("loading")

      adapter  = new Adapter(url)
      postData =
        id: equipment_type_id
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
        $("[data-object='command-#{equipment_type_id}-#{cmd}']").toggleClass("loading")

    removeEquipmentType: (equipment_type_id) =>

      if confirm "Are you sure?"

        url        = $("#root").data("url")
        csrf_token = $("#root").data("csrf_token")

        $("[data-object ='equipment-type-#{equipment_type_id}']").toggleClass("loading")

        adapter  = new Adapter(url)
        postData =
          id: equipment_type_id

        scope = this
        adapter.delete csrf_token, postData, ( (data, status) ->
          # request ok
          $('html').trigger('equipment-type-deleted', data)
        ), ( (data, status) ->
          # request failed
        ), () ->
          # request finished
          $("[data-object='equipment-type-#{equipment_type_id}']").toggleClass("loading")


    render: ->
      scope = this
      dom.div {className: "content"},

        dom.div null, "Provider: #{@props.data.equipment_type.provider}"
        dom.div null, "URL:      #{@props.data.equipment_type.url}"
        dom.div null, "Notes:    #{@props.data.equipment_type.notes}"

        dom.h3 null, "Actions"

        dom.div {className: "ui buttons mini"},
          dom.button
            className: "ui button"
            onClick: @editEquipmentType.bind(this, @props.data)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"

          dom.div {className: "or"}

          dom.button
            className: "ui button negative"
            onClick: @removeEquipmentType.bind(this, @props.data.equipment_type.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"

        React.createElement(EquipmentTypeModal, {equipment_type: @props.data.equipment_type})


  class EquipmentTypeUnit extends React.Component

    displayName: "Equipment Type Unit"

    constructor: (props) ->
      super(props)

    render: ->
        dom.div {className: "ui card"},
          React.createElement(EquipmentTypeUnitHeader, {data: @props})
          React.createElement(EquipmentTypeUnitBody, {data: @props})


  class EquipmentTypeNoRecords extends React.Component

    displayName: "Equipment Type no records"

    constructor: (props) ->
      super(props)

    render: ->
      if @props.output
        dom.h3 null, "No records found."
      else
        dom.h3 null, ""


  class EquipmentTypePagination extends React.Component

    displayName: "Equipment Type pagination"

    constructor: (props) ->
      super(props)

    clickNextPage: ->
      $('html').trigger("equipment-type-next-page")

    clickPrevPage: ->
      $('html').trigger("equipment-type-prev-page")

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
        next_page: @props.next
        prev_page: @props.prev

    buildEquipmentTypes: ->
      @state.collection.map (equipment_type) =>
        React.createElement(EquipmentTypeUnit, {equipment_type: equipment_type, key: equipment_type.id})

    loadEquipmentTypes: (url) ->
      adapter = new Adapter(url)
      adapter.loadData (data) =>
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
      $('html').on 'update-equipment-types', (event, data) =>
        if @state.next_page
          $('html').trigger("equipment-type-current-page")
        else
          index          = _.findIndex @state.collection, {id: data.id}
          new_collection = @state.collection
          count          = @state.count

          if index >= 0
            new_collection[index] = data
          else
            if not @state.count or (@state.count % 9) == 0
              $('html').trigger("equipment-type-current-page")
            else
              count += 1
              new_collection.push(data)

          @setState
            collection: new_collection
            no_records: false
            count: count


      $('html').on 'equipment-type-deleted', (event, data) =>
        count = @state.count - 1
        if @state.next_page
          $('html').trigger("equipment-type-current-page")
        else if @state.prev_page and (count % 9) == 0
          $('html').trigger("equipment-type-prev-page")
        else
          filtered_equipment_types = _.filter @state.collection, (equipment_type) =>
            equipment_type.id != data.id

          @setState
            collection: filtered_equipment_types
            no_records: if filtered_equipment_types.length > 0 then false else true
            count: count

      $('html').on 'equipment-type-next-page', (event, data) =>
        @loadEquipmentTypes(@state.next_page)

      $('html').on 'equipment-type-prev-page', (event, data) =>
        @loadEquipmentTypes(@state.prev_page)

      $('html').on 'equipment-type-current-page', (event, data) =>
        @loadEquipmentTypes(@getUrlCurrentPage())

    newEquipmentType: ->
      $('html').trigger("edit-equipment-type-dialog-new")

    render: ->
      dom.div null,
        dom.h2 className: "ui dividing header",
          "Artwork::Equipment Types"
          dom.button
            className: "button ui mini right floated positive"
            onClick: @newEquipmentType
          , "",
            dom.i {className: "plus icon"}, ""
            "New Equipment Type"
        dom.div {className: "ui three cards"},
          @buildEquipmentTypes()
        React.createElement(EquipmentTypeNoRecords, {output: @state.no_records})
        React.createElement(EquipmentTypePagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / 9), 
          next: @state.next_page, prev: @state.prev_page})
        React.createElement(EquipmentTypeModal, {equipment_type: {}})


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
