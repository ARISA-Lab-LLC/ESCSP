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

    function updateDeploymentID() {

        var i, id, deploymentID = "Deployment ID: ";
    
        id = generateDeploymentID(count);

        for (i = 0; i < id.length; i += 1) {

            deploymentID += toHex(id[i]);

        }

        document.getElementById('deployment_id').innerHTML = deploymentID;

    }

    /* Main code entry point */

    updateDeploymentID();

    document.addEventListener("DOMContentLoaded", function () {

        /* Set up listener for the chime button */

        document.getElementById("tone_button").addEventListener("click", function () {

            disableButton("tone_button");

            var date = new Date();

            audioMothChimeConnector.playTone(4000, function () {

                enableButton("tone_button");

            });

        });

        /* Set up listener for the chime button */

        document.getElementById("chime_button").addEventListener("click", function () {

            disableButton("chime_button");

            var date = new Date();

            audioMothChimeConnector.playTime(date, function () {

                enableButton("chime_button");

            });

        });

        /* Set up listener for the deployment button */

        document.getElementById("deployment_button").addEventListener("click", function () {

            disableButton("deployment_button");

            var date = new Date();

            var id = generateDeploymentID(count);

            count = (count + 1) % 256;

            audioMothChimeConnector.playTimeAndDeploymentID(date, id, function () {

                enableButton("deployment_button");

                updateDeploymentID();

            });

        });

    });

}());