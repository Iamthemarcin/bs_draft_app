
function disp_dropdown(){
    var dropdown_elements = $('.dropdown>.row, #dropdown-search');
    dropdown_elements.each(function(i,obj){
        obj.classList.toggle('dropdown-content-display')
        $('#dropdown-search').focus()
    })
}
$('.dropdown-invis-btn').click(disp_dropdown)

// dont mind this abomination of jquery combined with js :) 
function map_search(){
    maps = $('.dropdown-content-container')
    searchInput = $('#dropdown-search')
    filter = searchInput[0].value.toLowerCase()
    cols_to_not_hide = []
    maps.each(function (i, map) {
        map.classList.add("hide")
        col = $(this).parent(".dropdown-col")
        map_name = $(this).children(".dropdown-content").children(".map-name").text().toLowerCase()
        col.addClass('hide')

        if (map_name.includes(filter)){
            map.classList.remove("hide")
            cols_to_not_hide.push(col) //its not unique but w/e 
            $(this).siblings('.full-disp-break').addClass('hide')  //the break separates em modes nicely unless stuff gets hidden then its just weird go away baka
          }
    })
    cols_to_not_hide.forEach(col => {
        col.removeClass('hide')
    })


}
