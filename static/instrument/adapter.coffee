class @Adapter

  constructor: (url) ->
    @url = url

  loadData: (ok, failed) =>
    $.ajax({
      url: @url
      dataType: 'json'
    }).done( (data, status) =>
      if data
        ok(data) if ok
    ).error( (data, status) ->
      alert 'Error loading page. Please try again later.'
      failed(data, status) if failed
    )
