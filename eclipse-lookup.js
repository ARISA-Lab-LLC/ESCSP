const eclipse_elements = {
  "04-08-24": [
    2460409.26284, 18.0, -4.0, 4.0, 74.0, 74.0, -0.318244, 0.5117116, 3.26e-5,
    -8.42e-6, 0.219764, 0.2709589, -5.95e-5, -4.66e-6, 7.5862002, 0.014844,
    -2.0e-6, 89.591217, 15.0040817, 0.0, 0.535814, 0.0000618, -1.28e-5,
    -0.010272, 0.0000615, -1.27e-5, 0.0046683, 0.004645,
  ],
};

// page for each language should define this variable
var LANGUAGE;

/**
 * Represents an single Eclipse event.
 */
class EclipseEvent {
  constructor(date, type, coverage, start, totalStart, mid, totalEnd, end) {
    this.date = date;
    this.type = type;
    this.coverage = coverage;
    this.start = start;
    this.totalStart = totalStart;
    this.totalEnd = totalEnd;
    this.end = end;
    this.mid = mid;
  }

  /**
   *
   * @returns The eclipse date.
   */
  displayDate() {
    return this.convertDate(this.date);
  }

  /**
   *
   * @returns The eclipse type.
   */
  displayType() {
    return this.convertType(this.type);
  }

  /**
   *
   * @returns The eclipse coverage percentage.
   */
  displayCoverage() {
    // If eclipse type is partial but coverage is 100% then override
    // coverage to 99.99%
    if (type == 1 && Math.floor(this.coverage) == 100) {
      return "99.99%";
    }

    return this.coverage.toFixed(2) + "%";
  }

  /**
   *
   * @returns The time of the first contact.
   */
  startTime() {
    return this.convertTime(this.date, this.start);
  }

  /**
   *
   * @returns The time of the mid contact.
   */
  midTime() {
    return this.convertTime(this.date, this.mid);
  }

  /**
   *
   * @returns The time of the last contact.
   */
  endTime() {
    return this.convertTime(this.date, this.end);
  }


  /**
  *
  * @returns The time of when the total or annular phase begins.
  */
  totalStartTime() {
    return this.convertTime(this.date, this.totalStart);
  }

  /**
  *
  * @returns The time of when the total or annular phase ends.
  */
  totalEndTime() {
    return this.convertTime(this.date, this.totalEnd);
  }

  /**
   *
   * @returns The eclipse date.
   */
  eventDate() {
    return new Date(this.date);
  }

  /**
   * @returns A string representation of the eclipse type.
   */
  convertType() {
    switch (this.type) {
      case 0:
        switch (getLanguage()) {
          case "en":
            return "None";
          case "es":
            return "Ninguno";
        }
      case 1:
        switch (getLanguage()) {
          case "en":
            return "Partial";
          case "es":
            return "Parcial";
        }
      case 2:
        switch (getLanguage()) {
          case "en":
            return "Annular";
          case "es":
            return "Anular";
        }
      case 3:
        switch (getLanguage()) {
          case "en":
            return "Total";
          case "es":
            return "Total";
        }
    }
  }

  /**
   * Converts event date and time to language-sensitive representation.
   *
   * @param {string} date The eclipse event date
   * @param {string} time The eclipse event time
   * @returns A formatted date
   */
  convertTime(date, time) {
    if (date == null || time == null) {
      return "";
    }

    var dateStr = `${date}T${time}Z`;
    var date = new Date(dateStr);

    var options = { hour: "numeric", minute: "numeric", timeZoneName: "short" };

    return date.toLocaleTimeString(getLanguageCode(), options);
  }

  /**
   * Converts event date to language-sensitive representation.
   *
   * @param {string} date The eclipse event date
   * @returns A formatted date
   */
  convertDate(date) {
    if (date == null) {
      return "";
    }

    const options = { timeZone: "UTC" };
    var date = new Date(date);
    return date.toLocaleDateString(getLanguageCode(), options);
  }
}

jQuery(document).ready(function ($) {
  document
    .getElementById("zipButton")
    .addEventListener("click", getZipLocation, false);
  document
    .getElementById("locationButton")
    .addEventListener("click", getUserLocation, false);

  showView(false, "partialEclipseTable");
  showView(false, "totalEclipseTable");
  showView(false, "spinner");
});

/**
 * @returns Returns the language code for the language of the current page.
 */
function getLanguageCode() {
  switch (getLanguage()) {
    case "en":
      return "en-US";
    case "es":
      return "es-419";
  }
}

/**
 * @returns The language of the current page.
 */
function getLanguage() {
  if (LANGUAGE == null) {
    return "en";
  }

  return LANGUAGE;
}

/**
 * Sets the visibility of an element.
 * @param {boolean} show whether an element is visible or not
 * @param {*} view the element
 */
function showView(show, view) {
  const display = show ? "flex" : "none";
  var viewElement = document.getElementById(view);
  viewElement.style.display = display;
}

/**
 * Determines the user location using the browser geolocation API.
 * @param {*} event a click event
 */
