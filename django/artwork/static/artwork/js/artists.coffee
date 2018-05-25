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


  class ArtistUnitHeader extends React.Component

    displayName: "Artist Header"

    constructor: (props) ->
      super(props)

    render: ->
      dom.div {className: "extra content"},
        dom.h3 {className: "left floated"},
          dom.i {className: "ui icon check circle"}, ""
          dom.span null, @props.data.artist.name


  class ArtistUnitBody extends React.Component

    displayName: "Artist Body"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editArtist: (data) ->
      $('html').trigger("edit-artist-dialog-#{data.artist.id}", data)

    removeArtist: (artist_id) ->

      if confirm "Are you sure?"

        url        = $("#root").data("url")
        csrf_token = $("#root").data("csrf_token")

        $("[data-object ='artist-#{artist_id}']").toggleClass("loading")

        adapter  = new Adapter(url)
        postData =
          id: artist_id

        adapter.delete csrf_token, postData, ( (data, status) ->
          # request ok
          $('html').trigger('artist-deleted', data)
        ), ( (data, status) ->
          # request failed
        ), () ->
          # request finished
          $("[data-object='artist-#{artist_id}']").toggleClass("loading")

    render: ->
      date_time = @props.data.artist.created.substr(0, 10) + " " +
                  @props.data.artist.created.substr(11, 8)
      dom.div {className: "content"},

        dom.p null, "Email:   #{@props.data.artist.email}"
        dom.p null, "Phone:   #{@props.data.artist.phone}"
        dom.p null, "URL:     #{@props.data.artist.url}"
        dom.p null, "Notes:   #{@props.data.artist.notes}"
        dom.p null, "Created: #{date_time}"

        dom.h3 null, "Actions"

        dom.div {className: "ui buttons mini"},
          dom.button
            className: "ui button"
            onClick: @editArtist.bind(this, @props.data)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"

          dom.div {className: "or"}

          dom.button
            className: "ui button negative"
            onClick: @removeArtist.bind(this, @props.data.artist.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"

        React.createElement(ArtistModal, {artist: @props.data.artist})


  class ArtistUnit extends React.Component

    displayName: "Artist Unit"

    constructor: (props) ->
      super(props)

    render: ->
        dom.div {className: "ui card"},
          React.createElement(ArtistUnitHeader, {data: @props})
          React.createElement(ArtistUnitBody, {data: @props})


  class ArtistNoRecords extends React.Component

    displayName: "Artist no records"

    constructor: (props) ->
      super(props)

    render: ->
      if @props.output
        dom.h3 null, "No records found."
      else
        dom.h3 null, ""


  class ArtistPagination extends React.Component

    displayName: "Artist pagination"

    constructor: (props) ->
      super(props)

    clickNextPage: ->
      $('html').trigger("artist-next-page")

    clickPrevPage: ->
      $('html').trigger("artist-prev-page")

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

    buildArtists: ->
      @state.collection.map (artist) =>
        React.createElement(ArtistUnit, {artist: artist, key: artist.id})

    loadArtists: (url) ->
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
      $('html').on 'update-artists', (event, data) =>
        if @state.next_page
          $('html').trigger("artist-current-page")
        else
          index          = _.findIndex @state.collection, {id: data.id}
          new_collection = @state.collection
          count          = @state.count

          if index >= 0
            new_collection[index] = data
          else
            if not @state.count or (@state.count % 9) == 0
              $('html').trigger("artist-current-page")
            else
              count += 1
              new_collection.push(data)

          @setState
            collection: new_collection
            no_records: false
            count: count


      $('html').on 'artist-deleted', (event, data) =>
        count = @state.count - 1
        if @state.next_page
          $('html').trigger("artist-current-page")
        else if @state.prev_page and (count % 9) == 0
          $('html').trigger("artist-prev-page")
        else
          filtered_artists = _.filter @state.collection, (artist) =>
            artist.id != data.id

          @setState
            collection: filtered_artists
            no_records: if filtered_artists.length > 0 then false else true
            count: count

      $('html').on 'artist-next-page', (event, data) =>
        @loadArtists(@state.next_page)

      $('html').on 'artist-prev-page', (event, data) =>
        @loadArtists(@state.prev_page)

      $('html').on 'artist-current-page', (event, data) =>
        @loadArtists(@getUrlCurrentPage())

    newArtist: ->
      $('html').trigger("edit-artist-dialog-new")

    render: ->
      dom.div null,
        dom.h2 className: "ui dividing header",
          "Artwork::Artists"
          dom.button
            className: "button ui mini right floated positive"
            onClick: @newArtist.bind(this)
          , "",
            dom.i {className: "plus icon"}, ""
            "New artist"
        dom.div {className: "ui three cards"},
          @buildArtists()
        React.createElement(ArtistNoRecords, {output: @state.no_records})
        React.createElement(ArtistPagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / 9),
          next: @state.next_page, prev: @state.prev_page})
        React.createElement(ArtistModal, {artist: {}})


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
