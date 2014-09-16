module.exports = 
  sizeof: (txt) ->
    len = 0
    if txt.replace(/(^\s*)|(\s*$)/g, "") == ''
      return 0
    arr = txt.split('')
    i = 0
    for val in arr
      if val.charCodeAt(0) < 128
        len++
      else
        len += 2
      i++
    return len

  EnEight : (data) ->
    monyer = new Array()
    i = 0
    while i < data.length
      monyer += "\\" + data.charCodeAt(i).toString(8)
      i++
    monyer

  DeEight : (data) ->
    monyer = new Array()
    s = data.split("\\")
    i = 1
    while i < s.length
      monyer += String.fromCharCode(parseInt(s[i], 8))
      i++
    monyer

  mkdirSync : (url, mode, cb) ->
    fs = require 'fs'
    arr = url.split("/")
    mode = mode or '0755'
    cb = cb or ->
    arr.shift()  if arr[0] is "."
    arr.splice 0, 2, arr[0] + "/" + arr[1]  if arr[0] is ".."
    inner = (cur) ->
      fs.mkdirSync cur, mode  unless fs.existsSync(cur)
      if arr.length
        inner cur + "/" + arr.shift()
      else
        cb()
    arr.length and inner(arr.shift())