function getLocationFromZipCode(zipcode, callback) {
    var data = {
		'action': 'google_maps_endpoint',
		'google_maps_zipcode': zipcode
	};

	jQuery.get(ajax_object.ajax_url, data, function(response) {
        callback(response);
	})
    .fail(function() {
        callback(null);
    });
}

function registerAudioMothUser(email, zip_code, serial_number, callback) {
    var data = {
		'action': 'audio_moth_endpoint',
        'email': email,
        'zip_code': zip_code,
        'serial_number': serial_number
	};

	jQuery.post(ajax_object.ajax_url, data, function(response) {
        callback(response);
	})
    .fail(function() {
        callback(null);
    });
}

function retrieveAudioMothUsers(callback) {
    var data = {
		'action': 'audio_moth_users_endpoint',
	};
    jQuery.get(ajax_object.ajax_url, data, function(response) {
        callback(response);
	})
    .fail(function() {
        callback(null);
    });
}
