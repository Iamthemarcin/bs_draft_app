
function disp_dropdown(){
    var dropdown_elements = $('.dropdown>.row');
    dropdown_elements.each(function(i,obj){
        obj.classList.toggle('dropdown-content-display')
    })
}

$('.dropdown-invis-btn').click(disp_dropdown)