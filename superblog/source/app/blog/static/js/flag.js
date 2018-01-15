(() => {

let form = document.getElementById('flagform')
form.addEventListener('submit', (evt) => {
    evt.preventDefault()
    let data = new FormData(form)
    let xhr = new XMLHttpRequest()
    xhr.open('POST', '/flag_api', false)
    xhr.send(data)
    if (xhr.status === 200) {
      document.getElementById('flag').innerText = JSON.parse(xhr.response)
    } else {
      alert('Invalid or outdated captcha')
    }
    return true
}, false)

})()
