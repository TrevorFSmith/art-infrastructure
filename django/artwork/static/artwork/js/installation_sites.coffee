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


  class InstallationSiteUnit extends React.Component

    displayName: "Installation Site Unit"

    constructor: (props) ->
      super(props)
      @state = @state || {}

    editInstallationSite: (data) =>
      $('html').trigger("edit-installation-site-dialog-#{data.installation_site.id}", data)

    removeInstallationSite: (installation_site_id) =>

      if confirm "Are you sure?"

        url        = $("#root").data("url")
        csrf_token = $("#root").data("csrf_token")

        $("[data-object ='installation-site-#{installation_site_id}']").toggleClass("loading")

        adapter  = new Adapter(url)
        postData =
          id: installation_site_id

        adapter.delete csrf_token, postData, ( (data, status) ->
          # request ok
          $('html').trigger('installation-site-deleted', data)
        ), ( (data, status) ->
          # request failed
        ), () ->
          # request finished
          $("[data-object='installation-site-#{installation_site_id}']").toggleClass("loading")

    render: ->
      date_time = @props.installation_site.created.substr(0, 10) + " " +
                  @props.installation_site.created.substr(11, 8)

      dom.div {className: "ui card"},
        dom.div {className: "extra content"},
          dom.h3 {className: "left floated"},
            dom.i {className: "ui icon check circle"}, ""
            dom.span null, @props.installation_site.name

        dom.div {className: "content"},
          dom.div null, "Location:   #{@props.installation_site.location}"
          dom.div null, "Photos:"
          dom.div className: "ui list",
            @props.installation_site.photos_info.map (photo) ->
              dom.div className: "item", 
                dom.a href: "/media/" + photo.image, photo.title
          dom.div null, "Equipment:"
          dom.div className: "ui list",
            @props.installation_site.equipment_info.map (equipment) ->
              dom.div className: "item", equipment.name
          dom.div null, "Notes:   #{@props.installation_site.notes}"
          dom.div null, "Created: #{date_time}"

        dom.div {className: "ui buttons mini attached bottom"},
          dom.button
            className: "ui button"
            onClick: @editInstallationSite.bind(this, @props)
          , "",
            dom.i {className: "pencil icon"}, ""
            "Edit"
          dom.div {className: "or"}
          dom.button
            className: "ui button negative"
            onClick: @removeInstallationSite.bind(this, @props.installation_site.id)
          , "",
            dom.i {className: "trash icon"}, ""
            "Delete"

        React.createElement(InstallationSiteModal, {installation_site: @props.installation_site})


  class InstallationSiteNoRecords extends React.Component

    displayName: "Installation Site no records"

    constructor: (props) ->
      super(props)

    render: ->
      if @props.output
        dom.h3 null, "No records found."
      else
        dom.h3 null, ""


  class InstallationSitePagination extends React.Component

    displayName: "Installation Site pagination"

    constructor: (props) ->
      super(props)

    clickNextPage: ->
      $('html').trigger("installation-site-next-page")

    clickPrevPage: ->
      $('html').trigger("installation-site-prev-page")

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

    buildInstallationSites: ->
      @state.collection.map (installation_site) =>
        React.createElement(InstallationSiteUnit, {installation_site: installation_site, key: installation_site.id})

    loadInstallationSites: (url) ->
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
      $('html').on 'update-installation-sites', (event, data) =>
        if @state.next_page
          $('html').trigger("installation-site-current-page")
        else
          index          = _.findIndex @state.collection, {id: data.id}
          new_collection = @state.collection
          count          = @state.count

          if index >= 0
            new_collection[index] = data
          else
            if not @state.count or (@state.count % 9) == 0
              $('html').trigger("installation-site-current-page")
            else
              count += 1
              new_collection.push(data)

          @setState
            collection: new_collection
            no_records: false
            count: count


      $('html').on 'installation-site-deleted', (event, data) =>
        count = @state.count - 1
        if @state.next_page
          $('html').trigger("installation-site-current-page")
        else if @state.prev_page and (count % 9) == 0
          $('html').trigger("installation-site-prev-page")
        else
          filtered_installation_sites = _.filter @state.collection, (installation_site) =>
            installation_site.id != data.id

          @setState
            collection: filtered_installation_sites
            no_records: if filtered_installation_sites.length > 0 then false else true
            count: count

      $('html').on 'installation-site-next-page', (event, data) =>
        @loadInstallationSites(@state.next_page)

      $('html').on 'installation-site-prev-page', (event, data) =>
        @loadInstallationSites(@state.prev_page)

      $('html').on 'installation-site-current-page', (event, data) =>
        @loadInstallationSites(@getUrlCurrentPage())

    newInstallationSite: ->
      $('html').trigger("edit-installation-site-dialog-new")

    render: ->
      dom.div null,
        dom.h2 className: "ui dividing header",
          "Artwork::InstallationSites"
          dom.button
            className: "button ui mini right floated positive"
            onClick: @newInstallationSite
          , "",
            dom.i {className: "plus icon"}, ""
            "New installation site"
        dom.div {className: "ui three cards"},
          @buildInstallationSites()
        React.createElement(InstallationSiteNoRecords, {output: @state.no_records})
        React.createElement(InstallationSitePagination, {
          page: @state.current_page, pages: Math.ceil(@state.count / 9),
          next: @state.next_page, prev: @state.prev_page})
        React.createElement(InstallationSiteModal, {installation_site: {}})


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
