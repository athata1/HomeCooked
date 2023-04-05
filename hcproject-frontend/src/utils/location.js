import { getByStateCity, getByCityState, getByZip, zipLookAhead, cityLookAhead, stateLookAhead} from 'zcs'
var states = require("us-state-converter")

function getZip(zipcode) {
  try {
  let zipObject = getByZip(zipcode);
  let city = zipObject.city;
  let abbr = zipObject.state;
  let state = states(abbr);
  state = state.name.toUpperCase()
  return [city, state];
  }
  catch {
    return undefined;
  }
}

export {getZip};