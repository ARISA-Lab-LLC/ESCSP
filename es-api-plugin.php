<?php
/**
 * Plugin Name: Eclipse Soundscapes API Plugin
 * Plugin URI:  https://eclipsesoundscapes.org
 * Description: Custom WordPress plugin to execute API requests.
 * Version:     1.3.3
 * Author:      Joel Goncalves
 * Author URI:  https://joel.cv
 */


add_action( 'init', 'enqueue_js');
function enqueue_js() {
    wp_enqueue_script( 'ajax-script', plugins_url( 'js/api.js' ), array('jquery'), '1.1.0' );

    wp_localize_script( 'ajax-script', 'ajax_object',
            array( 'ajax_url' => admin_url( 'admin-ajax.php' ) ) );
}

function google_maps_endpoint_handler() {
    $zipcode = strval( $_GET['google_maps_zipcode'] );

    // Make a request to Google Maps API to get the latitude and longitude.
    // Replace "YOUR_API_KEY" with your actual Google Maps API key.
    $api_key = 'API_KEY';
    $url = "https://maps.googleapis.com/maps/api/geocode/json?address=$zipcode&key=$api_key";
    $response = wp_remote_get($url);

    if (!is_wp_error($response)) {
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body);
        
        if ($data->status === 'OK' && !empty($data->results)) {
            $latitude = $data->results[0]->geometry->location->lat;
            $longitude = $data->results[0]->geometry->location->lng;

            // Return the latitude and longitude as JSON response.
            wp_send_json(array(
                'latitude' => $latitude,
                'longitude' => $longitude,
            ));
        }
    }

    // If there was an error or the response was invalid, return an empty JSON response.
    wp_send_json(array());
    wp_die();
}
add_action('wp_ajax_google_maps_endpoint', 'google_maps_endpoint_handler');
add_action('wp_ajax_nopriv_google_maps_endpoint', 'google_maps_endpoint_handler');


/* AudioMoth Feature */

function validate_audiomoth_form($email, $zip_code, $serial_number) : ?array {
    if ($email) {
        // validate email
        $email = filter_var($email, FILTER_VALIDATE_EMAIL);
        if ($email === false) {
            $errors['email'] = 'Enter a valid email';
        }
    } else {
        $errors['email'] = 'Enter your email';
    }

    if ($zip_code) {
        $zip_code = trim($zip_code);
        if ($zip_code === '' || strlen($zip_code) < 5 || strlen($zip_code) > 10) {
            $errors['zip_code'] = 'Enter a valid zip code';
        }
    } else {
        $errors['zip_code'] = 'Enter your zip code';
    }


    if ($serial_number) {
	$serial_number = trim($serial_number);
        if ( $serial_number === '' || strlen($serial_number) !== 16 ) {
            $errors['serial_number'] = 'Enter a valid AudioMoth serial number';
        }
    } else {
        $errors['serial_number'] = 'Enter your AudioMoth serial number';
    }

    return $errors;
}

function send_confirmation_email($data) {
    $to = $data['email'];
    $subject = 'AudioMoth Registration';
    $headers[] = 'Content-Type: text/html';
    $headers[] = 'Cc: AudioMoth@eclipsesoundscapes.org';

    $id = $data['id'];
    $email = $to;
    $zip_code = $data['zip_code'];
    $serial_number = $data['serial_number'];

    ob_start();
    include( get_stylesheet_directory() . '/templates/audio-moth-email-template.php' );
    $content = ob_get_clean();

    $set_email_from = function() { return 'Admin@ArisaLab.org'; };
    add_filter('wp_mail_from', $set_email_from);
    wp_mail( $to, $subject, $content, $headers );
}

function audio_moth_registration_handler() {
    $email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
    $zip_code = filter_input(INPUT_POST, 'zip_code', FILTER_SANITIZE_STRING);
    $serial_number = filter_input(INPUT_POST, 'serial_number', FILTER_SANITIZE_STRING);

    $success = TRUE;
    $errors = validate_audiomoth_form($email, $zip_code, $serial_number);

    if ($errors) {
        $success = FALSE;
    }

    if (!$success) {
        wp_send_json(array("success" => FALSE, "errors" => $errors));
    } else {
        global $wpdb;
        $table_name = $wpdb->prefix . 'audiomoth_users';
        $result = $wpdb->insert( $table_name, array( 'email' => $email, 'zip_code' => $zip_code, 'serial_number' => $serial_number ) );
        
        if ($result) {
            $id = $wpdb->insert_id;
    
            $data = array(
                "id" => $id, "email" => $email, "zip_code" => $zip_code, "serial_number" => $serial_number);

            send_confirmation_email($data);

            wp_send_json( array( "success" => TRUE, "data" => $data ) );
        } else {
            wp_send_json(array());
        }
    }
}
add_action('wp_ajax_audio_moth_endpoint', 'audio_moth_registration_handler');

function audiomoth_create_db() {
    global $wpdb;
    $charset_collate = $wpdb->get_charset_collate();
    require_once( ABSPATH . 'wp-admin/includes/upgrade.php' );
   
    //* Create the audiomoth users table
    $table_name = $wpdb->prefix . 'audiomoth_users';
    $sql = "CREATE TABLE $table_name (
    id INTEGER NOT NULL AUTO_INCREMENT,
    email VARCHAR(254) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    serial_number VARCHAR(16) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
    ) AUTO_INCREMENT=500 $charset_collate;";

    dbDelta( $sql );
   }
   register_activation_hook( __FILE__, 'audiomoth_create_db' );

function audio_moth_users_handler() {
    global $wpdb;
    $table_name = $wpdb->prefix . 'audiomoth_users';
    $results = $wpdb->get_results( "SELECT * FROM " . $table_name, ARRAY_A );
    if ( $wpdb->last_error ) {
        wp_send_json(array("success" => false, "error" => $wpdb->last_error));
    } else {
        wp_send_json(array("success" => true, "data" => $results));
    }
}
add_action('wp_ajax_audio_moth_users_endpoint', 'audio_moth_users_handler');
add_action('wp_ajax_nopriv_audio_moth_users_endpoint', 'audio_moth_users_handler');
