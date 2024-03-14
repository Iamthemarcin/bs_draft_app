
$('.dropdown').click(function (){
    var dropdown_elements = $('.dropdown-content-container');
    dropdown_elements.each(function(i,obj){
        obj.classList.toggle('dropdown-content-display')
    })
});
