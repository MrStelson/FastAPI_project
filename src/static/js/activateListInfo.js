const listBtn = document.getElementById('infoListBtn')
const infoList = document.getElementById('infoList')

window.addEventListener('click', () =>{
    if(infoList.classList.contains('displayDeactivated')){
        return
    }
    document.getElementById('infoList').classList.add('displayDeactivated')
})

listBtn.addEventListener('click', function(event){
    event.stopPropagation(); //не "всплывает"
    infoList.classList.toggle('displayDeactivated')
})