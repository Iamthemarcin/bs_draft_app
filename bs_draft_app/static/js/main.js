$(document).ready(()=>{
  brawler_search()
  change_font_size()
  $(document).keydown(function (event) {
    let key = event.key
    if (key == "r" && event.target.tagName == 'BODY'){
      reset_picks()
    }
    if (key == "Enter" && event.target.id == 'search'){
      first_brawler = $('.brawler-img:not(.hide)')[0]
      choose_brawler(first_brawler)
    }
    // on escape hide dropdown if visible, remove all things from the searchbox and show all brawlers again
    if (key == "Escape"){ 
      $("#search").blur();
      $("#search").val("")
      $(".brawler-img").removeClass("hide")

      var dropdown = $('.dropdown>.row');
      
      if ($(dropdown).hasClass( "dropdown-content-display" )){
        disp_dropdown()
      }
    }
  });
});

function scroll_me_daddy(){
  var scrollable_container = document.getElementsByClassName('brawlers-box')[0];
  scrollable_container.addEventListener("wheel", function (e) {
      if (e.deltaY > 0) {
          scrollable_container.scrollLeft += 100;
        e.preventDefault();
      }
      else {
          scrollable_container.scrollLeft -= 100;
        e.preventDefault();
      }
    });
  }
scroll_me_daddy()

function change_font_size(){
  map_name = $( ".map-name")
  len = map_name.text().length
  if (len > 20){
    font_size = 1.75 - (9/len)/5
    map_name.css( "font-size", `${font_size}vh` )
  }
}

function brawler_search(){
  const brawlers = document.getElementsByClassName("brawler-img")
  const searchInput = document.querySelector("#search")
  searchInput.addEventListener("input", (e) => {
    const input_value = e.target.value.toLowerCase()
    Array.from(brawlers).forEach(function (brawler) {
      brawler.classList.add("hide")
      brawler_name = brawler.id.toLowerCase().slice(0,-4) // the names have .png at the end cuz i just use data from brawlify api, im SURE ill change that later :)
      if (brawler_name.includes(input_value)){
        brawler.classList.remove("hide")
      }
    });
  })

}


pick_number = 1


function choose_brawler(brawler){
  
  //check if brawler has been picked through the top_brawlers list. If it has change the brawler variable to the same brawler but in
  //the main brawler list (it has all the attrs i need and i need to gray that one out etc etc many reasons ok)
  if (brawler.classList.contains("top-brawler")){
    brawler_name = brawler.src.split("/").pop()
    brawler = document.querySelector(`.brawler-img[id='${brawler_name}']`)
  }
  
  //check if the brawler has been picked, if not add the picked class
  if (brawler.classList.contains("brawler-picked")){return}
  //get the next player box in order that doesnt have the picked class and then add the image of the picked brawler to it.
  //remove the border from that box and add it to the next one.
  const picked_brawler_img_src = brawler.src
  player_box = document.querySelector(".pick-image:not(.pick-box-picked)#p" + pick_number);
  if(player_box){
    //remove the rainbow border from curr pick and add it to the next pick, to showcase which player is picking next
    player_box.children[0].classList.remove("rainbow-border")
    next_player_box = document.querySelector(".pick-image:not(.pick-box-picked)#p" + (pick_number+1));
    if (next_player_box){
      next_player_box.children[0].classList.add("rainbow-border")
    }
    
    brawler.classList.add("brawler-picked")
    brawler.style.opacity = 0.35 //signal that the brawler has been picked
    player_pick_image = player_box.children[0]
    let width = player_pick_image.width;
    let height = player_pick_image.height;
    // add picked class since we picked a brawler for da box
    player_box.classList.add("pick-box-picked")
    // cant just switch bg images since the image should cover bout 60% of the box, theres prolly better way
    const brawler_img = new Image(width, height);
    brawler_img.src = picked_brawler_img_src
    brawler_img.style.position= "absolute";
    brawler_img.style.left="50%";
    brawler_img.style.transform= "translateX(-50%)";
    brawler_img.style.zIndex=1;
    brawler_img.style.paddingBottom = "3vh";
    brawler_img.classList.add("picked-brawler-img")
    player_box.appendChild(brawler_img);
    brawler_img.classList.add(pick_number)
    brawler_img.classList.add(brawler.id.slice(0,-4).replaceAll(' ','-')) //brawler_name

    padding = Math.abs(brawler_img.width-width)
    // for some reason i cant change the size before loading and if i do it onload it looks weird when zoomed (idk why either its off by like 1 pixel) so i add adequate padding and it JUST WORKS
    brawler_img.style.paddingRight = padding/2
    brawler_img.style.paddingLeft = padding/2
  }
  // if all brawlers are picked the next brawler click just removes all the picks
  else{
    reset_picks()
    pick_number--
  }
  retrieve_top_picks()

  pick_number++
  
  searchbox = document.querySelector("#search")
  searchbox.value = ''
  //i want to focus on the searchbox element so people can type without scrolling to it. Not on mobile tho cuz its annoying
  if (window.innerWidth > 1280){
    var cursorFocus = function(elem) {
      var x = window.scrollX, y = window.scrollY;
      elem.focus();
      window.scrollTo(x, y);
    }
    cursorFocus(searchbox)
  }
  const all_brawlers = document.getElementsByClassName("brawler-img");
  Array.from(all_brawlers).forEach((brawler)=> {
    brawler.classList.remove('hide')
  })

}

