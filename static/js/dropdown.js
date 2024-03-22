
function disp_dropdown(){
    var dropdown_elements = $('.dropdown>.row, #dropdown-search');
    dropdown_elements.each(function(i,obj){
        obj.classList.toggle('dropdown-content-display')
        $('#dropdown-search').focus()
    })
}
$('.dropdown-invis-btn').click(disp_dropdown)

// usin js instead of jquery for no real reason aside from it feels cooler 😎
function map_search(){
    maps = $('.dropdown-content-container')
    searchInput = $('#dropdown-search')
    filter = searchInput[0].value.toLowerCase()
    maps.each(function (i, map) {
        map.classList.add("hide")
        col = $(this).parent(".dropdown-col")
        if (!(typeof(col) === "undefined")){
            col.addClass("hide")
            var last_defined_col = col //spaghetti, but first map of every col should set the col to last_defined_col everytime RIGHT no bugs possible RIGHT
        }
        map_name = $(this).children(".dropdown-content").children(".map-name").text().toLowerCase()
        

        if (map_name.includes(filter)){
            console.log(map_name, " ", filter)
            map.classList.remove("hide")
            last_defined_col.removeClass("hide")
          }
    })
}
