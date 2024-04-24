
function disp_dropdown(){
    var dropdown_elements = $('.dropdown>.row, #dropdown-search');
    dropdown_elements.each(function(i,obj){
        obj.classList.toggle('dropdown-content-display')
        $('#dropdown-search').focus()
        searchInput = $('#dropdown-search').val()
        if (searchInput == ''){
            $('br').removeClass('hide')
            $('.dropdown-col').removeClass('hide')
            $('.dropdown-content-container').removeClass('hide')
        }
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
    if (filter == ''){ //if empty filter its better to have a break cuz it looks weird
        $('br').removeClass('hide')
    }
}

function change_map(){
    //change map in frontend
    map_icon_src = $(this).children('.map-icon').children().attr("src")
    mode_name = $(this).children('.mode-name').text()
    map_name = $(this).children('.map-name').text().replace(/\/\n/g, '').trim() //theres prolly better way of getting this nicely. cant be bothered.
    background_color = $(this).css("background-color");

    $('#current-map-icon').attr("src", map_icon_src)
    $('#current-mode-name').text(mode_name)
    $('#current-map-name').text(map_name)
    $('#current-selected-map-clipped-bg').css("background-color", background_color) //cringe
    $('#dropdown-search').val('')
    //disp_dropdown will remove all hide classes and inputs when the input val is nothing 
    disp_dropdown()

    //get info bout the new map and change the top pick recommendations
    fetch("map_change", {
    method: "POST",
    headers: {
        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
    },
    body: JSON.stringify({
        'map_name': map_name,
    }),
    })
    .then(response => response.json())
    .then(data => {
        data['brawlers'].forEach(function(brawler, i) {
            $(`#brawler_name${i}`).text((i+1) + '. ' + brawler['brawler_name'])
            $(`#win_rate${i}`).children('strong').text( brawler['win_rate'] + '%')
            $(`#use_rate${i}`).children('strong').text(brawler['use_rate'] + '%')
            $(`#viability${i}`).children('strong').text(brawler['viability'])
            img_source_array = $(`#brawler_img${i}`).attr('src').toString().split("/")
            img_source_array.pop()
            img_source_array.push(`${brawler['brawler_name']}.png`)
            new_source = img_source_array.join('/')
            $(`#brawler_img${i}`).attr('src', new_source)
        })
        map_src = data['map_src']
        $('#current-map-pic').attr('src', map_src)
    });
}
$('.dropdown-content').click(change_map)