function getUserLocation(event) {
  event.preventDefault();

  if (navigator.geolocation) {
    showView(true, "spinner");
    navigator.geolocation.getCurrentPosition(
      getUserPosition,
      handleUserLocationError,
      {
        enableHighAccuracy: true,
        timeout: 7000,
        maximumAge: 0,
      }
    );
  } else {
    switch (getLanguage()) {
      case "en":
        alert("Geolocation is not supported by this browser.");
        break;
      case "es":
        alert("La geolocalización no es compatible con este navegador");
        break;
    }
  }
}

/**
 * Retrieves user latitude and longitude from geolocation API result and shows upcoming eclipse events.
 * @param {*} position A geolocation position
 */
function getUserPosition(position) {
  showView(false, "spinner");

  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;

  showUpcomingEclipse(latitude, longitude);
}

/**
 * Displays a geolocation error message to the user.
 * @param {*} error An error result from geolocation API request.
 */
function handleUserLocationError(error) {
  showView(false, "spinner");

  switch (error.code) {
    case error.PERMISSION_DENIED:
      switch (getLanguage()) {
        case "en":
          alert("User denied the request for Geolocation");
          break;
        case "es":
          alert("Usuario denegó la solicitud de Geolocalización");
          break;
      }
      break;
    case error.POSITION_UNAVAILABLE:
      switch (getLanguage()) {
        case "en":
          alert("Location information is unavailable");
          break;
        case "es":
          alert("La información de ubicación no está disponible");
          break;
      }
      break;
    case error.TIMEOUT:
      switch (getLanguage()) {
        case "en":
          alert("The request to get user location timed out");
          break;
        case "es":
          alert(
            "Se agotó el tiempo de espera de la solicitud para obtener la ubicación del usuario"
          );
          break;
      }
      break;
    case error.UNKNOWN_ERROR:
      switch (getLanguage()) {
        case "en":
          alert("An unknown error occurred");
          break;
        case "es":
          alert("Un error desconocido ocurrió");
          break;
      }
      break;
  }
}

/**
 * Determines location coordinates from a zip code and shows upcoming eclipse events.
 * @param {*} event A click event.
 */
function getZipLocation(event) {
  event.preventDefault();

  var zipcode = document.getElementById("zipInput").value.trim();

  if (!zipcode) {
    switch (getLanguage()) {
      case "en":
        alert("Invalid Zip Code");
        break;
      case "es":
        alert("Código postal no válido");
        break;
    }
    return;
  }

  if (zipcode.length != 5) {
    switch (getLanguage()) {
      case "en":
        alert("Please enter a 5 digit Zip Code");
        break;
      case "es":
        alert("Ingrese un código postal de 5 dígitos");
        break;
    }
    return;
  }

  showView(true, "spinner");

  getLocationFromZipCode(zipcode, function (response) {
    showView(false, "spinner");

    if (response == null) {
      switch (getLanguage()) {
        case "en":
          alert("Unable to retrieve location from zip code");
          break;
        case "es":
          alert("No se puede recuperar la ubicación del código postal");
          break;
      }
    } else {
      showUpcomingEclipse(response["latitude"], response["longitude"]);
    }
  });
}

/**
 * Calculates eclipse event details for the selected date based on location coordinates.
 * @param {*} latitude 
 * @param {*} longitude
 */
function showUpcomingEclipse(latitude, longitude) {
  selected_date = document.getElementById("select_date").value;
  elements = eclipse_elements[selected_date];

  calculate(elements, latitude, longitude);

  const event = new EclipseEvent(
    getC1Date(elements),
    gettype(),
    getcoverage(),
    getC1Time(elements),
    getC2Time(elements),
    getMidTime(elements),
    getC3Time(elements),
    getC4Time(elements)
  );

  loadTable(event);
}

/**
 * Shows details of an eclipse event.
 * @param {*} event Eclipse event.
 */
function loadTable(event) {
  if (event.type == 3) {
    document.getElementById("tdTotalDate").innerHTML = event.displayDate();
    document.getElementById("tdTotalCoverage").innerHTML = event.displayCoverage();
    document.getElementById("tdTotalEclipseType").innerHTML = event.displayType();
    document.getElementById("tdTotalEclipseStart").innerHTML = event.startTime();
    document.getElementById("tdTotalMaxEclipse").innerHTML = event.midTime();
    document.getElementById("tdTotalEclipseEnd").innerHTML = event.endTime();
    document.getElementById("tdTotalEclipseFullStart").innerHTML = event.totalStartTime();
    document.getElementById("tdTotalEclipseFullEnd").innerHTML = event.totalEndTime();
    
    showView(false, "partialEclipseTable");
    showView(true, "totalEclipseTable");
  } else {
    document.getElementById("tdDate").innerHTML = event.displayDate();
    document.getElementById("tdCoverage").innerHTML = event.displayCoverage();
    document.getElementById("tdEclipseType").innerHTML = event.displayType();
    document.getElementById("tdEclipseStart").innerHTML = event.startTime();
    document.getElementById("tdMaxEclipse").innerHTML = event.midTime();
    document.getElementById("tdEclipseEnd").innerHTML = event.endTime();

    showView(false, "totalEclipseTable");
    showView(true, "partialEclipseTable");
  }
}
