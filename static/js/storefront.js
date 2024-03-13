let name=""
function setEditable() {
    let confirmBtn = document.getElementById('confirm')
    let cancelBtn = document.getElementById('cancel')
    let logoBtn = document.getElementById('logoBtn')
    let bannerBtn = document.getElementById('bannerBtn')
    let storeName = document.getElementById('storeName')
    let editBtn = document.getElementById('edit')
    storeName.removeAttribute('readonly')
    confirmBtn.removeAttribute('hidden')
    confirmBtn.removeAttribute('disabled')
    cancelBtn.removeAttribute('hidden')
    cancelBtn.removeAttribute('disabled')
    logoBtn.classList.remove('invisible')
    logoBtn.classList.remove('disabled')
    bannerBtn.classList.remove('invisible')
    bannerBtn.classList.remove('disabled')
    editBtn.classList.add('invisible')
    editBtn.classList.add('disabled')

     name = document.getElementById('storeName').value
}

function cancelEditable() {
    let confirmBtn = document.getElementById('confirm')
    let cancelBtn = document.getElementById('cancel')
    let logoBtn = document.getElementById('logoBtn')
    let bannerBtn = document.getElementById('bannerBtn')
    let storeName = document.getElementById('storeName')
    let editBtn = document.getElementById('edit')
    storeName.setAttribute('readonly', 'true')
    confirmBtn.setAttribute('hidden', 'true')
    confirmBtn.setAttribute('disabled', 'true')
    cancelBtn.setAttribute('hidden', 'true')
    cancelBtn.setAttribute('disabled', 'true')
    logoBtn.classList.add('invisible')
    logoBtn.classList.add('disabled')
    bannerBtn.classList.add('invisible')
    bannerBtn.classList.add('disabled')
    editBtn.classList.remove('invisible')
    editBtn.classList.remove('disabled')

    document.getElementById('logoInput').value = '';
    document.getElementById('storeName').value = name;
}