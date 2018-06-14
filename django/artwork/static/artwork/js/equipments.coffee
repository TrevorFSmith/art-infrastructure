do ->

  dom = {}

  dom.i      = React.createFactory "i"
  dom.p      = React.createFactory "p"
  dom.h3     = React.createFactory "h3"
  dom.h2     = React.createFactory "h2"
  dom.div    = React.createFactory "div"
  dom.span   = React.createFactory "span"
  dom.button = React.createFactory "button"
  dom.a      = React.createFactory "a"


  "use strict"


  class EquipmentUnit extends React.Component

    displayName: "Equipment Body"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editEquipment: (data) =>
      $('html').trigger("edit-equipment-dialog-#{data.equipment.id}", data)

    removeEquipment: (equipment_id) =>

      if confirm "Are you sure?"

        url        = $("#root").data("url")
        csrf_token = $("#root").data("csrf_token")

        $("[data-object ='equipment-#{equipment_id}']").toggleClass("loading")

        adapter  = new Adapter(url)
        postData =
          id: equipment_id

        adapter.delete csrf_token, postData, ( (data, status) ->
          # request ok
          $('html').trigger('equipment-deleted', data)
        ), ( (data, status) ->
          # request failed
        ), () ->
          # request finished
          $("[data-object='equipment-#{equipment_id}']").toggleClass("loading")

    render: ->
      date_time = @props.equipment.created.substr(0, 10) + " " +
                  @props.equipment.created.substr(11, 8)

      dom.div {className: "ui card"},
        dom.div {className: "extra content"},
          dom.h3 {className: "left floated"},
            dom.i {className: "ui icon check circle"}, ""
            dom.span null, @props.equipment.name

        dom.div {className: "content"},
          dom.div null, "Email: #{@props.equipment.email}"
          dom.div null, "Type:  #{@props.equipment.equipment_type_name}"
          dom.div null, "Device type:  #{@props.equipment.device_type_name}"
          dom.div null, "Device name:  #{@props.equipment.device_name}"
          dom.div null, "Photos:"
          dom.div className: "ui list",
            @props.equipment.photos_info.map (photo) ->
              dom.div className: "item", 
                dom.a {href: "/media/" + photo.image, target: "_blank"}, photo.title
          dom.div null, "Notes:   #{@props.equipment.notes}"
          dom.div null, "Created: #{date_time}"

        dom.div {className: "ui buttons mini attached bottom"},
          dom.button
            className: "ui button"
            onClick: @editEquipment.bind(this, @props)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"
          dom.div {className: "or"}
          dom.button
            className: "ui button negative"
            onClick: @removeEquipment.bind(this, @props.equipment.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"

        React.createElement(EquipmentModal, {equipment: @props.equipment})


  class EquipmentNoRecords extends React.Component

    displayName: "Equipment no records"

    constructor: (props) ->
      super(props)

    render: ->
      if @props.output
        dom.h3 null, "No records found."
      else
        dom.h3 null, ""


  class EquipmentPagination extends React.Component

    displayName: "Equipment pagination"

    constructor: (props) ->
      super(props)

    clickNextPage: ->
      $('html').trigger("equipment-next-page")

    clickPrevPage: ->
      $('html').trigger("equipment-prev-page")

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

    buildEquipments: ->
      @state.collection.map (equipment) =>
        React.createElement(EquipmentUnit, {equipment: equipment, key: equipment.id})

    loadEquipments: (url) ->
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
      $('html').on 'update-equipments', (event, data) =>
        if @state.next_page
          $('html').trigger("equipment-current-page")
        else
          index          = _.findIndex @state.collection, {id: data.id}
          new_collection = @state.collection
          count          = @state.count

          if index >= 0
            new_collection[index] = data
          else
            if not @state.count or (@state.count % 9) == 0
              $('html').trigger("equipment-current-page")
            else
              count += 1
              new_collection.push(data)

          @setState
            collection: new_collection
            no_records: false
            count: count


      $('html').on 'equipment-deleted', (event, data) =>
        count = @state.count - 1
        if @state.next_page
          $('html').trigger("equipment-current-page")
        else if @state.prev_page and (count % 9) == 0
          $('html').trigger("equipment-prev-page")
        else
          filtered_equipments = _.filter @state.collection, (equipment) =>
            equipment.id != data.id

          @setState
            collection: filtered_equipments
            no_records: if filtered_equipments.length > 0 then false else true
            count: count

      $('html').on 'equipment-next-page', (event, data) =>
        @loadEquipments(@state.next_page)

      $('html').on 'equipment-prev-page', (event, data) =>
        @loadEquipments(@state.prev_page)

      $('html').on 'equipment-current-page', (event, data) =>
        @loadEquipments(@getUrlCurrentPage())

    newEquipment: ->
      $('html').trigger("edit-equipment-dialog-new")

    render: ->
      dom.div null,
        dom.h2 className: "ui dividing header",
          "Artwork::Equipments"
          dom.button
            className: "button ui mini right floated positive"
            onClick: @newEquipment
          , "",
            dom.i {className: "plus icon"}, ""
            "New equipment"
        dom.div {className: "ui three cards"},
          @buildEquipments()
        React.createElement(EquipmentNoRecords, {output: @state.no_records})
        React.createElement(EquipmentPagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / 9),
          next: @state.next_page, prev: @state.prev_page})
        React.createElement(EquipmentModal, {equipment: {}})


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
