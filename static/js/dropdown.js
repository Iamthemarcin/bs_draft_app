
function disp_dropdown(){
    var dropdown_elements = $('.dropdown>.row, #dropdown-search');
    dropdown_elements.each(function(i,obj){
        obj.classList.toggle('dropdown-content-display')
        $('#dropdown-search').focus()
    })
}
$('.dropdown-invis-btn').click(disp_dropdown)

// You input some string in mapsearch box, this string gets compared to all the maps.
// first  you hide every map card and column. Then, if the string is in the map name, you un-hide it. You also mark in which
// column (theres 3) the string has been found. This column gets saved in cols_to_not_hide. After everything ends you
// remove the hide class from the columns found in it. Documenting this just in case something is fucked and i miss the most obvious
// fix in the world for two hours... again...
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
            $(this).siblings('br').addClass('hide')  //the break separates em modes nicely unless stuff gets hidden then its just weird go away baka
          }
    })
    cols_to_not_hide.forEach(col => {
        col.removeClass('hide')
    })
}

function change_map(){
    map_icon_src = $(this).children('.map-icon').children().attr("src")
    mode_name = $(this).children('.mode-name').text()
    map_name = $(this).children('.map-name').text()
    background_color = $(this).css("background-color");

    $('#current-map-icon').attr("src", map_icon_src)
    $('#current-mode-name').text(mode_name)
    $('#current-map-name').text(map_name)
    $('#current-selected-map').css("background-color", background_color)
    disp_dropdown()
}
$('.dropdown-content').click(change_map)
