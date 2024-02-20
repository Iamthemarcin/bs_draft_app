
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

function brawler_search(){
  const brawlers = document.getElementsByClassName("brawler-img")
  const searchInput = document.querySelector("[brawler-search]")
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
brawler_search()

pick_number = 1
function choose_brawler(brawler){
  fetch(`info/${brawler.id.split(".")[0]}`, {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    }
  })
  .then(response => response.json())
  .then(data => {
    console.log(data['context']);
  });
  
  //check if the brawler has been picked, if not add the picked class
  if (brawler.classList.contains("brawler-picked")){return}
  //get the next player box in order that doesnt have the picked class and then add the image of the picked brawler to it
  const picked_brawler_img_src = brawler.src
  player_box = document.querySelector(".pick-image:not(.pick-box-picked)#p" + pick_number);
  pick_number++
  if(player_box){
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
    brawler_img.id = "brawler-img"
    player_box.appendChild(brawler_img);
    padding = Math.abs(brawler_img.width-width)
    // for some reason i cant change the size before loading and if i do it onload it looks weird when zoomed (idk why either its off by like 1 pixel) so i add adequate padding and it JUST WORKS
    brawler_img.style.paddingRight = padding/2
    brawler_img.style.paddingLeft = padding/2
  }
  // if all brawlers are picked the next brawler click just removes all the picks for now, maybe ill change that into a reset button or sth
  else{
    console.log('why are the frogs gay?')

    while (document.getElementById("brawler-img")){
      img = document.getElementById("brawler-img")
      img.remove();
      $('.pick-box-picked').removeClass('pick-box-picked');
      $('.brawler-picked').css('opacity', 1)
      $('.brawler-picked').removeClass('brawler-picked');
      pick_number = 1
    }


  }
}

