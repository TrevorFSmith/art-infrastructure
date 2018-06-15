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


  class ArtistGroupUnit extends React.Component

    displayName: "ArtistGroup Body"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editArtistGroup: (data) =>
      $('html').trigger("edit-artist-group-dialog-#{data.artist_group.id}", data)

    removeArtistGroup: (artist_group_id) =>

      if confirm "Are you sure?"

        url        = $("#root").data("url")
        csrf_token = $("#root").data("csrf_token")

        $("[data-object ='artist-group-#{artist_group_id}']").toggleClass("loading")

        adapter  = new Adapter(url)
        postData =
          id: artist_group_id

        adapter.delete csrf_token, postData, ( (data, status) ->
          # request ok
          $('html').trigger('artist-group-deleted', data)
        ), ( (data, status) ->
          # request failed
        ), () ->
          # request finished
          $("[data-object='artist-group-#{artist_group_id}']").toggleClass("loading")

    render: ->
      date_time = @props.artist_group.created.substr(0, 10) + " " +
                  @props.artist_group.created.substr(11, 8)

      dom.div {className: "ui card"},
        dom.div {className: "extra content"},
          dom.h3 {className: "left floated"},
            dom.i {className: "ui icon check circle"}, ""
            dom.span null, @props.artist_group.name

        dom.div {className: "content"},
          dom.div null, "Artists:"
          dom.div className: "ui list",
            @props.artist_group.artists_info.map (artist) ->
              dom.div className: "item", artist.name
          dom.div null, "URL:     #{@props.artist_group.url}"
          dom.div null, "Created: #{date_time}"

        dom.div {className: "ui buttons mini attached bottom"},
          dom.button
            className: "ui button"
            onClick: @editArtistGroup.bind(this, @props)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"
          dom.div {className: "or"}
          dom.button
            className: "ui button negative"
            onClick: @removeArtistGroup.bind(this, @props.artist_group.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"

        React.createElement(ArtistGroupModal, {artist_group: @props.artist_group})


  class ArtistGroupNoRecords extends React.Component

    displayName: "ArtistGroup no records"

    constructor: (props) ->
      super(props)

    render: ->
      if @props.output
        dom.h3 null, "No records found."
      else
        dom.h3 null, ""


  class ArtistGroupPagination extends React.Component

    displayName: "ArtistGroup pagination"

    constructor: (props) ->
      super(props)

    clickNextPage: ->
      $('html').trigger("artist-group-next-page")

    clickPrevPage: ->
      $('html').trigger("artist-group-prev-page")

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

    buildArtistGroups: ->
      @state.collection.map (artist_group) =>
        React.createElement(ArtistGroupUnit, {artist_group: artist_group, key: artist_group.id})

    loadArtistGroups: (url) ->
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
      $('html').on 'update-artist-groups', (event, data) =>
        if @state.next_page
          $('html').trigger("artist-group-current-page")
        else
          index          = _.findIndex @state.collection, {id: data.id}
          new_collection = @state.collection
          count          = @state.count

          if index >= 0
            new_collection[index] = data
          else
            if not @state.count or (@state.count % @state.page_size) == 0
              $('html').trigger("artist-group-current-page")
            else
              count += 1
              new_collection.push(data)

          @setState
            collection: new_collection
            no_records: false
            count: count


      $('html').on 'artist-group-deleted', (event, data) =>
        count = @state.count - 1
        if @state.next_page
          $('html').trigger("artist-group-current-page")
        else if @state.prev_page and (count % @state.page_size) == 0
          $('html').trigger("artist-group-prev-page")
        else
          filtered_artist_groups = _.filter @state.collection, (artist_group) =>
            artist_group.id != data.id

          @setState
            collection: filtered_artist_groups
            no_records: if filtered_artist_groups.length > 0 then false else true
            count: count

      $('html').on 'artist-group-next-page', (event, data) =>
        @loadArtistGroups(@state.next_page)

      $('html').on 'artist-group-prev-page', (event, data) =>
        @loadArtistGroups(@state.prev_page)

      $('html').on 'artist-group-current-page', (event, data) =>
        @loadArtistGroups(@getUrlCurrentPage())

    newArtistGroup: ->
      $('html').trigger("edit-artist-group-dialog-new")

    render: ->
      dom.div null,
        dom.h2 className: "ui dividing header",
          "Artwork::ArtistGroups"
          dom.button
            className: "button ui mini right floated positive"
            onClick: @newArtistGroup
          , "",
            dom.i {className: "plus icon"}, ""
            "New artist group"
        dom.div {className: "ui three cards"},
          @buildArtistGroups()
        React.createElement(ArtistGroupNoRecords, {output: @state.no_records})
        React.createElement(ArtistGroupPagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / @state.page_size),
          next: @state.next_page, prev: @state.prev_page})
        React.createElement(ArtistGroupModal, {artist_group: {}})


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
