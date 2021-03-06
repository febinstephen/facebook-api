function getUserData() {
	FB.api('/me', function(response) {
//		document.getElementById('response').innerHTML = 'Hello ' + response.name;
        var access_token =   FB.getAuthResponse()['accessToken'];
        <!--AJAX script to pass access-token recieved from facebook -->
        var data = {
             "access_token": access_token,
             "fname": response.name,
             "lname": response.name,
             "email": 'godsonfebin@gmail.com',
             "provider": 'facebook' }

        $.ajax({
                data: data,
                url: 'http://localhost:8000/api/v1/register/',
                type: 'post',
                success: function (data) {
                    console.log("Success");
                    // Do something with the data
                    window.location.href = 'http://localhost:8000/api/v1/';
                }
        });

	});
}

window.fbAsyncInit = function() {
	//SDK loaded, initialize it
	FB.init({
		appId      : '372518956510929',
		xfbml      : true,
		version    : 'v2.2'
	});

	//check user session and refresh it
	FB.getLoginStatus(function(response) {
		if (response.status === 'connected') {
			//user is authorized
			document.getElementById('loginBtn').style.display = 'none';
			getUserData();
		} else {
		    console.log("not connected");
			//user is not authorized
		}
	});

};

//load the JavaScript SDK
(function(d, s, id){
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id)) {return;}
	js = d.createElement(s); js.id = id;
	js.src = "//connect.facebook.com/en_US/sdk.js";
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

//add event listener to login button
document.getElementById('loginBtn').addEventListener('click', function() {
	//do the login
	FB.login(function(response) {
		if (response.authResponse) {
			//user just authorized your app
			document.getElementById('loginBtn').style.display = 'none';
			getUserData();
		}
	}, {scope: 'email,public_profile', return_scopes: true});
}, false);