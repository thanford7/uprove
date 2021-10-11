
const Pages = {};
const pageNameRegex = /^\.\/.*?.\/(.*?Page)\.js$/;
function importAll(r) {
    r.keys().forEach((key) => (Pages[key.match(pageNameRegex)[1]] = r(key)))
}

importAll(require.context('./modules/pages', true, /^\.\/.*?.\/(.*?Page)\.js$/));
export default Pages;

