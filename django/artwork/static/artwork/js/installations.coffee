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


  class InstallationUnit extends React.Component

    displayName: "Installation Unit"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editInstallation: (data) =>
      $('html').trigger("edit-installation-dialog-#{data.installation.id}", data)

    removeInstallation: (installation_id) =>

      if confirm "Are you sure?"

        url        = $("#root").data("url")
        csrf_token = $("#root").data("csrf_token")

        $("[data-object ='installation-#{installation_id}']").toggleClass("loading")

        adapter  = new Adapter(url)
        postData =
          id: installation_id

        adapter.delete csrf_token, postData, ( (data, status) ->
          # request ok
          $('html').trigger('installation-deleted', data)
        ), ( (data, status) ->
          # request failed
        ), () ->
          # request finished
          $("[data-object='installation-#{installation_id}']").toggleClass("loading")

    render: ->
      date_time = @props.installation.created.substr(0, 10) + " " +
                  @props.installation.created.substr(11, 8)

      dom.div {className: "ui card"},
        dom.div {className: "extra content"},
          dom.h3 {className: "left floated"},
            dom.i {className: "ui icon check circle"}, ""
            dom.span null, @props.installation.name

        dom.div {className: "content"},
          dom.div null, "Site:   #{@props.installation.site_name}"
          dom.div null, "Artist groups:"
          dom.div className: "ui list",
            @props.installation.groups_info.map (group) ->
              dom.div className: "item", group.name
          dom.div null, "Artists:"
          dom.div className: "ui list",
            @props.installation.artists_info.map (artist) ->
              dom.div className: "item", artist.name
          dom.div null, "Users:"
          dom.div className: "ui list",
            @props.installation.users_info.map (user) ->
              dom.div className: "item", user.username
          dom.div null, "Photos:"
          dom.div className: "ui list",
            @props.installation.photos_info.map (photo) ->
              dom.div className: "item", 
                dom.a {href: "/media/" + photo.image, target: "_blank"}, photo.title
          dom.div null, "Documents:"
          dom.div className: "ui list",
            @props.installation.documents_info.map (document) ->
              dom.div className: "item", 
                dom.a {href: "/media/" + document.doc}, document.title
          dom.div null, "Notes:   #{@props.installation.notes}"
          dom.div null, "Created: #{date_time}"

        dom.div {className: "ui buttons mini attached bottom"},
          dom.button
            className: "ui button"
            onClick: @editInstallation.bind(this, @props)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"
          dom.div {className: "or"}
          dom.button
            className: "ui button negative"
            onClick: @removeInstallation.bind(this, @props.installation.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"

        React.createElement(InstallationModal, {installation: @props.installation})


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
        next_page: @props.next
        prev_page: @props.prev

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
      $('html').on 'update-installations', (event, data) =>
        if @state.next_page
          $('html').trigger("installation-current-page")
        else
          index          = _.findIndex @state.collection, {id: data.id}
          new_collection = @state.collection
          count          = @state.count

          if index >= 0
            new_collection[index] = data
          else
            if not @state.count or (@state.count % 9) == 0
              $('html').trigger("installation-current-page")
            else
              count += 1
              new_collection.push(data)

          @setState
            collection: new_collection
            no_records: false
            count: count


      $('html').on 'installation-deleted', (event, data) =>
        count = @state.count - 1
        if @state.next_page
          $('html').trigger("installation-current-page")
        else if @state.prev_page and (count % 9) == 0
          $('html').trigger("installation-prev-page")
        else
          filtered_installations = _.filter @state.collection, (installation) =>
            installation.id != data.id

          @setState
            collection: filtered_installations
            no_records: if filtered_installations.length > 0 then false else true
            count: count

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
          "Artwork::Installations"
          dom.button
            className: "button ui mini right floated positive"
            onClick: @newInstallation
          , "",
            dom.i {className: "plus icon"}, ""
            "New installation"
        dom.div {className: "ui three cards"},
          @buildInstallations()
        React.createElement(InstallationNoRecords, {output: @state.no_records})
        React.createElement(InstallationPagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / 9),
          next: @state.next_page, prev: @state.prev_page})
        React.createElement(InstallationModal, {installation: {}})


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
