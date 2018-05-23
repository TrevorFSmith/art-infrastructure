class @Adapter

  constructor: (url) ->
    @url = url

  loadData: (ok, failed) ->
    $.ajax({
      url: @url
      dataType: 'json'
    }).done( (data, status) ->
      if data
        ok(data) if ok
    ).error( (data, status) ->
      console.log(data, status)
      failed(data, status) if failed
    )

  pushData: (type, token, data, ok, failed, finished) =>
    $.ajax({
      url: @url
      dataType: 'json'
      data: data
      type: type
      headers: {"X-CSRFToken": token}
    }).error( (data, status) ->
      console.log(data)
      console.log(status)
      failed(data, status) if failed
    ).done( (data, status) ->
      if data
        ok(data) if ok
    ).complete ->
      finished() if finished

  delete: (token, data, ok, failed, finished) =>
    $.ajax({
      url: @url
      dataType: 'json'
      data: data
      type: 'DELETE'
      headers: {"X-CSRFToken": token}
    }).error( (data, status) ->
      console.log(data)
      console.log(status)
      failed(data, status) if failed
    ).done( (data, status) ->
      if data
        ok(data) if ok
    ).complete ->
      finished() if finished
