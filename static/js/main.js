
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
      brawler_name = brawler.id.toLowerCase().slice(0,-4) // the names have .png at the end cuz i just use data from some random api
      if (brawler_name.includes(input_value)){
        brawler.classList.remove("hide")
      }
    });
  })
}
brawler_search()

pick_number = 1
function choose_brawler(brawler){
  //get the next player box in order that doesnt have the picked class and then add the image of the picked brawler to it
  const picked_brawler_img_src = brawler.src
  player_box = document.querySelector(".pick-image:not(.picked)#p" + pick_number);
  pick_number++
  if(player_box){
    player_pick_image = player_box.children[0]
    let width = player_pick_image.width;
    let height = player_pick_image.height;
    // add picked class since we picked a brawler for da box
    player_box.classList.add("picked")
    // cant just switch bg images since the image only covers bout 60% of the box
    const brawler_img = new Image(width, height);
    brawler_img.src = picked_brawler_img_src
    brawler_img.style.position= "absolute";
    brawler_img.style.left="50%";
    brawler_img.style.transform= "translateX(-50%)";
    brawler_img.style.zIndex=1;
    brawler_img.style.paddingBottom = "3vh";
    player_box.appendChild(brawler_img);
    padding = Math.abs(brawler_img.width-width)
    // for some reason i cant change the size before loading and if i do it onload it looks weird when zoomed (idk why either its off by like 1 pixel) so i add adequate padding and it JUST WORKS
    brawler_img.style.paddingRight = padding/2
    brawler_img.style.paddingLeft = padding/2
  }
}

