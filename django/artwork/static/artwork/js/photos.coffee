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


  class PhotoUnitHeader extends React.Component

    displayName: "Photo Header"

    constructor: (props) ->
      super(props)

    render: ->
      dom.div {className: "extra content"},
        dom.h3 {className: "left floated"},
          dom.i {className: "ui icon check circle"}, ""
          dom.span null, @props.data.photo.title


  class PhotoUnitBody extends React.Component

    displayName: "Photo Body"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editPhoto: (data) =>
      $('html').trigger("edit-photo-dialog-#{data.photo.id}", data)

    removePhoto: (photo_id) =>

      if confirm "Are you sure?"

        url        = $("#root").data("url")
        csrf_token = $("#root").data("csrf_token")

        $("[data-object ='photo-#{photo_id}']").toggleClass("loading")

        adapter  = new Adapter(url)
        postData =
          id: photo_id

        adapter.delete csrf_token, postData, ( (data, status) ->
          # request ok
          $('html').trigger('photo-deleted', data)
        ), ( (data, status) ->
          # request failed
        ), () ->
          # request finished
          $("[data-object='photo-#{photo_id}']").toggleClass("loading")

    render: ->
      date_time = @props.data.photo.created.substr(0, 10) + " " +
                  @props.data.photo.created.substr(11, 8)
      dom.div {className: "content"},
        dom.div null, "Photo:",
          dom.a {href: @props.data.photo.image}, "__link__"
        dom.div null, "Caption:     #{@props.data.photo.caption}"
        dom.div null, "Description: #{@props.data.photo.description}"
        dom.div null, "Created:     #{date_time}"

        dom.h3 null, "Actions"

        dom.div {className: "ui buttons mini"},
          dom.button
            className: "ui button"
            onClick: @editPhoto.bind(this, @props.data)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"

          dom.div {className: "or"}

          dom.button
            className: "ui button negative"
            onClick: @removePhoto.bind(this, @props.data.photo.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"

        React.createElement(PhotoModal, {photo: @props.data.photo})


  class PhotoUnit extends React.Component

    displayName: "Photo Unit"

    constructor: (props) ->
      super(props)

    render: ->
        dom.div {className: "ui card"},
          React.createElement(PhotoUnitHeader, {data: @props})
          React.createElement(PhotoUnitBody, {data: @props})


  class PhotoNoRecords extends React.Component

    displayName: "Photo no records"

    constructor: (props) ->
      super(props)

    render: ->
      if @props.output
        dom.h3 null, "No records found."
      else
        dom.h3 null, ""


  class PhotoPagination extends React.Component

    displayName: "Photo pagination"

    constructor: (props) ->
      super(props)

    clickNextPage: ->
      $('html').trigger("photo-next-page")

    clickPrevPage: ->
      $('html').trigger("photo-prev-page")

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

    buildPhotos: ->
      @state.collection.map (photo) =>
        React.createElement(PhotoUnit, {photo: photo, key: photo.id})

    loadPhotos: (url) ->
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
      $('html').on 'update-photos', (event, data) =>
        if @state.next_page
          $('html').trigger("photo-current-page")
        else
          index          = _.findIndex @state.collection, {id: data.id}
          new_collection = @state.collection
          count          = @state.count

          if index >= 0
            new_collection[index] = data
          else
            if not @state.count or (@state.count % 9) == 0
              $('html').trigger("photo-current-page")
            else
              count += 1
              new_collection.push(data)

          @setState
            collection: new_collection
            no_records: false
            count: count


      $('html').on 'photo-deleted', (event, data) =>
        count = @state.count - 1
        if @state.next_page
          $('html').trigger("photo-current-page")
        else if @state.prev_page and (count % 9) == 0
          $('html').trigger("photo-prev-page")
        else
          filtered_photos = _.filter @state.collection, (photo) =>
            photo.id != data.id

          @setState
            collection: filtered_photos
            no_records: if filtered_photos.length > 0 then false else true
            count: count

      $('html').on 'photo-next-page', (event, data) =>
        @loadPhotos(@state.next_page)

      $('html').on 'photo-prev-page', (event, data) =>
        @loadPhotos(@state.prev_page)

      $('html').on 'photo-current-page', (event, data) =>
        @loadPhotos(@getUrlCurrentPage())

    newPhoto: ->
      $('html').trigger("edit-photo-dialog-new")

    render: ->
      dom.div null,
        dom.h2 className: "ui dividing header",
          "Artwork::Photos"
          dom.button
            className: "button ui mini right floated positive"
            onClick: @newPhoto
          , "",
            dom.i {className: "plus icon"}, ""
            "New photo"
        dom.div {className: "ui three cards"},
          @buildPhotos()
        React.createElement(PhotoNoRecords, {output: @state.no_records})
        React.createElement(PhotoPagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / 9),
          next: @state.next_page, prev: @state.prev_page})
        React.createElement(PhotoModal, {photo: {}})


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
