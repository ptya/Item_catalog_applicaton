// START of Google signin code
function initClient() {
  // Retrieve the singleton for the GoogleAuth library and set up the client.
  gapi.load('auth2', function() {
    auth2 = gapi.auth2.init({
      client_id: appConfig.goo_id,
      cookiepolicy: 'single_host_origin',
    });
  });
  // Ready to setup the login button
  goGooLogin();
}

function goGooLogin() {
  // Display the button and attach function
  $('#goo-btn').removeClass('hidden');
  $('#goo-btn').click(function() {
    auth2.grantOfflineAccess().then(signInCallback);
  });
}

function signInCallback(authResult) {
  if (authResult['code']) {
    $('.login').addClass('hidden');
    $('#status').removeClass('hidden');
    $('#status').html('Logging you in..');
    $.ajax({
      beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', appConfig.csrf_token);
        }
      },
      type: 'POST',
      url: `/gconnect?state=${appConfig.state}`,
      processData: false,
      contentType: 'application/octet-stream; charset=utf-8',
      data: authResult['code'],
      success: function(result) {
        if(result) {
          window.location.href="/login_success";
        } else if (authResult['error']) {
          console.log('There was an error: ' + authResult['error']);
        } else {
          $("#goo").html('Failed to make a server-side call. Check you configuration and console.');
        }
      }
    });
  }
}
// END of Google signin code

// START of Facebook signin code
window.fbAsyncInit = function() {
  FB.init({
    appId      : appConfig.fb_id,
    cookie     : true,
    xfbml      : true,
    version    : 'v2.10'
  });

  // Check if user is already logged into the app
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
  // Ready to setup the login button
  goFBLogin();
};

// Load the SDK asynchronously
(function(d, s, id){
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) {return;}
  js = d.createElement(s); js.id = id;
  js.src = "https://connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function goFBLogin() {
  // Display the button and attach function
  $('#fb-btn').removeClass('hidden');
  $('#fb-btn').click(function() {
    FB.login(function(response) {
      statusChangeCallback(response);
    }, {scope: 'public_profile, email'});
  });
}

function statusChangeCallback(response) {
  if (response.status === 'connected') {
    var accessToken = FB.getAuthResponse()['accessToken'];
    $('.login').addClass('hidden');
    $('#status').removeClass('hidden');
    $('#status').html('Logging you in..');
    $.ajax({
      beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', appConfig.csrf_token);
        }
      },
      type: 'POST',
      url: `/fbconnect?state=${appConfig.state}`,
      processData: false,
      data: accessToken,
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
        if(result) {
          window.location.href="/login_success";
        } else {
          $('#fb').html('Failed to make a server-side call. Check your configuration and console.');
        }
      }
    });
  }
}
// END of Facebook signin code

// START of Github signin code
$(document).ready(function() {
  $('#gh-btn').click(function(){
    $('.login').addClass('hidden');
    $('#status').removeClass('hidden');
    $('#status').html('Logging you in..');
    window.location = `https://github.com/login/oauth/authorize?client_id=${appConfig.gh_id}&redirect_uri=http://localhost:8000/ghconnect&scope=user&state=${appConfig.state}`;
  });
});
// END of Github signin code
