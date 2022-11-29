'use strict';

/*global window, document, AudioMothChimeConnector */

var Sound = (function () {

    var count = 0;

    var audioMothChimeConnector = new AudioMothChimeConnector();

    /* Function to enable and disable button */

    function enableButton(id) {

        document.getElementById(id).disabled = false;

    }

    function disableButton(id) {

        document.getElementById(id).disabled = true;

    }

    /* Update the text */

    function toHex (value) {

        var string = '00000' + value.toString(16).toUpperCase();
    
        return string.substr(string.length - 2);
    
    }

    function generateDeploymentID(value) {

        var i, id = [];

        for (i = 0; i < 8; i += 1) {

            id.push((value + i) % 256);

        }

        return id;

    }


    /* Main code entry point */

    document.addEventListener("DOMContentLoaded", function () {

       

        /* Set up listener for the chime button */

        document.getElementById("chime_button").addEventListener("click", function () {

            disableButton("chime_button");

            var date = new Date();
            setTimeout(function () {
                // ...
                audioMothChimeConnector.playTime(date, function () {

                    enableButton("chime_button");

                });
                
            }, 3000);

            audioMothChimeConnector.playTime(date, function () {

                //enableButton("chime_button");

            });

            


            

        });


    });

}());