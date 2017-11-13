// Setting 3 seconds timeout with dynamic countdown
setTimeout(function() {window.location.href = "/";}, 3000);
let timeleft = 2;
let timer = setInterval(function(){
  document.getElementById("info").innerHTML =
    `You will be redirected in ${timeleft--} seconds..`;
  if(timeleft == 0) {
    clearInterval(timer);
  }
},1000);
