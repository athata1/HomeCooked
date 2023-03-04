var Filter = require('bad-words'),
    filter = new Filter();

function filterBad(text) {
  try {
    return filter.clean(text);
  }
  catch (e) {
    return text;
  }
}
export {filterBad}