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
      console.log(data)
      console.log(status)
      failed(data, status) if failed
    )