function reset_picks(){
  imgs = $(".picked-brawler-img")
  imgs.remove();
  $('.pick-box-picked').removeClass('pick-box-picked');
  $('.brawler-picked').css('opacity', 1)
  $('.brawler-picked').removeClass('brawler-picked');
  $('.rainbow-border').removeClass('rainbow-border')
  pick_number = 1

  $('#p1 img').addClass("rainbow-border")
  retrieve_top_picks()
  }

function retrieve_top_picks(){
  picked_brawlers = $('.picked-brawler-img')
  brawler_data = {}
  picked_brawlers.each(function (index, brawler){
    brawler_info = brawler.className.split(' ')
    brawler_name = brawler_info[2].replaceAll('-', ' ')
    if (brawler_name == '8 Bit' | brawler_name == 'R T'){ //for whatever reason those two are the only differently named ones in the unofficial api. all the rest dont get to keep the - in the name lol.
      brawler_name = brawler_name.replaceAll(' ', '-')
    }
    brawler_pick_number = brawler_info[1]
    brawler_data[brawler_pick_number-1] = brawler_name  //pick number starts from 1.
  })
  top_brawlers = []
  for (let i = 0; i <17; i++){
    brawler_name = $(`#brawler_name${i}`).text().slice((i+1).toString().length + 2)
    brawler_name = brawler_name.replaceAll('-', ' ')
    top_brawlers.push()
  }
  
  //brawler_name = brawler.id.toString().slice(0,-4)
  map_name = $('#current-map-name').text().replace(/\/\n/g, '').trim()
  //send the picked brawler info to the server then update the top reccommended picks accordingly
  fetch("brawler_pick", {
    method: "POST",
    headers: {
        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
    },
    body: JSON.stringify({
        'brawler_data': brawler_data,
        'map_name': map_name,
        'top_brawlers': top_brawlers
    }),
    })
    .then(response => response.json())
    .then(data => {
        for (let i = 0; i <data.top_brawlers.length; i++){
          $(`#brawler_name${i}`).text((i+1) + '. ' + data.top_brawlers[i].brawler_name)
          $(`#win_rate${i}`).children('strong').text( data.top_brawlers[i].win_rate + '%')
          $(`#use_rate${i}`).children('strong').text(data.top_brawlers[i].use_rate + '%')
          $(`#viability${i}`).children('strong').text(data.top_brawlers[i].viability)
          img_source_array = $(`#brawler_img${i}`).attr('src').toString().split("/")
          img_source_array.pop()
          img_source_array.push(`${data.top_brawlers[i].brawler_name}.png`)
          new_source = img_source_array.join('/')
          $(`#brawler_img${i}`).attr('src', new_source)
        }
    })
  }


// func to display manual. It shows the first manual, then on body click hides the prev manual and shows the next one. On last step it just hides the manual.
var manual_stage = 0
body_listener_enabled = false//during function execution, every body press will go to the next stage. when func isnt executing, body behaves normally

function switch_manuals(){
  if (body_listener_enabled == false){
    return
  }
  if (manual_stage < (manuals.length - 1)){
    $(`.${manuals[manual_stage]}`).toggle()
    $(`.${manuals[manual_stage + 1]}`).toggle()
    manual_stage += 1
  }
  else if (manual_stage == (manuals.length-1)){
    $(`.${manuals[manual_stage]}`).toggle()
    body_listener_enabled = false;
    manual_stage = 0
    return;
  }
}

$(".manual").on("click", function(e){
  e.stopPropagation(); //dont wanna trigger the body click right away, it messes my brain up
  $("body").off("click"); //if I already pressed the manual before, I would add another body listener rn, causing it to listen for clicks twice.
  manuals = ["map-manual", "search-manual", "top-picks-manual", "reset-manual"]
  body_listener_enabled = true; //I want to start listening to all clicks and switch the manuals only. All other actions disabled by handler below
  $(`.${manuals[manual_stage]}`).toggle()
  })

// when executing the manual event chain, I don't want anything else to be clickable.
document.addEventListener("click", handler, true);
function handler(e) {
  if (body_listener_enabled == true){
    switch_manuals()
    e.stopPropagation();
    e.preventDefault();
  }
}

